# huuthinh812 — phản tư cá nhân (≤ 200 từ)

- Ở vai trò QA lead, tôi viết công cụ so sánh đầu ra headless theo từng byte, smoke test bàn giao kho từ Gather sang Quán và bộ test schema kho cá thể v1.2. [Công cụ QA](https://github.com/ddkhoa2605/K5-L3B-LAB-Day12-AI-SDLC-HKT/commit/2e5adcf) · [Test kho v1.2](https://github.com/ddkhoa2605/K5-L3B-LAB-Day12-AI-SDLC-HKT/commit/a2e0357)
- Tôi hỗ trợ nhóm tích hợp bằng cách lập ma trận kiểm chứng Phase 3, ghi rõ các test và bằng chứng cần đối chiếu khi hai chế độ dùng chung schema kho mới. [Ma trận kiểm chứng](https://github.com/ddkhoa2605/K5-L3B-LAB-Day12-AI-SDLC-HKT/commit/b57599d)
- AI đề xuất dùng `cmp` để so sánh hai file JSONL. Khi thử trên Windows, tôi gặp lỗi vì môi trường thiếu lệnh này. Tôi chuyển sang `filecmp` và SHA256 để nhóm dùng cùng một quy trình trên Windows và Linux. [Nhật ký AI](https://github.com/ddkhoa2605/K5-L3B-LAB-Day12-AI-SDLC-HKT/blob/main/docs/ai-usage-log.md)
- Tôi học được rằng khi đổi schema dùng chung, cần kiểm tra cả dữ liệu hợp lệ lẫn dữ liệu phải bị từ chối. Với kiểm tra tính tất định, tôi cần giữ nguyên seed và đầu vào rồi so sánh toàn bộ kết quả.
