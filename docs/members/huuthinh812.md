# huuthinh812 — phản tư cá nhân (≤ 200 từ)

- **Tôi đã làm:**
  - QA Lead: Xây dựng công cụ kiểm tra tất định (`tools/check_determinism.py`), skill `determinism-check`, bộ test QA (`tests/test_qa_determinism.py`) ([#7](https://github.com/ddkhoa2605/K5-L3B-LAB-Day12-AI-SDLC-HKT/pull/7)).
  - Thiết lập công cụ kiểm tra nhóm `tools/check_team.py` và bộ test `tests/test_team_check.py`.
  - Viết bộ test đặc tả schema kho cá thể v1.2 (`tests/test_p3_schema.py`) và chạy smoke test tích hợp 2 tiến trình `tools/smoke_integration.py`.
  - Giám sát hồi quy (regression) và ma trận kiểm chứng xuyên suốt 4 phase.
- **Tôi đã review:**
  - Review các PR `#17` (Gather v1.1), `#20` (Kho v1.2), `#24` (HUD v1.2), `#25` (Release Phase 4).
  - Yêu cầu bổ sung bằng chứng và kiểm tra tính tất định trước khi approve.
- **AI sai ở đâu và tôi phát hiện thế nào:**
  - AI ban đầu dùng lệnh `cmp` của Linux làm hỏng kiểm thử trên Windows; tôi đã yêu cầu viết lại bằng Python `filecmp` và băm SHA256 đa nền tảng.
- **Điều tôi học được:**
  - Kiểm thử hộp đen tự động và tính tất định byte-by-byte là chốt chặn tin cậy nhất khi làm việc với AI tốc độ cao.
