# PLAN 4 – Người 4 phụ trách `qa` (QA Lead)
> **Phiên bản:** Cập nhật đồng bộ theo PRD-0 & Kế hoạch tổng thể (21/11/2026)  
> **Vị trí file:** `plan4.md` và `docs/plan/plan4.md`  
> **Vai trò:** QA Lead – Chốt kết luận chất lượng, gác cổng kỹ thuật và khuyến nghị tag/Release.

---

## 1. VAI TRÒ & QUY TRÌNH

* **Module chính:** `qa` (Kiểm thử, Công cụ QA, Đo lường chất lượng).
* **Vai quy trình:** **QA Lead** – Chịu trách nhiệm tối cao về chất lượng sản phẩm, tính tất định (*determinism*), và cấp phép cho Integrator (Người 2) gắn tag / release.
* **Quan hệ dự phòng:** Dự phòng cho **Người 1** (`sim/gather`). Được dự phòng bởi **Người 3** (`client/ui`).
* **Quan hệ review:** Reviewer chính của **Người 3** (`client/ui`). Được review bởi **Người 3**.
* **Trọng số điểm quyết định:**
  * Test tự động ẩn (*headless*): **25 điểm** (Trọng yếu nhất).
  * Kiểm chứng và bằng chứng: **15 điểm** (`docs/verification/`, `docs/proof/`).
  * Harness AI: **10 điểm** (Sở hữu skill `determinism-check` trong `.agents/skills/`).

---

## 2. PHẠM VI & ĐIỀU CHỈNH THEO PRD-0 MỚI

Theo bản cập nhật PRD-0 từ Lab Board:
1. **Không mời giảng viên:** Chỉ cần repo public là đủ.
2. **Quy tắc làm việc nhóm:** Ruleset, PR, CI là tự chọn nhưng nhóm thống nhất **áp dụng đầy đủ** để lấy trọn 25 điểm Teamwork.
3. **Definition of Done (DoD) bổ sung:**
   * README phải ghi cách chạy từ bản clone sạch $\le 3$ lệnh (hỗ trợ cả Windows & Linux/macOS).
   * Lệnh test chạy bằng đúng 1 lệnh duy nhất.
   * `game.contract.json` khớp hoàn toàn với bản chạy thực tế.
   * **Smoke test 2 tiến trình:** Chạy Gather xuất file kho $\rightarrow$ Quán đọc kho đó (ví dụ: `stock: {"bong_sung": 2, "ca_loc": 1}` ở tick 0) thành công trên nhánh `main`.
   * HUD đọc được trạng thái khi chơi; phần sáng tạo (nếu có) phải tắt ở headless.

---

## 3. TIẾN ĐỘ THỰC TẾ & KẾ HOẠCH HÀNH ĐỘNG (4 PHASE)

### Hiện trạng đã hoàn thành (Phase 1 Baseline):
- [x] Đã thiết lập công cụ `tools/check_determinism.py` kiểm tra byte-by-byte SHA256 tự động đa nền tảng.
- [x] Đã cấu hình Skill AI `.agents/skills/determinism-check/SKILL.md` (đạt tiêu chí Harness AI).
- [x] Đã viết bộ test chuyên dụng `tests/test_qa_determinism.py` (5 tests), nâng tổng số test lên **37/37 tests PASS**.
- [x] Đã lưu bằng chứng cơ sở: `docs/proof/phase-1/baseline_test.txt` và `determinism_baseline.txt`.
- [x] Đã điền sẵn ma trận nghiệm thu tại `docs/verification/phase-1.md` và nhật ký `docs/ai-usage-log.md`.

---

### A. Phase 1 (0:00 – 1:00) — Nghiệm thu Lõi Gather & Quán
- [x] **Setup & Baseline (T-0:00 - T-0:15):** Đã hoàn thành (37 tests xanh, determinism pass 100%).
- [ ] **Test đón đầu & Hỗ trợ (T-0:15 - T-0:45):**
  * Theo dõi PR của Người 1: Xác minh lặn/nổi (`dive`/`surface`), oxy, ngạt (`choke`), trừ máu (`hp`), ngất (`faint`), hái hoa, bắt cá, giỏ LIFO.
  * Theo dõi PR của Người 2: Xác minh khách vào bàn, đặt chỗ nguyên liệu (`reserved`), hết món (`no_dish`), kiên nhẫn (`patience`), bếp chín, bưng bê, trả tiền + boa.
