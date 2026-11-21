# PLAN 3 – Người 3 phụ trách `client/ui` (chỉ UI)

> Đặt tại `docs/plan/plan3.md` (không đặt trong `docs/members/`).
> **Nguồn yêu cầu:** mục 1–7 theo PRD-0 (Phase 1, Test Contract v1.0) và `docs/plan/plan.md` (đã có trên `main` từ #8); **mục 8 theo TICKET-02 (Phase 2, v1.1)**. Cả hai đọc từ lab board ngày 21/11/2026. Phase 3–4 chưa phát hành. Nếu lệch nhau thì ưu tiên lab board.

> **Tình trạng trên `main` (cập nhật 21/11/2026, sau review #10):**
> - Đã merge #1–#6, #8 và #14. `chonoi.live` đã có `--mode day` (menu, pause, DayIntro/EveningIntro, Shop, Summary), kèm **ADR-0002** của Người 2. Việc UI của Người 3 giờ là **hoàn thiện và kiểm** giao diện đó, không dựng lại (chi tiết ở mục 8 và Phụ lục v1.1 của `ui-interface.md`).
> - ADR kế tiếp cho client 3D / route tĩnh là **ADR-0003**.
> - **Phạm vi Người 3 = chỉ UI** (theo `docs/plan/phase-2.md`: AC-P2-07 phần UI/Shop, AC-P2-08; tag và retro là AC-P2-10 của Người 2). `plan.md` và `phase-1.md` còn ghi Người 3 kiêm Scrum: lệch, cần nhóm sửa cho thống nhất.
> - `TEAM.md` đã điền ở #15.
> - AC phần UI Phase 1 nối vào **AC-P1-10** trong `docs/plan/phase-1.md` (snapshot HUD tối thiểu).

## 1. Vai trò

- **Module chính:** `client/ui` (đồ họa, âm thanh, menu, HUD theo PRD).
- **Vai quy trình:** không giữ vai quy trình riêng; chỉ làm UI. Nội dung sáng tạo phía UI (module `content`) làm sau khi lõi xong.
- **Dự phòng cho:** Người 4. **Được dự phòng bởi:** Người 2.
- **Reviewer chính của:** `qa`. **Được review bởi:** Người 2 (và Người 4 là reviewer chính của UI).
- **Điểm liên quan:** chất lượng sản phẩm (10, UI/HUD đúng PRD); như mọi thành viên: ≥ 3 commit có nội dung, review PR, ghi `docs/ai-usage-log.md`.

## 2. Phạm vi

- `chonoi.live` (bản v1.0 lúc lập plan) là cửa sổ thử bằng hình khối; từ #14 có thêm `--mode day`. Nó chạy cùng lớp sim với headless ở 60 tick/s và **chỉ đọc snapshot**. Thanh oxy, Máu, giỏ, cá, nút hái chỉ hiện khi luật tương ứng đã được viết, nên UI **phụ thuộc** Người 1/2.
- Điều khiển (PRD-0 §2): WASD/mũi tên để bơi/đi, E (`interact`: cập bến, hái, nấu, bưng, phục vụ), Space (`catch`: bắt cá khi lặn), R chơi lại (của cửa sổ thử).
- Góc nhìn: buổi sáng (gather) là **mặt cắt nhìn ngang** `[x,d]` (d tăng xuống dưới); buổi tối (quán) **nhìn từ trên xuống** `[x,z]`.
- `chonoi/live.py` và `chonoi/web/index.html` thuộc khung giảng viên: hạn chế sửa; **sửa thì PR riêng + ADR**. Starter chỉ dùng thư viện chuẩn Python. Đổi engine/ngôn ngữ là quyết định của nhóm: làm trong một PR, Integrator duyệt, sửa `build_cmd`/`run_cmd`/`headless_cmd` và `ci.yml`, giữ job `ci / test`.
- UI **không tính lại luật**; mọi state lấy từ snapshot/event của sim. Ngoại lệ duy nhất là **giá trị hiển thị suy ra từ snapshot** (ví dụ "kho khả dụng", xem 3.A). Không thêm trường snapshot mới vì như vậy là đổi output contract.
- Asset ngoài chỉ CC0/CC-BY/MIT hoặc tự tạo, ghi nguồn trong `CREDITS.md`. Không commit API key/token/`.env`.

## 3. Kế hoạch

### A. Requirement & UX (Phase 1 theo PRD-0; các phase sau chờ ticket)
- [ ] Màn hình Phase 1: Gather (sáng), Quán (tối), kết thúc buổi (`gather_end`/`quan_end`), chơi lại. Nối hai buổi qua file kho (`--inventory-out` → `--inventory`). Chế độ `day` là của **phase sau, chờ ticket**; không làm ở Phase 1.
- [ ] **HUD tối thiểu (PRD-0 §2, bắt buộc, phải đọc được trong lúc chơi):**
    - Gather: thời gian, oxy, Máu, giỏ.
    - Quán: **kho khả dụng**, món gọi, kiên nhẫn, trạng thái bếp, món trên tay, tiền, uy tín.
- [ ] "Kho khả dụng" = `stock` − Σ `customers[].reserved`. Snapshot `stock` gồm cả phần giữ chỗ (PRD-0 D/E), nên UI tự trừ để **hiển thị**, không ảnh hưởng luật. Có thể hiện thêm thời gian ca ở Quán.
- [ ] Feedback gắn với event thật (PRD-0 §E):

| Tình huống | Event |
|---|---|
| Lặn / nổi | `dive`, `surface` |
| Hết oxy, ngạt, ngất | `oxygen_empty`, `choke`, `faint` (kèm `lost`) |
| Hái / nút mọc lại | `gather`, `node_regrown` |
| Bắt cá | `fish_caught` |
| Giỏ đầy | `hold_full` (`action`, `required`, `free`) |
| Kết thúc sáng | `gather_end` (`time`/`docked`/`fainted`, `inventory`) |
| Khách đến / thiếu món | `customer_arrived`, `no_dish` |
| Bếp | `cook_started`, `dish_ready`, `dish_picked` |
| Phục vụ / trả tiền | `served`, `paid` (`base_price`, `tip`, `amount`) |
| Khách rời | `customer_left` (`patience`/`closing`, `reputation`) |
| Hết ca | `quan_end` |

- [ ] Wireframe/UI flow cho Gather và Quán; AC UI nối tiếp **AC-P1-10** (HUD tối thiểu) trong `docs/plan/phase-1.md`, cùng PO.

### B. Interface (Phase 1 kickoff, chốt trước phút 15)
- [ ] Cùng Người 1/2 chốt trong `docs/contracts/` giao diện `sim/*` ↔ `client/ui`:
    - **Gather đọc:** `time_left_ticks`, `player.{pos, heading_deg, oxygen_ticks, oxygen_max_ticks, hp, hp_max, at_surface}`, `hold`, `hold_count`, `hold_capacity`, `nodes[]` (`ready`, `regrow_ticks`), `fish[]`.
    - **Quán đọc:** `time_left_ticks`, `player.pos`, `stock`, `hand`, `stoves[]` (`state`, `dish`, `cook_ticks_left`), `tables[]` (`customer_id`), `customers[]` (`dish_id`, `patience_ticks_left`, `state`, `reserved`), `money`, `reputation`.
    - **Chung:** `money`, `earned`, `reputation`, `score`, `state`.
    - **Lệnh gửi vào:** `move` [−1,1]², `interact`, `catch` (chỉ tác động ở cạnh lên).
- [ ] Chạy thử `python3 -m chonoi.live --mode gather` và `--mode quan` (`--seed N`, `--port 8000`). Nối hai buổi bằng `--inventory-out kho.json` rồi `--inventory kho.json`.
- [ ] Fallback khi field thiếu/null hoặc entity biến mất. Dùng snapshot giả và kho mẫu `docs/contracts/inventory.sample.json` trong lúc chờ sim.

### C. Implementation
- [ ] Branch `feature/ui-<task>`; PR ≤ ~400 dòng.
- [ ] Layout và HUD theo 3.A; hiển thị state thật; xử lý kết thúc phiên, restart, lỗi đầu vào.
- [ ] Không nhúng số liệu gameplay (lấy từ `game.contract.json`/snapshot); không sửa logic sim trong PR UI.
- [ ] Sửa `live.py`/`web/index.html` chỉ khi cần, bằng PR riêng + ADR (`docs/adr/`, mẫu `0000-template.md`). Đã có ADR-0001 (kind kho) và ADR-0002 (mode day/pause); ADR mới là 0003.
- [ ] Đọc diff mọi code AI sinh trước khi mở PR.

### D. Phong cách (PRD-0 §3)
- [ ] Sông nước màu phù sa, bờ dừa nước, nhà sàn, ánh hồng buổi sớm. Buổi tối có đèn dây vàng và khói bếp.
- [ ] Út Sen mặc áo bà ba, buộc khăn rằn, đeo kính lặn tự chế và giỏ lưới.
- [ ] Được bắt đầu bằng hình khối 2D, rồi nâng dần. Khuyến khích giọng Nam Bộ trong thoại. Tôn trọng văn hóa địa phương; asset có quyền sử dụng và ghi `CREDITS.md`.

### E. Sáng tạo của nhóm (tùy chọn, sau khi lõi xong)
- [ ] Được thêm nhân vật, loài cá/cây, sinh vật, món, khu vực, cơ chế nhỏ, câu chuyện, đồ họa, âm nhạc, giao diện.
- [ ] Điều kiện: **tắt ở headless, hoặc bảo đảm không đổi tick, event, tiền, uy tín, snapshot** theo contract. Ghi mục "Sáng tạo của nhóm" trong README **kèm bằng chứng ngắn rằng lõi vẫn đúng** (Người 4 chạy headless trước/sau, `cmp`).
- [ ] Nhóm 4 người không bắt buộc làm mở rộng; độ phức tạp không được cộng điểm. Ưu tiên một ý tưởng gọn, chạy ổn. PR module `content`.

### F. Test & PR
- [ ] Chạy UI bằng `run_cmd`. Kiểm Gather (bơi, oxy, Máu, giỏ, hái, bắt, cập bến) và Quán (khách, món gọi, kiên nhẫn, bếp, tay, tiền, uy tín). Kiểm cả restart, kết thúc, dữ liệu thiếu, UI không hiện state cũ.
- [ ] Chụp ảnh/video vào `docs/proof/phase-n/` (Phase 1: `docs/proof/phase-1/`, dẫn link từ `docs/verification/phase-1.md`).
- [ ] Chạy `PYTHONPATH=tests:. python3 -m unittest discover -s tests -v` trước PR.
- [ ] PR theo template (Closes #, phase, module `ui`/`content`, AC, bằng chứng ảnh/lệnh, đóng góp AI, rủi ro); Người 2 và 4 review theo dòng.

## 4. Tiêu chí nghiệm thu

- [ ] HUD tối thiểu Gather và Quán đúng PRD-0 §2, đọc được trong lúc chơi; chơi được cả hai buổi.
- [ ] UI kết nối sim qua hợp đồng; không thực thi luật ở client (chỉ suy ra giá trị hiển thị như kho khả dụng).
- [ ] Hiển thị đúng state, xử lý field thiếu/null; input không mất.
- [ ] Phần sáng tạo (nếu có) không đổi output headless, có bằng chứng trong README.
- [ ] Mọi thay đổi framework có PR riêng + ADR.
- [ ] ≥ 3 commit có nội dung bằng tài khoản của mình.
- [ ] Có bằng chứng UI trong `docs/proof/`; CI không bị ảnh hưởng; game chạy được tại mỗi tag.

## 5. Phối hợp

| Người | Nội dung |
|---|---|
| Người 1 | State/event Gather (oxy, Máu, giỏ, nút, cá, `gather_end`); file kho thật trước phút 25 |
| Người 2 | State/event Quán; hợp đồng kho; thứ tự merge, build/run command, gắn tag; review PR UI |
| Người 4 | Checklist test thủ công, ảnh/video, `cmp` headless cho phần sáng tạo; review PR UI |

## 6. Prompt AI

> Đọc `AGENTS.md`, README, `docs/STARTER.md`, PRD đúng phase (Phase 1: PRD-0 §2, §3, §E) và `docs/contracts/`. Trước khi code, mô tả màn hình, component, field snapshot cần hiển thị và mapping input (WASD/mũi tên, E, Space). HUD tối thiểu: Gather gồm thời gian, oxy, Máu, giỏ; Quán gồm kho khả dụng (= stock − reserved), món gọi, kiên nhẫn, bếp, món trên tay, tiền, uy tín. Không tự tạo luật gameplay ở client; mọi state lấy từ snapshot/event. Không hard-code số liệu gameplay; không thêm trường snapshot. Giữ tương thích `build_cmd`/`run_cmd`/`headless_cmd`. Không sửa `chonoi/live.py` hay `chonoi/web/` ngoài PR riêng có ADR. Phần sáng tạo phải tắt ở headless. Asset ngoài chỉ CC0/CC-BY/MIT và ghi `CREDITS.md`. Chạy app, kiểm Gather và Quán, xử lý field thiếu/null, cung cấp bằng chứng và báo cáo test thực tế.

## 7. Báo cáo cuối công việc

- Issue / Branch / PR / Phase:
- Công nghệ/UI framework:
- Màn hình/component hoàn thành; AC đã đạt:
- State/command/event đã dùng (link `docs/contracts/`):
- Thay đổi framework (PR + ADR):
- Lệnh chạy:
- Kịch bản đã kiểm tra; ảnh/video (`docs/proof/phase-n/...`):
- Vấn đề còn tồn tại:
- Nội dung đã ghi vào `docs/ai-usage-log.md`:

## 8. Phase 2 — TICKET-02 "Một ngày ở chợ nổi" (Test Contract v1.1, hạn tag `phase-2` lúc 1:55)

Theo `docs/plan/phase-2.md` (#6), Người 3 nhận **AC-P2-08** (menu, pause, HUD sáng/tối) và **AC-P2-07** (`--mode day`, Shop, nâng cấp, `--days`, pause) **cùng Người 4**. `chonoi/day.py` đã có trên `main` (#14, 26 test trong `tests/test_day.py`), nên AC-P2-07 giờ là **kiểm chứng**: Người 4 chạy `cmp` hai lần cùng seed, `--days 5`, ngất → quán kho rỗng với gather thật; Người 3 kiểm giao diện Shop và vòng ngày bằng mắt. Chi tiết trường và màn hình ở phụ lục v1.1 của `docs/contracts/ui-interface.md` (#12), trong đó mỗi mục có nhãn **[T]** (ticket yêu cầu) hoặc **[ĐX]** (đề xuất của Người 3).

**Nguyên tắc:** làm hết [T] trước, cho đạt tag `phase-2`. [ĐX] và phần sáng tạo chỉ làm sau khi lõi đã đúng (TICKET-02 §3). Phạm vi lõi chỉ có Cá Sấu; Rắn Hổ Mây và các mục trong bảng Mở rộng không bắt buộc với nhóm 4 người.

**Cập nhật:** #14 của Người 2 (`--mode day`, Shop, pause, ADR-0002, khung các màn hình) **đã merge vào `main`**. Phần còn lại của Người 3 là đưa giao diện `chonoi/web/index.html` trên `main` đạt [T] (đã review #14), qua một PR thường từ `main`.

### 8.1 Việc theo thứ tự ưu tiên

**Bắt buộc [T]: làm trước, chặn tag `phase-2`**
1. **Chữ không chân ≥ 18 px ở 1280×720** trên mọi màn hình (`index.html` hiện dùng 10–16 px).
   - **Kho khả dụng** ở HUD quán: `index.html` đang hiện `stock` (gồm phần khách đã giữ), phải là `stock − Σ reserved`.
   - **Tiền ca** ở HUD quán: đang hiện tổng `money`, phải là `stats.day.earned` (hoặc `earned` − `earned` đầu pha).
   - **Giỏ theo loại**: thêm số đếm và tên từng loại.
2. **HUD sáng:** Máu (theo `hp_max`, 4–5 khi có Áo phao); oxy dưới 25% đổi màu / nhấp nháy; "Hết hơi!" khi oxy cạn; thời gian đổi màu khi ≤ 30 s; độ sâu; giỏ theo loại; **đã lấy / cần**; hồi bắt; gợi ý hái / cập bến khi đến gần; **"Thủy quái!" + viền tím khi có thủy quái gần** (`index.html` hiện chỉ hiện sau khi bị cắn).
3. **HUD quán:** đồng hồ ca; tiền ca; uy tín; món và kiên nhẫn **tại từng bàn**, đổi màu khi < 25%; tiến độ bếp / trạng thái món chín; món đang cầm; kho khả dụng.
4. **Các màn hình** (khung đã có ở #14, kiểm đủ nội dung): Menu chính (Chơi, Thoát) → DayIntro (Ngày, danh sách Má Tư đọc, tự chuyển sau 4 s hoặc khi nhấn phím) → EveningIntro (số lượng nhập kho, món nấu được) → DayResult (khách phục vụ / bỏ đi, tiền, boa, thay đổi uy tín) → Shop (Bình oxy, Áo phao; đóng sớm được, tự đóng khi hết giờ) → Summary sau Ngày 5 (tổng tiền, tổng điểm, uy tín, món bán chạy).
5. **Pause:** Esc/P; menu làm mờ nền, có Tiếp tục và Về menu; dừng đồng hồ và mọi timer gameplay, kể cả trong Shop.
6. **≥ 30 FPS trung bình ở 1280×720**, có số đo. Ảnh chụp và số đo lưu vào `docs/proof/phase-2/`.

**Đề xuất [ĐX]: chỉ làm khi hết [T]**
7. Thước độ sâu tô 3 vùng; phiếu order T1–T4 cố định trên màn hình; mũi tên chỉ quái ngoài khung nhìn; nhân vật nhấp nháy khi bất tử; phím 1/2/Enter trong Shop; bộ đếm FPS bật bằng phím.

**Sáng tạo: sau cùng, không chặn tag, phải tắt ở headless**
8. Nâng demo `client/demo/ui-3d-demo.html` lên v1.1: cá kèo, Cá Sấu Năm Chèo, ghe cây bẹo cho Shop, 4 bàn. Muốn đưa thành client thật thì cần **ADR-0003** (route tĩnh, vendor `three.module.min.js` kèm LICENSE thay cho CDN).

### 8.2 Nhịp theo TICKET-02 §5
| Phút | Việc của Người 3 |
|---|---|
| 0–5 | Chốt giao diện chuyển pha; chia việc AC-P2-07 với Người 4 |
| 5–20 | Chữ ≥ 18 px; HUD sáng v1.1 [T] trên `main` |
| 20 | Báo tiến độ UI ở standup (Người 2 điều phối); chơi thử HUD trên bản tích hợp |
| 20–35 | HUD quán v1.1 [T]; kiểm nội dung Shop, Pause, DayResult, Summary |
| 35–45 | Chơi thử trọn 1 Ngày và nhiều Ngày (kiểm cấp nâng cấp có hiệu lực từ Ngày sau); chụp 1280×720; đo FPS; cùng Người 4 điền `docs/verification/phase-2.md` |
| 45–50 | Góp ý retro phần UI (Người 2 điều phối, AC-P2-10) |
| 50–55 | Dự phòng; Người 2 gắn `phase-2` chậm nhất 1:55 |

### 8.3 Tiêu chí nghiệm thu Phase 2 (phần Người 3)
- [ ] Chơi trọn vòng ngày có menu, pause và HUD; DayIntro công bố đúng kế hoạch D1–D5.
- [ ] HUD sáng/tối có đủ mọi thành phần **[T]** của ticket; chữ ≥ 18 px ở 1280×720 (có ảnh); ≥ 30 FPS (có số đo).
- [ ] Shop mua đúng: trừ `money`, giữ `earned`; cấp hiển thị ngay, có hiệu lực từ Ngày kế; `buy_failed` khi không đủ tiền hoặc đã tối đa.
- [ ] Thay đổi giao diện không đụng headless: Người 4 `cmp` output trước/sau.
- [ ] Ghi phần AI đã dùng cho UI vào `docs/ai-usage-log.md`.

### 8.4 Rủi ro
- **Gather v1.1 chưa có** trên `main` (cá bơi/sinh, Cá Sấu `monsters[]`, nút N5/N6, của Người 1). Vòng ngày hiện chỉ kiểm được với gather v1.0 (#8). "Thủy quái!" và viền tím chưa kiểm bằng mắt được cho tới khi có `monsters[]`; ghi trung thực trong verification.
- Sửa `chonoi/web/index.html` (file khung, đã có ADR-0002): báo Người 2 trước để không sửa cùng lúc.
