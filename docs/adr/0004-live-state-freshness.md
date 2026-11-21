# ADR-0004: `/state` của `chonoi.live` mang khối `freshness` cho HUD độ tươi

- Trạng thái: đề xuất (cần Người 2 / Integrator duyệt)
- Ngày, người quyết: 2026-11-21, Người 3 (`client/ui`)

## Bối cảnh
TICKET-03 (Test Contract v1.2) yêu cầu HUD cho người chơi đọc được độ tươi hoặc nhận ra hàng ươn. Hàng ươn khi `fresh < freshness.spoiled_below`. Ngưỡng này nằm ở `tuning.freshness` (ADR-0003, PR #19/#20).

`/state` hiện chỉ gửi `meta = tuning[pha]`, tức `gather` hoặc `quan`, nên client không biết ngưỡng. AGENTS.md cấm ghi cứng số liệu, nên client không được tự đặt 30.

## Các lựa chọn đã cân nhắc
1. Thêm khóa `freshness` vào `/state`, lấy nguyên `tuning.freshness` (chọn).
2. Đưa `freshness` vào `meta`. Bị loại vì `meta` hiện là đúng `tuning[pha]`, nên trộn khóa khác vào sẽ làm lẫn ý nghĩa.
3. Client suy ra hàng ươn từ event `spoiled`. Bị loại vì cá thể ươn sẵn từ scenario không phát event, và bộ đệm event chỉ có 40 dòng.
4. Ghi cứng 30 trong client. Vi phạm AGENTS.md.

## Quyết định
`LiveGame.state_json()` thêm `snap["freshness"] = tuning.get("freshness")`. Giá trị là `null` khi manifest chưa khai (v1.0/v1.1).

## Hệ quả
| Module | File | Test | Người |
|---|---|---|---|
| Live (khung) | `chonoi/live.py` (1 dòng) | `tests/test_live.py`: `LiveStateFreshnessTest` (có/không khai) | Người 3 |
| UI | `chonoi/web/index.html` (adapter kho v1.1/v1.2, HUD độ tươi) | kiểm bằng trình duyệt, bằng chứng `docs/proof/phase-3/` | Người 3 |

- Khóa chỉ có ở `/state` của `chonoi.live`. Snapshot JSONL headless **không đổi**; đã kiểm bằng `cmp` output `gather`, `quan`, `day` trước và sau khi sửa.
- Không đổi Test Contract.
