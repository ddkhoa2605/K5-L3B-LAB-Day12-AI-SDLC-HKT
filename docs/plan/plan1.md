# PLAN 1 – Người 1: `sim/gather` + PO (Cập nhật Phase 3)

> Đặt tại `docs/plan/plan1.md`. Kế hoạch tổng thể: `docs/plan/plan.md`.
> **Nguồn:** TICKET-03 "Mùa Nước Nổi" (lab board, phát hành 10:59), Test Contract v1.2. **Hạn tag `phase-3`:** trước **2:30** (35 phút).

---

## 1. Vai trò của Người 1
- **Module chính:** [chonoi/sim/gather.py](../../chonoi/sim/gather.py); vai **PO** (giữ [docs/clarify.md](../clarify.md)).
- **Reviewer chính của:** Người 2 (`sim/quan`). Dự phòng cho Người 2.
- **Phụ trách AC (phần Gather của TICKET-03):** **AC-P3-01** — kho cá thể, độ tươi, ươn, bàn giao kho phía Gather.
- **Ngoài phạm vi Người 1:** hao tươi kho quán 0.25/s, giữ chỗ theo id, giá theo tươi, đặt trước, `day` (Người 2); HUD độ tươi (Người 3); `CHANGELOG.md`, smoke/regression tổng (Người 4 + Integrator).

## 2. Hiện trạng đầu Phase 3
- Phase 2 Gather (AC-P2-05/06) đạt, 116 test xanh. **Chưa commit/push, chưa merge vào `main`** (xem mục 6, việc đầu tiên).

## 3. Việc Phase 3 của Người 1 (AC-P3-01)

| # | Việc | File | Trạng thái |
|---|---|---|---|
| 1 | Kho cá thể `{id,kind,fresh}`; id `I1,I2…` cấp theo thứ tự vào giỏ, nối tiếp cả khi dùng/bỏ; LIFO theo thứ tự vào giỏ | `chonoi/sim/gather.py` | Xong |
| 2 | Hao tươi 0.5/s (2 đơn vị/tick, 240 đơn vị/điểm), hàng mới = 100 và hao từ bước sau, kẹp đáy 0 | `gather.py` | Xong |
| 3 | Ươn `fresh < 30`: vẫn chiếm ô; `spoiled{item_id,kind,location:"hold"}` đúng một lần, theo id, so ngưỡng trước làm tròn | `gather.py` | Xong |
| 4 | `lost` (monster_hit/faint), `gather_end.inventory`, snapshot `hold` theo schema cá thể; ngất → kho rỗng | `gather.py` | Xong |
| 5 | File kho v1.2: `read_inventory_v12`, `write_inventory` nhận mảng cá thể, nguyên tử, sắp theo id, số nguyên khi tròn (100, 97.5) | `chonoi/inventory.py` | Xong (thay đổi cộng thêm, báo Người 2) |
| 6 | Kiểm `gather.hold` mảng cá thể (id trùng/rỗng, kind lạ, fresh ngoài [0,100] → mã 2) và khối `freshness` | `scenario.py`, `contract.py` | Xong |
| 7 | Công tắc tương thích: có `tuning.freshness` → v1.2; không có → v1.1 y nguyên (kho đếm, không hao) để `main` vẫn chạy | `gather.py` | Xong |
| 8 | Test, bằng chứng, `docs/verification/phase-3.md`, `clarify.md`, `ai-usage-log.md` | `tests/test_gather_p3.py`, `docs/proof/phase-3/` | Xong |
| 9 | **Bật v1.2 trong manifest** (`contract_version:"1.2"` + `freshness`) | `game.contract.json` | **Chờ Người 2** (quán/day đọc kho cá thể) |
| 10 | Smoke `gather --inventory-out` → `quan --inventory` ở v1.2 (id/kind/fresh khớp sau lần hao ở bước gather) | `docs/proof/phase-3/` | **Chờ #9** |
| 11 | Mở rộng Dòng nước lũ (`current`) | — | Không làm (không bắt buộc nhóm 4 người) |

### Thứ tự một bước Gather v1.2 (phần đã cài)
Đồng hồ, cooldown, hồi nút → **hao tươi hàng có sẵn, phát `spoiled` theo id** → bơi, oxy, ngạt → Cá Sấu/hit (LIFO) → bến trước hái → bắt cá → hết giờ → cá bơi/sinh. Hàng vừa hái/bắt chưa hao trong bước đó.

## 4. Tiêu chuẩn nghiệm thu

| AC | Yêu cầu | Kiểm chứng | Kết quả |
|---|---|---|---|
| AC-P3-01 | Gather v1.2: hao 0.5/s, ươn <30 (`spoiled` một lần, theo id), kho cá thể, `lost`/`gather_end`/snapshot theo schema, file kho nguyên tử đọc lại giữ nhánh ở 30, kho đếm/sai schema → mã 2 | `tests/test_gather_p3.py` (21 test), [smoke](../proof/phase-3/smoke_gather_v12.txt) | Đạt phần Gather; tích hợp quán chờ #9–#10 |
| Hồi quy | P1–P2 còn hiệu lực | 137/137 test ([unittest.txt](../proof/phase-3/unittest.txt)) | Đạt |

## 5. Kế hoạch thời gian (35 phút)
- **0–7':** phân tích tác động (bảng dưới), chốt công tắc `freshness`, báo Người 2 thay đổi `inventory.py`.
- **7–25':** cài Gather + adapter file + test (xong). Phút 20: smoke kho cùng Người 2.
- **25–32':** khi quán sẵn sàng, bật v1.2 trong manifest (Integrator), chạy smoke hai tiến trình + `day`, regression, bằng chứng.
- **32–35':** dự phòng; Người 2 gắn `phase-3`.

| Module | File đổi | Test | Người |
|---|---|---|---|
| Gather | `chonoi/sim/gather.py` | thêm `test_gather_p3.py`; giữ `test_gather_lat*`, `test_gather_p2` | Người 1 |
| Adapter file kho | `chonoi/inventory.py` (thêm `read_inventory_v12`, `write_inventory` nhận mảng) | `test_gather_p3.py` | Người 1 → Người 2 duyệt |
| Scenario/contract | `chonoi/scenario.py`, `chonoi/contract.py` | `test_gather_p3.py` | Người 1 |
| Quán, day, headless đọc kho | `quan.py`, `day.py`, `headless.py` | test quán/day | Người 2 |
| HUD | `chonoi/web/` | thủ công | Người 3 |

## 6. Việc cần làm ngay / rủi ro
1. **Commit + push `feature/gather-p2` rồi mở PR vào `main`** (Phase 2 và 3 cùng nằm trên nhánh, chưa lên `main`; merge `origin/main` sẽ xung đột `docs/clarify.md`, giữ cả hai bên). Chạy lại test sau merge vì `main` có thêm `test_day.py`, `test_burn.py`.
2. `inventory.py` là file dùng chung: thay đổi chỉ cộng thêm, nhưng cần Người 2 duyệt.
3. Không bật `contract_version:"1.2"` khi quán/day còn đọc kho đếm; sau khi bật, mọi fixture kho đếm trong test cũ phải đổi và ghi lý do vào `CHANGELOG.md`.
4. Mở rộng `current` và đặt trước không làm; ghi trung thực trong `docs/verification/phase-3.md`.

## 7. Ghi chú PO
- `docs/clarify.md` mục 19–22: công tắc `freshness`, hao từ bước sau, đơn vị 240/điểm, mở rộng không bắt buộc.
- Nhật ký AI: `docs/ai-usage-log.md` (dòng Phase 3, Người 1).