- [ ] **Review PR Người 3 (`client/ui`) (T-0:45 - T-0:50):**
  * Kiểm tra diff từng dòng: Đảm bảo UI chỉ đọc snapshot, không sửa state của Sim, phím WASD, E, Space, R chuẩn.
- [ ] **Nghiệm thu T-10 phút (T-0:50 - T-1:00):**
  * Chạy smoke test 2 tiến trình Gather $\rightarrow$ Quán:
    ```bash
    python3 -m chonoi.headless --mode gather --seed 42 --ticks 600 --out gather.jsonl --inventory-out kho.json
    python3 -m chonoi.headless --mode quan --seed 42 --ticks 600 --inventory kho.json --out quan.jsonl
    ```
  * Chạy `python tools/check_determinism.py` cho cả 2 mode.
  * Cập nhật `docs/verification/phase-1.md`, lưu log vào `docs/proof/phase-1/`.
  * Báo Người 2 (Integrator) gắn tag `phase-1`.

---

### B. Phase 2 (1:00 – 1:55) — Mở rộng theo PRD-2 & Chế độ Day
- [ ] Nhận PRD-2 từ Lab Board qua PO. Kiểm tra yêu cầu chế độ ngày (`--mode day`).
- [ ] Viết bổ sung các test cases mới cho Phase 2 trong `tests/test_qa_phase2.py`.
- [ ] Chạy kiểm thử hồi quy (*Regression testing*): Đảm bảo các tính năng cũ của Phase 1 không bị vỡ.
- [ ] T-10 phút (1:45): Chạy toàn bộ test, kiểm tra determinism, điền `docs/verification/phase-2.md`, cấp phép gắn tag `phase-2`.

---

### C. Phase 3 (1:55 – 2:30) — Change Request “Mùa Nước Nổi” (Test Contract v1.2, 35 phút)
- [x] **Xây dựng Test Fixture & Specification Schema v1.2 (`tests/test_p3_schema.py`):**
  * Đặc tả và kiểm tra Schema kho cá thể `{"items": [{"id": "I1", "kind": "ca_linh", "fresh": 100}]}`.
  * Negative test: Từ chối kho đếm cũ bằng mã thoát 2, bắt trùng id, kind lạ, fresh ngoài miền `[0, 100]`.
  * Viết sẵn test case cho kịch bản mẫu PRD-03: cá thể `fresh: 30` ở tick 0 bị ươn ở tick 1 phát event `spoiled`.
- [x] **Lập Kế hoạch & Ma trận kiểm chứng:** Soạn `docs/plan/phase-3.md` và `docs/verification/phase-3.md`.
- [x] **Lưu bằng chứng baseline regression:** Chạy 143 tests xanh và lưu `docs/proof/phase-3/baseline_test.txt`.
- [ ] **Giám sát & Hỗ trợ tích hợp (T-7 - T-20 phút):**
  * Theo dõi Người 1 (Gather): Hao tươi giỏ 0.5/s, kẹp đáy 0, phát `spoiled` khi < 30, xuất kho cá thể nguyên tử khi `gather_end`.
  * Theo dõi Người 2 (Quán): Hao tươi kho 0.25/s, phát `spoiled`, giữ chỗ theo id tươi nhất, nhả khi ươn, chốt giá món `floor(niêm yết × avg(fresh) / 100)`.
- [ ] **Smoke test bàn giao kho v1.2 (T-20 - T-25 phút):**
  * Chạy kịch bản tích hợp 2 tiến trình: Gather cập bến xuất kho cá thể -> Quán nạp với `--ticks 0`, kiểm tra khớp từng byte/trường.
