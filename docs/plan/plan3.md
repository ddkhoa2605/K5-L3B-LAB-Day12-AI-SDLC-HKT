# PLAN 3 – Người 3 phụ trách `client/ui` (chỉ UI)

> Đặt tại `docs/plan/plan3.md` (không đặt trong `docs/members/`).
> **Nguồn yêu cầu:** đối chiếu PRD-0 (tab Phase 1 trên lab board, đọc ngày 21/11/2026) và `docs/plan/plan.md` (đã có trên `main` từ #8). Mục 1–7 là kế hoạch Phase 1 (Test Contract v1.0); Phase 2 thêm ở mục 8 (#13). Nếu lệch nhau thì ưu tiên lab board.

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
