# ADR-0003: Kho cá thể và độ tươi (Test Contract v1.2) — sửa module khung

- Trạng thái: đề xuất (cần PO/nhóm xác nhận)
- Ngày, người quyết: 2026-11-21, Người 2 (Integrator)

## Bối cảnh
TICKET-03 (Phase 3) đổi kho từ **đếm** `{"items": {kind: n}}` sang **cá thể** `{"items": [{id, kind, fresh}]}`, thêm độ tươi (hao, ươn, giữ chỗ theo id, giá theo tươi) và yêu cầu kho đếm trả mã 2 ở v1.2. Khái niệm "kho" nằm ở `inventory.py` (khung), `contract.py` (khung), `headless/runner/live` (khung), cùng `gather.py` (Người 1), `quan.py`, `scenario.py`, `day.py` (Người 2) và gần 90 chỗ trong test.

## Các lựa chọn đã cân nhắc
1. **Cắt thẳng sang v1.2** (chọn): chỉ giữ schema cá thể; test cũ được chuyển sang cá thể; kho đếm → mã 2.
2. Hỗ trợ cả hai theo `contract_version` (adapter đọc kho đếm cho v1.0/v1.1): giữ được fixture cũ nhưng nhiều mã hơn, dễ lệch hai nhánh luật, và không có người dùng v1.0/v1.1 nào sau Phase 3.
3. Giữ kho đếm trong sim và chỉ đổi file: không đạt (giữ theo id, giá theo tươi cần cá thể ngay trong sim).

## Quyết định
Phương án 1. Tính độ tươi bằng **số nguyên** (240 đơn vị/điểm) trong module mới `chonoi/freshness.py` để chính xác ở ngưỡng 30 và phép `floor`. Một `IdAllocator` tiền tố `I` dùng chung gather → quan → Shop → Ngày kế.

## Hệ quả — bảng tác động
| Module | File | Thay đổi | Test | Người |
|---|---|---|---|---|
| Độ tươi (mới) | `chonoi/freshness.py` | đơn vị nguyên, hao, ươn, chọn tươi nhất, giá | `tests/test_freshness.py` | 2 |
| Adapter kho (khung) | `chonoi/inventory.py` | schema cá thể, kho đếm → mã 2, ghi theo id | `test_smoke_p1`, `test_inventory_kinds`, `test_freshness` | 2 |
| Manifest (khung) | `chonoi/contract.py`, `game.contract.json` | `contract_version` 1.2, `tuning.freshness` | `test_burn::ContractExtensions` | 2 |
| Scenario | `chonoi/scenario.py` | `hold`/`stock` mảng cá thể, `reserved` mảng id, kiểm theo id, nhận `monsters:[]` | `test_quan`, `test_freshness` | 2 |
| Quán | `chonoi/sim/quan.py` | giữ theo id, spoiled, giữ lại một lần, giá theo tươi | `test_quan*`, `test_burn`, `test_freshness` | 2 |
| Lặn (adapter tối thiểu) | `chonoi/sim/gather.py` | `hold` cá thể, hao, `spoiled`, `lost`, `gather_end` | `test_gather_lat1/2`, `test_freshness` | 2 → 1 duyệt |
| day | `chonoi/day.py` | allocator chung, id Ngày kế, Shop kho cá thể | `test_day`, `test_freshness` | 2 |
| Giao diện | `chonoi/web/index.html` | HUD độ tươi/ươn | thủ công | **3 (chưa làm)** |

**Thứ tự tích hợp giữ `main` chạy được:** (1) PR docs này (hợp đồng + ADR) → (2) PR lõi, một lượt (commit theo lát: freshness+inventory+manifest → scenario+gather adapter → quan → day → test) → (3) HUD (Người 3) → (4) mở rộng (đặt trước). Không có trạng thái trung gian vì cắt thẳng; mỗi PR phải xanh.
