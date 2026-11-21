# Kế hoạch tổng thể – Day 12 AI SDLC: Quán Ăn Chợ Nổi (bản cập nhật 21/11/2026)

> Đặt tại `docs/plan/plan.md`. Kế hoạch cá nhân: `docs/plan/plan1.md` … `plan4.md`.
> **Không đặt vào `docs/members/`**: thư mục đó dành cho phản tư cá nhân `docs/members/<handle>.md` (≤ 200 từ).

## 0. Tình trạng nguồn yêu cầu (đọc trước)

Bản này đối chiếu với repo `VinUni-AI20k/K5-L3B-LAB-Day12-AI-SDLC` (README mới, `AGENTS.md`, `docs/STARTER.md`, `docs/contracts/README.md`, `docs/plan/phase-1.md`, `docs/verification/phase-1.md`, `docs/members/TEMPLATE.md`, PR template).

- **PRD-0 đã đọc từ lab board (tab Phase 1, 21/11/2026)** và tóm tắt ở `docs/plan/phase-1.md` (AC-P1-01…). Nguồn gốc vẫn là lab board; khi lệch, ưu tiên lab board. PRD Phase 2–4 chưa mở: cập nhật plan khi có.
- Điểm PRD-0 khác bản plan cũ: (1) **không mời giảng viên**, chỉ cần repo public; (2) CI, ruleset, PR, CODEOWNERS chỉ là **"nên"** (nhóm chọn cách khác không bị trừ điểm), nhưng nhóm này **tự chọn** dùng; (3) DoD yêu cầu README ghi cách chạy ≤ 3 lệnh, điều khiển, cách tính điểm, test chạy bằng 1 lệnh; (4) smoke test hai tiến trình gather → quan qua file kho.
- Bản README thô trên `raw.githubusercontent.com` có thể lệch với bản hiển thị trên GitHub (lịch tag, thang điểm). Khi có chênh lệch, **ưu tiên lab board và giảng viên**; plan này theo bản README mới nhất đã đọc.

## 1. Mục tiêu

Nhóm 4 người làm game 2D *Quán Ăn Chợ Nổi* bằng AI-assisted SDLC trong **3 giờ, 4 phase**, mỗi phase gắn tag đúng hạn và game **chạy được tại mỗi tag**; kiểm chứng bằng Test Contract (cùng seed + input → output giống từng byte, chế độ headless `gather` và `quan`).

## 2. Lịch phase và hạn tag (theo README)

| Mốc | Phase | Hạn tag |
|---|---|---|
| 0:00 | Phase 1 (PRD-0) | `phase-1` trước **1:00** |
| 1:00 | Phase 2 | `phase-2` trước **1:55** |
| 1:55 | Phase 3 | `phase-3` trước **2:30** |
| 2:30 | Phase 4 | `phase-4` **và Release `v1.0.0`** trước **3:00** |

Quy tắc: hết giờ phase thì **gắn tag và chuyển tiếp**; phần chưa xong ghi **trung thực** trong `docs/verification/phase-n.md`. Người gắn tag: **Integrator (Người 2)**; mốc **code freeze 10 phút trước hạn**, chạy lại test và headless trên `main` rồi mới tag.

### Chu trình lặp cho mỗi phase

| Bước | Tỉ lệ thời gian | Việc |
|---|---|---|
| 1. Nhận PRD | ~10% | Đọc PRD phase trên lab board (có trợ giảng AI theo phase, đăng nhập claude.ai); PO ghi điểm chưa rõ vào `docs/clarify.md` |
| 2. AC & issue | ~10% | Viết AC (`AC-P<n>-<xx>`), tạo issue (template `.github/ISSUE_TEMPLATE/feature.md`), gán người, link phụ thuộc; viết `docs/plan/phase-n.md` ≤ 1 trang |
| 3. Làm song song | ~55% | Mỗi người một branch/issue/PR nhỏ |
| 4. Tích hợp & kiểm chứng | ~15% | Merge theo thứ tự Integrator, chạy toàn bộ test, determinism `cmp`, điền `docs/verification/phase-n.md` |
| 5. Freeze & tag | ~10% | Code freeze, tag, ghi tồn đọng trung thực, standup/ghi chú |

