# PLAN 3 – Người 3 phụ trách `client/ui` (Scrum/Release, trưởng nhóm)

> Đặt tại `docs/plan/plan3.md` (không đặt trong `docs/members/`).
> **Nguồn yêu cầu:** mục 1–7 theo PRD-0 (Phase 1, Test Contract v1.0); **mục 8 theo TICKET-02 (Phase 2, v1.1)**. Cả hai đọc từ lab board ngày 21/11/2026. Phase 3–4 chưa phát hành. Nếu lệch nhau thì ưu tiên lab board.

## 1. Vai trò

- **Module chính:** `client/ui` (đồ họa, âm thanh, menu, HUD theo PRD).
- **Vai quy trình:** Scrum/Release + trưởng nhóm (fork, setup, `AGENTS.md`, standup, retro, điều phối demo). Phụ trách thêm nội dung sáng tạo (module `content`) sau khi lõi xong và **README theo DoD PRD-0** (xem 3.H).
- **Dự phòng cho:** Người 4. **Được dự phòng bởi:** Người 2.
- **Reviewer chính của:** `qa`. **Được review bởi:** Người 2 (và Người 4 là reviewer chính của UI).
- **Điểm liên quan:** làm việc nhóm (25), harness AI (10, `AGENTS.md`), retro (10), chất lượng sản phẩm (10), demo (5).

## 2. Phạm vi

- `chonoi.live` hiện chỉ là cửa sổ thử bằng hình khối. Nó chạy cùng lớp sim với headless ở 60 tick/s và **chỉ đọc snapshot**. Thanh oxy, Máu, giỏ, cá, nút hái chỉ hiện khi luật tương ứng đã được viết, nên UI **phụ thuộc** Người 1/2.
- Điều khiển (PRD-0 §2): WASD/mũi tên để bơi/đi, E (`interact`: cập bến, hái, nấu, bưng, phục vụ), Space (`catch`: bắt cá khi lặn), R chơi lại (của cửa sổ thử).
- Góc nhìn: buổi sáng (gather) là **mặt cắt nhìn ngang** `[x,d]` (d tăng xuống dưới); buổi tối (quán) **nhìn từ trên xuống** `[x,z]`.
- `chonoi/live.py` và `chonoi/web/index.html` thuộc khung giảng viên: hạn chế sửa; **sửa thì PR riêng + ADR**. Starter chỉ dùng thư viện chuẩn Python. Đổi engine/ngôn ngữ là quyết định của nhóm: làm trong một PR, Integrator duyệt, sửa `build_cmd`/`run_cmd`/`headless_cmd` và `ci.yml`, giữ job `ci / test`.
- UI **không tính lại luật**; mọi state lấy từ snapshot/event của sim. Ngoại lệ duy nhất là **giá trị hiển thị suy ra từ snapshot** (ví dụ "kho khả dụng", xem 3.B). Không thêm trường snapshot mới vì như vậy là đổi output contract.
- Asset ngoài chỉ CC0/CC-BY/MIT hoặc tự tạo, ghi nguồn trong `CREDITS.md`. Không commit API key/token/`.env`.

## 3. Kế hoạch

### A. Setup (Phase 1, ~5 phút đầu)
- [ ] Fork repo tên **`K5-L3B-LAB-Day12-AI-SDLC-<ten-nhom>`**, để **public**.
- [ ] Thêm 3 thành viên làm Collaborator quyền **Write**. **Không cần mời giảng viên**: repo public là đủ (PRD-0 §4).
- [ ] Bật Actions và import `.github/ruleset-main.json`. PRD-0 coi đây là tùy chọn; nhóm **chọn dùng** và không bypass.
- [ ] PR đầu tiên gồm:
    - `TEAM.md` **đủ 4 người** (handle thật; thiếu thì `ci / test` đỏ) + thỏa thuận nhóm ≤ 10 dòng: kênh liên lạc, giờ standup, cách quyết khi bất đồng, việc cần làm khi có người trễ/vướng.
    - `team` và `team_size` = 4 trong `game.contract.json`.
    - Chờ CI xanh, ≥ 1 người khác duyệt, rồi merge.
- [ ] Tạo issues (template `.github/ISSUE_TEMPLATE/feature.md`): 4 lát (bơi/oxy/biên/giỏ; hái/bắt/cập bến/kho; khách/giữ chỗ/kiên nhẫn; bếp/bưng/phục vụ/tiền), hợp đồng, 2 skill, UI/HUD, README, `docs/`.

### B. Requirement & UX (Phase 1 theo PRD-0; các phase sau chờ ticket)
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

