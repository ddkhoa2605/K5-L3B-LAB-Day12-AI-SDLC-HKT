# PLAN 2 – Người 2 phụ trách `sim/quan` + scenario + tích hợp (Integrator)

> Đặt tại `docs/plan/plan2.md` (không đặt trong `docs/members/`).

## 1. Vai trò

- **Module chính:** `sim/quan` (`chonoi/sim/quan.py`) và kiểm mâu thuẫn scenario mức luật (`chonoi/scenario.py`).
- **Vai quy trình:** Integrator – giữ `docs/contracts/`, quyết thứ tự merge, **gắn tag `phase-1…phase-4` và Release `v1.0.0`**, duyệt PR đổi ngôn ngữ/CI nếu có.
- **Dự phòng cho:** Người 3. **Được dự phòng bởi:** Người 1.
- **Reviewer chính của:** `sim/gather`, `client/ui`. **Được review bởi:** Người 1.
- **Điểm liên quan:** test headless ẩn (25), làm việc nhóm (25), harness AI (10, skill `pr-checklist`).

## 2. Phạm vi (theo README/STARTER)

Chế độ `quan`: buổi tối, nhìn từ trên xuống, vị trí `[x, z]`.

Nhóm phải viết: khách, giữ chỗ, bếp, bưng món, phục vụ, tiền, uy tín; kiểm mâu thuẫn scenario ở mức luật. Khung đã có: CLI, mã thoát 0/1/2, đọc/ghi kho, JSONL tất định, RNG, ID.

Số liệu (thời lượng, bounds, vị trí bếp/bàn, lịch/chu kỳ khách, patience, thời gian ăn, giới hạn mang, tip, đổi uy tín, menu/recipe/giá) đọc từ `game.contract.json`; không hard-code. Event Quán theo **mục E của PRD-0**.

### 2.1 Luật Quán theo PRD-0 (đã đọc từ lab board 21/11/2026)

Giá trị mẫu của preset (chỉ để viết test; code luôn đọc từ contract; ngoài preset còn có "dải hợp lệ" mà scenario/test có thể đổi):
- `tuning.quan`: `duration_s` 180, bounds x[0,16] z[0,10], start [8,5], `walk_speed` 4.0, `ramp_max_ticks` 6, `interact_radius` 1.5, bếp B1 [2,8], bàn T1 [9,2], `first_customer_tick` 120, `customer_interval_s` 15, `patience_s` 60, `eat_s` 10, `burn_s` null, `carry_limit` 1, `tip_rate` 0.2, `tip_min_patience_ratio` 0.5, `tip_reputation` 0.2, `left_reputation_delta` −0.5, `reputation_initial` 3.0 (min 0, max 5).
- Menu: `ca_loc_nuong_trui` (ca_loc×1, nấu 6s, giá 60); `goi_bong_sung` (bong_sung×2, 4s, 40); `lau_ca_linh_dien_dien` (ca_linh×3 + bong_dien_dien×1, 10s, 120). Quy đổi giây → tick ở 60 Hz; tiền là số nguyên (nghìn đồng).

**Thứ tự xử lý một tick (mục F, Quán)** — bước k đọc frame `tick=k`, ghi event tại k+1, `sim_tick`/`phase_tick` +1:
1. Tăng đồng hồ, giảm timer ca/nấu/ăn/kiên nhẫn; chỉ tăng `ready_ticks` cho món đã ready ở đầu bước.
2. Xét bếp theo id: nấu xong → `ready`, `ready_ticks=0`; không cháy.
3. Di chuyển (Euclid, tăng/giảm tốc, chặn mép), rồi tối đa **một** `interact` chọn theo (khoảng cách, bếp trước bàn, id); đối tượng không tương tác được thì bỏ lượt. Bếp idle lấy đơn `reserved` cũ nhất (theo `order_tick`, rồi id bàn), tiêu nguyên liệu đã giữ, chốt giá, phát `cook_started`; bếp ready giao món cho tay trống (`dish_ready`/`dish_picked`); bàn nhận đúng `order_id` → khách ăn (`served`), tip = `floor(tiền món × tip_rate)` nếu tỷ lệ kiên nhẫn còn lại ≥ `tip_min_patience_ratio`, ngược lại 0.
4. Theo id bàn: khách ăn xong → trả tiền (`paid`), rời bàn. Khách waiting hết kiên nhẫn → `customer_left` (reason `patience`), uy tín += `left_reputation_delta`, nhả phần giữ, bỏ món liên quan, nguyên liệu đã dùng không hoàn lại. Hết ca: khách ăn trả ngay, khách chờ rời với reason `closing` không trừ uy tín; rồi phát `quan_end`. Tip cộng `tip_reputation` khi thu tiền (kẹp theo tuning).
5. Sinh khách: từ `first_customer_tick`, rồi mỗi `customer_interval_s × 60` tick; không còn bàn → bỏ lượt; chọn món theo seed trong 3 món đủ nguyên liệu (tồn vật lý trừ phần giữ); không có món → `no_dish`; khách mới giữ đúng công thức ngay, `order_tick = phase_tick`, kiên nhẫn đầy.

