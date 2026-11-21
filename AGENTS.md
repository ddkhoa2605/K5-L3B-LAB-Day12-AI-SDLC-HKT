# AGENTS.md — hướng dẫn chung cho mọi agent AI của nhóm

> Cập nhật file này qua các phase (lịch sử git phải cho thấy điều đó). Ngắn gọn, có lệnh chạy thật.

## Lệnh
- Test: `PYTHONPATH=tests:. python3 -m unittest discover -s tests -v`
- Headless: `python3 -m chonoi.headless --mode gather|quan|day --seed 1 --ticks 600 --out out.jsonl` (`day` thêm `--days 1..5`; scenario `--scenario`, input `--inputs`; kho file chỉ ở gather/quan: `--inventory-out`, `--inventory`)
- Chơi trên trình duyệt: `python3 -m chonoi.live --mode day --days 5` (hoặc `gather` / `quan`); mở địa chỉ in ra; WASD, E, Space, Esc/P tạm dừng, R chơi lại, F3 xem FPS. Windows: đặt `PYTHONIOENCODING=utf-8`.
- Kiểm tất định: `python3 tools/check_determinism.py --mode gather|quan` · smoke hai tiến trình: `python3 tools/smoke_integration.py` · thành viên: `python3 tools/check_team.py`
- Contract v1.3: `bench_cmd` = `python3 tools/bench.py --seed 42 --duration 30 --out bench.json` (cần Chrome), `soak_cmd` = `python3 tools/soak.py --seed 7 --days 10 --out soak.json`

## Cấu trúc & quy ước
- (Starter Python là TÙY CHỌN; nhóm có thể dùng ngôn ngữ khác nếu giữ Test Contract.) Khung do giảng viên cấp: `chonoi/{headless,inputs,scenario,contract,rng,ids,jsonl,inventory,runner,live}.py` và `chonoi/web/`. Hạn chế sửa; nếu phải sửa thì báo cả nhóm và ghi lại lý do.
- Luật chơi của nhóm: `chonoi/sim/gather.py`, `chonoi/sim/quan.py`; vòng ngày `chonoi/day.py`, tạm dừng `chonoi/pause.py`, độ tươi `chonoi/freshness.py`. Không còn `TODO(nhóm)`.
- **Kho là kho CÁ THỂ (contract v1.2):** file kho `{"items":[{"id","kind","fresh"}]}`; kho đếm kiểu cũ trả mã 2. Độ tươi tính bằng số nguyên 240 đơn vị/điểm, ươn khi `fresh < 30`; id cá thể `I1, I2…` cấp bằng `IdAllocator`, tăng xuyên pha và Ngày.
- Mở rộng bật trong manifest (`extensions`): `reservations` (Khách đặt trước), `burn` (cháy món, tắt khi `burn_s: null`). Fixture muốn "lõi thuần" đặt `random_reservations: false`.
- Sửa module khung (`inventory, contract, headless, runner, live, inputs`) cần PR riêng + ADR (`docs/adr/`, hiện 0001–0005).
- **Số liệu chỉ đọc từ `game.contract.json` / dữ liệu**, không hard-code trong luật.
- Mọi số ngẫu nhiên đi qua `Streams` (`chonoi/rng.py`); không dùng `random` toàn cục, không dùng đồng hồ hệ thống.
- Sắp danh sách thực thể bằng `ids.sort_by_id`; cấp id bằng `IdAllocator`.

## Nên tránh
- Không sửa `docs/contracts/`, `game.contract.json` (khóa contract) hoặc schema kho khi chưa báo cả nhóm (đổi hợp đồng ảnh hưởng mọi module).
- Không làm hỏng nhánh chính: trước khi đẩy, chạy test. Không đẩy thẳng `main`; gắn tag `phase-n` đúng mốc.
- Không bịa yêu cầu: chỗ mơ hồ thì ghi `docs/clarify.md` và hỏi PO.
- Không sửa test cho xanh khi luật sai; phải sửa luật hoặc ghi lý do đổi test trong commit.

## Quy tắc làm việc với agent
- Mỗi agent một việc rõ ràng (một lát). Cho agent đọc PRD/ticket đúng phase và hợp đồng kho trước.
- Agent làm xong phải chạy test và ghi kết quả vào mô tả commit hoặc `docs/proof/`; người đọc lại thay đổi trước khi đẩy.
- Sáng tạo thêm được khuyến khích nhưng phải tắt ở headless (xem README, mục "Tự do sáng tạo").

## Skills / hooks của nhóm
- `pr-checklist` (`.agents/skills/pr-checklist/SKILL.md`, Người 2): dùng **trước khi mở PR** (tác giả) và **trước khi merge** (reviewer) để soát Closes #, phạm vi ≤ ~400 dòng, AC, hard-code/RNG/tất định, hợp đồng, test và nhận xét theo dòng.
- `determinism-check` (`.agents/skills/determinism-check/SKILL.md`, Người 4): chạy headless hai lần cùng seed rồi so SHA256/`cmp` cho `gather` và `quan` (`python3 tools/check_determinism.py --mode gather|quan`); dùng sau mỗi PR merge vào `main` và trước mỗi tag.
- Hợp đồng tích hợp của nhóm: `docs/contracts/contract.md` (khóa, đổi cần 2 approvals).
