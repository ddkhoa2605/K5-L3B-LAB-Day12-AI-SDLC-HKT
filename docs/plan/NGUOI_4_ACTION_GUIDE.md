# CẨM NANG HÀNH ĐỘNG CHO NGƯỜI 4 (QA LEAD)
> **Dự án:** Quán Ăn Chợ Nổi (Day 12 AI SDLC)  
> **Phiên bản:** Cập nhật đồng bộ theo `plan.md`, `plan4.md` và PRD-0 mới (21/11/2026)  
> **Hệ điều hành hỗ trợ:** Windows (PowerShell) & Linux / macOS

---

## 1. TỔNG QUAN VAI TRÒ & TIÊU CHUẨN ĐÁNH GIÁ (PRD-0 MỚI)

Người 4 nắm giữ vai trò **QA Lead (Trưởng nhóm Đảm bảo Chất lượng)** — người gác cổng kỹ thuật tối cao cho toàn bộ dự án.

### Ma trận trách nhiệm (RACI)
* **Chịu trách nhiệm chính (Accountable/Responsible):**
  * Toàn bộ thư mục `tests/` và hoạt động kiểm thử tự động.
  * Tính tất định (*Determinism*): Cùng `seed` và `input` thì output byte-by-byte giống hệt nhau.
  * Hợp đồng file kho (*Inventory Contract*): Đảm bảo `gather` xuất kho đúng schema và `quan` đọc kho chính xác.
  * Kiểm chứng & Bằng chứng: Điền `docs/verification/phase-n.md` và lưu dữ liệu thật vào `docs/proof/phase-n/`.
  * Skill AI của nhóm: Xây dựng và duy trì skill `determinism-check` trong `.agents/skills/determinism-check/`.
  * **Cấp phép gắn Tag:** Người 2 (Integrator) chỉ được bấm gắn tag khi Người 4 xác nhận toàn bộ test đã pass và determinism đạt 100%.
* **Reviewer chính của:** Người 3 (`client/ui`). Nhận xét code theo dòng cụ thể trên GitHub PR.
* **Dự phòng cho:** Người 1 (`sim/gather`). Sẵn sàng nhận việc nếu Người 1 vướng quá 10 phút.

### Tiêu chuẩn nghiệm thu bổ sung (DoD PRD-0):
1. **Test tự động ẩn (*Headless Test* - 25 điểm):** Phải đảm bảo output JSONL đúng contract, exit code = 2 khi tham số sai, không ghi file rác khi lỗi.
2. **Lệnh test 1 dòng duy nhất:** Bắt buộc toàn bộ test suite phải kích hoạt được bằng đúng 1 câu lệnh.
3. **Smoke test 2 tiến trình trên `main`:** Chạy Gather xuất file kho $\rightarrow$ Quán nạp file kho đó thành công.
4. **README $\le 3$ lệnh:** Rà soát hướng dẫn chạy từ clone sạch không vượt quá 3 lệnh.
5. **Chế độ sáng tạo:** Tính năng đồ họa/âm thanh bổ sung (nếu có) phải tắt hoàn toàn ở headless mode.

---

## 2. NHỮNG VIỆC NGƯỜI 4 LÀM ĐỘC LẬP KHI CHƯA CÓ DATA CỦA NGƯỜI KHÁC

Bạn **không cần chờ** Người 1, 2, hay 3 code xong thì mới bắt đầu. Dưới đây là các đầu việc bạn thực hiện ngay lập tức bằng dữ liệu giả lập (*mock fixture*) và công cụ độc lập:

### Việc 1: Thiết lập & Kiểm tra Công cụ Tính tất định (ĐÃ HOÀN THÀNH)
* **Mục tiêu:** Tạo công cụ kiểm tra byte-by-byte SHA256 tự động đa nền tảng.
* **File liên quan:** `tools/check_determinism.py` và `.agents/skills/determinism-check/SKILL.md`.
* **Lệnh chạy:**
  ```powershell
  python tools/check_determinism.py --mode gather --seed 1 --ticks 600
  python tools/check_determinism.py --mode quan --seed 1 --ticks 600
  ```

### Việc 2: Viết Bộ Test Kiểm tra Tham số CLI & Exit Code 2 (ĐÃ HOÀN THÀNH)
* **Mục tiêu:** Viết các test case phủ các trường hợp lỗi đầu vào: ticks âm, snapshot-every = 0, mode lạ, trùng đường dẫn in/out.
* **File liên quan:** `tests/test_qa_determinism.py` (5/5 tests pass).
* **Kết quả:** Đã nâng tổng số test suite từ 32 lên **37 tests PASS 100%**.

