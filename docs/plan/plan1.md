# PLAN 1 – Người 1: `sim/gather` (lát 1 + 2) + PO

> Đặt tại `docs/plan/plan1.md`. Tổng thể: `docs/plan/plan.md`.
> **Nguồn:** PRD-0 (lab board, tab Phase 1, phát hành 08:02) mục 2, 6, 7 và Test Contract v1.0 mục A–G. Mục F "Gather" là luật chuẩn; khi code lệch plan này thì PRD thắng.

## 1. Vai trò

- Module: [chonoi/sim/gather.py](../../chonoi/sim/gather.py). Vai: PO (giữ `docs/clarify.md`, hỏi Anh Năm hàng xóm ở tab Phase 1 của lab board hoặc giảng viên; không có trả lời thì tự đặt giả định và ghi lại).
- PRD chia 4 lát: **lát 1** (bơi, oxy, chặn biên, giỏ) và **lát 2** (hái, bắt cá, cập bến, ghi file kho) là của mình; lát 3–4 (khách, bếp, tiền) là của Người 2.
- Dự phòng cho Người 2; được Người 4 dự phòng. Review chéo với Người 2.
- Hạn: tag `phase-1` chậm nhất 1:00. Dự phòng 55–60'.

## 2. Khung đã có / việc còn lại

Đã có trong `gather.py`: bơi + tăng/giảm tốc (`ramp.py`), chặn mép, đồng hồ, đếm ngược nút + `node_regrown`, cập bến `docked`, hết giờ `time`, snapshot, `inventory_items()`. Runner lo ghi kho một lần, nguyên tử.

Còn thiếu: dive/surface, oxy, ngạt/choke, ngất, hái, bắt cá, giỏ đầy (`hold_full`).

## 3. Luật Gather theo PRD (thứ tự một bước)

Bước k đọc frame tick k, biến trạng thái k → k+1, ghi event tại k+1. Số liệu đọc từ `self.t`, không hard-code.

1. **Đồng hồ:** giảm `time_left_ticks`, hồi bắt, hồi nút. Nút từ 1 về 0 → `node_regrown` (theo id), hái được ngay.
2. **Bơi + chặn biên** (đã có), rồi so đầu/cuối bước → `dive` / `surface` (data: `pos` sau di chuyển; chỉ khi đổi phía biên `d ≤ 0.5`).
3. **Oxy theo `d` cuối bước:**
   - Mặt nước (`d ≤ surface_depth`): `+oxygen_refill_per_tick`, kẹp tối đa, **reset `zero_oxy_ticks` = 0**.
   - Dưới nước: `−1`, kẹp 0. Phát `oxygen_empty` (data `oxygen_ticks: 0`) khi từ dương xuống 0.
   - Mỗi bước dưới nước **kết thúc với oxy 0** (kể cả bước vừa chạm 0) → `zero_oxy_ticks += 1`. Đủ `choke_interval_ticks` (60): đặt lại 0, `hp −= 1`, phát `choke` (data `hp` sau trừ).
   - Chạm oxy 0 ở tick t và ở dưới nước liên tục (đếm ban đầu 0) → choke đầu tiên ở **t+59**. Nổi lên đúng bước đáng lẽ ngạt thì hồi oxy, không ngạt.
   - `hp = 0` → bỏ giỏ **LIFO** (nhặt sau bỏ trước), phát `faint` (`cause:"choke"`, `lost` = mảng kind theo thứ tự bỏ, `hp:0`), rồi `gather_end` reason `fainted` với kho rỗng, **dừng bước**.
4. **Cạnh lên `interact`:** xét **bến trước** (khoảng cách Euclid tới `dock_pos` trên `[x,d]`, tính cả đúng mép) → trong bến thì `gather_end` `docked` ngay. Ngoài bến: **chỉ hái khi ở mặt nước**; chọn nút `ready` gần nhất trong `interact_radius`, hòa theo id nhỏ. Đủ chỗ → thêm `node_yield` món (kind = kind của nút), `regrow_ticks = regrow_s × 60`, phát `gather` (`node_id, kind, amount`). Thiếu chỗ → `hold_full` (`action:"gather"`, `node_id`, `required`, `free`), nút giữ nguyên. Dưới nước thì `interact` ngoài bến bị bỏ qua.
5. **Cạnh lên `catch`:** chỉ khi `catch_cd_ticks == 0` **và dưới nước**; chọn đúng **một** đàn gần nhất trong `catch_radius` (hòa theo id). Đủ chỗ cho **toàn bộ** `fish_yield[kind]` → thêm hết, xóa đàn, phát `fish_caught` (`fish_id, kind, yield`), đặt `catch_cd_ticks = catch_cooldown_s × 60`. Thiếu chỗ → `hold_full` (`action:"catch"`, `fish_id`, `required`, `free`), giữ đàn, **không đặt cooldown**, không thử đàn khác (không nhận một phần). Không có đàn trong tầm → không event, không cooldown. Sai pha (ở mặt nước) → bỏ qua.
6. **Hết giờ:** `time_left_ticks = 0` → `gather_end` `time` ở mọi độ sâu, giữ giỏ **sau** các hành động trên. `E` đúng mép bến ở bước cuối vẫn `docked` nếu còn Máu; hái/bắt hợp lệ ở bước cuối vẫn vào kho.
7. Kết thúc → chốt kho ngay, dừng xử lý. `--ticks` chạm trước khi kết thúc → **không** tạo/ghi đè file kho (reason `tick_limit` ở dòng `end`).

