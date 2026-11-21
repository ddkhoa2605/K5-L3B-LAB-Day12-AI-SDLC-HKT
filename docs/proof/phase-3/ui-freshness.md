# Bằng chứng HUD độ tươi (TICKET-03, phần Người 3) — `chonoi/web/index.html`

Ngày 21/11/2026, nhánh `feature/ui-freshness-p3`. Chrome, khung vẽ ép 1280×720.

**Bản chạy v1.2:** ghép tạm cục bộ nhánh này với PR #20 (kho cá thể, độ tươi). Bản ghép không đẩy lên. #17 xung đột với #20 nên chưa ghép được; vì vậy chưa có Cá Sấu.

| Kiểm | Cách chạy | Kết quả |
|---|---|---|
| `/state` có ngưỡng ươn (ADR-0004) | `curl /state` | `freshness: {initial:100, gather_decay_per_s:0.5, quan_decay_per_s:0.25, spoiled_below:30}`; ở v1.1 là `null` |
| Giỏ: độ tươi từng ô, hàng ươn | `live --mode gather --scenario ui-fixtures/gather-hold-v12.json` (I1 100, I2 62, I3 30.5, I4 20) | Thanh độ tươi dưới mỗi ô; I3 và I4 tô xám, gạch đỏ; dòng đếm "bông súng ×1 (ươn 1) · cá linh ×2 · cá lóc ×1 (ươn 1)" ([ảnh](ui-freshness-gather.jpg)) |
| Event `spoiled` → thông báo | Bấm R chơi lại; I3 qua ngưỡng sau khoảng 1 s | Hiện "🥀 I3 bông súng đã ươn (giỏ)"; mở trang mới thì không hiện lại event cũ |
| Quán: kho khả dụng theo id, độ tươi, hàng ươn | `live --mode quan --scenario ui-fixtures/quan-stock-v12.json` | C1 giữ I3, C2 giữ I1 và I2, I4 và I5 đã ươn → "Kho khả dụng: (hết)"; dòng "Độ tươi: bông súng ≥63 · cá lóc ≥81 · 🥀 Ươn: bông súng ×1 · cá linh ×1" |
| Giá chốt theo tươi | Nấu đơn C1 ở B2 | Bếp hiện "Cá lóc nướng trui · 47k" (giá niêm yết 60, `base_price` 47 theo snapshot) ([ảnh](ui-freshness-quan.jpg)) |
| Không làm hỏng v1.1 | `main` + nhánh này (v1.1): `live --mode quan --inventory docs/contracts/inventory.sample.json`; `live --mode day` | Kho khả dụng v1.1 = `{bong_sung:2, ca_loc:0}` (C1 giữ cá lóc); EveningIntro đúng; không lỗi console |
| Logic adapter | node, snapshot giả | v1.1 trừ `reserved`; v1.2 bỏ hàng ươn và hàng đang giữ; ngưỡng `< 30` là ươn, đúng `30` thì chưa |
| Headless không đổi | `cmp` JSONL `gather`/`quan` (seed 1, 600 tick), `day` (3000 tick) trước và sau | Giống từng byte |
| Test | `PYTHONPATH=tests:. python3 -m unittest discover -s tests` | Nhánh này (v1.1): OK. Bản ghép với #20 (v1.2): OK |

Chưa kiểm: vòng `day` v1.2 đầy đủ (Shop) và bản có Cá Sấu (#17 cần gộp với #20 trước).