Ví dụ ngân sách thời gian: Phase 1 (60') ≈ 6'/6'/33'/9'/6' cộng 15' kickoff chồng ở đầu; Phase 2 (55'); Phase 3 (35' — rất ngắn, chỉ nhận việc vừa sức); Phase 4 (30', gồm Release và demo).

**Lưu ý quan trọng:** Phase 1 = PRD-0 và có tag chấm điểm sau 1 giờ ⇒ **luật lõi Gather/Quán phải chạy được trong Phase 1** (README: bài test headless ẩn chiếm điểm lớn nhất). Setup repo và hợp đồng phải xong trong ~15 phút đầu.

## 3. Thang điểm và cách kế hoạch phục vụ (100 điểm)

| Hạng mục | Điểm | Người chịu trách nhiệm chính | Việc then chốt |
|---|---|---|---|
| Test tự động ẩn (headless) | 25 | Người 1 + 2 (luật), Người 4 (kiểm) | Output đúng PRD, deterministic, exit code đúng, kho hợp lệ |
| Làm việc nhóm | 25 | Người 3 (Scrum) + cả nhóm | ≥ 3 commit có nội dung/người, PR có issue + review dòng cụ thể, standup, TEAM.md |
| Kiểm chứng và bằng chứng | 15 | Người 4 | `docs/verification/phase-n.md` + `docs/proof/phase-n/` thật, ghi trung thực |
| Harness AI | 10 | Người 3 (AGENTS.md), Người 2 và 4 (skills) | `AGENTS.md` cập nhật theo phase, ≥ 2 skill, `docs/ai-usage-log.md` |
| Đánh giá và retro | 10 | Người 3 + cả nhóm | `docs/retro.md`, `docs/members/<handle>.md` của từng người |
| Chất lượng sản phẩm | 10 | Người 3 (UI), Người 1/2 | Game chạy được tại mỗi tag, UI/HUD đúng PRD |
| Demo | 5 | Người 3 điều phối | Kịch bản demo ở Phase 4 |

## 4. Phân công 4 thành viên

| Người | Module chính | Vai quy trình | Người dự phòng cho | Reviewer chính của |
|---|---|---|---|---|
| Người 1 | `sim/gather` | PO (đầu mối hỏi giảng viên, giữ `docs/clarify.md`) | Người 2 | `sim/quan` |
| Người 2 | `sim/quan` | Integrator (giữ `docs/contracts/`, thứ tự merge, **gắn tag**, Release) | Người 3 | `sim/gather`, `client/ui` |
| Người 3 | `client/ui` | Scrum/Release + trưởng nhóm (fork, setup, `AGENTS.md`, standup, retro) | Người 4 | `qa` |
| Người 4 | `qa` | QA Lead | Người 1 | `client/ui` |

Ngoài module: `chonoi/scenario.py` (kiểm mâu thuẫn scenario mức luật) do **Người 2**; nội dung sáng tạo (module `content` trong PR template) do **Người 3** sau khi lõi xong. PR đụng `docs/contracts/`, khóa contract hoặc schema kho cần **2 approvals**.

## 5. Nguyên tắc bắt buộc từ repository

