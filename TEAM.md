# TEAM

**Tên nhóm:** HKT  **Số người:** 4  (khớp `team_size` trong `game.contract.json`)

| Thành viên | GitHub handle | Module chính | Vai quy trình | Người dự phòng cho |
|---|---|---|---|---|
| Vũ Đình Thắng (Người 1) | ThangVu2303 | `sim/gather` | PO | Người 2 (`sim/quan`) |
| Đoàn Đăng Khoa (Người 2) | ddkhoa2605 | `sim/quan` | Integrator + Release (gắn tag, retro) | Người 3 (`client/ui`) |
| Nguyễn Văn Minh (Người 3) | vminh21 | `client/ui` | — (chỉ làm UI) | Người 4 (`qa`) |
| Nguyễn Hữu Thịnh (Người 4) | huuthinh812 | `qa` | QA lead | Người 1 (`sim/gather`) |

**Vai quy trình:** PO (đầu mối hỏi giảng viên, giữ `docs/clarify.md`) · Integrator (giữ `docs/contracts/`, gắn tag) · QA lead · Scrum/Release. Có thể kiêm.

## Thỏa thuận làm việc nhóm (điền trong 15 phút kickoff, ≤ 10 dòng)

- Kênh liên lạc: nhóm chat chung của 4 người; thảo luận kỹ thuật ghi lại trên PR/issue GitHub.
- Khi bất đồng về thiết kế: mỗi bên nói tối đa 2 phút; không xong thì Integrator (Người 2) quyết và ghi lý do vào PR hoặc `docs/clarify.md`.
- Khi ai đó trễ hoặc vướng quá 10 phút: báo ngay trong kênh chat; người dự phòng (cột trên) nhận việc hoặc pair.
- Giờ standup giữa phase: phút 20 của mỗi phase, 2–3 phút (đã xong / sắp làm / đang vướng), Người 2 điều phối.
- Cách đọc code của nhau: mỗi PR có ít nhất 1 người khác review, nhận xét bám dòng; reviewer chính theo `docs/plan/plan.md` mục 4.
- Cách làm việc với Git: nhánh ngắn theo lát (`feature/…`, `docs/…`) + PR vào `main`, ≥ 1 review (đụng `docs/contracts/`, khóa contract hoặc schema kho: 2 approvals); Integrator (Người 2) merge theo thứ tự và gắn tag.
