# Changelog

Ghi breaking change theo từng Test Contract. Ngày theo lab (21/11/2026).

## Contract v1.3 (TICKET-04 Phát hành v1.0.0, Phase 4)

### Thêm & Cập nhật
- **Contract v1.3:** Nâng cấp `contract_version: "1.3"`.
- **Khai báo lệnh mới:** Thêm `bench_cmd: "python3 tools/bench.py"` và `soak_cmd: "python3 tools/soak.py"` ở gốc `game.contract.json`.
- **Công cụ Soak runner:** Xây dựng `tools/soak.py` chạy kiểm thử độ bền bỉ 10 Ngày không crash (`days_completed = 10`, `crashes = 0`), kế hoạch D1–D5 lặp ở Ngày 6–10.
- **Nâng cấp giao diện trực quan:** Cải thiện `chonoi/web/index.html` với đồ họa sông nước miền Tây Nam Bộ sinh động:
  - Bầu trời bình minh hồng cam, rặng dừa nước ven bờ, bến đò Rạch Sen mái lá dừa.
  - Sóng nước nhấp nhô, tia sáng mặt trời xuyên nước (*god rays / sunbeams*), bọt khí lặn.
  - Đàn cá linh, cá lóc, cá kèo quẫy đuôi sóng sin và hoa văn vảy cá sinh động.
  - Út Sen áo bà ba, khăn rằn Nam Bộ, kính lặn tự chế; Cá Sấu Năm Chèo gai lưng và mắt đỏ rực khi đuổi.
  - Quán nhà bè sàn gỗ ấm cúng, dây đèn vàng lung linh, bếp lò đất ngọn lửa bập bùng và khói bếp uốn lượn; khách ăn biểu cảm hài lòng / tức giận.
  - Giữ nguyên 100% tính tương thích chế độ tương phản cao (phím `H`) và bài benchmark `?bench=`.
- **Hoàn thiện tài liệu nghiệm thu & quy trình:** Bổ sung `docs/verification/phase-4.md`, hoàn thiện phản tư đủ 4 thành viên trong `docs/members/`, cập nhật `docs/retro.md` và gắn tag `phase-1` đến `phase-4`.

## Unreleased — Contract v1.2 (TICKET-03 "Mùa Nước Nổi", Phase 3)

### Breaking changes
- **Kho đếm → kho cá thể.** File kho `{"items": {kind: n}}` **không còn hợp lệ** (mã thoát 2). Schema mới:
  `{"items": [{"id": "I1", "kind": "ca_linh", "fresh": 100}, ...]}`; kho rỗng `{"items": []}`; id là chuỗi duy nhất khác rỗng,
  `kind` thuộc danh mục nguyên liệu, `fresh` hữu hạn trong [0, 100]. Ghi theo id (F2 trước F10), file tạm + thay nguyên tử,
  `fresh` giữ nguyên độ chính xác để đọc lại đúng nhánh ở ngưỡng 30.
- **`gather.hold` và `quan.stock` (scenario) là mảng cá thể**; `customers[].reserved` là **mảng id cá thể** (không còn map kind→số).
  Thiếu `reserved` ở đơn `reserved` → cấp tự động theo `order_tick` rồi id bàn (tươi nhất, id nhỏ).
- **JSONL:** snapshot `hold`, `stock` (quán, Shop), `customers[].reserved` theo schema mới; `gather_end.data.inventory`,
  `cook_started.data.items` (mảng cá thể sắp theo kind rồi id) và `lost` trong `faint` (LIFO) là mảng cá thể `{id, kind, fresh}`.
- **Giá niêm yết → giá theo độ tươi:** `base_price = floor(giá × trung bình fresh của các cá thể dùng / 100)`, boa tính trên giá đã chốt.
  Hệ quả: món nấu ở bước đầu của ca đã có giá thấp hơn 1 đơn vị (ví dụ 60 → 59) vì kho đã hao 1 đơn vị.
- **Giữ chỗ theo id** (thay cho giữ theo lượng); `contract_version` = `"1.2"`; manifest thêm `tuning.freshness`.

### Thêm
- Độ tươi: giỏ hao 0.5/s, kho quán 0.25/s (kể cả hàng đang giữ), pause dừng hao, món chín không hao; `fresh < 30` là ươn
  (vẫn chiếm ô, không dùng nấu), event `spoiled {item_id, kind, location: hold|stock}` đúng một lần, theo id.
- Id cá thể `I1, I2…` tăng xuyên pha và Ngày; Ngày kế cấp id mới cho mẫu `gather.hold`; `day` bàn giao không hao thêm ở tick chuyển pha, Shop không hao.
- Scenario gather nhận khóa `monsters` (chỉ mảng rỗng; thủy quái thuộc gather v1.1).
- **Mở rộng Khách đặt trước** (`extensions: ["reservations"]`, `tuning.reservations`): 2 đơn R1,R2/Ngày, trạng thái
  `scheduled → holding → waiting → served | failed`, giữ bàn từ `arrival − 30 s`, giá cuối ×1.5 (làm tròn xuống) rồi mới tính boa,
  lỡ đơn −1 uy tín đúng một lần; event `reservation_announced/arrived/served/failed`; scenario `quan.reservations[]`,
  `quan.random_reservations`; snapshot `reservations[]`, `customers[].reservation_id`, `tables[].reservation_id`;
  quán độc lập công bố ở tick 0 (sau snapshot), `day` công bố sau `phase_start(gather)`.
  **Lưu ý fixture:** mở rộng bật trong manifest nên scenario quán muốn "lõi thuần" cần `quan.random_reservations: false`.

### Cách cập nhật fixture
- Kho/`hold`/`stock` cũ `{"ca_loc": 2}` hoặc `["ca_loc", "bong_sung"]` → `[{"id":"I1","kind":"ca_loc","fresh":100}, ...]`
  (trong test dùng `tests/helpers.make_items({"ca_loc": 2})`, đếm lại bằng `counts(items)`).
- Đơn đã khai `reserved: {"ca_loc": 1}` → `reserved: ["I1"]` (id có trong kho, chưa ươn, đúng công thức, không dùng chung).

### Test thay đổi (lý do)
- Toàn bộ fixture/so sánh kho đếm đổi sang cá thể (`test_quan*.py`, `test_day.py`, `test_burn.py`, `test_smoke_p1.py`,
  `test_inventory_kinds.py`, `test_gather_lat*.py`, `test_python_starter_units.py`): luật schema đổi, **không** đổi kỳ vọng luật khác.
- Giá món ở bước đầu của ca (`test_quan.py::test_bep_nhan_don_cu_nhat…`, `test_quan_p2.py::test_lau_mam…`): 60 → 59, 200 → 199 do giá theo tươi.
- `test_quan_p2.py::test_contract_v11_…`: `contract_version` 1.1 → 1.2.
- Khi bật `reservations`: các test lõi đặt `random_reservations: false` trong fixture (helper), `test_day::test_day_ticks_0…` đếm thêm 2 event `reservation_announced`; `test_burn::ContractExtensions` khai `extensions` kèm `reservations`.
- Thêm: `tests/test_freshness.py` (ngưỡng 30, hao, giữ lại khi vừa ươn, giá, bàn giao, day, scenario mâu thuẫn).