### Việc 3: Lưu trữ Bằng chứng Baseline và Hồ sơ Nghiệm thu (ĐÃ HOÀN THÀNH)
* **Mục tiêu:** Lưu kết quả chạy 37 tests và mã băm SHA256 ban đầu làm bằng chứng gốc đối chiếu.
* **File liên quan:** 
  * `docs/proof/phase-1/baseline_test.txt`
  * `docs/proof/phase-1/determinism_baseline.txt`
  * `docs/verification/phase-1.md`
  * `docs/ai-usage-log.md`

### Việc 4: Soạn sẵn Kịch bản Smoke Test 2 Tiến trình qua File Kho
* **Mục tiêu:** Tạo script kiểm thử tự động luồng Gather xuất kho $\rightarrow$ Quán nạp kho mà không phụ thuộc vào code của Người 1/2 (dùng scenario mẫu).
* **Cách thực hiện:** Tạo lệnh hoặc script kiểm thử tự động, kiểm tra xem `kho.json` sinh ra có chứa đúng schema `{"items": {...}}` hay không.

### Việc 5: Viết Test đón đầu (Test-Driven Development) cho Gather & Quán
* **Mục tiêu:** Soạn trước các file test đón đầu `tests/test_gather_qa.py` và `tests/test_quan_qa.py` với dữ liệu scenario giả lập:
  * Fixture Gather: Scenario có `oxygen_ticks: 1`, sau 1 tick kiểm tra sự kiện `oxygen_empty`.
  * Fixture Quán: Scenario có `stock: {"ca_loc": 1}` và khách gọi `ca_loc_nuong_trui`, kiểm tra đặt chỗ nguyên liệu `reserved`.

---

## 3. CHECKLIST THEO TIMELINE 3 GIỜ (ĐỒNG BỘ 4 PHASE)

```
0:00 ──────────────── 1:00 ────────────── 1:55 ────────────── 2:30 ───────────── 3:00
│     PHASE 1 (60')    │   PHASE 2 (55')   │   PHASE 3 (35')   │   PHASE 4 (30')   │
│  Lõi Gather & Quán,  │  Mở rộng theo     │  Ổn định & Chống  │  DoD, Retro,      │
│  Smoke 2 tiến trình  │  PRD-2 (Day mode) │  lỗi biên         │  Demo & Release   │
└──────────────────────┴───────────────────┴───────────────────┴───────────────────┘
```

### Phase 1 (0:00 – 1:00) — MỤC TIÊU: Tag `phase-1` chạy được lõi
- [x] **0:00 - 0:15 (Setup & Baseline):** Đã chạy 37 tests, tạo tool `check_determinism.py`, skill AI, lưu proof baseline.
- [ ] **0:15 - 0:45 (Theo dõi & Test đón đầu):**
  * Theo dõi PR Người 1 (`gather.py`): Test lặn/nổi (`dive`/`surface`), tụt/hồi oxy, ngạt nước (`choke`), trừ máu (`hp`), ngất (`faint`), hái hoa, bắt cá, giỏ LIFO.
  * Theo dõi PR Người 2 (`quan.py`): Test khách vào, chọn món, đặt chỗ nguyên liệu, kiên nhẫn, bếp nấu, bưng bê, trả tiền + boa.
- [ ] **0:45 - 0:50 (Review PR Người 3):**
  * Review từng dòng diff của UI: Đảm bảo UI chỉ đọc snapshot, phím WASD, E, Space, R map đúng, không can thiệp biến sim.