1. Đọc `AGENTS.md`, `README.md`, `docs/STARTER.md`, `game.contract.json`, `docs/contracts/`, PRD đúng phase trước khi sửa code; đưa PRD/ticket đúng phase và `docs/contracts/` cho agent.
2. Starter Python tùy chọn. Luật nhóm ở `chonoi/sim/gather.py`, `chonoi/sim/quan.py` (`TODO(nhóm)`), `chonoi/scenario.py`. Module framework (`headless, inputs, scenario, contract, rng, ids, jsonl, inventory, runner, live` và `chonoi/web/`) hạn chế sửa; **bắt buộc sửa thì PR riêng + ADR** (lưu ý `scenario.py` vừa thuộc danh sách framework vừa là phần nhóm cần viết luật; hỏi PO/giảng viên nếu chưa rõ ranh giới, ghi vào `docs/clarify.md`). Hiện có thêm `chonoi/sim/ramp.py`: cần đọc để biết vai trò.
3. Số liệu chỉ ở `game.contract.json`/data file; luật chỉ đọc từ đó.
4. Ngẫu nhiên chỉ qua `Streams`; không `random` toàn cục, không đồng hồ hệ thống; `ids.sort_by_id`, `IdAllocator`.
5. Cùng seed + input → output giống từng byte.
6. Không sửa `docs/contracts/`, contract keys, schema kho nếu thiếu PR đủ 2 approvals.
7. Không push thẳng `main`; không tắt/bypass CI. PR dùng `.github/pull_request_template.md`: Closes #issue, phase, module (`gather|quan|ui|qa|content|contracts`), danh sách AC, bằng chứng (lệnh + output / đường dẫn `docs/proof/...` / ảnh), đóng góp AI (agent, prompt chính, phần đã đọc và sửa), rủi ro/việc dở, reviewer checklist.
8. Reviewer: nhận xét **gắn dòng cụ thể của diff**, không chỉ "LGTM"; PR ≤ ~400 dòng, 1 việc/PR.
9. Không sửa test cho pass khi luật sai; nếu sửa test phải giải thích trong PR.
10. Một agent – một branch – một issue; người phụ trách đọc diff trước khi mở PR; agent chạy test và dán kết quả vào PR.
11. ≥ 2 skill/hook/command của nhóm trong `.agents/skills/` (hiện chỉ có `.gitkeep`): Người 4 `determinism-check`; Người 2 `pr-checklist`.
12. Không dùng nội dung của nhóm khác; không commit API key/token/`.env`; asset ngoài chỉ CC0/CC-BY/MIT hoặc tự tạo và **ghi nguồn trong `CREDITS.md`**; bằng chứng phải thật.

## 6. Phase 1 – Kickoff, hợp đồng, lõi luật (0:00–1:00, tag `phase-1` trước 1:00)

### 6.1 Setup (trưởng nhóm Người 3, ~5 phút)
- [ ] Fork repo, đặt tên **`K5-L3B-LAB-Day12-AI-SDLC-<ten-nhom>`**, để **public**.
- [ ] Thêm 3 thành viên làm Collaborator quyền **Write**. **Không cần mời giảng viên** (repo public là đủ, theo PRD-0 mục 4).
- [ ] Bật GitHub Actions; import `.github/ruleset-main.json` (Settings → Rules → Rulesets). PRD-0 coi đây là tùy chọn, nhóm **chọn dùng** và không bypass.
- [ ] **PR đầu tiên:** điền `TEAM.md` **đủ 4 người** (tên, handle thật, module chính, vai, dự phòng) + thỏa thuận nhóm ≤ 10 dòng; sửa `team` và `team_size` = 4 trong `game.contract.json`. `ci / test` chạy `tools/check_team.py`: đỏ nếu thiếu bảng 4–6 người, `team_size` lệch, hoặc người mở PR không có trong danh sách. Commit của người không có trong `TEAM.md` **không được tính**.
- [ ] Mỗi người clone fork, chạy smoke test; Người 4 lưu baseline.

### 6.2 Kickoff 15 phút
- [ ] Điền thỏa thuận nhóm (kênh, bất đồng thiết kế, vướng > 10 phút, giờ standup, vòng review, quy ước commit/PR).
- [ ] **Chốt hợp đồng tích hợp `docs/contracts/`** (README của contracts nêu 3 mục bắt buộc):
  1. Schema file kho (khớp mục G PRD-0; kho ghi khi `gather_end`) + file mẫu hợp lệ `inventory.sample.json`.
  2. Interface `sim/*` ↔ `client/ui`: UI đọc state nào, gửi command nào.
  3. Danh sách event: tên, payload `data`, bên phát, bên nghe. Event Gather ví dụ: `gather`, `node_regrown`, `hold_full`, `fish_caught`, `gather_end`...; event Quán theo mục E PRD-0.
