# Bằng chứng HUD Phase 2 (AC-P2-08) — `chonoi/web/index.html`

Chạy trên Chrome (macOS), khung vẽ ép về **1280×720** (cửa sổ thật 1512×765, `innerWidth/innerHeight` ghi đè thành 1280×720 để kiểm bố cục). Ngày 21/11/2026, nhánh `feature/ui-hud-p2`.

| Kiểm | Cách chạy | Kết quả |
|---|---|---|
| Chữ ≥ 18 px | `text()` kẹp sàn `MIN_FONT = 18`; mọi chữ trên canvas đi qua `text()` | Đạt: không còn chữ < 18 px (đã soát `size:` trong file) |
| FPS ≥ 30 ở 1280×720 | F3 bật bộ đếm (trung bình cửa sổ 1 s) | gather 119–120 FPS, quán 120 FPS (`--mode day` và `--mode quan`) |
| HUD sáng | `python3 -m chonoi.live --mode day --days 1` | Thời gian, oxy (dưới 25% đổi màu + nhấp nháy), Máu, độ sâu, đã lấy/cần, giỏ theo loại, gợi ý hái/cập bến hiển thị, không chồng nhau |
| HUD quán | `python3 -m chonoi.live --mode quan --inventory docs/contracts/inventory.sample.json` | Kho khả dụng = stock − reserved (C2 giữ 2 bông súng → "(hết)"); tiền ca; uy tín; món + kiên nhẫn từng bàn; bếp B2 hiện tên món, số giây, rồi "Đã chín!"; món trên tay |
| EveningIntro | Cập bến trong `day` | Nhập kho, món nấu được; dòng "Bấm phím…" nằm trong khung (đã sửa) |
| "Thủy quái!" + viền tím | Gather `main` **chưa có `monsters[]`**: chèn tạm 1 Cá Sấu giả vào `/state` ở trình duyệt (không đụng sim) | `patrol` ở xa: không cảnh báo; `chase`: viền tím + "Thủy quái!" ([ảnh](ui-hud-gather-thuy-quai.jpg)). Cần kiểm lại khi gather v1.1 có `monsters[]` |

Chưa kiểm bằng mắt: màn Shop và Summary (cần chơi hết một Ngày).