- [ ] Wireframe/UI flow cho Gather và Quán; AC UI ghi vào `docs/plan/phase-1.md` cùng PO.

### C. Interface (Phase 1 kickoff, chốt trước phút 15)
- [ ] Cùng Người 1/2 chốt trong `docs/contracts/` giao diện `sim/*` ↔ `client/ui`:
    - **Gather đọc:** `time_left_ticks`, `player.{pos, heading_deg, oxygen_ticks, oxygen_max_ticks, hp, hp_max, at_surface}`, `hold`, `hold_count`, `hold_capacity`, `nodes[]` (`ready`, `regrow_ticks`), `fish[]`.
    - **Quán đọc:** `time_left_ticks`, `player.pos`, `stock`, `hand`, `stoves[]` (`state`, `dish`, `cook_ticks_left`), `tables[]` (`customer_id`), `customers[]` (`dish_id`, `patience_ticks_left`, `state`, `reserved`), `money`, `reputation`.
    - **Chung:** `money`, `earned`, `reputation`, `score`, `state`.
    - **Lệnh gửi vào:** `move` [−1,1]², `interact`, `catch` (chỉ tác động ở cạnh lên).
- [ ] Chạy thử `python3 -m chonoi.live --mode gather` và `--mode quan` (`--seed N`, `--port 8000`). Nối hai buổi bằng `--inventory-out kho.json` rồi `--inventory kho.json`.
- [ ] Fallback khi field thiếu/null hoặc entity biến mất. Dùng snapshot giả và kho mẫu `docs/contracts/inventory.sample.json` trong lúc chờ sim.

### D. Implementation
- [ ] Branch `feature/ui-<task>`; PR ≤ ~400 dòng.
- [ ] Layout và HUD theo 3.B; hiển thị state thật; xử lý kết thúc phiên, restart, lỗi đầu vào.
- [ ] Không nhúng số liệu gameplay (lấy từ `game.contract.json`/snapshot); không sửa logic sim trong PR UI.
- [ ] Sửa `live.py`/`web/index.html` chỉ khi cần, bằng PR riêng + ADR (`docs/adr/`, mẫu `0000-template.md`).
- [ ] Đọc diff mọi code AI sinh trước khi mở PR.

### E. Phong cách (PRD-0 §3)
- [ ] Sông nước màu phù sa, bờ dừa nước, nhà sàn, ánh hồng buổi sớm. Buổi tối có đèn dây vàng và khói bếp.
- [ ] Út Sen mặc áo bà ba, buộc khăn rằn, đeo kính lặn tự chế và giỏ lưới.
- [ ] Được bắt đầu bằng hình khối 2D, rồi nâng dần. Khuyến khích giọng Nam Bộ trong thoại. Tôn trọng văn hóa địa phương; asset có quyền sử dụng và ghi `CREDITS.md`.

### F. Sáng tạo của nhóm (tùy chọn, sau khi lõi xong)
- [ ] Được thêm nhân vật, loài cá/cây, sinh vật, món, khu vực, cơ chế nhỏ, câu chuyện, đồ họa, âm nhạc, giao diện.
- [ ] Điều kiện: **tắt ở headless, hoặc bảo đảm không đổi tick, event, tiền, uy tín, snapshot** theo contract. Ghi mục "Sáng tạo của nhóm" trong README **kèm bằng chứng ngắn rằng lõi vẫn đúng** (Người 4 chạy headless trước/sau, `cmp`).
- [ ] Nhóm 4 người không bắt buộc làm mở rộng; độ phức tạp không được cộng điểm. Ưu tiên một ý tưởng gọn, chạy ổn. PR module `content`.