- [ ] Hợp đồng đổi sau này: báo cả nhóm và ghi lý do; vì AGENTS.md khóa `docs/contracts/` và schema kho, PR đổi cần **2 approvals**.
- [ ] Người 3 tạo issues; PO điền AC từ PRD-0; `docs/plan/phase-1.md` (≤ 1 trang): Mục tiêu / Việc–người–phụ thuộc (link issue) / Rủi ro.

### 6.3 Làm song song
- Người 1: lõi Gather. Người 2: lõi Quán + scenario. Người 3: UI dựng khung theo snapshot/fixture, HUD khi luật có. Người 4: test, test matrix, headless `cmp`.
- Mỗi người **≥ 3 commit có nội dung** bằng tài khoản của mình trong cả lab (làm cặp: `Co-authored-by`).

### 6.4 Đóng phase
- [ ] `docs/verification/phase-1.md`: bảng AC | cách kiểm chứng | bằng chứng (`docs/proof/phase-1/...`) | kết quả (đạt/chưa đạt, ghi trung thực) + đánh giá ngắn (đạt/chưa đạt; cần chỉnh cho phase sau).
- [ ] Code freeze T-10', chạy test + headless, **tag `phase-1`**.

- [ ] **DoD PRD-0 bổ sung:** README ghi chạy từ clone sạch ≤ 3 lệnh (macOS/Linux), điều khiển, cách tính điểm, lệnh test (1 lệnh); `game.contract.json` khớp bản chạy; smoke hai tiến trình trên `main` (gather ghi kho → quan đọc đúng kho, ví dụ `stock:{"bong_sung":2,"ca_loc":1}` ở tick 0); HUD đọc được lúc chơi; mục "Sáng tạo của nhóm" nếu có.

**Gate:** `main` bảo vệ, CI xanh, TEAM.md đủ, hợp đồng chốt, lõi chạy được tại tag.

## 7. Phase 2, 3, 4 (theo PRD phát tại lab board)

Mỗi phase theo chu trình mục 2. Việc cố định:
- **Phase 2 (1:00–1:55):** mở rộng theo PRD-2; cập nhật `AGENTS.md`; kiểm tra chế độ `day` nếu PRD yêu cầu (README: `day` xuất hiện ở phase sau); tag `phase-2` trước 1:55.
- **Phase 3 (1:55–2:30):** khoảng 35 phút, chỉ nhận việc có AC rõ; sửa lỗi hồi quy; tag `phase-3` trước 2:30.
- **Phase 4 (2:30–3:00):** ổn định, `docs/retro.md`, `docs/members/<handle>.md` (mỗi người, ≤ 200 từ: đã làm + link commit; đã review + link; AI sai ở đâu và phát hiện thế nào; điều học được), `docs/ai-usage-log.md`, `CREDITS.md`, phần **"Sáng tạo của nhóm"** trong README nhóm nếu có thêm nội dung, demo, tag `phase-4` **và Release `v1.0.0`** trước 3:00.

## 8. Sáng tạo của nhóm (tùy chọn, chỉ sau khi lõi xong)

Được thêm nhân vật, loài, món, bản đồ, cơ chế, đồ họa, âm nhạc… với 3 điều kiện: (1) không phá phần cố định (phần sáng tạo phải **tắt ở headless** để test ẩn vẫn đúng), (2) ghi mục "Sáng tạo của nhóm" trong README nhóm, (3) làm phần lõi trước. PR module `content`. Người 4 kiểm headless trước/sau để chắc output không đổi.

## 9. Phối hợp và dependencies

```text
PRD-n (lab board) -> AC + issues
Người 1: Gather --inventory (gather_end)--> Người 2: Quán (+ scenario)
        |                                       |
        +-- state/events/commands (docs/contracts) --+
                          |
                          v
                 Người 3: UI/HUD (đọc snapshot)
                          |
                          v
        Người 4: verify (headless, cmp, proof) -> Người 2: tag/Release
```

