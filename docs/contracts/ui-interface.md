# Hợp đồng giao diện `sim/*` ↔ `client/ui` — BẢN NHÁP chờ nhóm duyệt

- Trạng thái: **đề xuất** (Người 3 soạn, ngày 21/11/2026). Cần Người 1 (gather), Người 2 (quán, Integrator) đồng ý trước khi chốt.
- Nguồn: PRD-0 Phase 1 (lab board, Test Contract v1.0 mục D, E, F) + API sẵn có của `chonoi/live.py`.
- Phạm vi: mục 2 trong `docs/contracts/README.md` ("UI đọc trạng thái nào, gửi lệnh nào") + bảng event mà UI nghe. Schema file kho (mục 1) do Người 2 giữ, không nằm ở đây.
- Quan hệ với `docs/contracts/contract.md` (PR #1, #6): file này **chi tiết hóa mục 2** của `contract.md` cho phía UI (tọa độ hiển thị, chống lặp event, phản hồi theo event, công nghệ đồ họa). Nếu hai file lệch nhau thì **`contract.md` thắng**; sửa file này cho khớp.
- Phiên bản: mục 0–8 theo Test Contract **v1.0** (Phase 1). **Phụ lục v1.1** (Phase 2, TICKET-02) ở cuối file bổ sung, chỗ nào không nhắc thì v1.0 vẫn đúng.

## 0. Nguyên tắc (không thương lượng)

1. **Sim là nguồn sự thật duy nhất.** UI chỉ đọc snapshot/event và gửi trạng thái phím. UI không quyết luật, không đổi tick, tiền, uy tín, kho.
2. **Headless không biết UI tồn tại.** Không file nào trong `chonoi/sim/`, `runner.py`, `headless.py` import code UI. Đồ họa, hiệu ứng, âm thanh, camera chỉ chạy ở trình duyệt, nên tự động "tắt ở headless" theo PRD.
3. **Không thêm trường vào snapshot/JSONL** để phục vụ UI: như vậy là đổi output contract và có thể làm trượt test ẩn. Cần thêm dữ liệu cho UI thì thêm vào phần `meta` của `/state` (chỉ có ở `chonoi.live`), qua PR + ADR.
4. **Giá trị suy ra chỉ để hiển thị** (ví dụ kho khả dụng, % kiên nhẫn) được tính ở UI từ snapshot + `meta`. Không gửi ngược vào sim.
5. **Không hard-code số gameplay** ở UI. Lấy từ `meta` (= `tuning[mode]` của `game.contract.json`). Tên hiển thị tiếng Việt của id (món, nguyên liệu) là dữ liệu trình bày, được phép để ở UI.

## 1. Kênh truyền (giữ nguyên API của `chonoi.live`)

| Hướng | Endpoint | Nội dung | Tần suất |
|---|---|---|---|
| sim → UI | `GET /state` | Snapshot đầy đủ (cùng trường với dòng snapshot headless) + `meta`, `events`, `finished`, `reason`, `error` | Poll mỗi khung hình (~16 ms) |
| UI → sim | `POST /input` | `{"move":[a,b], "interact":bool, "catch":bool}` = **trạng thái phím đang giữ** | Khi trạng thái phím đổi |
| UI → sim | `POST /restart` | Chơi lại cùng seed/scenario | Khi bấm R |

- Sim chạy 60 tick/s ở luồng nền và tự bắt **cạnh lên** của `interact`/`catch`. UI gửi "đang giữ", không gửi "vừa bấm".
- `move` có hai thành phần trong [−1, 1]. Thành phần thứ hai **dương = xuống (gather)** hoặc **về bắc (quán)**. Sai miền thì sim trả 400.
- Nối hai buổi: `python3 -m chonoi.live --mode gather --inventory-out kho.json`, rồi `python3 -m chonoi.live --mode quan --inventory kho.json`.
- Từ v1.1 (#14, ADR-0002) có thêm `--mode day [--days N]`, nút `pause`, `shop_done`, lệnh `buy` và các khóa `/state` riêng cho `day`: xem **Phụ lục v1.1** (#12).

## 2. Hệ tọa độ: sim → cảnh hiển thị

| Pha | Sim | Gợi ý cho cảnh 3D (Three.js, trục Y hướng lên) | Camera |
|---|---|---|---|
| gather | `[x, d]`, mét; `d` tăng xuống, `d ≤ surface_depth` là mặt nước; hướng 0° = +x, 90° = xuống | `(x, −d, 0)`. Trục Z chỉ dùng cho trang trí và parallax (bờ dừa nước, rong), không ảnh hưởng gameplay | Nhìn ngang (side-scroller 2.5D), bám theo Út Sen theo trục x |
| quán | `[x, z]`, mét; `z` hướng bắc | `(x, 0, −z)` | **Nhìn từ trên xuống** (PRD-0 §3), cố định trên nhà bè 16 × 10 m. Được nghiêng nhẹ để thấy chiều cao bếp/bàn, nhưng vẫn phải đọc như góc trên xuống |

Biên lấy từ `meta.bounds`. Bán kính tương tác lấy từ `meta.interact_radius`, `meta.catch_radius`, `meta.dock_radius` để vẽ vòng gợi ý.

## 3. Trạng thái UI đọc

### 3.1 Chung (mọi pha)

| Trường | Kiểu | Dùng cho UI |
|---|---|---|
| `mode`, `phase` | `"gather"`/`"quan"` | Chọn cảnh |
| `tick`, `phase_tick` | int | Phát hiện restart (tick giảm) |
| `time_left_ticks` | int (tick) | HUD thời gian = `ceil(t/60)` giây, dạng mm:ss |
| `money`, `earned` | int (nghìn đồng) | HUD tiền |
| `reputation` | số thực [0, 5] | HUD uy tín (sao) |
| `score` | int | Màn kết thúc: `earned + 100 × floor(reputation)` |
| `state` | `"playing"`/`"finished"` | |
| `finished`, `reason`, `error` (chỉ `/state`) | bool / chuỗi / chuỗi | Màn kết thúc; báo lỗi luật |
| `meta` (chỉ `/state`) | object = `tuning[mode]` | Số tối đa, bán kính, biên |
| `events` (chỉ `/state`) | 40 dòng event gần nhất | Hiệu ứng và thông báo (mục 4) |

### 3.2 Gather — HUD bắt buộc: thời gian, oxy, Máu, giỏ

| Trường | Kiểu | Dùng cho UI |
|---|---|---|
| `player.pos`, `player.vel`, `player.heading_deg` | [x,d] m, m/s, độ | Vị trí, hướng bơi, animation bơi/đứng |
| `player.oxygen_ticks` / `oxygen_max_ticks` | int | Thanh oxy; < 25% thì cảnh báo (viền đỏ, nhịp tim) |
| `player.hp` / `hp_max` | int | Máu (3 tim) |
| `player.zero_oxy_ticks` | int [0, 59] | Đồng hồ ngạt: còn `60 − zero_oxy_ticks` tick tới lần mất Máu kế |
| `player.at_surface` | bool | Đổi trạng thái hái/lặn, gợi ý phím E hay Space |
| `player.catch_cd_ticks` | int | Vòng hồi chiêu bắt |
| `hold` | mảng kind, cuối mảng = mới nhất | Giỏ (hiện theo thứ tự nhặt) |
| `hold_count` / `hold_capacity` | int | "Giỏ 7/12" |
| `nodes[]`: `id, kind, pos, ready, regrow_ticks` | | Bông điên điển / bông súng trên mặt nước; nút chưa `ready` thì mờ đi + vòng đếm ngược |
| `fish[]`: `id, kind, pos, heading_deg` | | Đàn cá (vẽ thành đàn boid **chỉ để trang trí** quanh `pos`; điểm bắt vẫn là `pos`) |

### 3.3 Quán — HUD bắt buộc: kho khả dụng, món gọi, kiên nhẫn, bếp, món trên tay, tiền, uy tín

| Trường | Kiểu | Dùng cho UI |
|---|---|---|
| `player.pos`, `player.vel` | [x,z] m | Út Sen trên nhà bè; hướng đi suy từ `vel` |
| `stock` | map kind → số, **gồm cả phần đã giữ** | Kho vật lý |
| `customers[].reserved` | map kind → số | Kho khả dụng = `stock − Σ reserved` (chỉ hiển thị) |
| `hand` | `{order_id, dish_id, base_price}` hoặc `null` | Món trên tay |
| `stoves[]`: `id, pos, state, dish, cook_ticks_left, ready_ticks` | `idle`/`cooking`/`ready` | Bếp: khói, thanh nấu, món chín |
| `tables[]`: `id, pos, customer_id` | | Bàn, ai đang ngồi |
| `customers[]`: `id, table_id, dish_id, state, patience_ticks_left, order_status, eat_ticks_left, base_price, tip` | | Bong bóng món gọi; vòng kiên nhẫn = `patience_ticks_left / (meta.patience_s × 60)`, chuyển xanh → vàng → đỏ; ăn thì hiện thanh ăn |

Snapshot chỉ liệt kê khách còn ngồi. Khách biến mất thì UI phát hiệu ứng rời bàn dựa vào event `customer_left`/`paid`.

## 4. Event UI nghe (PRD-0 mục E)

Đọc từ `events` của `/state`: các dòng `{type:"event", tick, phase, name, data}`. **Chống lặp:** UI lưu `lastTick` và chỉ xử lý dòng có `tick > lastTick` (event của một tick được ghi cùng lúc dưới khóa). Khi `tick` của snapshot giảm (restart), đặt `lastTick = 0` và xóa hiệu ứng đang chạy.

| Event | `data` | Phản hồi trên UI (gợi ý) |
|---|---|---|
| `dive` / `surface` | `pos` | Bọt nước + tiếng "tõm"; đổi màu nước, bật/tắt caustics |
| `oxygen_empty` | `oxygen_ticks:0` | Thanh oxy nhấp nháy đỏ, tiếng tim đập |
| `choke` | `hp` | Rung màn hình, mất một tim |
| `faint` | `cause, lost, hp:0` | Màn mờ dần, giỏ rơi từng món theo `lost` |
| `gather` / `node_regrown` | `node_id, kind, amount` / `node_id` | Chữ bay "+1 bông súng", bông nở lại |
| `fish_caught` | `fish_id, kind, yield` | Tia nước, "+3 cá linh", đàn cá biến mất |
| `hold_full` | `action, node_id/fish_id, required, free` | Lắc giỏ, "Giỏ đầy: cần 3, còn 2" |
| `gather_end` | `reason, inventory` | Màn tổng kết sáng (`docked` / `time` / `fainted`) |
| `customer_arrived` / `no_dish` | `order_id, table_id, dish_id` / `{}` | Khách chèo xuồng tới, bong bóng món / "Hết nguyên liệu" |
| `cook_started` / `dish_ready` / `dish_picked` | `stove_id, order_id, dish_id` (+`items, base_price`) | Khói bếp, tiếng chuông khi chín, món lên tay |
| `served` | `…, patience_ticks_left, base_price, tip` | Đặt món lên bàn |
| `paid` | `…, base_price, tip, amount, reason` | Đồng xu bay về HUD tiền; boa > 0 thì có sao bay lên uy tín |
| `customer_left` | `…, reason, reputation` | `patience` thì khách giận bỏ đi, uy tín nhấp nháy đỏ; `closing` thì khách chào về |
| `quan_end` | `reason, money, earned, shift_earned, reputation` | Màn tổng kết tối + điểm |

## 5. Lệnh UI gửi và phím

| Phím | Gửi | Ghi chú |
|---|---|---|
| WASD / mũi tên | `move` | Trong gather, S/↓ = lặn xuống (thành phần 2 dương); trong quán, W/↑ = về bắc (thành phần 2 dương). Khớp với `currentInput()` của `chonoi/web/index.html`; client mới phải giữ nguyên cách gán này |
| E | `interact` | Cập bến, hái (gather); nấu, bưng, phục vụ (quán) |
| Space | `catch` | Bắt cá khi đang lặn |
| R | `POST /restart` | |
| Chuột/cuộn | — | Camera và zoom **chỉ ở client**, không gửi vào sim |
| Mất focus cửa sổ | `move:[0,0]`, nút false | Tránh kẹt phím (khung đã làm) |

## 6. Đồ họa và công nghệ (đề xuất, cần nhóm chốt)

Hai game mẫu nhóm tham khảo ([Săn Cá Khủng](https://kenhgt247.github.io/cauca/), [Vỉa Hè Tochi](https://tochicafe247.netlify.app/)) **chỉ dùng làm cảm hứng: không sao chép mã hay asset** của các game này (README: không dùng nội dung của nhóm khác; asset ngoài chỉ CC0/CC-BY/MIT và ghi `CREDITS.md`). Cả hai đều dùng **Three.js r128 qua CDN**, hình low-poly dựng bằng code và **HUD bằng HTML/CSS phủ lên canvas**. Đề xuất đi cùng hướng đó, dùng bản mới hơn:

| Hạng mục | Đề xuất | Giấy phép | Ghi chú |
|---|---|---|---|
| Render 3D | Three.js (ES module, ghim phiên bản) | MIT | Cảnh low-poly dựng bằng code, không cần file model |
| Hậu kỳ | `EffectComposer`, `UnrealBloomPass` có sẵn trong `three/examples` | MIT | Bloom cho đèn dây vàng buổi tối, ánh hồng buổi sớm |
| Nước | Shader tự viết: mặt nước gợn sóng (vertex), caustics dưới đáy, tia sáng (god rays) bằng mặt phẳng trong suốt | Tự viết | Tham khảo [threejs-caustics](https://medium.com/@martinRenou/real-time-rendering-of-water-caustics-59cda1d74aa), [low-poly water](https://discourse.threejs.org/t/low-poly-ocean-water/33513) |
| Phong cách | Toon/cel shading (`MeshToonMaterial`) + viền | MIT | Hợp với hình khối 2D/3D đơn giản |
| Hạt | Bọt khí, khói bếp, đồng xu: `Points`/instancing tự viết | MIT | |
| Âm thanh | Web Audio API (hoặc Howler.js) | MIT | Nhạc và hiệu ứng tự tạo hoặc CC0 |
| Asset | Kenney.nl, Poly Pizza (chỉ lấy CC0/CC-BY) | CC0/CC-BY | Ghi đủ vào `CREDITS.md` |
| HUD | HTML/CSS overlay | Tự viết | Dễ đọc, dễ chụp bằng chứng |

**Không dùng** nếu chưa hỏi giảng viên: thư viện giấy phép ngoài CC0/CC-BY/MIT (ví dụ pmndrs `postprocessing` là Zlib, GSAP có điều khoản riêng, font Google là OFL). Gặp thì ghi vào `docs/clarify.md`.

Bố cục cảnh theo PRD-0 §3:
- **Gather:** sông màu phù sa, bờ dừa nước, nhà sàn, ánh hồng buổi sớm. Út Sen mặc áo bà ba, khăn rằn, kính lặn tự chế, giỏ lưới.
- **Quán:** nhà bè nhìn từ trên xuống, đèn dây vàng, khói bếp.

### Cần quyết trước khi code (chọn 1)

| Phương án | Cách làm | Ưu | Nhược |
|---|---|---|---|
| **A. Một file** | Thay `chonoi/web/index.html`: Three.js nạp bằng `importmap` từ CDN, mọi code trong một file | Chỉ sửa một file | Vẫn sửa file khung (`chonoi/web/`), nên **cần PR riêng + ADR**; mất client 2D dự phòng; cần mạng lúc chạy/demo |
| **B. Thêm route tĩnh** (khuyên dùng; Người 2 cũng nghiêng về B) | ADR + PR riêng: `live.py` phục vụ `chonoi/web/static/*`; client 3D là **trang mới** (ví dụ `/static/3d.html`); vendor `three.module.min.js` (MIT, kèm LICENSE) vào repo | Giữ nguyên `index.html` 2D làm dự phòng (test `<canvas` vẫn qua); chạy offline; code chia module | Sửa `live.py`, nên cần ADR + Integrator duyệt |

Cả hai phương án đều đụng file khung, nên cả hai cần ADR. Số ADR kế tiếp là **ADR-0003** (`0001` kind kho v1.1 và `0002` mode day/pause đã có trên `main`). Phương án B cần thêm test cho route tĩnh trong `tests/test_live.py`. Nạp Three.js từ CDN (phương án A, hoặc demo ở #11) thì hỏng khi offline và không có kiểm toàn vẹn; vì vậy bản client thật phải vendor kèm LICENSE. Nếu sửa `index.html`, file vẫn phải chứa thẻ `<canvas` (test `tests/test_live.py` kiểm tra); truyền canvas đó cho `WebGLRenderer`. `build_cmd` vẫn là `true` (không cần bundler).

### Thứ tự triển khai (bảo vệ tag `phase-1`)

1. **Phase 1:** làm HUD bắt buộc (mục 3.2, 3.3) ngay trên client canvas hiện có. Đây là phần DoD chấm lúc gắn tag.
2. **Sau khi HUD chạy và lõi luật đã merge:** làm client Three.js thành PR riêng. Client 3D **không bao giờ được chặn** việc gắn `phase-1` hay các tag sau.

## 7. Xử lý thiếu dữ liệu

- Trường chưa có (luật chưa viết) thì bỏ qua phần đó, không báo lỗi. Ví dụ chưa có `oxygen_ticks` thì ẩn thanh oxy.
- `/state` lỗi mạng thì hiện "Mất kết nối"; `error` khác null thì hiện "Luật báo lỗi, xem terminal, R để chơi lại".
- Entity biến mất khỏi mảng (cá bị bắt, khách rời) thì UI tự xóa mesh theo `id`. Entity mới thì tạo mesh. Khớp theo `id`, không theo chỉ số mảng.
- Chuyển động mượt: UI được nội suy vị trí hiển thị giữa hai snapshot. Đây chỉ là hình ảnh, HUD vẫn hiện số thật.

## 8. Câu hỏi mở cho nhóm

1. Chọn phương án A hay B ở mục 6? Người 2 nghiêng về **B**. Cả hai đều cần **ADR-0003** vì đụng file khung.
2. ~~Có cần thêm giá và thời gian nấu vào `/state` không?~~ Đã có: ở `--mode day`, `/state` có `menu_data` (= `tuning.menu`) từ #14.
3. Ai review hợp đồng này: Người 1 (mục 3.2), Người 2 (mục 3.3 + ADR), Người 4 (mục 4, chống lặp event)?

---

# Phụ lục v1.1 — Phase 2 (TICKET-02 "Một ngày ở chợ nổi")

Tên trường và event khớp phụ lục v1.1 của `contract.md` (#6); nếu lệch thì `contract.md` thắng.

**Nhãn nguồn:** **[T]** = TICKET-02 yêu cầu (bắt buộc cho tag `phase-2`). **[ĐX]** = đề xuất của Người 3, ticket không yêu cầu; nhóm được bỏ. Làm hết **[T]** trước, **[ĐX]** và phần sáng tạo làm sau, khi lõi đã đúng (TICKET-02 §3: "Hoàn thành lõi trước").

Phạm vi lõi: thủy quái chỉ có **Cá Sấu Năm Chèo** (M1, M2 từ Ngày 3). Rắn Hổ Mây, Lao xua, Vợt, Cháy món, Chợ Chú Sáu, Sổ tay/Cá Hô, Cài đặt/âm thanh nằm trong bảng **Mở rộng**, nhóm 4 người không bắt buộc.

## A. Kênh truyền `chonoi.live` v1.1 — đã có trên `main` (#14, ADR-0002)

| Thành phần | Trên `main` |
|---|---|
| CLI | `python3 -m chonoi.live --mode day [--days N]` (N ∈ 1..5). Mở ở menu chính |
| `POST /input` | Thêm `pause`, `shop_done` (boolean, sim bắt **cạnh lên**: client gửi `true` rồi `false`, không giữ) và `buy` (chuỗi `"oxygen"`/`"hp"`, server áp **đúng một bước** rồi xóa) |
| `meta` | Ở `day` là tuning của **pha hiện tại** (`gather` hoặc `quan`), không phải toàn bộ tuning |
| Khóa `/state` thêm ở `day` | `menu` (đang ở menu chính), `stats`, `days_total`, `shop` (= `tuning.shop`), `menu_data` (= `tuning.menu`) |
| `stats` | `{day: {served, left, tips, earned, reputation_start}, served, left, tips, sold: {dish_id: n}}`: server tự cộng theo Ngày và cả lượt |

Các khóa này **chỉ có ở `/state`**, không có trong snapshot headless, nên Test Contract không đổi.

## B. Các màn hình — [T] (TICKET-02, mục Menu, pause và HUD)

Vòng ngày [T]: `DayIntro → gather → EveningIntro → quan → DayResult → Shop → DayIntro…`, tổng kết sau Ngày 5. Shop đóng sớm được.

| Màn hình | Ticket yêu cầu hiện [T] | Lấy số liệu từ đâu |
|---|---|---|
| Menu chính | Chơi và Thoát | `menu` trong `/state` |
| DayIntro | Ngày và danh sách Má Tư đọc; **tự chuyển sau 4 s hoặc khi nhấn phím** | `day`, `day_plan.dishes`, `day_plan.ingredients` |
| EveningIntro | Số lượng nhập kho và món nấu được | `stock` đầu pha quán; món trong `day_plan.dishes` có công thức ≤ `stock` |
| DayResult | Khách đã phục vụ / bỏ đi, tiền, boa, thay đổi uy tín | `stats.day`: `served`, `left`, `earned`, `tips`; uy tín thay đổi = `reputation` − `stats.day.reputation_start` |
| Shop | Mua Bình oxy, Áo phao; đóng sớm được; tự đóng khi hết giờ | `upgrades`, `shop.upgrades` (giá theo cấp), `money`, `time_left_ticks`; event `bought` / `buy_failed` |
| Summary | Tổng tiền, tổng điểm, uy tín, món bán chạy | `money`, `earned`, `score`, `reputation`; món bán chạy từ `stats.sold` |

- [T] Cấp mua trong Shop chỉ có hiệu lực từ Ngày kế: HUD sáng tính oxy/Máu tối đa theo `active_upgrades`, không theo `upgrades`.
- Trên `main`, DayIntro/EveningIntro là lớp phủ **không tạm dừng sim**: tự đóng sau 4 s hoặc khi nhấn phím. Pause thật dùng Esc/P. Muốn các màn Intro tự pause thì phải sửa thêm `live.py`; hiện không cần, vì ticket không yêu cầu.

## C. Pause — [T]

- [T] Esc/P tạm dừng. Menu pause làm mờ nền, có **Tiếp tục** và **Về menu**; thêm Cài đặt chỉ khi làm mở rộng. Trên `main`: Enter để tiếp tục, M để về menu.
- [T] Dừng đồng hồ và mọi timer gameplay, kể cả trong Shop. Snapshot `state:"paused"`, event `paused` / `resumed`.
- `pause` là **cạnh lên**: gửi `true` rồi `false`.
- [ĐX] Animation trang trí (nước, đèn) chạy tiếp khi pause.

## D. HUD sáng v1.1

Cột "Trên `main`" ghi tình trạng `chonoi/web/index.html` (đọc code ngày 21/11/2026, **chưa kiểm bằng mắt**).

| Thành phần | Ticket yêu cầu [T] | Nguồn | Trên `main` | Đề xuất thêm [ĐX] |
|---|---|---|---|---|
| Máu | Có | `player.hp` / `hp_max` | Có (tim) | Nhấp nháy khi `invuln_ticks > 0` |
| Oxy | Dưới 25% đổi màu / nhấp nháy | `player.oxygen_ticks` / `oxygen_max_ticks` | Có (đổi màu) | |
| "Hết hơi!" | Khi oxy cạn | `oxygen_ticks = 0` dưới nước | Có | |
| Thời gian | Đổi màu khi còn ≤ 30 s | `time_left_ticks` ≤ 1.800 | Có | |
| Độ sâu | Có | `player.pos[1]` | Có, chữ 14 px | Thước tô 3 vùng nông/giữa/sâu |
| Giỏ theo loại | Có | `hold`, `hold_count` / `hold_capacity` | Có (ô màu + dòng đếm theo loại), chữ 12 px | |
| Đã lấy / cần | Có | `day_plan.ingredients`, đếm `hold` | Có, chữ 14 px | ✓ khi đủ |
| Hồi bắt | Có | `player.catch_cd_ticks` | Có, chữ 12 px | |
| Gợi ý hái / cập bến | Khi đến gần | Bán kính trong `meta`, nút `ready` | Có | |
| "Thủy quái!" + **viền tím** | Khi có thủy quái gần | `monsters[]` | **Chưa đúng**: dùng tạm `invuln_ticks > 0` (sau khi bị cắn), chưa có viền tím. Cần `monsters[]` từ gather v1.1 | Ngưỡng "gần" (xem H.1); mũi tên chỉ con ngoài khung nhìn |

Thực thể mới [T]: `fish[]` nay bơi (cá linh d ∈ [3,12], cá lóc [8,20], cá kèo [22,28]); `fish_spawned`; `monsters[]` Cá Sấu M1/M2 với `state` patrol/chase/recoil; `monster_hit` có `lost` theo LIFO; `faint` có `cause:"monster"`. Cách vẽ (dáng, rung màn hình) là [ĐX].

## E. HUD quán v1.1

| Thành phần | Ticket yêu cầu [T] | Nguồn | Trên `main` | Đề xuất thêm [ĐX] |
|---|---|---|---|---|
| Đồng hồ ca | Có | `time_left_ticks` | Có | |
| Tiền ca | Có | `earned` − `earned` đầu pha quán (`stats.day.earned`) | **Chưa**: đang hiện tổng `money` | |
| Uy tín | Có | `reputation` | Có | |
| Món + kiên nhẫn **tại từng bàn** | Đổi màu khi < 25% | `tables[].customer_id` → `customers[]` | Có | Phiếu order T1–T4 cố định trên màn hình |
| Tiến độ bếp / món chín | Có | `stoves[]`: `cook_ticks_left`, `state:"ready"` | Có (số giây, chữ 11 px) | |
| Món đang cầm | Có | `hand` | Có, chữ 11 px | |
| Kho khả dụng | Có | `stock − Σ customers[].reserved` | **Chưa đúng**: đang hiện `stock` (kho vật lý, gồm phần khách đã giữ) | |

## F. Yêu cầu kỹ thuật — [T]

| Yêu cầu | Trên `main` |
|---|---|
| Chữ không chân **≥ 18 px ở 1280×720**; bằng chứng: ảnh chụp trong `docs/proof/phase-2/` | **Chưa**: còn nhiều chữ 10–16 px |
| Trung bình **≥ 30 FPS ở 1280×720**; bằng chứng: số đo trong verification | **Chưa đo** |
| Kiểm bằng mắt Shop, EveningIntro, Summary, HUD quán | **Chưa** (#14 tự ghi nhận) |

- [ĐX] Bộ đếm FPS bật bằng phím trong client để đo.
- Tên hiển thị thêm (dữ liệu trình bày): `ca_keo` cá kèo, `keo_neo` kèo nèo; `canh_chua_ca_loc` Canh chua cá lóc bông điên điển, `ca_keo_nuong` Cá kèo nướng muối ớt, `lau_mam` Lẩu mắm miền Tây.

**Việc thật còn lại của Người 3** (theo D, E, F): chữ ≥ 18 px; kho khả dụng; tiền ca; giỏ theo loại có số đếm; "Thủy quái!" + viền tím (khi có `monsters[]`); đo FPS; ảnh 1280×720; kiểm bằng mắt các màn hình.

## G. Lệnh gửi và phím

| Phím (trên `main`) | Gửi | Nguồn |
|---|---|---|
| Esc / P | `pause` (cạnh lên) | [T] |
| Enter khi pause / M khi pause | `pause` (tiếp tục) / `POST /restart` (về menu) | [T] Tiếp tục, Về menu |
| Enter trong Shop | `shop_done` | [T] đóng sớm |
| 1 / 2 trong Shop | `buy:"oxygen"` / `buy:"hp"` | [T] mua |
| Q, F | `attack`, `photo` | Chỉ khi bật mở rộng Lao xua / Sổ tay |

## H. Câu hỏi mở (v1.1)

1. Ngưỡng "thủy quái gần" để hiện "Thủy quái!": ticket không định nghĩa. Đề xuất `detect_radius` của loài hoặc `state:"chase"`; ghi vào `docs/clarify.md` và hỏi Anh Năm.

## Nguồn

- [Săn Cá Khủng](https://kenhgt247.github.io/cauca/) và [Vỉa Hè Tochi](https://tochicafe247.netlify.app/): game mẫu nhóm gửi; kiểm tra ngày 21/11/2026, cả hai dùng Three.js r128 + HUD HTML.
- Tham khảo (từ kết quả tìm kiếm, chưa mở đọc kỹ): [Real-time rendering of water caustics](https://medium.com/@martinRenou/real-time-rendering-of-water-caustics-59cda1d74aa) · [Low-poly ocean/water (three.js forum)](https://discourse.threejs.org/t/low-poly-ocean-water/33513) · [How to create a shallow underwater scene](https://discourse.threejs.org/t/how-to-create-a-shallow-underwater-scene/62687)
- [7 small 3D browser games with zero model/texture/audio files](https://discourse.threejs.org/t/7-small-3d-browser-games-with-zero-model-texture-or-audio-files-900-kb-each/95438): ví dụ game Three.js dựng hoàn toàn bằng code.
- [MDN: 3D games on the Web](https://developer.mozilla.org/docs/Games/Techniques/3D_on_the_web)
- TICKET-02 "Một ngày ở chợ nổi" (lab board, tab Phase 2, đọc ngày 21/11/2026): nguồn của phụ lục v1.1.
