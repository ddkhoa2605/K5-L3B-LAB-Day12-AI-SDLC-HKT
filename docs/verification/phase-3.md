# Ma trận truy vết Phase 3 — phần Gather (Người 1)

> Phần quán/day/HUD/CHANGELOG do Người 2–4 điền vào cùng file khi tích hợp. Bảng dưới chỉ nêu phần Gather.

| AC | Cách kiểm chứng | Bằng chứng | Kết quả |
|---|---|---|---|
| AC-P3-01a Hao tươi gather 0.5/s, hàng mới 100 và hao từ bước sau, kẹp đáy 0 | `test_gather_p3.py` (Freshness) | [unittest.txt](../proof/phase-3/unittest.txt) | Đạt |
| AC-P3-01b Ươn `fresh < 30`: `spoiled` đúng một lần, theo id, so trước làm tròn; ví dụ ticket (fresh 30 → tick 1) | `test_gather_p3.py` (`test_vi_du_ticket…`, `test_nhanh_o_nguong_30_chinh_xac`, `test_nhieu_ca_the…`) | [unittest.txt](../proof/phase-3/unittest.txt) | Đạt |
| AC-P3-01c Kho cá thể: id `I1,I2…` nối tiếp theo thứ tự vào giỏ, hàng ươn vẫn chiếm ô, snapshot `hold` đúng schema | `test_gather_p3.py` (IdsAndSchema) | [unittest.txt](../proof/phase-3/unittest.txt) | Đạt |
| AC-P3-01d `lost` (monster_hit/faint) và `gather_end.inventory` là mảng cá thể; LIFO; ngất → kho rỗng | `test_gather_p3.py` (LossAndEnd) | [unittest.txt](../proof/phase-3/unittest.txt) | Đạt |
| AC-P3-01e File kho v1.2: ghi một lần khi `gather_end`, nguyên tử, sắp theo id, đọc lại giữ nhánh ở 30; kho đếm/sai schema → mã 2; scenario `hold` sai → mã 2 | `test_gather_p3.py` (InventoryFile, IdsAndSchema) | [unittest.txt](../proof/phase-3/unittest.txt), [smoke_gather_v12.txt](../proof/phase-3/smoke_gather_v12.txt) | Đạt |
| Hồi quy P1–P2 Gather | toàn bộ test | [unittest.txt](../proof/phase-3/unittest.txt): 137/137 | Đạt |

## Chưa làm / trung thực
- `game.contract.json` **chưa** đổi sang `contract_version: "1.2"` (Gather bật freshness qua khóa `tuning.freshness`, chưa có trong manifest). Chỉ bật khi quán (`--inventory` kho cá thể, hao 0.25/s, giữ chỗ theo id, giá theo tươi) và `day` của Người 2 sẵn sàng; nếu bật trước, quán đọc sai kho. Smoke hai tiến trình `gather → quan` vì thế **chưa chạy** ở v1.2.
- Mở rộng Dòng nước lũ (`current`) và Khách đặt trước: chưa làm (không bắt buộc nhóm 4 người).
- HUD độ tươi: thuộc Người 3.
