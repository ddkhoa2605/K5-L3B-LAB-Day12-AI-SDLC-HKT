# Kế hoạch Phase 1 (≤ 1 trang)

> Thời gian: 0:00 – 1:00 (hạn tag `phase-1` trước 1:00).
> Mục tiêu cốt lõi: Hoàn thành lõi luật Gather và Quán, đạt chuẩn Test Contract v1.0, chạy được headless và giao tiếp qua file kho.

## 1. Mục tiêu
- **Gather (`sim/gather`)**: Di chuyển, oxy/ngạt/ngất, cơ chế hái và bắt cá, cập bến, xuất kho nguyên tử.
- **Quán (`sim/quan`)**: Nấu ăn, phục vụ khách, tính tiền/uy tín, đọc kho từ buổi sáng.
- **Tích hợp**: Hợp đồng kho khớp schema mục G; smoke test 2 tiến trình thành công; tính tất định (deterministic) 100%.

## 2. Việc / Người / Phụ thuộc

| Thành viên | Module / Trách nhiệm | Việc chính | Phụ thuộc |
|---|---|---|---|
| **Người 1** | `sim/gather` + PO | Lát 1 (bơi, oxy, ngạt, ngất LIFO); Lát 2 (hái nút, bắt cá, giỏ đầy, cập bến); giữ `docs/clarify.md` | Độc lập; cung cấp kho cho Người 2 |
| **Người 2** | `sim/quan` + Integrator | Lát 3 (khách, gọi món, kiên nhẫn); Lát 4 (bếp, nấu, trả tiền, uy tín); kiểm `scenario.py`; chốt hợp đồng và gắn tag | Nhận file kho từ Người 1 |
| **Người 3** | `client/ui` + Scrum | Khung UI, HUD tối thiểu (thời gian, oxy, máu, giỏ, kho); setup repo, `AGENTS.md`, retro | Đọc snapshot từ `Session` của Người 1 & 2 |
| **Người 4** | `qa` + QA Lead | Viết test độc lập, kiểm tra tất định (`cmp`), ma trận truy vết `docs/verification/phase-1.md` | Kiểm sau khi Người 1 & 2 hoàn thành lát |

## 3. Danh sách AC cốt lõi (12 AC chuẩn Phase 1)
- **AC-P1-01**: Bơi, tăng/giảm tốc, chặn biên và chuyển phân vùng `dive`/`surface` (data `pos`).
- **AC-P1-02**: Cơ chế Oxy (mặt nước +6 kẹp max, dưới nước −1 kẹp 0) và phát `oxygen_empty` khi chạm 0.
- **AC-P1-03**: Cơ chế Ngạt (choke đầu tiên ở t+59, mỗi 60 tick −1 Máu, reset `zero_oxy_ticks` khi lên mặt nước).
- **AC-P1-04**: Máu về 0 → Ngất `faint` (xả giỏ LIFO, `gather_end fainted`, kho rỗng, dừng bước).
- **AC-P1-05**: Giỏ hàng cơ chế LIFO và trần sức chứa `hold_capacity`.
- **AC-P1-06**: Hái nguyên liệu ở mặt nước: nút `ready` gần nhất trong bán kính (dung sai `EPS`), hòa id nhỏ, `regrow_ticks = 1200`, `node_regrown`.
- **AC-P1-07**: Giỏ đầy khi hái: phát `hold_full` (`action: "gather"`), nút giữ nguyên.
- **AC-P1-08**: Bắt cá dưới nước: đàn cá gần nhất trong tầm (dung sai `EPS`), yield đủ (`ca_linh` 3, `ca_loc` 1), hồi chiêu 30 ticks; bỏ qua khi sai pha (ở mặt nước).
- **AC-P1-09**: Giỏ thiếu chỗ khi bắt cá: phát `hold_full` (`action: "catch"`), giữ đàn cá, không cooldown, không nhận một phần.
- **AC-P1-10**: Cập bến ưu tiên xét trước hái (`docked` ghi đúng giỏ); snapshot HUD tối thiểu (thời gian, oxy, máu, giỏ).
- **AC-P1-11**: Hết giờ `time` giữ giỏ sau hành động; kho ghi nguyên tử đúng một lần khi kết thúc, chạm `--ticks` không ghi.
- **AC-P1-12**: Tính tất định (cùng seed/input cho byte giống nhau 100%) và snapshot/event đúng schema PRD-0 mục E/G.

## 4. Rủi ro & Giảm thiểu
- **Quá tải lát 1+2**: Tách làm 2 lát rõ ràng, viết test unit theo từng lát, chốt clarify sớm.
- **Lệch schema kho**: Dùng chung `inventory.py`, kiểm chứng qua smoke test hai tiến trình ngay sau khi xong lát 2.
- **Sai ca biên (t+59, mép bán kính)**: Viết test scenario bao phủ các giá trị biên thay vì chỉ test tay.