**Đơn hàng:** payload `{order_id, dish_id, base_price}`, `order_id` = id khách. Trạng thái đơn `reserved → assigned → served` (hoặc `unfulfillable`).

**Event Quán (mục E):** `customer_arrived {order_id,table_id,dish_id}` / `no_dish {}`; `cook_started` (+`items`,`base_price`) / `dish_ready` / `dish_picked` đều có `stove_id,order_id,dish_id`; `served {order_id,table_id,dish_id,patience_ticks_left,base_price,tip}`; `paid {order_id,table_id,base_price,tip,amount,reason: finished_eating|closing}`; `customer_left {order_id,table_id,reason: patience|closing,reputation}`; `quan_end {reason:"time",money,earned,shift_earned,reputation}`. Dòng cuối `end`: `reason` là `time` hoặc `tick_limit`.

**Điểm:** `earned + 100 × floor(reputation)` ở mọi snapshot và `end`. Tiền/`earned` đầu lượt Quán độc lập = 0; kho vào chỉ khi có `--inventory` hoặc `scenario.quan.stock`, nếu không thì kho rỗng.

**Mã thoát 2 (scenario/inventory mâu thuẫn, mục D):** trường sai/chưa hỗ trợ, khối sai mode, id trùng, id bếp/bàn cập nhật không tồn tại, tọa độ ngoài miền, liên kết thiếu, bộ đếm âm/mâu thuẫn, giỏ quá trần, khai cả `quan.stock` và `--inventory`, nguyên liệu/món ngoài phạm vi, khách trùng bàn, giữ chỗ khác công thức hoặc quá tồn, bếp/tay giữ cùng đơn hoặc món không khớp đơn, tham chiếu id không tạo thực thể. Việc này thuộc `scenario.py` (Người 2 viết luật Quán; ranh giới framework hỏi PO — xem `docs/clarify.md`).

**Kho vào (mục G):** `{"items":{kind: số nguyên không âm}}`, chỉ khóa `items`; kind vắng tính 0; kho rỗng `{"items":{}}`; sai schema/kind lạ/giá trị ngoài miền → mã 2. Trần giỏ không áp lên kho Quán.

## 3. Kế hoạch

### A. Requirement
- [x] PRD-0 đã lấy (mục 2.1). PRD Phase 2–4 chưa mở: lấy khi lab board mở.
- [ ] Phối hợp PO chốt AC `AC-P1-xx` cho Quán và scenario (bản nháp ở `docs/plan/phase-1.md`).
- [ ] State machine khách (đến, chờ, xếp bàn, chờ món, ăn, rời) và món/bếp (chưa nấu, đang nấu, xong, đang mang, đã phục vụ) — điều chỉnh theo PRD.
- [ ] Quy tắc thiếu nguyên liệu, hết kiên nhẫn, bếp bận, mang quá giới hạn, mâu thuẫn scenario.
- [ ] Câu hỏi chưa rõ → `docs/clarify.md` (qua Người 1).

### B. Hợp đồng tích hợp (chủ trì ở kickoff 15', Phase 1)
- [ ] Soạn `docs/contracts/` cùng Người 1 và 3, đủ 3 mục:
  1. Schema kho (mục G PRD-0) + `inventory.sample.json` hợp lệ.
  2. Interface `sim/*` ↔ `client/ui` (state UI đọc, command UI gửi).
  3. Danh sách event (tên, `data`, bên phát, bên nghe); event Quán theo mục E PRD-0.
- [ ] PR hợp đồng: **2 approvals** (khóa theo AGENTS.md). Đổi sau này: báo cả nhóm + ghi lý do (+ ADR nếu đổi framework).
- [ ] Đọc `quan.py`, `scenario.py`, `inventory.py`, `contract.py`, `inputs.py`, `runner.py`, `sim/ramp.py`.
- [ ] Phân định ranh giới `scenario.py` (framework hay phần nhóm): hỏi PO, ghi `docs/clarify.md`.

### C. Implementation
- [ ] Branch `feature/quan-<task>`; PR ≤ ~400 dòng.
- [ ] Khách đến theo lịch/seed/contract; giữ bàn; recipe, kiểm nguyên liệu từ kho đầu vào, thời gian nấu.
- [ ] Bưng món, giới hạn mang, phục vụ; doanh thu/tip/uy tín.
- [ ] Phát event đúng hợp đồng; xử lý khách rời, thiếu nguyên liệu, edge cases.
- [ ] `Streams`, `IdAllocator`, `ids.sort_by_id`; không random toàn cục/system clock.
- [ ] Không hard-code số liệu; không sửa schema kho/contract trái quy trình.
- [ ] Đọc diff mọi code AI sinh trước khi mở PR.

