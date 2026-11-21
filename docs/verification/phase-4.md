# Ma trận truy vết Phase 4 — Phát hành v1.0.0 (TICKET-04; ghi trung thực)

> Bản viết lại: bản trước (commit `c8260d1` của tài khoản `VQuant68`, không có trong `TEAM.md`) ghi "Đạt" cho cả tag/Release khi chưa gắn tag nào. Số liệu dưới đây lấy từ lệnh đã chạy lại trên `main` sau PR #27.
> Hợp đồng: Test Contract v1.3. Bằng chứng: `docs/proof/phase-4/`, `docs/proof/ui-redesign/`.

| AC | Cách kiểm chứng | Bằng chứng | Kết quả |
|---|---|---|---|
| AC-P4-01 Manifest v1.3 | `game.contract.json`: `contract_version:"1.3"`, `bench_cmd`, `soak_cmd` ở gốc | `game.contract.json` dòng 2, 9, 10 | **Đạt** |
| AC-P4-02 Benchmark có render | `python3 tools/bench.py --seed 42 --duration 30 --out …` (Chrome headless 1280×720) | `docs/proof/ui-redesign/bench.json` (giao diện hiện tại): avg 59.97 fps, 1% low 52.8, load 1.05 s. Bản trước thiết kế lại: `docs/proof/phase-4/bench.json` avg 60.0 | **Đạt lệnh và file đúng schema**; mốc avg ≥ 60 chỉ để báo cáo và bản hiện tại thấp hơn 0.03 fps, 1% low ≥ 30 và load ≤ 10 s đều đạt |
| AC-P4-03 Cảnh báo | 3 cảnh báo bằng chữ/biểu tượng: thủy quái gần (viền tím), sắp hết oxy, khách sắp giận | `docs/proof/ui-redesign/canh-bao-*.jpg`, `docs/proof/phase-4/warn-*.jpg` | **Đạt** (ảnh quán có khách giả lập phía trình duyệt vì kho trống, đã ghi trong README bằng chứng) |
| AC-P4-04 Tương phản cao | Phím `H`, nhớ qua `localStorage` | `docs/proof/ui-redesign/tuong-phan-cao-lan-song.jpg`, `docs/proof/phase-4/warn-*-tuong-phan-cao.jpg` | **Đạt** |
| AC-P4-05 Soak 10 Ngày | `python3 tools/soak.py --seed 7 --days 10 --out docs/proof/phase-4/soak.json` | `docs/proof/phase-4/soak.json`: `days_completed` 10, `crashes` 0, `duration_s` 6.7, đủ khóa `days, days_completed, crashes, results, duration_s` | **Đạt**. Bot không điều khiển (không hái, nấu), nên `earned` ≈ 0: chỉ kiểm độ ổn định |
| AC-P4-06 Đóng gói, tag, Release | README chạy ≤ 3 lệnh; `CREDITS.md`; tag `phase-1…4`; Release `v1.0.0` | `README.md`, `CREDITS.md` | **Gắn trễ hạn**: tag và Release được gắn sau hạn 3:00 (xem `docs/retro.md`). Chưa có file `LICENSE` trong repo |
| AC-P4-07 Hồi quy, tất định | `PYTHONPATH=tests:. python3 -m unittest discover -s tests` · `tools/check_determinism.py` | **245 test OK (1 skipped)**; SHA256 gather `1b5af857…`, quan `4f610bcf…` giống giữa hai lần chạy | **Đạt** |

## Đánh giá ngắn
- **Đạt:** manifest v1.3, bench, soak, cảnh báo, tương phản cao, hồi quy và tất định.
- **Chưa/Không đạt hoàn toàn:** tag và Release gắn trễ hạn; không có `LICENSE`; avg FPS 59.97 (< 60, mốc báo cáo); soak không mô phỏng người chơi.
- **Điểm cần nhóm xem:** tài khoản `VQuant68` không có trong `TEAM.md` đã đẩy thẳng 3 commit lên `main` (xem `docs/clarify.md`).
