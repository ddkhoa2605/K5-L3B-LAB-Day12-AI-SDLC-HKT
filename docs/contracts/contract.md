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
<<<<<<< HEAD

---

# Phụ lục v1.1 (Phase 2, TICKET-02)

> Nguồn: TICKET-02 (lab board). Mục này **bổ sung** cho v1.0 ở trên; chỗ nào không nhắc thì v1.0 vẫn đúng. Người giữ: Người 2. Đổi cần 2 approvals.

## A. Dữ liệu chuẩn (`game.contract.json`, `contract_version: "1.1"`)
| Phạm vi | Nội dung | Ai làm | Trạng thái |
|---|---|---|---|
| `quan`, `menu` | bếp B1 [2,8], B2 [5,8]; bàn T1 [9,2], T2 [13,2], T3 [9,6], T4 [13,6]; 6 món (thêm `canh_chua_ca_loc`, `ca_keo_nuong`, `lau_mam`) | Người 2 | PR #5 |
| nguyên liệu | thêm `ca_keo`, `keo_neo` (kho/`hold`/`stock` nhận 6 kind) | Người 2 | PR #4 + ADR-0001 |
| `day_plan` | mảng 5 phần tử `{day, dishes, ingredients}`; `ingredients` = Σ công thức × suất (hàm `scenario.day_plan_ingredients`) | Người 2 | PR #5 |
| `gather` | `fish_initial` 8 đàn, cá kèo, N5/N6, bơi/sinh cá (`fish_speed, fish_turn_ticks, fish_max, fish_spawn_ticks, fish_spawn_clearance, fish_x, fish_depths, fish_spawn_x, fish_spawn_depths, fish_weights`) | Người 1 | chưa |
| `gather.monsters` | `species.ca_sau`, `spawns[]`, `invuln_ticks: 90`, `loss_ratio: 0.5` | Người 1 | chưa |
| `shop` | `{max_ticks, upgrades: {oxygen[], hp[]}}` (oxygen 200→45 s, 400→60 s; hp 250→4, 500→5) | Người 3/4 (day) | chưa |
| mở rộng | khai mã ở `extensions` tại gốc manifest nếu làm | — | không bắt buộc |

## B. CLI, input, pause
- `--mode gather|quan|day`, thêm `--days <N>` (1–5, mặc định 1, chỉ với `day`). `day` bàn giao kho trong bộ nhớ theo schema mục 1.
- Nút boolean mới: `pause` (cả ba mode), `shop_done` (Shop); `attack`, `photo` chỉ khi bật mở rộng. Chỉ cạnh lên; giữ nút qua đổi pha không tạo cạnh.
- `buy`: chuỗi khác rỗng, chạy chỉ ở frame khai báo; nhận `oxygen`, `hp` (+ `weapon`, `net`, `buy:<kind>`/`sell:<kind>` nếu bật). Lệnh không hỗ trợ trong Shop → `buy_failed`.
- Xét cạnh `pause` trước mọi thứ khác. Đang pause: chỉ tăng `tick` ngoài, bỏ qua cạnh hành động và `buy`; `sim_tick`, `phase_tick`, lịch, timer đứng yên. Cạnh lên tiếp theo phát `resumed` và chạy gameplay ngay bước đó.

## C. Scenario `day`
`{"day":{"money","earned","reputation","upgrades","day_plan"}, "gather":{...}, "quan":{...}}` — `gather`/`quan` là mẫu khởi tạo **mỗi Ngày**. Mặc định money/earned 0, uy tín theo tuning, `upgrades` `{}`, kế hoạch theo preset. Cần `0 ≤ money ≤ earned` (khai cả hai khi có tiền). `day.day_plan` ghi đè theo số Ngày, `ingredients` tính lại và so với giá trị khai. **Cấm** `quan.stock` và `quan.reputation` khi chạy `day`.

