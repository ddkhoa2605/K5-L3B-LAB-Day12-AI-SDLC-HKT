# Clarify — câu hỏi và câu trả lời (PO ghi, cả nhóm dùng chung)

| # | Ngày giờ | Câu hỏi | Trả lời / giả định | Ai quyết |
|---|---|---|---|---|
| 1 | 21/11/2026 08:15 | `invuln_ticks` trong khung có tác dụng gì ở Phase 1? | PRD-0 không có luật sát thương/bất tử ở Phase 1. Giữ 0, giảm dần nếu fixture nạp vào, không dùng. | PO |
| 2 | 21/11/2026 08:20 | Bấm `interact` đúng mép bán kính bến và cùng vị trí có nút hái thì thế nào? | Cập bến xét trước hái. Khoảng cách Euclid tính cả đúng mép (`<= dock_radius`). Trong bến thì kết thúc `docked` ngay. | PO / PRD-0 |
| 3 | 21/11/2026 08:25 | Dưới nước bấm `interact` ngoài bến có tác dụng gì không? | Không. Dưới nước thì `interact` ngoài bến bị bỏ qua, không event, không hái. | PO / PRD-0 |
| 4 | 21/11/2026 08:30 | Bắt cá ở mặt nước hoặc bấm `catch` khi đang cooldown? | Bỏ qua hoàn toàn, không phát sinh event và không đặt lại cooldown. | PO / PRD-0 |
| 5 | 21/11/2026 08:35 | Bắt cá khi giỏ còn chỗ trống nhưng nhỏ hơn yield của đàn? | Phát `hold_full` (`action: "catch"`), không nhận một phần, giữ nguyên đàn cá, không đặt cooldown. | PO / PRD-0 |
| 6 | 21/11/2026 08:40 | Đàn cá có bơi hoặc sinh thêm ở Phase 1 không? | Phase 1 đàn cá đứng yên, vị trí giữ nguyên. Bơi và sinh thêm thuộc Phase 2. | PO / Khung |
| 7 | 21/11/2026 08:45 | Quán gặp trường hợp `no_dish` thì xử lý ra sao? | Không tạo khách mới, không trừ hay thay đổi uy tín. | Cả nhóm |
| 8 | 21/11/2026 08:50 | Khách quán chưa nấu thì `base_price` và `tip` bằng bao nhiêu? | Khách chưa nấu có `base_price = 0`, `tip = 0`; giá chỉ chốt khi `cook_started`. | Cả nhóm |
| 9 | 21/11/2026 08:55 | `scenario.py` là khung (hạn chế sửa) hay phần nhóm cần viết (kiểm mâu thuẫn mức luật)? | Nhóm thêm kiểm tra mức luật trong `scenario.py` bằng PR riêng + ghi lý do (ADR-0001). | PO (Người 1) |
| 10 | 21/11/2026 09:00 | Khách fixture không có `dish_id`: hợp lệ không? | Thiếu `dish_id` → mã 2; đơn assigned/served mặc định giá menu. | Người 2 → PO |
| 11 | 21/11/2026 09:05 | Hết ca mà khách waiting đúng lúc kiên nhẫn = 0: `patience` hay `closing`? | `closing` (PRD: hết kiên nhẫn chỉ xét nếu ca còn giờ), không trừ uy tín. | Người 2 → PO |
| 12 | 21/11/2026 09:10 | Phase 1 có phải làm "Mở rộng" không? | Nhóm 4 người không bắt buộc, ưu tiên hoàn thành toàn bộ phần lõi. | PO |
| 13 | 21/11/2026 10:25 | Thứ tự bắt cá và cá bơi trong cùng 1 tick xử lý thế nào? | Thao tác `catch` của player được xét theo vị trí của cá trước khi cá bơi trong bước đó; cá bị bắt thì không tham gia bơi nữa. | PO (Người 1) |
| 14 | 21/11/2026 10:30 | Đàn cá mới sinh tại tick `360·k` có bơi ngay ở tick đó không? | Không, cá mới sinh tham gia bơi từ bước sau (`age_ticks = 0` lúc vừa sinh). | PO (Người 1) |
| 15 | 21/11/2026 10:35 | Cá Sấu Năm Chèo tuần tra và phát hiện người chơi ở d nào? | Chỉ tuần tra và phát hiện ở `d >= 10`. Nếu người chơi ở `d < 10` (vùng nông), Cá Sấu không chase hoặc lập tức quay về patrol. | PO (Người 1) |
| 16 | 21/11/2026 10:40 | Hướng lùi recoil của Cá Sấu khi chạm người chơi trùng tâm? | Quy chuẩn theo Ticket-02: nếu trùng tâm thì lùi theo hướng +x `[1, 0]`. Ngược lại chốt theo vector từ người chơi ra quái vật. | PO (Người 1) |
| 17 | 21/11/2026 10:45 | Quy tắc mất đồ LIFO khi bị Cá Sấu hit và khi ngất? | Bị hit: bỏ `floor(len(hold) / 2)` phần tử cuối mảng theo LIFO. Ngất do Cá Sấu: bỏ toàn bộ giỏ còn lại theo LIFO, mở quán với kho rỗng. | PO (Người 1) |
| 18 | 21/11/2026 10:50 | Quái vật trong chế độ gather độc lập nạp như thế nào? | Dùng bố trí Ngày 1: chỉ sinh quái M1 (from_day = 1) tuần tra [60,24] ↔ [64,24]. Quái M2 chỉ xuất hiện từ Ngày 3. | PO (Người 1) |
| 19 | 21/11/2026 11:10 | Gather bật freshness khi nào, khi quán/day chưa đổi sang kho cá thể? | Gather bật v1.2 khi manifest có `tuning.freshness`; không có thì giữ kho đếm v1.1, không hao. `game.contract.json` chỉ chuyển sang `"1.2"` khi quán/day (Người 2) sẵn sàng, tránh làm hỏng `main`. | PO (Người 1) → Người 2 |
| 20 | 21/11/2026 11:15 | Hàng mới hái/bắt trong tick có hao ngay tick đó không? | Không. Hao ở đầu bước chỉ áp lên hàng đã có; hàng mới `fresh = 100` và hao từ bước sau. | PO (Người 1) |
| 21 | 21/11/2026 11:20 | Số dùng để so ngưỡng 30 và xuất file? | 240 đơn vị/điểm (hao 2 đơn vị/tick ở gather), so ngưỡng trên số nguyên; xuất `fresh = đơn vị/240` (số nguyên khi tròn, ví dụ 100, 97.5) nên đọc lại giữ đúng nhánh ở 30. | PO (Người 1) |
| 22 | 21/11/2026 11:25 | Mở rộng Dòng nước lũ (current) và Khách đặt trước có bắt buộc không? | Không với nhóm 4 người. Người 1 chưa làm `current`; đặt trước thuộc quán/day (Người 2). Ghi trung thực trong verification. | PO (Người 1) |
