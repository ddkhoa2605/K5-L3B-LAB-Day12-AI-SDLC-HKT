# Kế hoạch Phase 3 (≤ 1 trang) — TICKET-03 Change Request “Mùa Nước Nổi”

Hạn tag `phase-3`: 2:30 (35 phút, 1:55–2:30). Hợp đồng: Test Contract v1.2 (`docs/contracts/contract.md`).

## Mục tiêu
- **Lõi Độ tươi & Kho cá thể:** Đổi schema kho đếm sang kho cá thể `{"items":[{"id":"I1","kind":"ca_linh","fresh":100}, ...]}`.
- **Hao tươi:** Giỏ giảm 0.5/s, Quán giảm 0.25/s. Kẹp đáy 0. Pause dừng hao.
- **Ngưỡng ươn:** `fresh < 30` không dùng nấu; phát event `spoiled` đúng một lần theo thứ tự id.
- **Giữ chỗ & Giá theo tươi:** Giữ theo cá thể tươi nhất; nhả & thử giữ lại khi hàng vừa ươn. Giá chốt `floor(niêm yết × avg(fresh) / 100)`.
- **Smoke bàn giao kho v1.2:** Gather xuất kho cá thể nguyên tử -> Quán nạp kho v1.2 (kho đếm cũ trả mã thoát 2).
- **Mở rộng (tùy chọn):** Dòng nước lũ (`current`), Khách đặt trước (`reservations`).

## Việc / người / phụ thuộc (AC nháp)
| AC | Nội dung | Người phụ trách | Phụ thuộc |
|---|---|---|---|
| AC-P3-01 | Cập nhật `game.contract.json` sang `contract_version: "1.2"`, thêm tuning `freshness` `{initial: 100, gather_decay_per_s: 0.5, quan_decay_per_s: 0.25, spoiled_below: 30}` | 2 (Integrator) | — |
| AC-P3-02 | Refactor `chonoi/inventory.py` sang schema kho cá thể v1.2; từ chối kho đếm cũ bằng mã 2 | 2 & 1 | AC-P3-01 |
| AC-P3-03 | Gather: hao tươi giỏ (0.5/s), phát event `spoiled` khi < 30, xuất kho cá thể khi `gather_end` | 1 | AC-P3-02 |
| AC-P3-04 | Quán: hao tươi kho (0.25/s), phát event `spoiled`, giữ chỗ theo id tươi nhất, nhả khi ươn, chốt giá món theo tươi | 2 | AC-P3-02 |
| AC-P3-05 | UI/HUD: hiển thị độ tươi hoặc nhận biết hàng ươn (số, thanh, nhãn hoặc biểu tượng) | 3 | AC-P3-03/04 |
| AC-P3-06 | QA: Xây dựng bộ test Schema kho v1.2 (`tests/test_p3_schema.py`), negative tests, kiểm tra ngưỡng ươn | 4 (QA) | AC-P3-02 |
| AC-P3-07 | Tích hợp & Smoke test bàn giao kho cá thể 2 tiến trình (`tools/smoke_integration.py`), kiểm tra tính tất định | 4 (QA) | AC-P3-03/04 |
| AC-P3-08 | Điền ma trận `docs/verification/phase-3.md`, lưu bằng chứng `docs/proof/phase-3/`, kiểm tra regression và gắn tag `phase-3` | 4 & 2 | Tất cả |

## Nhịp làm việc 35 phút
- **0–7 phút:** Phân tích tác động, ghi quyết định đổi schema kho, chốt thứ tự tích hợp.
- **7–20 phút:** Code song song lõi Độ tươi (Người 1 làm Gather, Người 2 làm Quán, Người 3 làm HUD, Người 4 viết test schema & smoke tool).
- **20–25 phút:** Standup nhanh, chạy smoke test bàn giao kho cá thể giữa Gather và Quán.
- **25–32 phút:** Chạy toàn bộ test suite, regression P1–P2, kiểm tra tính tất định byte-by-byte (`check_determinism.py`).
- **32–35 phút:** Code freeze, đẩy tag `phase-3` lên GitHub trước 2:30.

## Rủi ro & Giải pháp
1. **Thời gian rất ngắn (35 phút):** Chỉ tập trung vào lõi Độ tươi và Bàn giao kho cá thể. Nhóm 4 người KHÔNG bắt buộc làm phần mở rộng (`current`, `reservations`).
2. **Xung đột schema cũ/mới (Breaking Change):** Hỗ trợ chuyển đổi adapter hoặc bật đồng bộ v1.2 khi cả 2 đầu Gather và Quán đã sẵn sàng.
3. **Mã thoát 2 khi đọc kho cũ:** Khi contract là v1.2, các test cũ nạp kho đếm phải được cập nhật fixture sang mảng cá thể.
