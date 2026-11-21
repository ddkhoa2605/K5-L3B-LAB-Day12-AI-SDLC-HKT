# Hợp đồng tích hợp v1.0 (Phase 1)

> Nguồn: PRD-0 (lab board, mục A–G) + khung `chonoi/`. Khóa theo `AGENTS.md`: đổi file này cần báo cả nhóm, ghi lý do, **2 approvals**.
> Ba mục bắt buộc của `docs/contracts/README.md`: (1) schema kho, (2) giao diện sim ↔ UI, (3) danh sách sự kiện.

## 1. Schema file kho (mục G PRD-0)

Ví dụ hợp lệ: [`inventory.sample.json`](inventory.sample.json).

```json
{"items": {"bong_sung": 2, "ca_loc": 1}}
```

| Quy tắc | Chi tiết |
|---|---|
| Khóa gốc | Đúng một khóa `items` (khóa thừa → mã thoát 2) |
| `items` | object `kind → số nguyên ≥ 0`; kind ∈ `ca_loc, ca_linh, bong_dien_dien, bong_sung`; kind lạ, số âm, số thực, bool → mã 2 |
| Kind vắng | tính là 0; khi ghi, bỏ khóa có lượng 0; kho rỗng là `{"items":{}}` |
| Ai ghi | `gather` bằng `--inventory-out`, **đúng một lần**, chỉ khi có `gather_end`; nội dung khớp `data.inventory` của event `gather_end`. Chạm `--ticks` trước khi kết thúc → không tạo/ghi đè file |
| Cách ghi | file tạm cùng thư mục rồi thay thế nguyên tử; byte ổn định (khóa sắp theo id, `\n` cuối) |
| Ai đọc | `quan` bằng `--inventory`; tồn kho của quán **không** bị trần giỏ |
| Quán độc lập | thiếu cả `--inventory` và `scenario.quan.stock` → kho rỗng; tiền, `earned` đầu lượt = 0 |
| Xung đột | khai cả `--inventory` và `scenario.quan.stock` → mã 2 |
| Cờ theo mode | `--inventory` chỉ với `quan`; `--inventory-out` chỉ với `gather` |

## 2. Giao diện `sim/*` ↔ `client/ui`

UI **chỉ đọc snapshot** và **chỉ gửi input**; không gọi vào luật.

**Lớp dùng chung:** `chonoi.runner.Session(mode, tuning, scenario, seed, inventory)` → `snapshot()`, `step(inp)`, `end_row()`, `done`. Headless (`run`) và cửa sổ trực tiếp (`chonoi.live`) cùng chạy lớp này.

**UI gửi (command):** `LiveInputs.set(move=[x, d|z], interact=bool, catch=bool)`; mỗi tick `advance()`.
- `move`: hai số trong [−1, 1], chuẩn hóa nếu dài > 1. Thành phần thứ hai dương = xuống (gather) / hướng bắc (quan, `z`).
- `interact`, `catch`: chỉ **cạnh lên** (false → true) mới tác động; sai pha thì bỏ qua. `catch` chỉ có nghĩa ở gather.

**UI đọc (state), chung cho mọi snapshot:** `type, tick, sim_tick, mode, phase, phase_tick, state (playing|finished), time_left_ticks, money, earned, reputation, score`.

**Gather thêm:** `player{pos[x,d], vel, heading_deg, oxygen_ticks, oxygen_max_ticks, hp, hp_max, zero_oxy_ticks, invuln_ticks, catch_cd_ticks, at_surface}`, `hold[]` (thứ tự nhặt, mới nhất cuối), `hold_count`, `hold_capacity`, `nodes[{id,pos,kind,ready,regrow_ticks}]`, `fish[{id,pos,kind,heading_deg}]`.

**Quán thêm:**

