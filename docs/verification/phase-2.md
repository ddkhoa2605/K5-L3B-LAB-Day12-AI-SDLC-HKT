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