Cooldown L đặt ở tick t thì dùng lại từ t+L. Nút/đàn mặc định: nút ở `d = 0`, cá dưới nước; đàn đứng yên.

## 4. AC Phase 1 (phần Gather)

| AC | Yêu cầu | Kiểm chứng |
|---|---|---|
| AC-P1-01 | `dive`/`surface` phát đúng khi qua biên `d = 0.5`, data `pos` | scenario `pos` sát biên + inputs bơi xuống/lên |
| AC-P1-02 | Oxy: mặt nước +6 kẹp max, dưới nước −1 kẹp 0 | scenario `oxygen_ticks` nhỏ, so snapshot |
| AC-P1-03 | `oxygen_empty` đúng một lần khi từ dương xuống 0 | đếm event |
| AC-P1-04 | Ngạt: choke đầu ở t+59, mỗi 60 tick −1 Máu; nổi lên đúng bước đó thì không ngạt; `zero_oxy_ticks` reset khi ở mặt nước | `oxygen_ticks:0`, `pos` dưới nước; thêm ca biên t+59 |
| AC-P1-05 | Máu 0 → `faint` (`lost` LIFO) → `gather_end fainted`, kho rỗng, dừng bước | `hold` có 3 món, `hp:1`, `oxygen_ticks:0` |
| AC-P1-06 | Giỏ LIFO, trần `hold_capacity` | scenario `hold` gần đầy |
| AC-P1-07 | Hái: nút `ready` gần nhất, hòa id nhỏ, đúng mép bán kính; `regrow_ticks = 1200`; `node_regrown` sau 1200 bước | 2 nút cách đều; nút mép bán kính 2.0 |
| AC-P1-08 | `hold_full` khi hái thiếu chỗ, nút giữ nguyên | `hold` 12 món |
| AC-P1-09 | Bắt cá: đúng đàn gần nhất, yield đủ (`ca_linh` 3, `ca_loc` 1), cooldown 30 tick | 2 lần `catch` liên tiếp; lần 2 trong cooldown bị bỏ |
| AC-P1-10 | `catch` thiếu chỗ: `hold_full`, giữ đàn, không cooldown, không nhận một phần | `hold` 10 món + `ca_linh` (cần 3, trống 2) |
| AC-P1-11 | `catch` ở mặt nước hoặc không có đàn: không event, không cooldown | scenario |
| AC-P1-12 | Cập bến xét trước hái; `docked` ghi đúng giỏ; ngất ghi `{"items":{}}` | smoke `dock.json` (mục 6) |
| AC-P1-13 | Hết giờ `time` giữ giỏ; kho ghi đúng một lần, nguyên tử; chạm `--ticks` thì không ghi | `time_left_ticks:120`; `--ticks` nhỏ |
| AC-P1-14 | Tất định: cùng seed/tham số/input → JSONL + kho giống từng byte | `cmp` hai lần |
| AC-P1-15 | Snapshot/event đúng schema mục E (kể cả `hold_count`, `at_surface`, `oxygen_max_ticks`, `hp_max`) | đối chiếu JSONL |

## 5. Hợp đồng cần chốt trong 15' đầu

