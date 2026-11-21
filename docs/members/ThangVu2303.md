# ThangVu2303 — phản tư cá nhân (≤ 200 từ)

Vũ Đình Thắng · MSSV 2A202603753 · Người 1 (`sim/gather`, PO)

- Tôi đã làm (kèm link commit): lõi Gather Phase 1; Phase 2 (cá bơi/sinh, Cá Sấu Năm Chèo); Phase 3 (kho cá thể, độ tươi, ươn). Commit mới nhất: [58eaae7](https://github.com/ddkhoa2605/K5-L3B-LAB-Day12-AI-SDLC-HKT/commit/58eaae7) trên `feature/gather-p2`, có 21 test mới và `docs/verification/phase-3.md`.
- Tôi đã review (kèm link): chưa có review nào được ghi lại cho tới lúc viết; sẽ bổ sung link khi review PR `sim/quan` của Người 2.
- AI sai ở đâu và tôi phát hiện thế nào: AI so id bằng chuỗi nên `F10` đứng trước `F2` (sửa bằng `id_key`); tính sai vị trí Cá Sấu sau recoil vì quên một tick chase (phát hiện khi đọc trace từng tick); đổi `hold` thành mảng dict làm hai test Phase 1 fail (giữ `sim.hold` làm property thay vì sửa test).
- Điều tôi học được: đổi schema dùng chung phải có công tắc tương thích để `main` luôn chạy được; làm số liệu ở ngưỡng cần số nguyên (240 đơn vị/điểm) thay vì float; mọi chỗ mơ hồ nên ghi `docs/clarify.md` ngay.