### G. Test & PR
- [ ] Chạy UI bằng `run_cmd`. Kiểm Gather (bơi, oxy, Máu, giỏ, hái, bắt, cập bến) và Quán (khách, món gọi, kiên nhẫn, bếp, tay, tiền, uy tín). Kiểm cả restart, kết thúc, dữ liệu thiếu, UI không hiện state cũ.
- [ ] Chụp ảnh/video vào `docs/proof/phase-n/` (Phase 1: `docs/proof/phase-1/`, dẫn link từ `docs/verification/phase-1.md`).
- [ ] Chạy `PYTHONPATH=tests:. python3 -m unittest discover -s tests -v` trước PR.
- [ ] PR theo template (Closes #, phase, module `ui`/`content`, AC, bằng chứng ảnh/lệnh, đóng góp AI, rủi ro); Người 2 và 4 review theo dòng.

### H. README theo DoD PRD-0 (Người 3 nhận)
- [ ] Cách chạy từ clone sạch trong **≤ 3 lệnh** trên macOS/Linux.
- [ ] Điều khiển (WASD/mũi tên, E, Space).
- [ ] Cách tính điểm: `earned + 100 × floor(reputation)`.
- [ ] Lệnh test **1 lệnh**: `PYTHONPATH=tests:. python3 -m unittest discover -s tests -v`.
- [ ] Hợp đồng kho (schema + ví dụ), có thể dẫn link sang `docs/contracts/` (Người 2 giữ nội dung).
- [ ] Mục "Sáng tạo của nhóm" nếu có (3.F).

### I. Việc Scrum/Release & tài liệu
- [ ] Nhịp Phase 1 theo PRD-0 §6.4:
    - 0–15': kickoff, TEAM.md, chốt hợp đồng kho và interface.
    - Phút 20: rà lát đang vướng, điều người đã xong sang hỗ trợ.
    - **Trước phút 25**: nhắc Người 1 thử xuất file kho thật.
    - Giữa phase: standup.
    - 45–55': **smoke hai tiến trình** (gather ghi kho → quan đọc kho, ví dụ `stock:{"bong_sung":2,"ca_loc":1}` ở tick 0) và chơi thử trên `main`.
    - 55–60': dự phòng; Người 2 gắn `phase-1` chậm nhất 1:00.
- [ ] Standup 2–3 phút (đã xong / sắp làm / đang vướng) → `docs/standup.md`. Vướng > 10': báo kênh, người dự phòng nhận việc.
- [ ] `docs/plan/phase-n.md` ≤ 1 trang mỗi phase (cùng PO).
- [ ] Cập nhật `AGENTS.md` mỗi phase (lệnh chạy được, ngắn gọn; git history phải thấy các lần cập nhật).
- [ ] Giữ `docs/retro.md` (có số liệu); nhắc cả nhóm viết `docs/members/<handle>.md` ≤ 200 từ, `docs/ai-usage-log.md` (theo người và phase, kèm token/chi phí nếu đo được), `CREDITS.md`.
- [ ] Phase 4: điều phối kịch bản demo (trực tiếp hoặc video < 5 phút) và danh sách việc cuối trước Release `v1.0.0`; Người 4 chốt kết luận chất lượng, Người 2 gắn tag.
- [ ] ≥ 3 commit có nội dung bằng tài khoản của mình.

## 4. Tiêu chí nghiệm thu

- [ ] HUD tối thiểu Gather và Quán đúng PRD-0 §2, đọc được trong lúc chơi; chơi được cả hai buổi.
- [ ] UI kết nối sim qua hợp đồng; không thực thi luật ở client (chỉ suy ra giá trị hiển thị như kho khả dụng).
- [ ] Hiển thị đúng state, xử lý field thiếu/null; input không mất.
- [ ] Phần sáng tạo (nếu có) không đổi output headless, có bằng chứng trong README.
- [ ] README đạt DoD (≤ 3 lệnh, điều khiển, cách tính điểm, test 1 lệnh).
- [ ] Repo setup đúng (public, collaborator, `TEAM.md` đủ 4 người, `team_size` khớp, PR đầu merge).
- [ ] Mọi thay đổi framework có PR riêng + ADR; `AGENTS.md` được cập nhật theo phase.
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
- Cập nhật `AGENTS.md` / `docs/standup.md` / `docs/retro.md` / README:
- Vấn đề còn tồn tại:
- Nội dung đã ghi vào `docs/ai-usage-log.md`:

## 8. Phase 2 — TICKET-02 "Một ngày ở chợ nổi" (Test Contract v1.1, hạn tag `phase-2` lúc 1:55)

Theo `docs/plan/phase-2.md` (#6), Người 3 nhận **AC-P2-08** (menu, pause, HUD sáng/tối) và **AC-P2-07** (`--mode day`, Shop, nâng cấp, `--days`, pause) **làm cùng Người 4**: Người 4 làm vòng `day` headless, Người 3 làm UI và Shop. Chi tiết trường và màn hình ở phụ lục v1.1 của `docs/contracts/ui-interface.md`.

### 8.1 Việc theo thứ tự ưu tiên
1. **Chốt giao diện chuyển pha (phút 0–5)** cùng Người 2 và Người 4: thứ tự event `day_start → day_plan → phase_start(...)`; snapshot `day`, `day_plan`, `upgrades`, `active_upgrades`; input `pause`, `shop_done`, `buy`.
2. **ADR-0002 + PR sửa `chonoi.live`** (cùng Integrator): thêm `--mode day [--days N]`; `/input` nhận `pause`, `shop_done`, `buy` (áp `buy` đúng một lần); `meta` = toàn bộ tuning; giữ đủ event của pha. Có test trong `tests/test_live.py`.
3. **HUD sáng v1.1:** Máu theo `hp_max` (cấp Áo phao); oxy < 25% nhấp nháy; "Hết hơi!"; thời gian ≤ 30 s đổi màu; **thước độ sâu 3 vùng**; giỏ theo loại; **cần lấy / đã lấy**; hồi bắt; gợi ý hái / cập bến; **"Thủy quái!" + viền tím**.
4. **HUD quán v1.1:** phiếu order T1–T4 (món + kiên nhẫn, < 25% đổi màu); tiến độ B1, B2, trạng thái món chín; món đang cầm; kho khả dụng 6 loại; tiền ca; uy tín.
5. **Các màn hình:** Menu chính (Chơi/Thoát) → DayIntro (danh sách Má Tư, tự đóng sau 4 s hoặc khi nhấn phím) → EveningIntro (nhập kho, món nấu được) → DayResult (khách phục vụ/bỏ đi, tiền, boa, uy tín thay đổi) → **Shop** (Bình oxy, Áo phao; Xong / tự đóng sau 600 tick; `buy_failed` báo lý do) → Summary sau Ngày 5.
6. **Pause:** Esc/P; menu làm mờ nền, có Tiếp tục / Về menu; dừng đồng hồ và animation gameplay, kể cả trong Shop.
7. **Kỹ thuật:** chữ không chân **≥ 18 px ở 1280×720**; trung bình **≥ 30 FPS** ở 1280×720. Ảnh chụp và số đo lưu vào `docs/proof/phase-2/`.
8. *(Chỉ khi lõi xong)* Nâng demo `client/demo/ui-3d-demo.html` lên v1.1: cá kèo, Cá Sấu Năm Chèo, ghe cây bẹo cho Shop, phiếu order 4 bàn. Đây là phần sáng tạo, **không chặn tag**.

### 8.2 Nhịp theo TICKET-02 §5
| Phút | Việc của Người 3 |
|---|---|
| 0–5 | Chốt giao diện chuyển pha; chia việc AC-P2-07 với Người 4 |
| 5–20 | ADR-0002 + `live.py` mode `day`; khung các màn hình; HUD sáng v1.1 |
| 20 | Smoke tích hợp `gather --inventory-out → quan --inventory` cùng nhóm; standup 2–3 phút (vai Scrum) |
| 20–35 | HUD quán v1.1, Shop, Pause, DayResult/Summary; chốt luồng `day` |
| 35–45 | Chơi thử trọn 1 Ngày và nhiều Ngày (kiểm cấp nâng cấp có hiệu lực từ Ngày sau); chụp 1280×720; đo FPS; cùng Người 4 điền `docs/verification/phase-2.md` |
| 45–50 | Điều phối retro nhanh: một điều tốt, một điều vướng, một hành động có người nhận → `docs/retro.md` |
| 50–55 | Dự phòng; Người 2 gắn `phase-2` chậm nhất 1:55 |

### 8.3 Tiêu chí nghiệm thu Phase 2 (phần Người 3)
- [ ] Chơi trọn vòng ngày có menu, pause và HUD; DayIntro công bố đúng kế hoạch D1–D5.
- [ ] HUD sáng/tối có đủ mọi thành phần bắt buộc của ticket; chữ ≥ 18 px ở 1280×720 (có ảnh); ≥ 30 FPS (có số đo).
- [ ] Shop mua đúng: trừ `money`, giữ `earned`; cấp hiển thị ngay, có hiệu lực từ Ngày kế; `buy_failed` khi không đủ tiền hoặc đã tối đa.
- [ ] Sửa `chonoi.live` có ADR-0002 và test; headless không đổi output (Người 4 `cmp` trước/sau).
- [ ] `AGENTS.md`, `docs/standup.md`, `docs/retro.md`, `docs/ai-usage-log.md` cập nhật cho Phase 2.

### 8.4 Rủi ro
- AC-P2-07 phụ thuộc gather v1.1 của Người 1 (cá bơi, Cá Sấu) và quán v1.1 của Người 2 (#5). Trong lúc chờ, dùng fixture và sim giả để làm UI.
- Nếu ADR-0002 không kịp thì Phase 2 chơi thử bằng hai mode riêng, và **ghi trung thực** trong verification là vòng ngày chưa chơi được trên trình duyệt.
