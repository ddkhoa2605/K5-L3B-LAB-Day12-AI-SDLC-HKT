# ADR-0005: Benchmark có render qua `chonoi.live` + Chrome headless (`bench_cmd`)

- Trạng thái: đề xuất (cần Người 2 / Integrator duyệt)
- Ngày, người quyết: 2026-11-21, Người 3 (`client/ui`)

## Bối cảnh
TICKET-04 (v1.3) yêu cầu `<bench_cmd> --seed 42 --duration 30 --out bench.json`:
- Đo cảnh buổi sáng **có render** ở 1280×720, làm nóng 3 s rồi đo 30 s.
- Xuất `avg_fps`, `p1_low_fps`, `frames`, `measured_s`, `load_ms`.

Client của nhóm là canvas 2D trong trình duyệt (`chonoi/web/index.html`, phục vụ bởi `chonoi.live`), nên phải đo trong trình duyệt thật. Đo FPS của luồng Python thì không phản ánh render.

## Các lựa chọn đã cân nhắc
1. Mở client trong Chrome headless ở chế độ `?bench=`; trang ghi thời gian từng khung bằng `requestAnimationFrame` rồi `POST /bench`; `tools/bench.py` tính năm trường (chọn).
2. Viết renderer Python riêng (pygame…): thêm thư viện ngoài, và đo một client khác với client người chơi dùng.
3. Selenium/Playwright: thêm thư viện ngoài, trong khi starter chỉ dùng thư viện chuẩn.

## Quyết định
| File | Thay đổi |
|---|---|
| `tools/bench.py` (mới) | Dựng `LiveGame("gather", scenario mặc định, seed)` + `LiveServer(port=0)`. Mở Chrome headless `--window-size=1280,720`. Chờ báo cáo, tính năm trường bằng `compute_bench()` (hàm thuần), ghi file nguyên tử. Không có Chrome thì mã 2; đo thất bại thì mã 1 |
| `chonoi/live.py` | `POST /bench` lưu báo cáo vào `LiveGame.bench_reports` (giới hạn body riêng 1 MiB; `/input` giữ 4096) |
| `chonoi/web/index.html` | Chế độ `?bench=<s>&warmup=<s>`: khung vẽ cố định 1280×720, không gửi input (Út Sen đứng yên ở bến), gửi `first_frame` (cho `load_ms`) và `done` (thời gian từng khung sau làm nóng) |
| `game.contract.json` | Khóa gốc `bench_cmd: "python3 tools/bench.py"` |

Công thức:
- `avg_fps = frames / measured_s`.
- `p1_low_fps` = nghịch đảo thời gian trung bình (giây) của `max(1, ceil(0.01 × frames))` khung chậm nhất.
- `load_ms` = mốc khởi chạy `tools/bench.py` đến khung hình đầu tiên của cảnh đo.

## Hệ quả
- **Cần Chrome hoặc Chromium** trên máy chạy bench (macOS: đường dẫn mặc định; Linux: `google-chrome`/`chromium` trên PATH; hoặc biến `CHROME`). README ghi yêu cầu này.
- Mô phỏng và JSONL headless không đổi; `/bench` chỉ nhận báo cáo đo.
- Cảnh đo dùng gameplay đang có trên `main`. Độ tươi, cá bơi và Cá Sấu xuất hiện khi #17/#20 merge, không cần sửa bench.
- Test: `tests/test_bench.py` (công thức, đầu vào sai, thiếu Chrome) và `tests/test_live.py::LiveBenchRouteTest`.
- `contract_version: "1.3"` và `soak_cmd` thuộc lát headless/Release (Người 2), không nằm trong ADR này.
