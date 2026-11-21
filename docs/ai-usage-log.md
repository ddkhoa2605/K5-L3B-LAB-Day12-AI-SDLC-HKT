# Nhật ký dùng AI (theo phase và theo người)

| Phase | Người | Công cụ / model | Việc | Token / chi phí ước tính | Ghi chú (AI sai ở đâu?) |
|---|---|---|---|---|---|
| 1 | Người 2 | Claude Code (Sonnet 5.5) | Soạn skill `.agents/skills/pr-checklist/SKILL.md` (bản nháp) | chưa đo | Chưa dùng thử trên PR thật; cần chạy thử trên PR #1/#2 rồi chỉnh. |
| 2 | Người 2 | Claude Code (Sonnet 5.5) | Quán v1.1 (2 bếp/4 bàn/6 món, `day_plan`, móc `allowed_dishes`/`money`/`earned`/`reputation`), ADR-0001 — PR #4, #5 | chưa đo | Chưa có lỗi luật; test cũ `test_khong_con_ban_bo_luot` phải sửa vì luật đổi (đã ghi trong PR). Lần đầu viết lệnh shell gộp nhiều heredoc bị lỗi cú pháp, phải tách thành các bước riêng. |
| 2 | Người 2 | Claude Code (Sonnet 5.5) | Chế độ `day` (`chonoi/day.py`), `pause`, input v1.1, Shop/nâng cấp, `extensions`, ADR-0002 | chưa đo | (1) Kỳ vọng tick sai trong test: frame tick k sinh event ở tick k+1, nên đúng chỗ phải +2, không phải +1 (lỗi ở test, không ở luật). (2) Khi chạy thử `live` trên Windows, `print` tiếng Việt lỗi `UnicodeEncodeError` nếu không đặt `PYTHONIOENCODING=utf-8` (lỗi có sẵn của khung, chưa sửa). (3) Lần xem trình duyệt đầu, DayIntro biến mất ngay vì phím Enter ở menu cũng "bấm phím qua intro", rồi vì phím R; đã sửa. |
| 2 | Người 2 | Claude Code (Sonnet 5.5) | Mở rộng `burn_s` (cháy món), `tests/test_burn.py`; viết `docs/verification/phase-2.md`, retro, clarify #9–#17 | chưa đo | Cố ý để `burn` tắt mặc định vì bật sẽ đổi số lõi (`burn_s: null`); không kiểm được phản hồi của chấm tự động với phần này. |