| Trường | Nội dung |
|---|---|
| `player` | `{pos:[x,z], vel:[x,z]}` |
| `stock` | `{kind: n}` — tồn **vật lý** (gồm phần đã giữ cho khách) |
| `hand` | `null` hoặc `{order_id, dish_id, base_price}` (tối đa 1 món, `carry_limit`) |
| `stoves[]` | `{id, pos, state (idle\|cooking\|ready), dish (payload\|null), cook_ticks_left, ready_ticks}` |
| `tables[]` | `{id, pos, customer_id (null nếu trống)}` |
| `customers[]` | chỉ khách còn ngồi: `{id, table_id, dish_id, order_tick, state (waiting\|eating), patience_ticks_left, eat_ticks_left, order_status (reserved\|assigned\|unfulfillable\|served), reserved{kind:n}, base_price, tip}` |

HUD tối thiểu (AC-P1-10): thời gian, oxy, Máu, giỏ (sáng); kho, món gọi, kiên nhẫn, trạng thái bếp, món trên tay, tiền, uy tín (tối). Trường chưa có thì UI bỏ qua.

**Sai lệch cho phép khi chấm:** tọa độ ±0.1 m, uy tín ±0.01, thời gian ±2 tick; tiền, điểm, id, số lượng, lý do, thứ tự và tick event biên: chính xác. Tọa độ xuất tới 3 chữ số thập phân.

## 3. Danh sách sự kiện

Dòng JSONL: `{"type":"event","tick":k+1,"phase":"gather|quan","name":...,"data":{...}}`, theo thứ tự xử lý, trước snapshot của cùng tick. `items`, `lost` là mảng kind (`lost` theo LIFO).

### Gather (bên phát: `sim/gather` — Người 1; bên nghe: UI, QA, runner ghi kho)
| name | data |
|---|---|
| `gather` | `node_id, kind, amount` |
| `node_regrown` | `node_id` |
| `hold_full` | `action (gather\|catch), node_id\|fish_id, required, free` |
| `fish_caught` | `fish_id, kind, yield` |
| `dive` / `surface` | `pos` |
| `oxygen_empty` | `oxygen_ticks: 0` |
| `choke` | `hp` |
| `faint` | `cause:"choke", lost, hp:0` |
| `gather_end` | `reason (time\|docked\|fainted), inventory` (object theo mục 1) |

### Quán (bên phát: `sim/quan` — Người 2; bên nghe: UI, QA)
| name | data | Khi nào |
|---|---|---|
| `customer_arrived` | `order_id, table_id, dish_id` | khách mới ngồi, đã giữ nguyên liệu |
| `no_dish` | `{}` | có bàn trống nhưng không món nào đủ nguyên liệu khả dụng |
| `cook_started` | `stove_id, order_id, dish_id, items, base_price` | bếp idle nhận đơn reserved cũ nhất |
| `dish_ready` | `stove_id, order_id, dish_id` | nấu xong → `ready` |
| `dish_picked` | `stove_id, order_id, dish_id` | người chơi lấy món (tay trống) |
| `served` | `order_id, table_id, dish_id, patience_ticks_left, base_price, tip` | đặt món đúng bàn |
| `paid` | `order_id, table_id, base_price, tip, amount, reason (finished_eating\|closing)` | khách ăn xong trả tiền; `amount = base_price + tip` |
| `customer_left` | `order_id, table_id, reason (patience\|closing), reputation` | hết kiên nhẫn / hết ca |
| `quan_end` | `reason:"time", money, earned, shift_earned, reputation` | hết ca, sau khi dọn xong khách |

Dòng cuối của file: `{"type":"end","ticks","sim_tick","mode","state","reason","money","earned","reputation","score"}`; `reason` ∈ `time|docked|fainted` (gameplay) hoặc `tick_limit`. `score = earned + 100 × floor(reputation)` (hệ số `score.reputation_multiplier` trong `game.contract.json`).

### Quy tắc đã chốt cho phần PRD-0 chưa nói rõ (xem `docs/clarify.md`)
- Khi `no_dish`, **không** có khách được tạo (không đổi uy tín).
- Khách chưa nấu có `base_price = 0`, `tip = 0`; giá chốt khi `cook_started`.
- Khách fixture bắt buộc có `dish_id` hợp lệ (thiếu → mã 2).
- `carry_limit` hiện chỉ hỗ trợ giá trị 1.
