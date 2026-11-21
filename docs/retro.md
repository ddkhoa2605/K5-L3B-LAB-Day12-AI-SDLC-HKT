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
- Rà lại hành động Phase 2: `TEAM.md` đã điền đủ 4 người (#15) nhưng **trễ** (sau Phase 2); PR đã được review chéo và merge; gather v1.1/v1.2 tích hợp vào `day` (#17).
- Điều tốt: 245 test OK, tất định byte-identical (`tools/check_determinism.py`), `bench_cmd` và `soak_cmd` chạy được, thiết kế lại giao diện có bằng chứng thật (#27), mọi thay đổi khung có ADR.
- Điều tệ: **tag trễ hạn** (xem dưới); 25 PR mở dồn cuối nên phải gộp hàng loạt và giải nhiều xung đột `docs/`; một tài khoản không có trong `TEAM.md` (`VQuant68`) đẩy thẳng 3 commit lên `main`, trong đó có tài liệu phản tư viết thay người khác và verification ghi "Đạt" cho tag chưa tồn tại — đã gỡ/sửa trong PR `chore/review-vquant68`; Phase 3 còn thiếu dòng nước lũ.
- **Ghi trễ hạn tag:** đến khi hoàn tất PR này repo **chưa có tag nào**, trái yêu cầu gắn `phase-1…phase-4` đúng hạn (1:00 / 1:55 / 2:30 / 3:00) và Release `v1.0.0` trước 3:00. Nguyên nhân: Integrator (Người 2) dồn việc gộp PR, không gắn tag ở từng mốc. Tag gắn **sau hạn**, trỏ về commit gần nhất đã đủ việc của từng phase: `phase-1` = `bf35fe7` (gather + quán + hợp đồng v1.0), `phase-2` = `de3b58c` (quán v1.1, `day`, Shop, pause; **chưa** có gather v1.1 — vào ở #17), `phase-3` = `afa5c2a` (kho cá thể, độ tươi, đặt trước, HUD độ tươi), `phase-4` và `v1.0.0` = commit bàn giao trên `main` sau PR này. Lịch sử không tách sạch từng phase vì các PR vào `main` xen kẽ.
- Số liệu: commit trên `main` theo `git shortlog -sn` (tính cả merge): ddkhoa2605 66, vminh21 40, ThangVu2303 6, huuthinh812 4 (Hai Duong 9 là starter của giảng viên); review chéo bằng comment theo dòng ở hầu hết PR; token AI: chưa đo.
- Một lần AI sai và cách nhóm phát hiện: bản plan đầu của Người 2 ghi sai quy trình (mời giảng viên, coi CI là bắt buộc) — lộ ra khi đọc PRD-0 trên lab board; sau đó một lệnh shell làm mất chữ trong `clarify.md`, phát hiện khi đọc lại đầu ra và sửa trước khi merge.
- Nếu làm lại, đổi gì: gắn tag ngay ở mỗi mốc (đặt nhắc ở phút 55/1:50/2:25); chặn đẩy thẳng `main` bằng ruleset (hiện không bật); mỗi người tự viết phản tư của mình.
