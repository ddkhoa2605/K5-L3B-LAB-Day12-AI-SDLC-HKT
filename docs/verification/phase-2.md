# Ma trận truy vết Phase 2 (phần của Người 2: Quán, hợp đồng, vòng ngày; ghi trung thực)

> Chạy trên nhánh `feature/day-mode` (xếp chồng #2 → #5 → PR day-mode). **Chưa merge vào `main`, chưa gắn tag `phase-2`.** Khi merge xong, QA chạy lại trên commit bàn giao rồi cập nhật cột kết quả.
> Bằng chứng: `docs/proof/phase-2/` (`unittest-day.txt`: 104 test OK; `day-integration.txt`; `integration.txt`).

| AC | Cách kiểm chứng | Bằng chứng | Kết quả |
|---|---|---|---|
| AC-P2-01 `game.contract.json` v1.1 (`quan`, `menu`, `day_plan`, `shop`) | `tests/test_quan_p2.py::Data` (bảng D1–D5 đối chiếu độc lập), `tests/test_day.py` | `unittest-day.txt` | **Đạt trên nhánh**. Chưa có khóa `gather.*` v1.1 (Người 1) |
| AC-P2-02 Kind `ca_keo`, `keo_neo` | `tests/test_inventory_kinds.py` | PR #4, `unittest-day.txt` | **Đạt trên nhánh** (PR #4 chưa merge) |
| AC-P2-03 Quán 2 bếp/4 bàn/6 món, lịch khách, lọc theo kế hoạch | `tests/test_quan_p2.py`, `tests/test_quan.py` | `unittest-day.txt` | **Đạt** |
| AC-P2-04 Hợp đồng v1.1 | `docs/contracts/contract.md` (phụ lục v1.1) | PR #6 | **Chưa đạt**: PR chưa được 2 approvals; một số chi tiết triển khai (tick sự kiện, snapshot Shop) chưa ghi vào phụ lục |
| AC-P2-05 Gather số chuẩn, cá kèo, N5/N6, cá bơi + sinh | — | — | **Chưa đạt / chưa làm** (Người 1; PR #8 mới là gather Phase 1) |
| AC-P2-06 Cá Sấu, Máu, ngất do thủy quái | — | — | **Chưa đạt / chưa làm** (Người 1). Ngất do ngạt có ở PR #8, chưa merge |
| AC-P2-07 `--mode day`, `day_plan`, Shop, nâng cấp, `--days`, pause | `tests/test_day.py` (26 test): thứ tự pha/tick, mua oxy/hp, `buy_failed` (funds/max_level/unknown), Shop tự đóng 600 tick, pause, tất định `cmp`, mã 2 | `day-integration.txt` (`CMP_OK`, 2 Ngày, oxy cấp 1 áp dụng Ngày 2) | **Đạt một phần**: toàn vòng ngày chạy với gather khung (cập bến bằng `interact`). Chưa kiểm với luật gather thật, chưa có monsters, chưa kiểm ngất → quán kho rỗng |
| AC-P2-08 Menu, pause, HUD | Xem tay trên trình duyệt (menu, DayIntro, pause, HUD gather) | — (chưa có ảnh lưu trong repo) | **Đạt một phần**: Shop, EveningIntro, Summary và HUD quán **chưa xem bằng mắt**; chưa đo FPS ≥ 30 và chữ ≥ 18 px ở 1280×720 (nhiều chữ còn 10–14 px) |
| AC-P2-09 Smoke tích hợp, regression P1 | `docs/proof/phase-2/integration.txt` (gather `--inventory-out` → quan `--inventory`), toàn bộ test P1 vẫn chạy | `integration.txt`, `unittest-day.txt` | **Đạt** với kịch bản giả lập (kho dựng bằng `gather.hold`); **chưa** thử với luật gather thật. Test thay đổi: xem dưới |
| AC-P2-10 Tag `phase-2` | `git show phase-2` | — | **Chưa đạt** (chưa merge, thiếu phần Người 1) |

## Test đã sửa vì luật đổi (không phải để cho xanh)
- `tests/test_quan.py::test_khong_con_ban_bo_luot`: v1.1 có 4 bàn, nên phải ngồi kín 4 bàn mới bỏ lượt.
- `tests/test_smoke_p1.py::test_con_03_old_and_future_modes_rejected` → `…_old_and_unknown_modes_rejected`: `day` hợp lệ từ v1.1; `river`, `night` vẫn mã 2.

## Mở rộng
- `burn` (cháy món): đã cài luật và test (`tests/test_burn.py`) nhưng **tắt mặc định** (`burn_s: null`, không khai `extensions`) để giữ số lõi. Bật = đặt `"extensions": ["burn"]` và `quan.burn_s: 20` trong `game.contract.json`; nhóm 4 người không bắt buộc.

## Đánh giá ngắn
- **Đạt:** Quán v1.1, kế hoạch Ngày, vòng ngày headless, Shop/nâng cấp, pause, tất định.
- **Chưa đạt:** toàn bộ phần Gather v1.1 (cá bơi/sinh, Cá Sấu, N5/N6) và vì thế chưa thể nói "chơi trọn vòng ngày" đúng ticket; hợp đồng v1.1 chưa duyệt; HUD chưa đạt chuẩn chữ/FPS; chưa merge, chưa tag.
- **Cần chỉnh cho phase sau:** merge theo thứ tự #1 → #2 → #4 → #5 → PR day-mode; Người 1 nối `gather` v1.1 vào `DaySession` (không cần sửa `day.py` nếu giữ giao diện `GatherSim`); QA chạy `day --days 5`; chụp ảnh Shop/Summary.
