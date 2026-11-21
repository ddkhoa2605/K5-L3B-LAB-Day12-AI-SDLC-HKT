# Day 12 — AI SDLC: Quán Ăn Chợ Nổi

> **Làm theo nhóm 4–6 người** · Dùng AI để xây game 2D qua **4 phase** trong **3 giờ**: Út Sen lặn bắt cá, hái rau trên mặt nước rồi tối mở quán phục vụ khách.
> **Yêu cầu từng phase mở đúng mốc giờ tại lab board:** **[Chợ Nổi Lab](https://claude.ai/artifact/E35v787wSx2wDgPTNhMVDg)** (cần đăng nhập claude.ai; có trợ giảng AI cho từng phase).

## Bắt buộc (chỉ có thế)

Cách làm việc kỹ thuật là **tự do** (push thẳng, nhánh + PR, pair, có hay không CI…). Cái bắt buộc:

1. **Một repo chung:** trưởng nhóm **fork** repo này, đặt tên `K5-L3B-LAB-Day12-AI-SDLC-<ten-nhom>`, thêm mọi thành viên làm collaborator (*Settings → Collaborators*, quyền Write) và để repo **public** (giảng viên xem được, không cần mời).
2. **Cả nhóm cùng commit** bằng tài khoản GitHub của mình, mỗi người **≥ 3 commit có nội dung** (làm cặp thì ghi `Co-authored-by:`).
3. **Điền [`TEAM.md`](TEAM.md):** danh sách thành viên + thỏa thuận làm việc nhóm; sửa `team_size` trong [`game.contract.json`](game.contract.json). Commit của người không có trong `TEAM.md` không được tính.
4. **Gắn tag** `phase-1` … `phase-4` đúng hạn; chạy được tại từng tag.
5. **Ghi chép tối thiểu:** `docs/verification/phase-n.md`, `docs/clarify.md`, `docs/ai-usage-log.md`, `docs/retro.md`, `docs/members/<handle>.md`.

## Bắt đầu nhanh

```bash
git clone <fork-của-nhóm> && cd <fork-của-nhóm>
PYTHONPATH=tests:. python3 -m unittest discover -s tests -v        # smoke test
python3 -m chonoi.live --mode gather                                # chơi thử trên trình duyệt (tùy chọn)
```

Game cần chế độ **headless** theo Test Contract (`python3 -m chonoi.headless --mode gather|quan …`) để được chạy và chấm tự động. **Công nghệ không ràng buộc**: khung Python trong `chonoi/` chỉ là gợi ý, chi tiết ở [`docs/STARTER.md`](docs/STARTER.md).

## Tự do sáng tạo

Ngoài phần đề yêu cầu, nhóm được **thêm** nhân vật, loài cá/cây, sinh vật, món, bản đồ, cơ chế, câu chuyện, đồ họa, âm nhạc… với ba điều kiện: **không phá phần cố định** (tắt ở headless), ghi mục **"Sáng tạo của nhóm"** trong README của nhóm, và **làm lõi đúng trước**.

## Lịch 3 giờ

| Mốc | Phase | Hạn tag |
|---|---|---|
| 0:00 | Phase 1 (PRD-0) | `phase-1` trước 1:00 |
| 1:00 | Phase 2 | `phase-2` trước 1:55 |
| 1:55 | Phase 3 | `phase-3` trước 2:30 |
| 2:30 | Phase 4 | `phase-4` + Release `v1.0.0` trước 3:00 |

Hết giờ mỗi phase thì gắn tag rồi đi tiếp; chỗ chưa xong ghi trung thực trong bằng chứng.

## Đánh giá (100 điểm)

| Hạng mục | Điểm |
|---|---|
| Test tự động ẩn (headless, gồm kiểm tra lại phase trước) | 25 |
| Làm việc nhóm (một repo chung, chia việc, tích hợp, đổi yêu cầu) | 25 |
| Kiểm chứng & bằng chứng | 15 |
| Harness AI (AGENTS.md, skill, nhật ký dùng AI) | 10 |
| Đánh giá & retro | 10 |
| Chất lượng sản phẩm (đúng yêu cầu, mở rộng/sáng tạo) | 10 |
| Demo | 5 |

## Quy định

- Dùng AI thoải mái; **không sao chép repo của nhóm khác**; bằng chứng phải thật.
- Nhân vật, bối cảnh là bản gốc của lab; asset ngoài chỉ dùng CC0/CC-BY/MIT hoặc tự tạo, ghi nguồn trong `CREDITS.md`. Không commit API key, token, `.env`.

## Giao diện (client trên trình duyệt) — nhóm HKT

Yêu cầu: Python 3 (chỉ thư viện chuẩn) và một trình duyệt. Benchmark cần thêm Chrome hoặc Chromium.

```bash
python3 -m chonoi.live --mode day --days 5      # cả vòng ngày (menu, sáng, tối, Shop); mở địa chỉ được in ra
python3 -m chonoi.live --mode gather            # chỉ buổi sáng · --mode quan --inventory kho.json: chỉ buổi tối
python3 tools/bench.py --seed 42 --duration 30 --out bench.json   # benchmark có render (Chrome headless 1280×720)
```

| Phím | Tác dụng |
|---|---|
| WASD / mũi tên | Bơi (sáng) · đi (tối) |
| E | Cập bến, hái (sáng) · nấu, bưng, phục vụ (tối) |
| Space | Bắt cá khi lặn |
| Esc / P | Tạm dừng (Enter: tiếp tục · M: về menu) |
| 1 / 2 / Enter (Shop) | Mua Bình oxy / Áo phao / xong |
| H | Bật/tắt tương phản cao (nhớ giữa các lần mở) |
| F3 | Bật/tắt bộ đếm FPS |
| N | Bật/tắt âm thanh (nhớ giữa các lần mở) |
| J | Mở/đóng sổ tay (thành tựu + thống kê buổi) |
| R | Chơi lại |

- **Cảnh báo:** "Thủy quái Năm Chèo ở gần!" kèm viền tím, "Sắp hết oxy! Ngoi lên thở" (thêm tiếng tim đập), "Khách … sắp giận bỏ về!" (khách nổi gân giận, bong bóng viền đỏ có dấu "!"). Tất cả vẽ bằng canvas, không dùng emoji. Hàng ươn (độ tươi dưới ngưỡng `freshness.spoiled_below`) tô xám, có gạch, ghi "ươn".
- **Benchmark:** ghi `avg_fps`, `p1_low_fps`, `frames`, `measured_s`, `load_ms` (ADR-0005). Kết quả đã chạy: [`docs/proof/phase-4/bench.json`](docs/proof/phase-4/bench.json).
- Chi tiết hợp đồng sim ↔ UI ở `docs/contracts/ui-interface.md`.

## Sáng tạo của nhóm

Mọi phần dưới đây **chỉ chạy trong client trình duyệt** (`chonoi/web/index.html`): không đổi luật, không đổi snapshot/JSONL, không đọc ghi `game.contract.json`, nên headless và Test Contract không bị ảnh hưởng.

- **Đồ họa vẽ tay bằng canvas** (không dùng ảnh/emoji): quán nhà bè ban đêm (sàn ván, mái lá, đèn lồng, bếp cà ràng, bàn trải khăn caro, 6 kiểu thực khách miền Tây có biểu cảm chờ / sốt ruột / giận / đang ăn), cảnh lặn sông có camera bám Út Sen và nền parallax (bờ xa có chùa, nhà sàn, ghe chợ nổi; đáy sông có lu sành, xác ghe).
- **Bầy cá theo sản lượng:** mỗi con cá trên sim được vẽ thành một bầy đúng bằng `meta.fish_yield` (cá linh 3, cá kèo 2, cá lóc 1), có nhãn "Space ×N" khi vào tầm bắt.
- **Sinh vật trang trí, không bắt được:** đàn cá nhỏ hậu cảnh, rùa, cua đồng, ốc bươu, tép, nòng nọc, ếch trên lá súng (nhảy xuống khi Út Sen tới gần), chim bói cá lao xuống bắt cá, chuồn chuồn.
- **Bản đồ sông nhỏ** và **mũi tên mép màn hình** chỉ Năm Chèo, cá đang cần và bến (kèm khoảng cách).
- **Hiệu ứng:** icon bay vào giỏ + "+N" khi bắt/hái, rung màn hình và chớp đỏ khi bị Năm Chèo táp, trời chuyển từ bình minh sang buổi sáng theo đồng hồ ca lặn, càng sâu càng tối.
- **Âm thanh tổng hợp bằng WebAudio** (không có file âm thanh): bắt cá, hái, chuông món chín, tiền, khách bỏ về, tim đập khi sắp hết oxy. Tắt ở chế độ `?bench`.
- **Hoạt cảnh quán:** khách đi bộ từ bến vào ghế và ra về (vui thì thả tim, giận thì bốc khói); thỉnh thoảng có Cậu Vàng vào xin ăn (Út Sen lại gần thì nó mừng), idol mạng kéo fan vào check-in, thằng phá quán đá ghế rồi bị công an tới còng tay dẫn đi. Toàn bộ chỉ là hình ảnh: không đổi tiền, uy tín hay snapshot.
- **Thành tựu + sổ tay (phím J):** 9 thành tựu lưu trong `localStorage` của trình duyệt (ví dụ "Mẻ lưới đầu tiên", "Thoát hàm Năm Chèo", "Quán đắt khách").
