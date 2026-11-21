# Ma trận truy vết Phase 3 (phần của Người 2: schema kho, Quán, day, hợp đồng; ghi trung thực)

> Chạy trên nhánh `feature/reservations` (xếp chồng #20 lõi → #21 đặt trước; hợp đồng/ADR ở #19). **Chưa merge vào `main`, chưa gắn tag `phase-3`.** Khi merge xong, QA chạy lại trên commit bàn giao rồi cập nhật cột kết quả.
> Bằng chứng: `docs/proof/phase-3/` (`unittest.txt` 168 test OK trước mở rộng; `unittest-reservations.txt` 188 test OK; `integration.txt`).

| AC | Cách kiểm chứng | Bằng chứng | Kết quả |
|---|---|---|---|
| AC-P3-01 Kho cá thể qua file; kho đếm / sai schema / kind lạ / id trùng / fresh ngoài miền → mã 2 | `tests/test_smoke_p1.py::Integration`, `tests/test_freshness.py` (schema, scenario) | `integration.txt` mục 3 (mã 2, không tạo file) | **Đạt trên nhánh** |
| AC-P3-02 Độ tươi: hao gather 0.5/s, quán 0.25/s (kể cả hàng giữ), kẹp 0, pause dừng hao, món chín không hao | `tests/test_freshness.py::GatherDecay`, `::QuanDecayAndReserve`, `::CookPrice` | `unittest.txt` | **Đạt** |
| AC-P3-03 Ươn `fresh<30`: không dùng nấu, `spoiled` đúng một lần theo id, so ngưỡng trước làm tròn | cùng file (ví dụ ticket `fresh:30` → tick 1; ca `7202` đơn vị → tick 2) | `integration.txt` mục 1 | **Đạt** |
| AC-P3-04 Giữ theo id (tươi nhất, hòa id), vừa ươn → nhả hết và giữ lại đúng một lần theo `order_tick`/id bàn, thiếu → `unfulfillable` | `tests/test_freshness.py::QuanDecayAndReserve` | `unittest.txt` | **Đạt** |
| AC-P3-05 Giá theo tươi `floor(giá × TB fresh/100)`; boa trên giá đã chốt | `::CookPrice`, `tests/test_quan*.py` | `unittest.txt` | **Đạt** (giá ở bước đầu của ca là 59, không 60: xem `clarify.md` #28) |
| AC-P3-06 Bàn giao gather → quán (file) và `day`: id/kind/fresh khớp, không hao thêm ở tick chuyển pha, Shop không hao, id tăng xuyên Ngày | `tests/test_smoke_p1.py`, `::DayHandover` | `integration.txt` mục 2 và 4 (`cmp` hai lần giống byte, Ngày 2 id `I4,I5,I6`) | **Đạt** với gather khung + adapter |
| AC-P3-07 JSONL theo schema mới: `hold`, `stock`, `reserved`, `cook_started.items`, `lost` (LIFO), `gather_end.inventory` | các test trên | `unittest.txt` | **Đạt một phần**: `lost` trong `faint` do ngạt đạt; **`monster_hit.lost` chưa có** (thủy quái thuộc gather v1.1, Người 1) |
| AC-P3-08 HUD cho người chơi đọc độ tươi / nhận ra hàng ươn | — | — | **Chưa đạt / chưa làm** (Người 3; ngoài phạm vi Người 2). Snapshot đã đủ trường (`hold[].fresh`, `stock[].fresh`) |
| AC-P3-09 Ghi tác động, quyết định đổi schema, thứ tự tích hợp, CHANGELOG | `docs/adr/0003-…`, `docs/contracts/contract.md` (phụ lục v1.2), `CHANGELOG.md` | PR #19, #20 | **Đạt trên nhánh**; PR #19 cần 2 approvals, chưa review |
| AC-P3-10 Regression P1–P2 còn hiệu lực; test đổi có lý do | toàn bộ test đã migrate | `unittest-reservations.txt` (188 OK), `CHANGELOG.md` mục "Test thay đổi" | **Đạt** |
| AC-P3-11 Tag `phase-3` ≤ 2:30 | `git show phase-3` | — | **Chưa đạt** (chưa merge, thiếu HUD) |

## Mở rộng
| Mục | Kết quả |
|---|---|
| **Khách đặt trước** (`reservations`) | **Đạt** về luật: `tests/test_reservations.py` (20 test: sinh tất định, giữ bàn, đến giờ, fail occupied/stock/patience/closing/burnt, giá ×1.5 rồi boa, uy tín −1 một lần, day công bố sau `phase_start(gather)`). **Chưa**: HUD sáng "hiện hai đơn" (Người 3). Bật mặc định trong manifest → fixture lõi cần `random_reservations:false` |
| **Dòng nước lũ** (`current`) | **Không làm** (Lặn, Người 1; nhóm 4 người không bắt buộc). Đã đặc tả trong hợp đồng v1.2 mục F để giao |

## Sai khác / giả định cần xác nhận
- `docs/clarify.md` #24–#31 (thứ tự `spoiled`/`node_regrown`, sắp snapshot theo id, adapter gather, `monsters:[]`, giá 59, stream đặt trước).
- Ví dụ ticket có `"monsters":[]`: scenario gather chỉ nhận mảng rỗng.
- Adapter gather (hao tươi, `spoiled`, `lost`) do Người 2 viết tối thiểu trong commit riêng; Người 1 cần duyệt.
- Chưa chạy lại với gather v1.1 của Người 1 (cá bơi/sinh, Cá Sấu, dòng lũ) vì chưa có.

## Đánh giá ngắn
- **Đạt:** lõi kho cá thể + độ tươi (file, Quán, day), giữ theo id, giá theo tươi, tất định, ghi tác động/CHANGELOG, mở rộng đặt trước.
- **Chưa đạt:** HUD độ tươi (Người 3), `monster_hit.lost`/thủy quái và dòng lũ (Người 1), chưa merge, chưa tag; PR #19 chưa đủ 2 approvals.
- **Cần chỉnh cho phase sau:** merge theo thứ tự #19 → #20 → #21; Người 1 duyệt commit adapter gather rồi rebase gather v1.1; Người 3 làm HUD độ tươi + hai đơn đặt trước; QA chạy `day --days 5` và đo thời gian một Ngày.
