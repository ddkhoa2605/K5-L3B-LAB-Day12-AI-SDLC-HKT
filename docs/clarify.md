# Clarify — câu hỏi và câu trả lời (PO ghi, cả nhóm dùng chung)

| # | Ngày giờ | Câu hỏi | Trả lời / giả định | Ai quyết |
|---|---|---|---|---|
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