### D. Skill `pr-checklist` (yêu cầu AGENTS.md: ≥ 2 skill)
- [ ] `.agents/skills/pr-checklist`: nêu tên và khi dùng (trước khi mở/duyệt PR). Kiểm: Closes #, phase/module, AC, ≤ ~400 dòng, không hard-code/random/system clock, ID/sort, không đụng contract/framework, bằng chứng lệnh, reviewer nhận xét theo dòng.

### E. Test & PR
- [ ] Chạy:
  ```bash
  PYTHONPATH=tests:. python3 -m unittest discover -s tests -v
  python3 -m chonoi.headless --mode quan --seed 1 --ticks 600 --out quan-a.jsonl
  python3 -m chonoi.headless --mode quan --seed 1 --ticks 600 --out quan-b.jsonl
  cmp quan-a.jsonl quan-b.jsonl
  python3 -m chonoi.headless --mode gather --seed 1 --ticks 600 --out gather.jsonl --inventory-out kho.json
  python3 -m chonoi.headless --mode quan --seed 1 --ticks 600 --inventory kho.json --out quan.jsonl
  ```
- [ ] Smoke PRD-0: `dock.json` = `{"gather":{"hold":["ca_loc","bong_sung","bong_sung"]}}`, `dock-inputs.json` = `{"frames":[{"tick":0,"interact":true}]}`; chạy gather `--seed 42 --scenario dock.json --inputs dock-inputs.json --ticks 1 --inventory-out catch.json`, rồi `quan --seed 42 --inventory catch.json --ticks 0 --out quan.jsonl`; snapshot tick 0 phải có `stock:{"bong_sung":2,"ca_loc":1}`.
- [ ] Mở PR theo template (`Closes #`, phase, module `quan`/`contracts`, AC, bằng chứng, đóng góp AI, rủi ro); Người 1 review theo dòng.

### F. Việc Integrator (mỗi phase)
- [ ] Quyết thứ tự merge, kiểm xung đột interface, chạy toàn bộ test sau mỗi merge.
- [ ] Bất đồng thiết kế: nghe 2 phút rồi quyết, ghi ADR (`docs/adr/`).
- [ ] **Code freeze T-10'**: chạy test + headless trên `main`, xác nhận game chạy được, rồi **gắn tag** `phase-n` (hạn: 1:00 / 1:55 / 2:30 / 3:00).
- [ ] Phase 4: tạo **Release `v1.0.0`** cùng tag `phase-4` trước 3:00, sau khi QA (Người 4) đồng ý.
- [ ] Nếu nhóm đổi ngôn ngữ: một PR sửa `build_cmd`/`run_cmd`/`headless_cmd` và `ci.yml` (giữ job `ci / test` và bước kiểm thành viên; giữ `tests/test_smoke_p1.py`), Integrator duyệt.
- [ ] Review PR của Người 1 và Người 3.

### G. Việc nhóm
- [ ] ≥ 3 commit có nội dung; `docs/ai-usage-log.md`; `docs/members/<handle>.md` ≤ 200 từ.

## 4. Tiêu chí nghiệm thu

- [ ] Đáp ứng AC Quán/scenario; kho đầu vào đọc đúng, không đổi schema.
- [ ] Event và state đúng hợp đồng; luật nhất quán, không hard-code.
- [ ] Output tất định (`cmp`).
- [ ] `docs/contracts/` đủ 3 mục, PR 2 approvals đã merge; skill `pr-checklist` có trong `.agents/skills/`.
- [ ] 4 tag đúng hạn, game chạy tại mỗi tag; Release `v1.0.0`.

## 5. Phối hợp

| Người | Nội dung |
|---|---|
| Người 1 | Kho, event Gather, `gather_end`; review chéo |
| Người 3 | State/command/event cho UI; thứ tự merge; Người 2 review PR UI |
| Người 4 | Test recipe/patience/tiền/uy tín/scenario/determinism; xác nhận trước tag/Release |

## 6. Prompt AI

> Đọc `AGENTS.md`, README, `docs/STARTER.md`, PRD phase hiện tại, `game.contract.json`, `docs/contracts/`. Phân tích `chonoi/sim/quan.py`, `scenario.py`, inventory/inputs/runner. Chỉ làm issue được giao. Thiết kế state machine khách/bếp/món trước khi code. Dùng số liệu từ contract; randomness qua Streams; không system clock; ID và thứ tự ổn định. Phát event và đọc kho đúng hợp đồng. Không sửa contract/schema/test/framework trái quy trình. Chạy test và Quán headless hai lần rồi `cmp`, kiểm handoff với kho hợp lệ. Báo cáo diff, lệnh, kết quả thực tế, rủi ro.

## 7. Báo cáo cuối công việc

- Issue / Branch / PR / Phase:
- AC đã đạt:
- File đã thay đổi:
- Hợp đồng (`docs/contracts/`) và PR 2 approvals:
- Tag đã gắn (phase-1…4, v1.0.0) và thời điểm:
- Lệnh test và kết quả:
- Bằng chứng (`docs/proof/phase-n/...`):
- Vấn đề tích hợp / còn tồn tại:
- Nội dung đã ghi vào `docs/ai-usage-log.md`:
