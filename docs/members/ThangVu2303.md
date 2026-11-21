# ThangVu2303 — phản tư cá nhân (≤ 200 từ)

- **Tôi đã làm:**
  - PO, phụ trách module `sim/gather`: hoàn thiện Lát 1 (bơi, oxy, mất máu, giỏ) và Lát 2 (hái, bắt cá, cập bến, xuất kho).
  - Phase 2: Cài đặt cá bơi 1.5 m/s phản xạ mép, sinh cá theo lịch 360 tick; Cá Sấu Năm Chèo patrol, chase, hit mất máu và rơi nửa giỏ LIFO ([#17](https://github.com/ddkhoa2605/K5-L3B-LAB-Day12-AI-SDLC-HKT/pull/17)).
  - Phase 3: Kho cá thể `{id, kind, fresh}`, hao tươi 0.5/s, event `spoiled`, bộ test `test_gather_p3.py`.
  - Cập nhật quy trình và giải đáp thắc mắc trong `docs/clarify.md`.
- **Tôi đã review:**
  - Review các PR của Quán v1.0, Quán v1.1, chế độ `day` và `shop` của Người 2; PR UI của Người 3.
  - Góp ý chuẩn hóa dung sai float `EPS = 1e-9` và so sánh thứ tự ID chuẩn `id_key`.
- **AI sai ở đâu và tôi phát hiện thế nào:**
  - AI lệch tick bất tử (`invuln_ticks = 89` thay vì 90) và quên tính 1 tick chase trước khi Cá Sấu va chạm; phát hiện khi chạy trace step-by-step và đối chiếu TICKET-02.
- **Điều tôi học được:**
  - Đọc kỹ tài liệu hợp đồng và ma trận sự kiện theo từng tick trước khi viết assertion cho test.
