# Bằng chứng Phase 4 — phần Người 3 (UI, benchmark)

Ngày 21/11/2026, nhánh `feature/ui-release-p4`. macOS, Chrome. Khung vẽ 1280×720.

## Ba cảnh báo dễ nhận biết + tương phản cao (phím H)
| Cảnh báo | Cách dựng | Thường | Tương phản cao |
|---|---|---|---|
| Thủy quái gần ("⚠ Thủy quái gần!" + viền) | Gather; Cá Sấu giả `state:"chase"` chèn vào `/state` ở trình duyệt, vì `main` chưa có `monsters[]` | [ảnh](warn-gather-thuong.jpg) | [ảnh](warn-gather-tuong-phan-cao.jpg) |
| Oxy sắp hết ("⚠ Sắp hết oxy!") | Scenario `gather.player {pos:[20,8], oxygen_ticks:360}` → dưới 25% | cùng ảnh trên | cùng ảnh trên |
| Khách sắp giận ("⚠ Khách T2 sắp giận!" + 😠) | Scenario quán: khách T2 `patience_ticks_left: 700` (< 25% của 3600) | [ảnh](warn-quan-thuong.jpg) | [ảnh](warn-quan-tuong-phan-cao.jpg) |

Không lỗi console. Chế độ tương phản cao nhớ qua `localStorage` (phím H).

## Benchmark có render (ADR-0005)
`python3 tools/bench.py --seed 42 --duration 30 --out docs/proof/phase-4/bench.json`

| Bản | avg_fps | p1_low_fps | frames | measured_s | load_ms |
|---|---|---|---|---|---|
| Nhánh này (gameplay `main`, v1.1) — [`bench.json`](bench.json) | 60.0 | 55.31 | 1801 | 30.015 | 985 |
| Bản ghép tạm với #20 (độ tươi v1.2), không đẩy | 60.0 | 55.72 | 1801 | 30.015 | 990 |

**Phải đo lại trên `main` ở commit bàn giao.** TICKET-04 yêu cầu artifact lấy từ commit nộp. Sau khi #17, #20 và PR này merge, chạy lại lệnh trên rồi commit `bench.json` mới; khi đó cảnh đo có độ tươi, cá bơi và Cá Sấu.

Mốc báo cáo của ticket (avg ≥ 60, 1% low ≥ 30, load ≤ 10 s): đạt. FPS bị trần 60 bởi tần số khung của Chrome headless. Cảnh đo chưa có Cá Sấu vì #17 chưa merge.

## Không đổi headless
`cmp` JSONL `gather`/`quan` (seed 1, 600 tick) và `day` (3000 tick), trước và sau các thay đổi: giống từng byte. Test toàn bộ: OK.