- **Kho (mục G):** `{"items":{"bong_sung":2,"ca_loc":1}}`; chỉ khóa `items`, kind → số nguyên không âm, bỏ khóa lượng 0, rỗng là `{"items":{}}`. Ghi ví dụ vào `docs/contracts/` (đã có `inventory.sample.json`, đối chiếu) cùng Người 2.
- **Event Gather** (tên + data): `gather`, `node_regrown`, `hold_full`, `fish_caught`, `dive`, `surface`, `oxygen_empty`, `choke`, `faint`, `gather_end` (data theo mục E PRD). Ghi bảng vào `docs/contracts/`.
- **State cho UI** (Người 3, HUD tối thiểu): thời gian, oxy, Máu, giỏ (từ snapshot).
- **Kiểm scenario mức luật (mã 2)** thuộc `scenario.py` (Người 2): phần gather cần có `pos` ngoài miền, id trùng, kind lạ, `hold` quá `hold_capacity`, `oxygen_ticks` ngoài `[0,max]`, `hp` ngoài `[1,max]`, `zero_oxy_ticks` ngoài `[0,59]` hoặc dương khi không (oxy 0 và dưới nước), `time_left_ticks` không dương hoặc vượt thời lượng, `regrow_ticks` âm. Thống nhất với Người 2 ai viết phần nào.
- `invuln_ticks` có trong khung nhưng **PRD không có luật**: không dùng, giữ 0.

## 6. Quy trình và kiểm chứng

1. 0–15': đọc `gather.py`, `runner.py`, `inputs.py`, `inventory.py`, `ramp.py`, `docs/contracts/README.md`; điền `docs/clarify.md`; chốt hợp đồng.
2. 15–45': branch `feature/gather-oxy` (lát 1) rồi `feature/gather-catch` (lát 2); PR ≤ ~400 dòng, `Closes #issue`. Phút 20 rà vướng; trước phút 25 **thử xuất file kho thật** cho Người 2 dùng.
3. 45–55': smoke hai tiến trình, ma trận truy vết, chơi thử trên `main` (`python3 -m chonoi.live --mode gather`).
4. 55–60': dự phòng, tag.

```bash
PYTHONPATH=tests:. python3 -m unittest discover -s tests -v
python3 -m chonoi.headless --mode gather --seed 1 --ticks 600 --out gather-a.jsonl
python3 -m chonoi.headless --mode gather --seed 1 --ticks 600 --out gather-b.jsonl
cmp gather-a.jsonl gather-b.jsonl
# smoke hai tiến trình (PRD mục G)
echo '{"gather":{"hold":["ca_loc","bong_sung","bong_sung"]}}' > dock.json
echo '{"frames":[{"tick":0,"interact":true}]}' > dock-inputs.json
python3 -m chonoi.headless --mode gather --seed 42 --scenario dock.json --inputs dock-inputs.json --ticks 1 --out gather.jsonl --inventory-out catch.json
python3 -m chonoi.headless --mode quan --seed 42 --inventory catch.json --ticks 0 --out quan.jsonl
# kỳ vọng: snapshot quán tick 0 có stock {"bong_sung":2,"ca_loc":1}
```

Lưu output thật vào `docs/proof/phase-1/`, điền `docs/verification/phase-1.md` (AC → bằng chứng → đạt/chưa đạt, trung thực).

## 7. Ràng buộc

- Không hard-code số liệu; ngẫu nhiên chỉ qua `Streams` (gather không cần RNG); `ids.sort_by_id` (F2 trước F10); so bán kính bằng `<=` trước khi làm tròn; tọa độ xuất 3 chữ số do `jsonl.py` lo.
- Không sửa `game.contract.json`, `docs/contracts/`, schema kho, framework nếu chưa báo nhóm (PR riêng + ADR; contract cần 2 approvals).
- Không sửa test cho xanh khi luật sai.
- Đọc diff code AI sinh; ghi `docs/ai-usage-log.md` (cả chỗ AI sai); ≥ 3 commit có nội dung bằng tài khoản của mình; cuối lab `docs/members/<handle>.md` ≤ 200 từ.
- Sáng tạo (nếu làm, sau khi lõi xong) phải tắt ở headless. Nhóm 4 người không bắt buộc mục mở rộng.

## 8. Rủi ro

| Rủi ro | Giảm thiểu |
|---|---|
| PO kiêm code lát 1+2, quá tải | Clarify gọn trong 15' đầu; lát 2 giao Người 4 nếu trễ ở phút 20 |
| Ca biên (t+59, mép bán kính, bước cuối) sai | Viết test biên ngay từ AC, dùng scenario thay vì chơi tay |
| Lệch kho/event với Người 2, 3 | Chốt `docs/contracts/` trước khi code; xuất kho thật trước phút 25 |
| Mất tính tất định | `cmp` sau mỗi PR; không dùng set/dict thứ tự lạ, không đồng hồ hệ thống |

## 9. Báo cáo cuối công việc

- Issue / Branch / PR / Phase:
- AC đã đạt:
- File đã đổi:
- Lệnh test và kết quả thực tế:
- Bằng chứng (`docs/proof/phase-1/`):
- Tồn đọng (trung thực):