- [ ] **Nghiệm thu T-10 phút (T-25 - T-35 phút):**
  * Chạy lại toàn bộ test suite và `tools/check_determinism.py`.
  * Điền kết quả thực tế vào `docs/verification/phase-3.md`.
  * Báo Integrator (Người 2) gắn tag `phase-3` trước 2:30.

---

### D. Phase 4 (2:30 – 3:00) — Release v1.0.0 & Tổng kết
- [ ] Đóng băng code logic hoàn toàn.
- [ ] Kiểm tra tính năng sáng tạo (*Creative content* của Người 3): Chứng minh tính năng sáng tạo tắt hoàn toàn ở headless, output byte-by-byte vẫn chuẩn contract.
- [ ] Kiểm tra Definition of Done (DoD):
  * [ ] Clone sạch chạy được $\le 3$ lệnh.
  * [ ] Test chạy 1 lệnh duy nhất.
  * [ ] `game.contract.json` khớp bản chạy.
  * [ ] Bằng chứng `docs/proof/phase-4/` đầy đủ.
- [ ] Viết bài phản tư cá nhân tại `docs/members/<handle>.md` ($\le 200$ từ).
- [ ] Cập nhật `docs/ai-usage-log.md`.
- [ ] Báo Người 2 gắn tag `phase-4` và tạo Release `v1.0.0`.

---

## 4. BỘ LỆNH CHUẨN ĐỒNG BỘ ĐA NỀN TẢNG

### A. Lệnh Test 1 dòng (Windows PowerShell & Linux)
```powershell
# Windows PowerShell:
$env:PYTHONPATH="tests;."; python -m unittest discover -s tests -v

# Linux / macOS:
PYTHONPATH=tests:. python3 -m unittest discover -s tests -v
```

### B. Lệnh Kiểm tra Tất định (Đa nền tảng)
```bash
python tools/check_determinism.py --mode gather --seed 1 --ticks 600
python tools/check_determinism.py --mode quan --seed 1 --ticks 600
```

### C. Smoke test hai tiến trình Gather -> Quán (Bắt buộc theo DoD PRD-0)
```powershell
python tools/smoke_integration.py
```

### D. Kiểm tra danh sách thành viên (CI Gate)
```bash
python tools/check_team.py
```

---

## 5. MẪU BÁO CÁO NGHIỆM THU T-10 PHÚT TRƯỚC GẮN TAG

Mỗi khi đến mốc T-10 phút của từng phase, Người 4 chạy lệnh và cập nhật vào `docs/verification/phase-<n>.md`:

```markdown
# Ma trận truy vết Phase <n>

| AC | Cách kiểm chứng | Bằng chứng (link docs/proof/phase-<n>/...) | Kết quả |
|---|---|---|---|
| AC-P<n>-01: Chức năng lõi Gather/Quán | Chạy test suite toàn diện | [baseline_test.txt](docs/proof/phase-<n>/baseline_test.txt) | ĐẠT |
| AC-P<n>-02: Tính tất định Byte-by-Byte | Chạy check_determinism.py 2 lần | [determinism_baseline.txt](docs/proof/phase-<n>/determinism_baseline.txt) | ĐẠT |
| AC-P<n>-03: Smoke test 2 tiến trình kho | Headless gather xuất -> quan nạp | [integration_kho.txt](docs/proof/phase-<n>/integration_kho.txt) | ĐẠT |
| AC-P<n>-04: Bắt lỗi tham số (Exit code 2) | Chạy tests/test_qa_determinism.py | [baseline_test.txt](docs/proof/phase-<n>/baseline_test.txt) | ĐẠT |
| AC-P<n>-05: Sáng tạo tắt ở Headless | Chạy đối chiếu headless | [creative_headless_check.txt](docs/proof/phase-<n>/creative_headless_check.txt) | ĐẠT |

## Đánh giá ngắn
- Yêu cầu đạt: Đầy đủ các AC theo PRD và Test Contract.
- Khuyến nghị: CHẤP THUẬN GẮN TAG phase-<n>.
```
