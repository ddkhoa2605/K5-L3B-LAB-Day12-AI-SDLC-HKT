# Retro nhóm

## Phase 2 (nhanh) — BẢN NHÁP của Người 2, cả nhóm bổ sung
- Điều tốt: Quán và vòng ngày headless có test tự động (104 test) và `cmp` tất định; mọi thay đổi khung đều có PR riêng + ADR (0001, 0002); tài liệu hợp đồng viết trước khi code.
- Điều tệ: 7+ PR mở cùng lúc, nhiều PR xếp chồng, chưa PR nào được review/merge nên chưa thể tag đúng hạn; lát `day`/Shop/HUD chưa có người nhận từ đầu phase nên Người 2 làm thay; phần Gather v1.1 (cá bơi/sinh, Cá Sấu) chưa bắt đầu; CI đỏ vì `TEAM.md` chưa điền.
- 1 hành động cho Phase 3 (cần người nhận): Người 3 điền `TEAM.md` và review/merge #1, #2, #4, #5 theo thứ tự trong 10 phút đầu; Người 1 nối `gather` v1.1 vào `DaySession`.

## Phase 3 (nhanh) — BẢN NHÁP của Người 2, điều rút ra từ lần đổi kho
- Điều tốt: cắt thẳng sang kho cá thể (một lượt, không hai nhánh luật) nên không có trạng thái nửa vời; số nguyên 240 đơn vị/điểm làm ngưỡng 30 và `floor` chính xác, test dễ viết; đổi test có bảng lý do ở `CHANGELOG.md`.
- Điều tệ: khái niệm "kho" nằm ở ~9 file + ~9 file test nên PR lõi vượt xa 400 dòng; adapter gather phải tự viết thay vì chờ Người 1; bật mở rộng đặt trước mặc định làm 8 test lõi đỏ phải thêm `random_reservations:false`; HUD và dòng nước lũ chưa có người nhận từ đầu phase; một lệnh shell lỗi (heredoc không có dấu nháy) làm mất chữ trong `clarify.md` và đã đẩy lên một commit trước khi sửa.
- 1 hành động cho Phase 4 (cần người nhận): Người 3 làm HUD độ tươi + hai đơn đặt trước; Người 1 duyệt commit adapter rồi rebase gather v1.1; Người 2 viết mọi lệnh shell có `$`/backtick bằng file thay vì heredoc không nháy.

## Phase 4 (cuối)
- Rà lại hành động Phase 2: đã làm chưa? vì sao?
- Điều tốt / điều tệ:
- Số liệu: số commit theo người, cách đọc code của nhau, token theo người:
- Một lần AI sai và cách nhóm phát hiện:
- Nếu làm lại, đổi gì:
