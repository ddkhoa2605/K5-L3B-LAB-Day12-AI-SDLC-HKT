# Kế hoạch Phase 2 (≤ 1 trang) — TICKET-02 "Một ngày ở chợ nổi"

Hạn tag `phase-2`: 1:55 (55 phút). Hợp đồng: v1.1 (`docs/contracts/contract.md`, phụ lục v1.1).

## Mục tiêu
Số chuẩn v1.1; vòng ngày `gather → quan → Shop` trong `--mode day` (D1–D5); Cá Sấu/Máu/ngất; 2 bếp/4 bàn/6 món; pause, menu, HUD; smoke tích hợp; regression P1.

## Việc / người / phụ thuộc (AC nháp, PO chốt)
| AC | Nội dung | Người | Phụ thuộc |
|---|---|---|---|
| AC-P2-01 | `game.contract.json` v1.1 phần `quan`, `menu`, `day_plan` | 2 | — (PR #5) |
| AC-P2-02 | Kind `ca_keo`, `keo_neo` (ADR-0001) | 2 | — (PR #4) |
| AC-P2-03 | Quán 2 bếp/4 bàn/6 món, lịch khách, lọc theo kế hoạch Ngày | 2 | AC-P2-01/02 |
| AC-P2-04 | Hợp đồng v1.1 (CLI, input, scenario day, event) | 2 | PR #1 |
| AC-P2-05 | Gather: số chuẩn, kèo/N5-N6, cá bơi + sinh | 1 | AC-P2-04 |
| AC-P2-06 | Cá Sấu, Máu, ngất, `monster_hit` | 1 | AC-P2-05 |
| AC-P2-07 | `--mode day`: vòng ngày, `day_plan`, Shop, nâng cấp, `--days`, pause | 3 (cùng 4) | AC-P2-03/05 |
| AC-P2-08 | Menu, pause, HUD sáng/tối theo ticket | 3 | AC-P2-07 |
| AC-P2-09 | Smoke tích hợp gather → quan (phút 20), `day --days 1`, nhiều Ngày, regression P1; `verification/phase-2.md` | 4 | tất cả |
| AC-P2-10 | Tag `phase-2` ≤ 1:55; retro | 2 | AC-P2-09 |

Nhịp: 0–5 chốt giao diện chuyển pha · 5–20 build 4 lát, hợp đồng v1.1 · 20 smoke + standup · 20–35 build tiếp, chốt luồng day · 35–45 smoke day/nhiều Ngày/regression, verification, tag · 45–50 retro · 50–55 dự phòng.

## Rủi ro
- **Lát 4 (`day`, Shop, pause, HUD) lớn nhất và chưa có người nhận rõ** — cần chốt ngay phút 0–5.
- `gather.py` Phase 1 vẫn chưa xong → chặn AC-P2-05/06/07; ưu tiên merge PR của Người 1.
- Cả nhóm cùng sửa `game.contract.json` → xung đột dòng; Integrator giải quyết khi merge.
- 5 PR Phase 1–2 của Người 2 chưa merge (cần review); PR #5 xếp chồng lên #2 và #4.
