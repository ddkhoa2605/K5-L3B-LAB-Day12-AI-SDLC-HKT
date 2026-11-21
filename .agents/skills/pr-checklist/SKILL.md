---
name: pr-checklist
description: Kiểm PR của nhóm trước khi mở hoặc trước khi duyệt (Day 12 AI SDLC). Dùng khi tác giả sắp mở PR, hoặc reviewer sắp approve/merge. Soát liên kết issue, phạm vi, AC, hard-code, tính tất định, hợp đồng, bằng chứng và nhận xét theo dòng.
---

# pr-checklist

Người phụ trách: Người 2 (Integrator). Dùng **trước khi mở PR** (tác giả) và **trước khi merge** (reviewer). Chỉ đọc và báo cáo; không tự sửa code hay hợp đồng.

## Cách chạy
1. Xác định phạm vi: `git diff --stat origin/main...HEAD` (tác giả) hoặc `gh pr diff <số>` (reviewer).
2. Chạy test: `PYTHONPATH=tests:. python3 -m unittest discover -s tests`.
3. Nếu đụng `quan`/`gather`: chạy headless hai lần cùng seed rồi `cmp`
   (`python3 -m chonoi.headless --mode <gather|quan> --seed 1 --ticks 600 --out a.jsonl`, lặp với `b.jsonl`, `cmp a.jsonl b.jsonl`).
4. Soát từng mục dưới đây; mỗi mục trả **ĐẠT / CHƯA ĐẠT / KHÔNG ÁP DỤNG** kèm `file:dòng` khi chưa đạt.

## Checklist

**Mô tả PR** (`.github/pull_request_template.md`)
- [ ] `Closes #<issue>`, Phase, Module (`gather|quan|ui|qa|content|contracts`) đã điền.
- [ ] Danh sách AC (`AC-P<n>-<xx>`) đã tick đúng với phần đã làm.
- [ ] Bằng chứng là lệnh + đầu ra thật hoặc đường dẫn `docs/proof/phase-n/...`.
- [ ] Ghi phần AI đã làm: agent, prompt chính, phần người đã đọc và sửa.
- [ ] Ghi rủi ro / việc chưa làm trung thực.

**Phạm vi**
- [ ] Một việc một PR, ≤ ~400 dòng (kể cả test); vượt thì ghi lý do hoặc tách.
- [ ] Đúng branch quy ước (`feature/<module>-<task>`, `test/`, `docs/`, `content/`).
- [ ] Không push thẳng `main`; không tắt/bypass CI.

**Luật và dữ liệu**
- [ ] Không hard-code số chuẩn: thời lượng, vị trí, giá, boa, uy tín… phải đọc từ `game.contract.json`.
- [ ] Ngẫu nhiên chỉ qua `Streams`; không `import random`, không `time`/`datetime` làm logic.
- [ ] Thực thể sắp bằng `ids.sort_by_id`; id mới cấp bằng `IdAllocator`.
- [ ] Output tất định: `cmp` hai lần chạy cùng seed giống từng byte.
- [ ] Phần sáng tạo (nếu có) tắt ở headless và không đổi output chuẩn.

**Hợp đồng và khung**
- [ ] Không đổi `docs/contracts/`, khóa trong `game.contract.json`, schema kho. Nếu có: cần **2 approvals** và ghi lý do.
- [ ] Không sửa module khung (`headless, inputs, contract, rng, ids, jsonl, inventory, runner, live`, `chonoi/web/`) trừ PR riêng + ADR (`docs/adr/`). `scenario.py` xem `docs/clarify.md` #1.
- [ ] Tên và payload event khớp `docs/contracts/contract.md`.

**Test**
- [ ] Có test cho luật mới; test chạy xanh.
- [ ] Không sửa test cho xanh khi luật sai; nếu sửa test thì PR giải thích vì sao.
- [ ] Không có key/token/`.env`; asset ngoài có ghi nguồn trong `CREDITS.md`.

**Review (chỉ khi duyệt)**
- [ ] Người duyệt khác tác giả; ≥ 1 approval (2 nếu đụng contract/schema).
- [ ] Nhận xét **bám dòng cụ thể của diff**, không chỉ "LGTM".
- [ ] `ci / test` xanh.

## Mẫu báo cáo
```
pr-checklist: PR #<số> — <ĐẠT n/N>
CHƯA ĐẠT:
- <mục> — <file:dòng> — <vì sao / cách sửa>
Lệnh đã chạy: <lệnh> -> <kết quả thật>
```
Không nêu kết quả chưa chạy. Mục không kiểm được thì ghi rõ "chưa kiểm".
