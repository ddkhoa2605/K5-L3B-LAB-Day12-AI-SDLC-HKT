# Ma trận truy vết Phase 1

| AC | Cách kiểm chứng | Bằng chứng (link `docs/proof/phase-1/...`) | Kết quả (đạt / chưa đạt — ghi trung thực) |
|---|---|---|---|
| AC-P1-01 | Bơi qua biên `dive`/`surface` phát đúng kèm data `pos`, kẹp biên vận tốc | `test_gather_lat1.py` (DiveSurface), `test_smoke_p1.py` (Movement) / [test-results.txt](../proof/phase-1/test-results.txt) | Đạt |
| AC-P1-02 | Oxy: mặt nước +6 kẹp max, dưới nước −1 kẹp 0; `oxygen_empty` đúng 1 lần khi chạm 0 | `test_gather_lat1.py` (Oxygen) / [test-results.txt](../proof/phase-1/test-results.txt) | Đạt |
| AC-P1-03 | Ngạt: choke đầu ở t+59, mỗi 60 tick −1 Máu; nổi lên đúng bước đó thì không ngạt; reset khi ở mặt nước | `test_gather_lat1.py` (Choke) / [test-results.txt](../proof/phase-1/test-results.txt) | Đạt |
| AC-P1-04 | Máu 0 → `faint` (`lost` LIFO) → `gather_end fainted`, kho rỗng, dừng bước | `test_gather_lat1.py` (Faint) / [test-results.txt](../proof/phase-1/test-results.txt) | Đạt |
| AC-P1-05 | Giỏ hàng cơ chế LIFO, trần sức chứa `hold_capacity` | `test_gather_lat1.py` (Faint), `test_gather_lat2.py` (GatherInteract/CatchFish) / [test-results.txt](../proof/phase-1/test-results.txt) | Đạt |
| AC-P1-06 | Hái: nút `ready` gần nhất, hòa id nhỏ, đúng mép bán kính (dung sai `EPS`), `regrow_ticks = 1200`, `node_regrown` sau 1200 bước | `test_gather_lat2.py` (GatherInteract) / [test-results.txt](../proof/phase-1/test-results.txt) | Đạt |
| AC-P1-07 | `hold_full` khi hái thiếu chỗ, nút giữ nguyên không mọc lại | `test_gather_lat2.py` (GatherInteract) / [test-results.txt](../proof/phase-1/test-results.txt) | Đạt |
| AC-P1-08 | Bắt cá: đúng đàn gần nhất (dung sai `EPS`), yield đủ (`ca_linh` 3, `ca_loc` 1), cooldown 30 tick; bỏ qua khi ở mặt nước | `test_gather_lat2.py` (CatchFish) / [test-results.txt](../proof/phase-1/test-results.txt) | Đạt |
| AC-P1-09 | `catch` thiếu chỗ: `hold_full`, giữ đàn, không cooldown, không nhận một phần | `test_gather_lat2.py` (CatchFish) / [test-results.txt](../proof/phase-1/test-results.txt) | Đạt |
| AC-P1-10 | Cập bến xét trước hái; `docked` ghi đúng giỏ; HUD đủ trường tối thiểu (thời gian, oxy, máu, giỏ) | `test_gather_lat2.py` (DockAndTimeout), [gather-smoke.jsonl](../proof/phase-1/gather-smoke.jsonl), [gather-inventory.json](../proof/phase-1/gather-inventory.json) | Đạt |
| AC-P1-11 | Hết giờ `time` giữ giỏ sau hành động; kho ghi nguyên tử đúng một lần, chạm `--ticks` không ghi | `test_smoke_p1.py` (Integration/Movement), `test_gather_lat2.py` (DockAndTimeout) / [test-results.txt](../proof/phase-1/test-results.txt) | Đạt |
| AC-P1-12 | Tính tất định byte-matching 100% & snapshot/event đúng schema PRD-0 mục E/G | `test_smoke_p1.py` (Contract), SHA256 đối chiếu 2 lần chạy 600 ticks / [test-results.txt](../proof/phase-1/test-results.txt) | Đạt |

## Đánh giá ngắn
- Yêu cầu nào đạt / chưa đạt: Toàn bộ 12 AC của Phase 1 phần Gather (Lát 1 + Lát 2) đều ĐẠT 100%.
- Điều cần chỉnh cho phase sau: Bổ sung cơ chế cá bơi và sinh sản theo PRD-2.

---

# Phần QA của Người 4 (PR #7, gộp nguyên văn)

# Ma trận truy vết Phase 1

| AC | Cách kiểm chứng | Bằng chứng (link `docs/proof/phase-1/...`) | Kết quả (đạt / chưa đạt — ghi trung thực) |
|---|---|---|---|
| AC-P1-01: Smoke & Unit Tests Cơ sở | Chạy test suite toàn diện (`37/37 tests pass`) | [baseline_test.txt](docs/proof/phase-1/baseline_test.txt) | ĐẠT |
| AC-P1-02: Tính tất định Byte-by-Byte (Determinism) | Chạy tool `check_determinism.py` trên 2 lần chạy độc lập | [determinism_baseline.txt](docs/proof/phase-1/determinism_baseline.txt) | ĐẠT |
| AC-P1-03: Kiểm tra CLI & Bắt lỗi tham số (Exit Code = 2) | Chạy `tests/test_qa_determinism.py` phủ các ca tham số sai | [baseline_test.txt](docs/proof/phase-1/baseline_test.txt#L24-L26) | ĐẠT |
| AC-P1-04: Tích hợp Hợp đồng Kho (Gather xuất -> Quán nạp) | Chạy `Integration.test_inv_01_gather_writes_inventory_quan_reads_it` | [baseline_test.txt](docs/proof/phase-1/baseline_test.txt#L35-L37) | ĐẠT |
| AC-P1-05: Kiểm tra danh sách thành viên (TEAM.md) | Chạy `tools/check_team.py` qua `test_team_check.py` | [baseline_test.txt](docs/proof/phase-1/baseline_test.txt#L56-L59) | ĐẠT |

## Đánh giá ngắn
- **Yêu cầu nào đạt**: Khung kiểm thử tự động, tính tất định byte-by-byte (cả Gather và Quán), kiểm tra mã lỗi CLI và tính hợp lệ hợp đồng kho đều đạt 100%.
- **Yêu cầu chưa đạt**: Các luật chi tiết nâng cao (lặn ngạt, hái hoa, bắt cá, khách vào ăn) đang chờ Người 1 và Người 2 hoàn thiện logic trong sim.
- **Điều cần chỉnh cho phase sau**: Duy trì chạy tool `check_determinism.py` sau mỗi Pull Request merge vào `main`.
