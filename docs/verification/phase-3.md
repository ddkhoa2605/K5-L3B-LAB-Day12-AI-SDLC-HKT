# Ma trận truy vết Phase 3

> Chạy trên nhánh `test/qa-phase3`.
> Bằng chứng lưu tại: `docs/proof/phase-3/`.

| AC | Cách kiểm chứng | Bằng chứng | Kết quả |
|---|---|---|---|
| AC-P3-01: Contract v1.2 (`game.contract.json` tuning `freshness`) | Kiểm tra `contract_version == "1.2"`, tuning `freshness` đầy đủ 4 trường | `game.contract.json` | Chờ Người 2 cập nhật |
| AC-P3-02: Schema kho cá thể v1.2 & Từ chối kho đếm (Mã 2) | Chạy `tests/test_p3_schema.py` với các ca kho đếm cũ, trùng id, kind lạ, fresh ngoài miền | [test_p3_schema.py](tests/test_p3_schema.py) | **Đạt đặc tả** (Đã có bộ test) |
| AC-P3-03: Gather hao tươi giỏ (0.5/s) & Ngưỡng ươn 30 | Chạy headless Gather với kịch bản cá thể fresh 30 -> bắt buộc phát event `spoiled` ở tick 1 | `docs/proof/phase-3/gather_freshness.txt` | Chờ Người 1 tích hợp |
| AC-P3-04: Quán hao tươi (0.25/s), nhả giữ chỗ & Chốt giá theo tươi | Chạy headless Quán: `base_price = floor(niêm yết × avg(fresh) / 100)` | `docs/proof/phase-3/quan_freshness.txt` | Chờ Người 2 tích hợp |
| AC-P3-05: HUD thể hiện độ tươi & hàng ươn | Kiểm tra hiển thị trên trình duyệt (`python3 -m chonoi.live`) | Ảnh chụp UI `docs/proof/phase-3/hud_fresh.png` | Chờ Người 3 tích hợp |
| AC-P3-06: Bàn giao kho cá thể 2 tiến trình (DoD PRD-03) | Chạy `tools/smoke_integration.py` (Gather xuất kho cá thể v1.2 -> Quán nạp với `--ticks 0`) | `docs/proof/phase-3/smoke_handover.txt` | Sẵn sàng kịch bản |
| AC-P3-07: Tính tất định Byte-by-Byte Phase 3 | Chạy `python tools/check_determinism.py --mode gather/quan --seed 1 --ticks 600` | `docs/proof/phase-3/determinism_p3.txt` | Đạt baseline |
| AC-P3-08: Hồi quy (Regression) toàn bộ 135+ test suite | Chạy `python -m unittest discover -s tests -v` | [baseline_test.txt](docs/proof/phase-3/baseline_test.txt) | **Đạt 135/135 tests pass** |

## Đánh giá ngắn
- **Đạt:** Bộ test đặc tả schema kho cá thể v1.2 (`tests/test_p3_schema.py`) đã sẵn sàng. Toàn bộ 135 unit tests baseline của Phase 1 & 2 chạy qua 100%.
- **Chưa đạt:** Đang chờ Người 1 và Người 2 nâng cấp mã nguồn `chonoi/sim/gather.py`, `chonoi/sim/quan.py` và `chonoi/inventory.py` sang Contract v1.2.
- **Kế hoạch phối hợp:** Chạy smoke bàn giao kho ở phút thứ 20 giữa Gather và Quán, hoàn thành nghiệm thu trước 2:30.
