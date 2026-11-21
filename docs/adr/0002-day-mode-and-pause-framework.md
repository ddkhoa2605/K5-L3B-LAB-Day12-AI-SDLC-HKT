# ADR-0002: Chế độ `day`, pause, input v1.1 và `extensions` — sửa module khung

- Trạng thái: đề xuất (cần PO/nhóm xác nhận)
- Ngày, người quyết: 2026-11-21, Người 2 (Integrator)

## Bối cảnh
TICKET-02 (Test Contract v1.1) yêu cầu `--mode day --days N`, nút `pause` ở cả ba mode, `shop_done`, lệnh `buy`, và khai mã mở rộng ở `extensions`. Các module khung hiện hỗ trợ đúng v1.0: `headless.py` từ chối `day`, `inputs.py` chỉ nhận `interact/catch`, `runner.Session` không có pause, `contract.py` ép `burn_s` là `null`.

## Các lựa chọn đã cân nhắc
1. Viết `day` thành module mới, sửa tối thiểu các điểm nối của khung (chọn).
2. Fork cả khung thành `chonoi2/` (trùng lặp, dễ lệch, mất `live`/test sẵn).
3. Để người làm UI tự xử lý `day` trong `live.py` (luật lọt vào lớp hiển thị, headless không kiểm được).

## Quyết định
Phương án 1. Luật mới nằm ở file mới; chỉ sửa khung ở các điểm nối:

| File | Thay đổi |
|---|---|
| `chonoi/day.py` (mới) | `DaySession` ghép `GatherSim`+`QuanSim`+Shop, chuyển pha, nâng cấp, `load_day_scenario`, `run_day` (gom dòng rồi mới ghi: lỗi mâu thuẫn lúc dựng pha → mã 2, không để file dở) |
| `chonoi/pause.py` (mới) | `PauseGate` dùng chung gather/quan/day |
| `chonoi/inputs.py` | `BUTTONS_V11` (`pause`, `shop_done`), `buy` (chuỗi khác rỗng) trong `InputState`; `attack`/`photo` vẫn bị từ chối |
| `chonoi/runner.py` | `Session` tách `tick` (ngoài) và `sim_tick` (gameplay), phát `paused`/`resumed`, `state:"paused"` |
| `chonoi/headless.py` | nhận `--mode day`, `--days`; `day` cấm `--inventory/--inventory-out`; `--days` chỉ với `day` |
| `chonoi/contract.py` | khóa `extensions` (hiện chỉ `burn`); `burn_s` hữu hạn chỉ hợp lệ khi khai `burn` |
| `chonoi/live.py`, `chonoi/web/index.html` | `--mode day`, menu/pause/DayIntro/EveningIntro/Shop/Summary, HUD bổ sung |

## Hệ quả
- Test cũ `test_con_03_old_and_future_modes_rejected` đổi tên và bỏ `day` khỏi danh sách mode bị từ chối (v1.1 đã hỗ trợ); các mode `river`, `night` vẫn mã 2.
- Snapshot gather/quan có thêm trạng thái `paused` và `sim_tick` có thể nhỏ hơn `tick`; hành vi không pause không đổi (test v1.0 giữ nguyên).
- `game.contract.json`: thêm `tuning.shop`; `extensions` không khai ⇒ `burn_s: null` như lõi.
- Chưa có: monsters, cá bơi/sinh, `gather.*` v1.1 (việc của Người 1); thống kê DayResult/Summary chỉ có ở `live` (không đưa vào snapshot headless để khỏi lệch Test Contract).
