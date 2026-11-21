# ADR-0001: Thêm hai nguyên liệu `ca_keo`, `keo_neo` vào danh sách kind hợp lệ (contract v1.1)

- Trạng thái: đề xuất
- Ngày, người quyết: 2026-11-21, Người 2 (Integrator); cần PO/nhóm xác nhận

## Bối cảnh
TICKET-02 (Phase 2) mục 1.3 thêm hai nguyên liệu `ca_keo` (cá kèo) và `keo_neo` (kèo nèo). `chonoi/inventory.py` là module khung và giới hạn kind ở bốn giá trị của v1.0 (`KINDS_P1`), nên file kho/`hold`/`stock` chứa kind mới bị từ chối bằng mã 2.

## Các lựa chọn đã cân nhắc
1. Sửa hằng số kind trong `inventory.py` (thay đổi 3 dòng, tên cũ giữ nguyên làm alias).
2. Đọc danh sách kind từ `game.contract.json` (đúng tinh thần "số liệu ở dữ liệu" nhưng đụng nhiều chỗ khung: `headless`, `scenario`, `inventory`).
3. Bỏ kiểm kind (làm mất kiểm mâu thuẫn "nguyên liệu lạ → mã 2").

## Quyết định
Chọn 1: mở rộng tuple `KINDS`, giữ `KINDS_P1 = KINDS`. Đủ cho Phase 2; nếu phase sau thêm kind nữa thì cân nhắc phương án 2.

## Hệ quả
| Chỗ | Tác động |
|---|---|
| `chonoi/inventory.py` | `read_inventory`/`validate_items` nhận 6 kind |
| `chonoi/scenario.py` | `gather.hold` nhận `ca_keo`, `keo_neo` (qua `KINDS_P1`) |
| Test | `tests/test_inventory_kinds.py` (kind mới hợp lệ, kind lạ vẫn mã 2) |
| `docs/contracts/contract.md` | mục 1: kind ∈ 6 giá trị từ v1.1 |
