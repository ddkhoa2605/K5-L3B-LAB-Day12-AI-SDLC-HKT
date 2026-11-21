# Ma trận truy vết Phase 2 

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

## `contract_version: "1.1"` nhưng manifest còn thiếu khóa (trung thực, theo review #5)
`game.contract.json` đã tự nhận v1.1 nhưng **chưa có** các khóa sau (Người 1 / lát gather):
- `gather.fish_initial` còn 6 đàn (v1.1: 8), chưa có cá kèo (`fish_yield.ca_keo`), chưa có nút N5/N6 (`keo_neo`).
- `gather.fish_speed`, `fish_turn_ticks`, `fish_max`, `fish_spawn_ticks`, `fish_spawn_clearance`, `fish_x`, `fish_depths`, `fish_spawn_x`, `fish_spawn_depths`, `fish_weights` (cá bơi/sinh).
- `gather.monsters` (`species.ca_sau`, `spawns[]`, `invuln_ticks`, `loss_ratio`).
- `chonoi/scenario.py`: `NODE_KINDS`, `FISH_KINDS` còn là kind của v1.0 nên nút `keo_neo` / đàn `ca_keo` bị mã 2 (ADR-0001 ghi giao Người 1).
- Đã có: `quan`, `menu`, `day_plan`, `shop`. Mở rộng: `burn` cài sẵn nhưng tắt.
Nếu tag `phase-2` mà các khóa gather chưa xong thì phải ghi nhận ở đây là **chưa đạt** cho AC-P2-05/06.

## Test đã sửa vì luật đổi (không phải để cho xanh)
- `tests/test_quan.py::test_khong_con_ban_bo_luot`: v1.1 có 4 bàn, nên phải ngồi kín 4 bàn mới bỏ lượt.
- `tests/test_smoke_p1.py::test_con_03_old_and_future_modes_rejected` → `…_old_and_unknown_modes_rejected`: `day` hợp lệ từ v1.1; `river`, `night` vẫn mã 2.

## Mở rộng
- `burn` (cháy món): đã cài luật và test (`tests/test_burn.py`) nhưng **tắt mặc định** (`burn_s: null`, không khai `extensions`) để giữ số lõi. Bật = đặt `"extensions": ["burn"]` và `quan.burn_s: 20` trong `game.contract.json`; nhóm 4 người không bắt buộc.

## Đánh giá ngắn
- **Đạt:** Quán v1.1, kế hoạch Ngày, vòng ngày headless, Shop/nâng cấp, pause, tất định.
- **Chưa đạt:** toàn bộ phần Gather v1.1 (cá bơi/sinh, Cá Sấu, N5/N6) và vì thế chưa thể nói "chơi trọn vòng ngày" đúng ticket; hợp đồng v1.1 chưa duyệt; HUD chưa đạt chuẩn chữ/FPS; chưa merge, chưa tag.
- **Cần chỉnh cho phase sau:** merge theo thứ tự #1 → #2 → #4 → #5 → PR day-mode; Người 1 nối `gather` v1.1 vào `DaySession` (không cần sửa `day.py` nếu giữ giao diện `GatherSim`); QA chạy `day --days 5`; chụp ảnh Shop/Summary.

---

# Phần gather của Người 1 (PR #17, gộp nguyên văn)

# Ma trận truy vết Phase 2

| AC | Cách kiểm chứng | Bằng chứng (link `docs/proof/phase-2/...`) | Kết quả (đạt / chưa đạt — ghi trung thực) |
|---|---|---|---|
| AC-P2-01 | Quán: Cấu hình chuẩn v1.1 (2 bếp B1/B2, 4 bàn T1..T4, thực đơn 6 món ca_loc, bong_sung, lau_linh, canh_chua, ca_keo, lau_mam) | `test_quan_p2.py` (Data/Kitchen) / [unittest.txt](../proof/phase-2/unittest.txt) | Đạt |
| AC-P2-02 | Quán: Lịch khách 120 + 900·k, giữ nguyên liệu khi gọi món, vào ghế nhỏ nhất, thiếu nguyên liệu thì no_dish | `test_quan_p2.py` (Schedule/Arrival) / [unittest.txt](../proof/phase-2/unittest.txt) | Đạt |
| AC-P2-03 | Quán: Bếp nhận đơn reserved cũ nhất, giao món ≤ 1.5m, boa floor(20%) khi kiên nhẫn ≥ 50%, uy tín +0.2, trừ 0.5 khi bỏ về | `test_quan_p2.py` (Kitchen/Serving) / [unittest.txt](../proof/phase-2/unittest.txt) | Đạt |
| AC-P2-04 | Quán: Đóng ca khách ăn trả ngay, dọn món và phần giữ, tính điểm earned + 100 × floor(reputation) | `test_quan_p2.py` (Closing/Payment) / [unittest.txt](../proof/phase-2/unittest.txt) | Đạt |
| AC-P2-05 | Gather: Số chuẩn v1.1, cá kèo yield 2, nút kèo nèo N5/N6, cá bơi 1.5 m/s, dải độ sâu theo loài, phản xạ mép x ∈ [4,96] và d theo loài, đổi hướng mỗi 120 tick theo seed fish_swim; sinh cá tại 360·k, clearance > 1.0 m, trọng số 40:30:30, seed fish_spawn | `test_gather_p2.py` (FishSwimming, FishSpawning, NewKindsAndYields), [gather-p2-run.jsonl](../proof/phase-2/gather-p2-run.jsonl) / [unittest.txt](../proof/phase-2/unittest.txt) | Đạt |
| AC-P2-06 | Gather: Cá Sấu Năm Chèo patrol 1.0 m/s giữa các waypoint, chase 3.0 m/s khi player d ≥ 10 & dist ≤ 10m, thoát chase khi dist > 16m hoặc player d < 10. Chạm ≤ 1.5m (d ≥ 10, invuln = 0): -1 Máu, bỏ floor(n/2) LIFO, invuln 90 tick, quái recoil 60 tick lùi xa player 2/60 m/bước. Ngất monster khi hp = 0: bỏ hết giỏ LIFO, mở quán kho rỗng | `test_gather_p2.py` (CaSauNamCheo), [gather-p2-run.jsonl](../proof/phase-2/gather-p2-run.jsonl) / [unittest.txt](../proof/phase-2/unittest.txt) | Đạt |

## Đánh giá ngắn
- **Yêu cầu nào đạt / chưa đạt:** Toàn bộ các AC của Phase 2 (AC-P2-01 đến AC-P2-06) đều ĐẠT 100%. 116/116 test pass.
- **Tính tất định:** Chạy headless `--mode gather --seed 1 --ticks 600` hoàn toàn ổn định byte-to-byte và đúng tiến trình sinh cá tại tick 360.
- **Điều cần chuẩn bị cho Phase sau (Phase 3 & 4):** Chuẩn bị tích hợp vòng lặp ngày (Day loop: DayIntro → gather → EveningIntro → quan → DayResult → Shop), kế hoạch ngày D1..D5 và hệ thống nâng cấp Shop.
