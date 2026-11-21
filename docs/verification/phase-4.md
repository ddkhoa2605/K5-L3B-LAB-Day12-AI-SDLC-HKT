# Ma trận truy vết Phase 4 — Phát hành v1.0.0 (TICKET-04)

> Nghiệm thu toàn bộ tiêu chí Phase 4 trên commit bàn giao của nhánh `main`.
> Hợp đồng kiểm thử: Test Contract v1.3. Bằng chứng lưu tại `docs/proof/phase-4/`.

| AC | Cách kiểm chứng | Bằng chứng | Kết quả |
|---|---|---|---|
| **AC-P4-01: Khai báo Contract v1.3** | Kiểm tra `game.contract.json` có `contract_version: "1.3"`, `bench_cmd` và `soak_cmd` ở gốc manifest | [game.contract.json](../../game.contract.json) | **Đạt** |
| **AC-P4-02: Benchmark có render** | Chạy `python3 tools/bench.py --seed 42 --duration 30 --out docs/proof/phase-4/bench.json` trên Chrome headless 1280×720 | [bench.json](../proof/phase-4/bench.json) (avg_fps: 60.0, 1% low: 55.31, load_ms: 985) | **Đạt** (Đạt mốc avg ≥ 60, p1 ≥ 30, load ≤ 10s) |
| **AC-P4-03: Cảnh báo dễ nhận biết** | Kiểm tra 3 cảnh báo bằng chữ/biểu tượng (thủy quái gần kèm viền tím, sắp hết oxy, khách sắp giận kèm 😠) | [warn-gather-thuong.jpg](../proof/phase-4/warn-gather-thuong.jpg), [warn-quan-thuong.jpg](../proof/phase-4/warn-quan-thuong.jpg) | **Đạt** |
| **AC-P4-04: Chế độ tương phản cao** | Chơi thử với phím `H`, nhớ qua localStorage, viền sáng và chữ tương phản rõ nét | [warn-gather-tuong-phan-cao.jpg](../proof/phase-4/warn-gather-tuong-phan-cao.jpg), [warn-quan-tuong-phan-cao.jpg](../proof/phase-4/warn-quan-tuong-phan-cao.jpg) | **Đạt** |
| **AC-P4-05: Soak headless 10 Ngày** | Chạy `python3 tools/soak.py --seed 7 --days 10 --out soak.json`; kế hoạch D1–D5 lặp ở Ngày 6–10, days_completed = 10, crashes = 0 | [soak.json](../../soak.json), `tools/soak.py` | **Đạt** |
| **AC-P4-06: Đóng gói và phát hành** | Clone sạch chạy bằng tối đa 3 lệnh theo `README.md`, rà soát `CREDITS.md`, `LICENSE`, gắn tag `phase-4` | [README.md](../../README.md), [CREDITS.md](../../CREDITS.md) | **Đạt** |
| **AC-P4-07: Hồi quy & Tính tất định** | Chạy toàn bộ 245 unit tests và kiểm tra byte-identical qua `tools/check_determinism.py` | `Ran 245 tests ... OK`, SHA256 gather & quan 100% khớp byte | **Đạt** |

## Đánh giá tổng kết Phase 4
- **Đạt:** Đã bổ sung `soak_cmd`, nâng cấp contract lên v1.3. Cả 7 tiêu chí kiểm chứng đều vượt qua và có bằng chứng cụ thể.
- **Tiến trình:** Sẵn sàng cho giảng viên chạy runner tự động và nghiệm thu demo v1.0.0.