- [ ] **0:50 - 1:00 (Nghiệm thu T-10 phút):**
  * Chạy smoke test 2 tiến trình Gather $\rightarrow$ Quán trên nhánh `main`.
  * Chạy `python tools/check_determinism.py` kiểm tra byte-by-byte.
  * Kiểm tra danh sách nhóm: `python tools/check_team.py`.
  * Điền [docs/verification/phase-1.md](file:///d:/learncode/du_an/AIthucchien/thuchanhb12/K5-L3B-LAB-Day12-AI-SDLC-HKT/docs/verification/phase-1.md).
  * Phát lệnh cho Người 2 gắn tag `phase-1`.

---

### Phase 2 (1:00 – 1:55) — MỤC TIÊU: Tag `phase-2`
- [ ] Nhận PRD-2 từ Lab Board qua PO. Kiểm tra yêu cầu chế độ ngày (`--mode day`).
- [ ] Viết test bổ sung cho Phase 2; chạy kiểm thử hồi quy (*regression testing*) đảm bảo tính năng cũ không lỗi.
- [ ] T-10 phút (1:45): Chạy toàn bộ test suite, kiểm tra determinism, cập nhật `docs/verification/phase-2.md`, cấp phép gắn tag `phase-2`.

---

### Phase 3 (1:55 – 2:30) — MỤC TIÊU: Tag `phase-3` (35 phút)
- [ ] Tập trung kiểm thử các ca biên (*Edge cases*):
  * Giỏ hàng đầy 12 món $\rightarrow$ hái tiếp hoặc bắt cá tiếp phải bắn `hold_full`.
  * Oxy chạm đáy đúng tick hết giờ.
  * Kho chỉ còn 1 cá nhưng 2 khách cùng muốn gọi món cá.
- [ ] T-10 phút (2:20): Chạy full test suite, cập nhật `docs/verification/phase-3.md`, báo Người 2 gắn tag `phase-3`.

---

### Phase 4 (2:30 – 3:00) — MỤC TIÊU: Tag `phase-4` & Release `v1.0.0`
- [ ] Đóng băng code logic hoàn toàn.
- [ ] Rà soát toàn bộ Definition of Done (DoD):
  * [ ] README chạy từ clone sạch $\le 3$ lệnh.
  * [ ] Test chạy 1 lệnh duy nhất.
  * [ ] Tính năng sáng tạo tắt hoàn toàn ở headless mode.
  * [ ] Smoke test 2 tiến trình pass trên `main`.
- [ ] Viết bài phản tư cá nhân tại `docs/members/<handle>.md` ($\le 200$ từ).
- [ ] Cập nhật `docs/ai-usage-log.md`.
- [ ] Báo Người 2 gắn tag `phase-4` và tạo Release `v1.0.0`.

---

## 4. BỘ LỆNH VẬN HÀNH CHUẨN 1 DÒNG (ĐA NỀN TẢNG)

### A. Lệnh chạy toàn bộ Test Suite (1 lệnh duy nhất)
```powershell
# Trên Windows PowerShell:
$env:PYTHONPATH="tests;."; python -m unittest discover -s tests -v

# Trên Linux / macOS:
PYTHONPATH=tests:. python3 -m unittest discover -s tests -v
```

### B. Lệnh Kiểm tra Tính tất định tự động (Byte-by-Byte)
```powershell
python tools/check_determinism.py --mode gather --seed 1 --ticks 600 ; python tools/check_determinism.py --mode quan --seed 1 --ticks 600
```

### C. Lệnh Smoke Test 2 Tiến trình qua File Kho (Bắt buộc theo DoD PRD-0)
Chạy tool tự động hóa tích hợp độc lập:
```powershell
python tools/smoke_integration.py
```
Hoặc chạy lệnh CLI thủ công (cần truyền input cập bến ở tick 0):
```powershell
# Tạo input cập bến sạch UTF-8:
python -c "import json; open('in_dock.json','w',encoding='utf-8').write(json.dumps({'frames': [{'tick': 0, 'interact': True}]}))"

# Tiến trình 1: Gather kết thúc xuất kho
python -m chonoi.headless --mode gather --seed 42 --ticks 1 --inputs in_dock.json --out gather.jsonl --inventory-out kho.json

# Tiến trình 2: Quán nạp kho vừa xuất
python -m chonoi.headless --mode quan --seed 42 --ticks 1 --inventory kho.json --out quan.jsonl
Write-Host "Mã thoát Smoke Test:" $LASTEXITCODE
```

### D. Lệnh Kiểm tra Danh sách Nhóm & CI Gate
```powershell
python tools/check_team.py
```

---

## 5. MẪU BÁO CÁO NGHIỆM THU ĐẦY ĐỦ TRƯỚC MỖI MỐC TAG

Người 4 cập nhật vào `docs/verification/phase-<n>.md`:

```markdown
# Ma trận truy vết Phase <n>

| AC | Cách kiểm chứng | Bằng chứng (link docs/proof/phase-<n>/...) | Kết quả |
|---|---|---|---|
| AC-P<n>-01: Chức năng lõi Gather/Quán | Chạy toàn bộ test suite (37 tests) | [baseline_test.txt](docs/proof/phase-<n>/baseline_test.txt) | ĐẠT |
| AC-P<n>-02: Tính tất định Byte-by-Byte | Chạy tool check_determinism.py | [determinism_baseline.txt](docs/proof/phase-<n>/determinism_baseline.txt) | ĐẠT |
| AC-P<n>-03: Smoke test 2 tiến trình kho | Headless gather xuất -> quan nạp | [integration_kho.txt](docs/proof/phase-<n>/integration_kho.txt) | ĐẠT |
| AC-P<n>-04: Bắt lỗi tham số (Exit code 2) | Chạy tests/test_qa_determinism.py | [baseline_test.txt](docs/proof/phase-<n>/baseline_test.txt#L24-L26) | ĐẠT |
| AC-P<n>-05: Sáng tạo tắt ở Headless | Chạy đối chiếu headless | [creative_headless_check.txt](docs/proof/phase-<n>/creative_headless_check.txt) | ĐẠT |

## Đánh giá ngắn
- Yêu cầu đạt: Đầy đủ các AC theo PRD-0 và Definition of Done.
- Tồn đọng (nếu có - ghi trung thực): ...
- Khuyến nghị: CHẤP THUẬN GẮN TAG phase-<n>.
```
