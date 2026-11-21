# Clarify — câu hỏi và câu trả lời (PO ghi, cả nhóm dùng chung)

| # | Ngày giờ | Câu hỏi | Trả lời / giả định | Ai quyết |
|---|---|---|---|---|
| 1 | 2026-11-21 | `scenario.py` là khung (hạn chế sửa) hay phần nhóm cần viết (kiểm mâu thuẫn mức luật)? | Chưa có trả lời. Giả định tạm: nhóm thêm kiểm tra mức luật trong `scenario.py` bằng PR riêng + ghi lý do. Cần hỏi Anh Năm hàng xóm/giảng viên. | PO (Người 1) |
| 2 | 2026-11-21 | PRD-0 mẫu ghi `team: cho-noi-01`, `headless_cmd: ./game headless`; starter dùng `python3 -m chonoi.headless`. Dùng giá trị nào? | Chưa có trả lời. Giả định: giữ starter Python, `headless_cmd` theo starter, `team` = tên nhóm thật. | PO |
| 3 | 2026-11-21 | Smoke PRD-0: lệnh gather bị cắt (`--ticks 1 --ou…`) trên lab board; có đúng là `--inventory-out catch.json` (quan đọc `catch.json`)? | Đã đối chiếu `tests/test_smoke_p1.py::test_inv_01…`: đúng. Đóng. | Người 2 |
| 5 | 2026-11-21 | PRD-0 mục F chưa nói rõ khi `no_dish`: có tạo khách (đơn `unfulfillable`) hay không? | Giả định: **không** tạo khách, không đổi uy tín. Ghi ở `docs/contracts/contract.md`. Cần PO xác nhận. | Người 2 → PO |
| 6 | 2026-11-21 | Khách fixture không có `dish_id`: hợp lệ không? `base_price` khi chưa nấu là gì? | Giả định: thiếu `dish_id` → mã 2 (cần để cấp giữ chỗ theo công thức); khách chưa nấu `base_price = 0`, giá chốt lúc `cook_started`; đơn assigned/served mặc định giá menu. | Người 2 → PO |
| 7 | 2026-11-21 | Hết ca mà khách waiting đúng lúc kiên nhẫn = 0: `patience` hay `closing`? | Giả định: `closing` (PRD: hết kiên nhẫn chỉ xét "nếu ca còn giờ"), không trừ uy tín. | Người 2 → PO |
| 8 | 2026-11-21 | Boa: `floor(món × tip_rate)` dùng float; có cần epsilon? Uy tín cộng/trừ dễ trôi số thực. | Giả định: không epsilon cho boa; uy tín làm tròn 6 chữ số sau mỗi lần đổi để `floor(reputation)` không lệch. | Người 2 |
| 4 | 2026-11-21 | Phase 1 có phải làm "Mở rộng" không? | PRD-0: nhóm 4 người không bắt buộc. Giả định: không làm trong Phase 1. | PO |
| 9 | 2026-11-21 | Ai làm lát `--mode day` / Shop / pause / menu / HUD (TICKET-02, lát 4)? | Chưa có người nhận. Giả định tạm: Người 2 dựng khung (`chonoi/day.py`, `pause.py`, ADR-0002) trong PR riêng; Người 3 hoàn thiện giao diện, Người 4 kiểm. Cần PO xác nhận. | PO |
| 10 | 2026-11-21 | Khóa `day_plan` và `shop` nằm ở đâu trong `game.contract.json`? Ticket chỉ nói "khóa thêm". | Giả định: dưới `tuning`, cùng cấp `quan`, `menu`. | PO |
| 11 | 2026-11-21 | Khi cạnh `pause` kết thúc pause, các cạnh hành động cùng frame có chạy không? | Giả định: có, gameplay chạy ngay trong bước đó với đủ cạnh của frame (ticket: "chạy gameplay ngay trong bước đó"). Khi đang pause và vào pause thì bỏ qua mọi cạnh hành động và `buy`. | Người 2 |
| 12 | 2026-11-21 | Event ở tick 0 (`day_start`, `day_plan`, `phase_start`) nằm trước hay sau snapshot tick 0? | Giả định: sau snapshot tick 0 (snapshot "sau khi dựng fixture, trước mọi input"). Không thêm snapshot riêng khi đổi pha. | Người 2 |
| 13 | 2026-11-21 | Trường `mode` trong snapshot/`end` của `day` là gì? | Giả định: `"day"`; `phase` là `gather/quan/shop`. | Người 2 |
| 14 | 2026-11-21 | Lệnh `buy` mở rộng (`weapon`, `net`, `buy:<kind>`) khi chưa bật mở rộng? | Giả định: `buy_failed` với `reason:"unknown"` (ticket: lệnh không hỗ trợ). `out_of_stock` chỉ khi có Chợ Chú Sáu. | Người 2 |
| 15 | 2026-11-21 | Cấp nâng cấp khai ở `day.upgrades` có hiệu lực từ Ngày 1 không? | Giả định: có (`active_upgrades` = `upgrades` lúc khởi tạo). | Người 2 |
| 16 | 2026-11-21 | Bật `burn` thế nào, và mặc định? | Giả định: tắt mặc định (`burn_s: null`, không khai `extensions`) để giữ số lõi; bật bằng `extensions:["burn"]` + `quan.burn_s: 20`. Nhóm 4 người không bắt buộc. | Người 2 |
| 17 | 2026-11-21 | DayIntro/EveningIntro có tạm dừng đồng hồ không? | Giả định: không (chỉ lớp phủ, tự tắt sau 4 s hoặc khi bấm phím); pause thật dùng Esc/P. | Người 2 → Người 3 |
| 18 | 21/11/2026 08:15 | `invuln_ticks` trong khung có tác dụng gì ở Phase 1? | PRD-0 không có luật sát thương/bất tử ở Phase 1. Giữ 0, giảm dần nếu fixture nạp vào, không dùng. | PO |
| 19 | 21/11/2026 08:20 | Bấm `interact` đúng mép bán kính bến và cùng vị trí có nút hái thì thế nào? | Cập bến xét trước hái. Khoảng cách Euclid tính cả đúng mép (`<= dock_radius`). Trong bến thì kết thúc `docked` ngay. | PO / PRD-0 |
| 20 | 21/11/2026 08:25 | Dưới nước bấm `interact` ngoài bến có tác dụng gì không? | Không. Dưới nước thì `interact` ngoài bến bị bỏ qua, không event, không hái. | PO / PRD-0 |
| 21 | 21/11/2026 08:30 | Bắt cá ở mặt nước hoặc bấm `catch` khi đang cooldown? | Bỏ qua hoàn toàn, không phát sinh event và không đặt lại cooldown. | PO / PRD-0 |
| 22 | 21/11/2026 08:35 | Bắt cá khi giỏ còn chỗ trống nhưng nhỏ hơn yield của đàn? | Phát `hold_full` (`action: "catch"`), không nhận một phần, giữ nguyên đàn cá, không đặt cooldown. | PO / PRD-0 |
| 23 | 21/11/2026 08:40 | Đàn cá có bơi hoặc sinh thêm ở Phase 1 không? | Phase 1 đàn cá đứng yên, vị trí giữ nguyên. Bơi và sinh thêm thuộc Phase sau. | PO / Khung |
| 24 | 2026-11-21 | Thứ tự  so với  trong một bước gather? | Giả định:  trước, rồi  (ticket: "đồng hồ, cooldown, hồi nút và độ tươi"). | Người 2 |
| 25 | 2026-11-21 | / trong snapshot sắp thế nào? | Giả định:  (quán, Shop) và file kho sắp theo id (F2 trước F10);  giữ thứ tự vào giỏ (cần cho LIFO). | Người 2 |
| 26 | 2026-11-21 | Ranh giới adapter gather: ai sở hữu hao tươi// trong ? | Người 2 viết adapter tối thiểu (commit riêng) để  không vỡ; Người 1 duyệt và sở hữu từ đó. Không đụng nút/cá/dòng lũ. | Người 2 → Người 1 |
| 27 | 2026-11-21 | Ví dụ ticket dùng  trong scenario gather; khóa này thuộc gather v1.1 chưa cài. | Giả định: nhận  chỉ khi là mảng rỗng; khác rỗng → mã 2 cho đến khi Người 1 cài thủy quái. | Người 2 → Người 1 |
| 28 | 2026-11-21 | Giá chốt khi nấu ở bước đầu của ca đã thấp hơn niêm yết 1 đơn vị (60 → 59) do kho hao ngay ở bước 1. Có đúng ý ticket? | Giả định: đúng (hao tươi xử lý trước tương tác theo thứ tự tick Quán); đã ghi CHANGELOG. Cần PO xác nhận. | PO |
| 29 | 2026-11-21 | Khách chưa nấu có  bao nhiêu khi giá theo tươi? | Giữ nguyên v1.1: 0 cho đến  (giá chốt lúc nấu). | Người 2 |
| 30 | 2026-11-21 | Stream RNG cho Khách đặt trước (R1,R2): tên nào? | Giả định:  (stream riêng, không đổi chuỗi của stream cũ). | Người 2 |
| 31 | 2026-11-21 | Cập nhật phiên bản  khi mở rộng chưa làm hết (HUD, dòng lũ)? | Giả định: manifest tự nhận 1.2; phần chưa làm (HUD độ tươi — Người 3, dòng lũ — Người 1) ghi trung thực ở . | Người 2 |