## D. Output thêm
- Snapshot: `state:"paused"`; trong `day`, mọi snapshot có `day, day_plan, upgrades, active_upgrades`; `phase` ∈ `gather|quan|shop`; Shop có `stock` dư và `time_left_ticks`; snapshot đổi pha ghi pha mới với `phase_tick:0`. Event mang pha cũ; vỏ event trong `day` thêm `day`.
- Event mới: `monster_hit`, `fish_spawned`, `faint` (thêm `cause:"monster"`), `day_start`, `phase_start`, `day_plan {dishes, ingredients}`, `paused`, `resumed`, `bought {upgrade, level, price, money}`, `buy_failed {action, reason: funds|max_level|out_of_stock|unknown}`, `shop_end {reason: done|time}`. Mở rộng: `attack`, `monster_stunned`, `photo`, `released`, `dish_burnt`, `vendor_trade`.
- Snapshot gather thêm `monsters[]` (cùng trường với scenario, thêm `state`) và `player.invuln_ticks`; có Sổ tay thì thêm `ca_ho` (object hoặc `null`).
- `data` của event mới: `monster_hit {monster_id, hp, lost, pos}` (`pos` là vị trí người chơi, `lost` mảng kind theo LIFO) · `fish_spawned {id, kind, pos}` · `day_start {}` · `phase_start {}` · `day_plan {dishes, ingredients}` · `paused {}` · `resumed {}` · `faint` thêm `cause:"monster"` (`lost` liệt kê phần giỏ còn lại, `hp:0`).
- Dòng `end` của `day` thêm `days_completed`; đủ số Ngày → `reason:"days_complete"`.

### C2. Scenario gather v1.1 (TICKET-02 mục 4.3) — Người 1 cài
- `gather.player` thêm `invuln_ticks` (và `attack_cd_ticks` nếu bật Lao).
- `gather.fish[]` thêm `age_ticks` (mặc định 0: số bước cá đã tham gia bơi). `random_fish:false` tắt **cả** cá mặc định, bơi và sinh; cá fixture đứng yên. Khai `fish` khi cờ bật thì thay đàn ban đầu, vẫn bơi/sinh.
- `gather.monsters[]` thay danh sách mặc định: `{id, kind, pos, waypoints, target_idx, state, state_ticks_left, recoil_dir}`. Hai waypoint; `target_idx` 0 hoặc 1 (mặc định 1); `state` mặc định `patrol`; `recoil_dir` là vector đơn vị khi recoil, `null` ở trạng thái khác; `recoil`/`stunned` cần timer dương. Bỏ mảng thì dùng bố trí đúng Ngày.
- Nếu bật Sổ tay: `gather.ca_ho` là `{id, pos, heading_deg, photographed}` hoặc `null`; `random_ho:false` tắt sinh/di chuyển tự động. Nếu bật cháy: `quan.stoves[].ready_ticks` dựng tuổi món chín.
- **Khách `eating` (quan):** phải khai `base_price` và `tip`; thiếu → mã 2 (đã cài ở `scenario.py`).

## E. Chuyển pha và thứ tự
`day_start → day_plan → phase_start(gather)`; sau `gather_end` dựng quán và phát `phase_start(quan)` cùng tick (kể cả khi ngất); sau `quan_end` dựng Shop và phát `phase_start(shop)` cùng tick; pha mới chỉ chạy gameplay từ bước sau. Shop xử lý **một** `buy` trước cạnh `shop_done` (kể cả bước cuối); đóng Shop tăng `days_completed`, kết thúc hoặc dựng Ngày kế ngay tick đó; cấp đã mua chỉ sao sang `active_upgrades` khi dựng Ngày mới.

## F. Giao diện Quán trong `day` (Người 2 → người làm `day`)
`QuanSim(tuning, scenario, streams, ids, inventory=None, allowed_dishes=None, money=0, earned=0, reputation=None)`:
- `allowed_dishes`: tập id món của `day_plan[Ngày]`; khách chỉ chọn trong tập này, **sau đó** mới lọc theo nguyên liệu khả dụng. `None` = cả 6 món (quán chạy riêng).
- `money`, `earned`, `reputation`: trạng thái giữ qua Ngày; `shift_earned` luôn bắt đầu 0 mỗi ca.
- Khách fixture có món ngoài kế hoạch → `BadInput` (mã 2).
- Kho thực lúc mở quán = `hold` của `gather_end` (hoặc kho bàn giao rỗng khi ngất); truyền vào `inventory=`.

## G. Chưa chốt (hỏi PO, xem `docs/clarify.md`)
Ai làm vòng `--mode day` / Shop / pause / menu / HUD (lát 4); vị trí khóa `day_plan`, `shop` trong manifest (đang đặt dưới `tuning`).
=======
- Khách fixture `state:"eating"` **phải khai** `base_price` và `tip` (PRD-0 mục D: "khai `base_price,tip` đã chốt"); thiếu một trong hai → mã 2. Các trạng thái khác thì `base_price` mặc định theo menu / 0 và `tip` mặc định 0.
>>>>>>> origin/main
