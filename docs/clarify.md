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