- HUD chỉ hiện khi luật tương ứng đã cài ⇒ UI phụ thuộc Người 1/2; trong lúc chờ dùng snapshot giả.
- Người 4 chuẩn bị test ngay từ khi có AC, không chờ cuối phase.

## 10. Git workflow

```text
feature/gather-<task> | feature/quan-<task> | feature/ui-<task> | test/qa-<task> | docs/<topic> | content/<topic>
```

PR checklist: Closes #; phase; module; AC; bằng chứng; AI contributions; rủi ro; ≤ ~400 dòng; không đụng contract/framework trái quy trình; reviewer nhận xét theo dòng; `ci / test` xanh; ≥ 1 approver khác (2 nếu đụng contract/schema).

## 11. Quy tắc AI (prompt nền cho mọi thành viên)

> Đọc `AGENTS.md`, README, `docs/STARTER.md`, PRD đúng phase và `docs/contracts/` trước khi làm. Chỉ làm issue được giao trên branch hiện tại. Không đổi contract, schema, test hay module framework trong `chonoi/` ngoài PR riêng có ADR. Không hard-code số liệu; đọc từ `game.contract.json`. Randomness chỉ qua Streams; không dùng system clock. Giữ output deterministic, dùng `IdAllocator` và `ids.sort_by_id`. Chạy test và headless trước khi kết thúc; báo cáo file đổi, lệnh, kết quả thực tế, rủi ro để dán vào PR. Yêu cầu mơ hồ → ghi `docs/clarify.md`, không tự suy diễn.

Mỗi người ghi vào `docs/ai-usage-log.md`: mục đích, prompt/agent, file ảnh hưởng, phần đã kiểm chứng, phần chỉnh sửa. Ghi cả chỗ AI sai (dùng cho phản tư cá nhân).

## 12. Nhịp phối hợp

- Kickoff 15'. Standup giữa mỗi phase: Done / Next / Blocker → `docs/standup.md`. Vướng > 10': báo kênh, người dự phòng nhận việc.
- Trước PR: tác giả đọc diff + chạy test. Trước merge: reviewer kiểm scope, AC, test, contract, CI, nhận xét theo dòng.
- Cuối phase: QA điền verification; Người 3 cập nhật `AGENTS.md` và `docs/retro.md`.

## 13. Điều kiện hoàn thành toàn lab

- [ ] Fork đúng tên, public; Actions + ruleset bật; 3 thành viên còn lại là Collaborator Write (không cần mời giảng viên).
- [ ] `TEAM.md` đủ 4 người thật, `team_size`/`team` đúng; mỗi người ≥ 3 commit có nội dung.
- [ ] Tag `phase-1…phase-4` đúng hạn, game chạy được tại mỗi tag; Release `v1.0.0`.
- [ ] Gather, Quán, scenario đạt AC; UI đáp ứng PRD; headless + determinism pass.
- [ ] `docs/contracts/` đủ 3 mục + `inventory.sample.json` hợp lệ.
- [ ] `docs/verification/phase-n.md` (n = 1..4) + `docs/proof/phase-n/` thật; `docs/plan/phase-n.md`.
- [ ] `AGENTS.md` cập nhật theo phase; ≥ 2 skill trong `.agents/skills/`; `docs/ai-usage-log.md`.
- [ ] `docs/retro.md`, `docs/standup.md`, `docs/clarify.md`, `docs/members/<handle>.md` cho cả 4 người.
- [ ] `CREDITS.md` nếu có asset ngoài; không có key/token/`.env`.
- [ ] Demo tái lập được.

## 14. Tham chiếu

- Repo: https://github.com/VinUni-AI20k/K5-L3B-LAB-Day12-AI-SDLC (README, AGENTS.md, TEAM.md, `docs/STARTER.md`, `docs/contracts/README.md`, `.github/pull_request_template.md`).
- PRD từng phase và lab board: theo giảng viên.
