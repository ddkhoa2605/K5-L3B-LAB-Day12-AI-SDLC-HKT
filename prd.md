Phase 1 · hạn tag phase-1 lúc 1:00 · phát hành 08:02

PRD-0 — Quán Ăn Chợ Nổi (Phase 1)
Day 12 · AI SDLC · Nhóm 4–6 người · 60 phút (0:00–1:00) · Test Contract v1.0 · Hạn đẩy tag phase-1 1:00.

1. Chúng tôi muốn gì
Quán Ăn Chợ Nổi là game quản lý quán ăn mang bản sắc miền Tây Nam Bộ. Người chơi là Út Sen, cô bé ở chợ nổi Rạch Sen. Khi Má Tư đau lưng, Út Sen lặn bắt cá và hái rau trên sông Chín Khúc vào buổi sáng. Tối đến, em nấu và phục vụ khách trên nhà bè của Má Tư. Những gì mang về quyết định quán có thể bán món nào.

Tự do sáng tạo
Ngoài yêu cầu của PRD và Test Contract, nhóm được tự do thêm nhân vật, loài cá hoặc cây, sinh vật mới, món ăn, khu vực, cơ chế nhỏ, sự kiện, câu chuyện, đồ họa, âm nhạc hoặc giao diện theo ý mình.

Giữ đúng luật lõi, số chuẩn và Test Contract. Tắt phần tự thêm ở headless hoặc bảo đảm nó không đổi tick, sự kiện, tiền, uy tín và snapshot theo contract khi chạy test.
Ghi ý tưởng đã làm vào mục “Sáng tạo của nhóm” trong README.md, kèm bằng chứng ngắn cho thấy lõi vẫn đúng.
Làm lõi đúng trước, sáng tạo sau. Ưu tiên một ý tưởng gọn, chạy ổn và hoàn thiện. Điểm sáng tạo nằm ở hạng mục chất lượng sản phẩm, độ phức tạp không được cộng điểm.
2. Phạm vi Phase 1
Lõi (mọi nhóm)
Buổi sáng (gather). Bơi trong mặt cắt 2D của sông, theo chiều ngang và độ sâu [x,d]. Út Sen tiêu oxy dưới nước, hồi oxy khi nổi lên và có 3 Máu, chỉ mất do ngạt. Hái tại nút trên mặt nước và dùng nút bắt cá (catch) khi lặn. Bản mặc định có 6 đàn cá đứng yên. Giỏ có sức chứa giới hạn. Cập bến hoặc hết giờ thì bàn giao phần còn trong giỏ qua file kho. Ngất thì kết thúc buổi sáng với kho rỗng.
Buổi tối (quan). Quán có 1 bếp B1, 1 bàn T1 và 3 món. Khách chọn món nấu được với kho khả dụng và giữ chỗ nguyên liệu khi gọi. Người chơi nấu → bưng → phục vụ trước khi khách hết kiên nhẫn. Khách ăn xong trả tiền, có thể boa. Khách hết kiên nhẫn làm giảm uy tín.
Hai buổi chơi được riêng và nối nhau qua hai tiến trình headless dùng chung file kho. Điều khiển gợi ý là WASD hoặc phím mũi tên để bơi/đi, E để tương tác và Space để bắt cá. HUD tối thiểu cho biết thời gian, oxy, Máu, giỏ ở buổi sáng và kho khả dụng, món gọi, kiên nhẫn, trạng thái bếp, món trên tay, tiền và uy tín ở buổi tối.
Mở rộng
Kỳ vọng mở rộng tính cho cả buổi lab. Nhóm 4 người không bắt buộc, nhóm 5 người hoàn thành ít nhất 1 mục, nhóm 6 người ít nhất 2 mục.

3. Cảm giác và phong cách
Sông nước màu phù sa, bờ dừa nước, nhà sàn và ánh hồng buổi sớm. Tối có đèn dây vàng và khói bếp. Út Sen mặc áo bà ba, buộc khăn rằn, đeo kính lặn tự chế và giỏ lưới. Dùng mặt cắt nhìn ngang cho cảnh lặn và góc nhìn từ trên xuống cho nhà bè. Có thể bắt đầu bằng hình khối 2D. Giọng Nam Bộ trong thoại được khuyến khích. Tôn trọng văn hóa địa phương, dùng tài sản có quyền sử dụng và ghi nguồn trong CREDITS.md.

4. Công nghệ và cách vào lab
Starter Python là một lựa chọn. Nhóm được chọn ngôn ngữ, engine và thư viện. Nếu đổi công nghệ, cập nhật build_cmd, run_cmd và headless_cmd để giữ đúng Test Contract. Smoke test chạy hộp đen qua headless_cmd.

Trưởng nhóm fork VinUni-AI20k/K5-L3B-LAB-Day12-AI-SDLC về tài khoản của mình, đặt tên K5-L3B-LAB-Day12-AI-SDLC-<ten-nhom> và mời các thành viên làm collaborator với quyền Write trong Settings → Collaborators. Để repo public là đủ cho giảng viên xem, không cần mời giảng viên.
Điền TEAM.md trong fork chung và đặt team_size trong game.contract.json khớp số thành viên thực tế.
Nhóm có thể bật GitHub Actions hoặc dùng ruleset nếu phù hợp với cách làm đã chọn.

5. Nguyên liệu và món
ID nguyên liệu	Tên
ca_loc	Cá lóc
ca_linh	Cá linh
bong_dien_dien	Bông điên điển
bong_sung	Bông súng
ID món	Món	Công thức
ca_loc_nuong_trui	Cá lóc nướng trui	ca_loc ×1
goi_bong_sung	Gỏi bông súng	bong_sung ×2
lau_ca_linh_dien_dien	Lẩu cá linh bông điên điển	ca_linh ×3 + bong_dien_dien ×1
Dùng preset mẫu hoặc chọn giá, thời gian nấu và các số cho phép ở mục A. Khai đúng các giá trị đang chạy trong tuning.

6. Cách làm việc nhóm
Quy trình kỹ thuật do nhóm tự chọn. Có thể push thẳng, dùng nhánh và Pull Request (PR), pair/mob hoặc review trực tiếp. Cả nhóm phải chia việc, phối hợp và tích hợp giữa các module trong một fork chung. Mỗi người có commit gắn với tài khoản GitHub của mình, tối thiểu 3 commit có nội dung trong cả buổi lab; commit của người không có trong TEAM.md không được tính. Khi làm chung một commit, ghi Co-authored-by: cho người cùng làm.

Nên dùng các thực hành phù hợp với nhóm, như CI/CD, PR có review và approval, bảo vệ nhánh, ruleset, issue/board, CODEOWNERS, ADR hoặc template. Ví dụ, nhóm có thể ghi hợp đồng ở docs/contracts/ và nhờ hai người duyệt PR đổi schema. Các cách này đều tùy chọn. Nhóm chọn cách khác không bị trừ điểm. Thực hành hiệu quả được cộng ở hạng mục thực hành kỹ thuật.

6.1. Kickoff và planning trong 15 phút đầu
Chia bốn lát ở mục 6.2 và ghi vào TEAM.md tên, GitHub handle, module chính và vai của từng người. Có thể kiêm vai. Gợi ý PO hỏi Anh Năm hàng xóm (trợ giảng AI ở tab Phase 1 của lab board; anh là khách hàng, trả lời ngắn các chỗ PRD chưa nói rõ) hoặc giảng viên, Integrator điều phối tích hợp và tag, QA lead giữ bộ test và ma trận truy vết, Scrum/Release theo dõi mốc bàn giao.
Chốt thỏa thuận nhóm ngắn trong TEAM.md gồm kênh liên lạc, giờ standup, cách quyết khi bất đồng và việc cần làm khi có người trễ hoặc vướng. Có thể thử trao đổi trong 2 phút trước khi nhờ người đã thống nhất chốt, hoặc báo kênh nhóm khi vướng quá 10 phút để có người hỗ trợ.
Chốt sớm hợp đồng file kho giữa gather và quan theo mục G. Ghi schema và một ví dụ kho hợp lệ trong README.md hoặc một file ở docs/contracts/. Chốt các sự kiện và giao diện giữa mô phỏng và UI, như sim/*–client/ui (trạng thái đọc được, lệnh gửi vào). Bắt đầu các lát song song sau khi thống nhất, dùng kho mẫu để làm quán.
Nếu cần backlog, dùng checklist, issue/board hoặc docs/plan/phase-1.md. Gợi ý ghi đầu việc, AC-P1-xx, người làm và phần phụ thuộc.
6.2. Bốn lát làm song song
Lát	Phạm vi
1	Bơi, oxy, chặn biên, giỏ.
2	Hái, bắt cá, cập bến, ghi file kho.
3	Khách, giữ chỗ nguyên liệu, kiên nhẫn.
4	Bếp, bưng, phục vụ, tiền.
Nhóm 4 người có thể giao mỗi người một lát. Người thêm ở nhóm 5–6 có thể lo HUD, QA hoặc hỗ trợ lát đang chậm. Gợi ý review chéo giữa các lát, đổi vai người lái và người dẫn đường khi pair/mob. Phút 20 của mỗi phase, nên rà lát đang vướng và điều người đã xong sang hỗ trợ. Standup có thể gói trong 2–3 phút với ba ý đã xong, sắp làm và đang vướng.

6.3. Kiểm chứng và ghi chép
Mỗi phase chạy kiểm chứng trên commit bàn giao ở main và đẩy tag phase-n đúng hạn. Ghi docs/verification/phase-n.md theo AC → bằng chứng → kết quả đạt/chưa đạt, kèm cách kiểm chứng. Ở Phase 1, lưu kết quả thật trong docs/proof/phase-1/ và dẫn từ docs/verification/phase-1.md.
Chỗ nào PRD mơ hồ thì hỏi Anh Năm hàng xóm trên lab board trước; anh không trả lời được thì nhóm tự đặt giả định. Ghi câu hỏi, trả lời và quyết định trong docs/clarify.md. Cập nhật docs/ai-usage-log.md theo người và phase, kèm token/chi phí nếu đo được. Ghi retro trong docs/retro.md và phản tư của mỗi người trong docs/members/<handle>.md.
Đánh giá cá nhân dựa trên bằng chứng trong repo chung (commit của từng người, phần mình làm, việc giúp người khác), phản tư cá nhân và đánh giá chéo. Số PR và lượt review không dùng để chấm cá nhân.
6.4. Lịch gợi ý (60 phút)
Phút trong phase	Việc
0–15	Vào fork, chia vai, ghi TEAM.md, chốt hợp đồng kho và bắt đầu các lát song song.
15–45	Build và phối hợp các lát. Rà hỗ trợ ở phút 20, thử xuất file kho thật trước phút 25, standup giữa phase.
45–55	Chạy smoke hai tiến trình và chơi thử trên main. Hoàn thiện ma trận truy vết và gắn tag.
55–60	Dự phòng. Đẩy phase-1 chậm nhất 1:00.
7. Định nghĩa hoàn thành (DoD)
 Chơi được cả hai buổi, đúng phạm vi lõi. HUD đọc được trong lúc chơi.
 game.contract.json khớp bản chạy và đầy đủ Test Contract v1.0. Smoke hai tiến trình trên main cho thấy quán nhận đúng file kho.
 README.md ghi cách chạy từ clone sạch trong tối đa 3 lệnh trên macOS hoặc Linux, điều khiển, cách tính điểm và lệnh test. Test của nhóm chạy được bằng 1 lệnh.
 Fork chung có đủ collaborator và commit gắn với tài khoản GitHub của từng người. TEAM.md có danh sách và thỏa thuận nhóm. team_size khớp danh sách.
 Hợp đồng kho đã thống nhất, có schema và ví dụ hợp lệ trong README.md hoặc docs/contracts/.
 Có docs/verification/phase-1.md và bằng chứng chạy ở commit gắn tag. Đã cập nhật ghi chép tối thiểu ở mục 6.3.
 Nếu có phần tự sáng tạo, mục “Sáng tạo của nhóm” trong README.md có bằng chứng lõi vẫn đúng.
 Đẩy tag phase-1 trỏ tới commit bàn giao trên main chậm nhất 1:00.
Test Contract v1.0 (bắt buộc)
Headless chạy logic ở 60 tick/s, độc lập với cửa sổ, GPU và tốc độ render. Đơn vị vị trí là mét. gather dùng [x,d] với x hướng đông, d tăng xuống dưới, hướng 0° là +x và 90° là xuống. quan dùng [x,z] với z hướng bắc.

A. File game.contract.json ở gốc repo
Các khóa trong preset v1.0 dưới đây đều bắt buộc. Có thể dùng nguyên bộ số mẫu. team là mã nhóm, team_size là số thành viên thực tế. headless_cmd nhận các cờ ở mục B, run_cmd mở game và build_cmd chuẩn bị bản chạy. Quy đổi thời gian có hậu tố _s sang số tick nguyên ở 60 Hz. Tiền lưu bằng số nguyên, đơn vị nghìn đồng.

{
  "contract_version": "1.0",
  "team": "cho-noi-01",
  "team_size": 4,
  "headless_cmd": "./game headless",
  "run_cmd": "./game",
  "build_cmd": "./build",
  "tuning": {
    "tick_hz": 60,
    "gather": {
      "duration_s": 180,
      "bounds": {"x":[0,100],"d":[0,30]},
      "dock_pos": [2,0],
      "dock_radius": 3,
      "start_pos": [2,0],
      "start_heading_deg": 0,
      "swim_speed": 4.0,
      "ramp_max_ticks": 6,
      "surface_depth": 0.5,
      "oxygen_max_s": 30,
      "oxygen_refill_per_tick": 6,
      "choke_interval_ticks": 60,
      "hp_max": 3,
      "hold_capacity": 12,
      "interact_radius": 2.0,
      "node_yield": 1,
      "regrow_s": 20,
      "catch_radius": 2.0,
      "catch_cooldown_s": 0.5,
      "fish_yield": {"ca_linh":3,"ca_loc":1},
      "nodes": [
        {"id":"N1","kind":"bong_dien_dien","pos":[12,0]},
        {"id":"N2","kind":"bong_dien_dien","pos":[28,0]},
        {"id":"N3","kind":"bong_sung","pos":[44,0]},
        {"id":"N4","kind":"bong_sung","pos":[60,0]}
      ],
      "fish_initial": [
        {"id":"F1","kind":"ca_linh","pos":[15,5],"heading_deg":0},
        {"id":"F2","kind":"ca_loc","pos":[30,10],"heading_deg":0},
        {"id":"F3","kind":"ca_linh","pos":[45,10],"heading_deg":0},
        {"id":"F4","kind":"ca_loc","pos":[60,16],"heading_deg":0},
        {"id":"F5","kind":"ca_linh","pos":[75,5],"heading_deg":0},
        {"id":"F6","kind":"ca_loc","pos":[90,16],"heading_deg":0}
      ]
    },
    "quan": {
      "duration_s": 180,
      "bounds": {"x":[0,16],"z":[0,10]},
      "start_pos": [8,5],
      "walk_speed": 4.0,
      "ramp_max_ticks": 6,
      "interact_radius": 1.5,
      "stoves": [{"id":"B1","pos":[2,8]}],
      "tables": [{"id":"T1","pos":[9,2]}],
      "first_customer_tick": 120,
      "customer_interval_s": 15,
      "patience_s": 60,
      "eat_s": 10,
      "burn_s": null,
      "carry_limit": 1,
      "tip_rate": 0.2,
      "tip_min_patience_ratio": 0.5,
      "tip_reputation": 0.2,
      "left_reputation_delta": -0.5,
      "reputation_initial": 3.0,
      "reputation_min": 0,
      "reputation_max": 5
    },
    "menu": {
      "ca_loc_nuong_trui": {"recipe":{"ca_loc":1},"cook_s":6,"price":60},
      "goi_bong_sung": {"recipe":{"bong_sung":2},"cook_s":4,"price":40},
      "lau_ca_linh_dien_dien": {"recipe":{"ca_linh":3,"bong_dien_dien":1},"cook_s":10,"price":120}
    },
    "score": {"reputation_multiplier": 100}
  }
}
Dải hợp lệ. Hai ca 60–600 s, khoang 4–30 ô, kiên nhẫn 20–180 s, bán kính bến/hái/bắt/tương tác quán 0.5–5 m, tốc độ bơi/đi 1–10 m/s, hồi bắt 0–10 s, oxy tối đa 10–120 s. Giá là số nguyên dương, thời gian nấu/mọc lại/ăn/chu kỳ khách là số tick dương sau quy đổi. first_customer_tick nguyên dương và trước khi đóng ca. ramp_max_ticks khai trần 0–6 tick. tip_rate > 0, tip_min_patience_ratio ∈ (0,1], tip_reputation > 0, left_reputation_delta < 0. Thời lượng, khoang, oxy, kiên nhẫn đều hữu hạn. Các luật và giá trị còn lại lấy theo preset, trừ vị trí các nút và đàn cá có thể chọn trong miền hợp lệ. Cố định ID và công thức 3 món, 4 loại nguyên liệu, 1 ô/nguyên liệu, 1 bếp B1, 1 bàn T1, ít nhất một nút mỗi loại cây, 6 đàn đứng yên có cả hai loài cá, burn_s: null. Nút mặc định đặt ở d = 0, đàn cá ở dưới nước.

B. Tham số headless
<headless_cmd> --mode gather|quan --seed <int>
  [--scenario <file.json>] [--inputs <file.json>]
  [--inventory <file.json>] [--inventory-out <file.json>]
  --ticks <N> --out <file.jsonl> [--snapshot-every <N>]
Bắt buộc có --mode, --seed, --ticks, --out. Seed là số nguyên có dấu biểu diễn chính xác trong JSON. --ticks là số bước ngoài tối đa, nguyên không âm. Giá trị 0 chỉ dựng fixture. --snapshot-every là số nguyên dương, mặc định 10.
--inventory chỉ dùng với quan, --inventory-out chỉ dùng với gather. Đầu ra dùng đường dẫn riêng, tách khỏi đầu vào.
Mã 0 khi kết thúc lượt hoặc chạm giới hạn bước, 2 khi cờ/dữ liệu sai hoặc fixture mâu thuẫn, 1 khi lỗi thực thi/ghi đầu ra. Chẩn đoán qua stderr. Kiểm tra dữ liệu xác định được lúc khởi tạo trước khi ghi JSONL hoặc inventory. Gameplay kết thúc thì dừng sớm, ghi snapshot cuối và end.
C. File inputs
{"frames":[
  {"tick":0,"move":[0,1]},
  {"tick":120,"move":[0,0],"catch":true},
  {"tick":121,"catch":false},
  {"tick":180,"interact":true},
  {"tick":181,"interact":false}
]}
tick nguyên không âm, tăng nghiêm ngặt. Trước frame đầu, move = [0,0] và các nút là false. Frame chỉ cập nhật trường có mặt. Thiếu file inputs tương đương không điều khiển.
move gồm hai số hữu hạn trong [−1,1], chuẩn hóa nếu độ dài > 1. Thành phần thứ hai dương là xuống trong gather ([x,d]), về bắc trong quan ([x,z]).
Nút boolean interact dùng để cập bến hoặc hái trong gather và để nấu, bưng hoặc phục vụ trong quan. Nút boolean catch dùng để bắt cá trong gather. Nút chỉ tác động ở cạnh lên từ false sang true. Hành động đúng kiểu nhưng sai pha được bỏ qua. Tên trường sai hoặc chưa hỗ trợ, kiểu sai, tick lặp/giảm → mã 2.
D. File scenario (dựng tình huống để test)
Gốc nhận khối trùng mode. Ví dụ đặt nút đúng mép bán kính hái của preset.

{"gather":{
  "player":{"pos":[20,0],"heading_deg":0},
  "hold":["ca_loc","bong_sung"],
  "nodes":[{"id":"N1","kind":"bong_dien_dien","pos":[22,0]}],
  "fish":[],
  "random_fish":false,
  "time_left_ticks":120
}}
Khối / trường	Nội dung
gather.player	pos,vel,heading_deg,oxygen_ticks,hp,zero_oxy_ticks,catch_cd_ticks. Mặc định vị trí và hướng theo tuning, vận tốc [0,0], oxy và Máu đầy.
gather.hold	Mảng kind theo thứ tự nhặt (mới nhất cuối), mặc định rỗng.
gather.nodes[] / fish[]	Nút {id,kind,pos,regrow_ticks} (0 là ready) · cá {id,kind,pos,heading_deg} (hướng mặc định 0°).
gather	random_fish,time_left_ticks.
quan.player	{pos,vel}, mặc định vị trí theo tuning và vel:[0,0].
quan.stock / hand	stock là giá trị items ở mục G, gồm cả phần giữ chỗ. hand là payload món hoặc null, mặc định null.
quan.stoves[] / tables[]	Bếp {id,pos,state,dish,cook_ticks_left,ready_ticks}. state là idle (mặc định), cooking hoặc ready. ready_ticks là tuổi món trên bếp, mặc định 0 khi ready. Bàn {id,pos}, người ngồi suy từ khách.
quan.customers[]	{id,table_id,dish_id,order_tick,state,patience_ticks_left,eat_ticks_left,order_status,reserved,base_price,tip}. reserved là map kind → số lượng.
quan	time_left_ticks,random_customers,reputation. Uy tín mặc định theo tuning.
nodes, fish, customers thay thế danh sách mặc định, [] là rỗng. stoves, tables cập nhật theo id hiện có. Id duy nhất trong mỗi mảng. Sắp id bằng khóa (tiền tố, hậu tố số hoặc −1, id gốc). Tiền tố là phần trước dãy chữ số ASCII cuối id, hoặc toàn id nếu không có hậu tố. Chuỗi so theo mã Unicode. F2 đứng trước F10. Id mới nối sau hậu tố lớn nhất của họ id tương ứng đã nạp hoặc phát trong lượt.
Các cờ random_* mặc định true. random_fish: false tắt cá mặc định, cá fixture đứng yên. random_customers: false tắt khách tự sinh, vẫn dùng khách fixture.
time_left_ticks mặc định theo tuning. Khi khai, dùng số nguyên dương không vượt thời lượng pha. phase_tick bắt đầu từ 0, lịch khách tính theo phase_tick kể cả khi rút ngắn ca. Bộ đếm chưa kích hoạt mặc định 0. vel là vận tốc tự bơi/đi đã chặn mép. Oxy trong [0, max], Máu trong [1, max]. zero_oxy_ticks trong [0,59] và chỉ dương khi oxy bằng 0 và người chơi dưới nước.
Payload món là {order_id,dish_id,base_price}, với order_id bằng id khách. Khách mặc định waiting, order_tick:0, kiên nhẫn đầy, order_status:reserved. Các trạng thái đơn là reserved/assigned/unfulfillable/served. Thiếu reserved ở đơn reserved thì cấp theo công thức theo order_tick rồi id bàn. Đơn assigned có đúng một món ở bếp hoặc tay, phần giữ rỗng. Bếp cooking có timer dương và món khớp đơn. Khách eating phải là served, có timer ăn dương và khai base_price,tip đã chốt. Đơn unfulfillable còn chờ, giữ chỗ rỗng và không có món.
Mã 2 cho trường sai/chưa hỗ trợ, khối sai mode, id trùng trong danh sách, id bếp/bàn cập nhật không tồn tại, tọa độ ngoài miền, liên kết thiếu, bộ đếm âm/mâu thuẫn, giỏ quá trần, khai cả quan.stock và --inventory, nguyên liệu/món ngoài phạm vi, khách trùng bàn, giữ khác công thức hoặc quá tồn, bếp và tay giữ cùng đơn hoặc món không khớp đơn. Tham chiếu id không tạo thực thể.
E. Output JSONL
Mỗi dòng là một object JSON UTF-8. Chụp snapshot ở tick 0 sau khi dựng fixture, ở bội số của --snapshot-every và ở tick dừng. Mỗi tick tối đa một snapshot. Ghi event theo thứ tự xử lý rồi snapshot. Dòng end luôn cuối.

Pha	Trường snapshot
Chung	type:"snapshot",tick,sim_tick,mode,phase,phase_tick,state,time_left_ticks,money,earned,reputation,score. tick là số bước ngoài, sim_tick là số bước gameplay toàn lượt. state là playing hoặc finished.
gather	player theo D, thêm oxygen_max_ticks,hp_max,at_surface. hold,hold_count,hold_capacity,nodes[],fish[]. Nút có ready bằng regrow_ticks == 0.
quan	player,stock,hand,stoves[],tables[],customers[] theo D. Bàn thêm customer_id (trống là null). Chỉ liệt kê khách còn ngồi.
{"type":"event","tick":1,"phase":"gather","name":"gather","data":{"node_id":"N1","kind":"bong_dien_dien","amount":1}}
name	data
gather / node_regrown	node_id,kind,amount / node_id.
hold_full	action (gather/catch), node_id hoặc fish_id tương ứng, required,free.
fish_caught	fish_id,kind,yield, một event mỗi đàn lấy đủ yield.
dive / surface	pos sau di chuyển, chỉ khi đổi phía của biên mặt nước.
oxygen_empty / choke	oxygen_ticks:0 khi vừa chạm 0 / hp sau trừ.
faint	cause:"choke",lost,hp:0.
gather_end	reason (time/docked/fainted), inventory là object theo G.
customer_arrived / no_dish	order_id,table_id,dish_id / {} khi có bàn mà thiếu món.
cook_started / dish_ready / dish_picked	Mọi event có stove_id,order_id,dish_id. Bắt đầu nấu thêm items,base_price.
served	order_id,table_id,dish_id,patience_ticks_left,base_price,tip.
paid	order_id,table_id,base_price,tip,amount,reason (finished_eating/closing). base_price là tiền món trước boa.
customer_left	order_id,table_id,reason (patience/closing), reputation.
quan_end	reason:"time",money,earned,shift_earned,reputation. money là số dư, earned là tổng thu cả lượt, shift_earned là thu trong ca.
items và lost trong event là mảng kind. lost theo thứ tự bỏ, nhặt sau bỏ trước (LIFO). Dòng cuối có type:"end",ticks,sim_tick,mode,state,reason,money,earned,reputation,score. reason là time/docked/fainted cho gather, time cho quan, hoặc tick_limit khi gameplay chưa xong. Kết thúc đúng bước cuối được cấp thì ưu tiên lý do gameplay. Điểm ở mọi snapshot và end là earned + 100 × floor(reputation).

{"type":"end","ticks":10800,"sim_tick":10800,"mode":"quan","state":"finished","reason":"time","money":72,"earned":72,"reputation":3.2,"score":372}
Sắp mảng thực thể theo id, hold theo thứ tự nhặt và cook_started.items theo kind. Xuất tọa độ đến 3 chữ số thập phân. So bán kính và tính giá trước định dạng. So chính xác tiền, điểm, id, số lượng, countdown và lý do. Dung sai quan sát tọa độ ±0.1 m, uy tín ±0.01 và đo thời gian ±2 tick. Deadline, lịch, cạnh, thứ tự và tick của event biên dùng giá trị chính xác.
Cùng bản chạy, máy, seed, tham số và nội dung đầu vào phải cho JSONL và file kho giống nhau từng byte. Tách RNG giao diện và đồng hồ thực khỏi mô phỏng. Duyệt ứng viên theo thứ tự cố định, id món theo mã Unicode. Chọn ngẫu nhiên nhất quán trong mỗi bản nộp. Fixture muốn dựng nhánh cụ thể thì đặt dữ liệu và tắt phần ngẫu nhiên liên quan.
F. Luật bắt buộc khi xử lý một bước
Bước k đọc frame có tick = k, biến trạng thái k thành k+1 và ghi event tại k+1. Mỗi bước tăng sim_tick và phase_tick một đơn vị, dùng phase_tick sau tăng cho lịch. Timer không âm. Cooldown L đặt ở tick t dùng lại từ t+L. Thực thể sinh cuối bước tham gia tương tác/di chuyển từ bước sau.

Dùng khoảng cách Euclid trên mặt phẳng của pha, tính cả đúng mép bán kính. Vận tốc hội tụ về speed × move trong tối đa ramp_max_ticks, rồi giữ đích. Tích phân với Δt = 1/60 s. Chặn từng thành phần ở biên chữ nhật và triệt thành phần vận tốc hướng ra ngoài. Vận tốc snapshot là vận tốc tự điều khiển sau chặn mép. Hướng mặt theo move khác 0 gần nhất, đứng yên giữ hướng cuối. Nội thất quán không cản đường.

Gather

Tăng đồng hồ, giảm timer ca, hồi bắt và hồi nút. Nút từ 1 về 0 phát node_regrown theo id và có thể hái ngay.
Bơi, chặn biên, so đầu và cuối bước để phát dive hoặc surface. Tính oxy theo d cuối bước. Mặt nước (d ≤ 0.5) cộng 6 tick oxy, kẹp tối đa và reset ngạt. Dưới nước trừ 1 tick, kẹp 0. Phát oxygen_empty khi từ dương xuống 0. Mỗi bước dưới nước kết thúc với oxy 0, kể cả bước vừa chạm 0, tăng zero_oxy_ticks. Đủ 60 thì đặt lại đếm về 0, trừ 1 Máu, phát choke. Máu 0 thì bỏ giỏ theo LIFO, phát faint rồi gather_end với fainted và kho rỗng, dừng bước. Chạm oxy 0 ở t và ở dưới nước liên tục thì ngạt lần đầu ở t+59 nếu đếm ban đầu là 0. Nổi lên đúng bước đáng lẽ ngạt thì hồi oxy và không ngạt.
Ở cạnh interact, xét bến trước bằng khoảng cách tới tâm trên [x,d]. Trong bến kết thúc ngay docked. Ngoài bến, chỉ hái khi ở mặt nước. Chọn nút ready gần nhất trong bán kính, hòa theo id. Đủ chỗ thì thêm 1 nguyên liệu, đặt regrow_ticks = regrow_s × 60 và phát gather. Thiếu chỗ phát hold_full, nút giữ nguyên.
Ở cạnh catch, nếu hết hồi và đang dưới nước thì chọn đúng đàn gần nhất trong bán kính, hòa theo id. Thêm toàn bộ yield, xóa đàn, phát fish_caught và đặt catch_cooldown_s × 60 nếu đủ chỗ. Thiếu chỗ phát hold_full, giữ đàn và cooldown, không thử đàn khác. Không có đàn trong tầm thì không có sự kiện bắt hay hồi chiêu.
Timer ca về 0 thì kết thúc time ở mọi độ sâu, giữ giỏ sau các hành động trên. Chốt kho ngay khi kết thúc và dừng xử lý. E đúng mép bến ở bước cuối vẫn cho docked nếu còn Máu. Ngoài bến, hái hoặc bắt hợp lệ ở bước cuối vẫn vào kho.
Quán

Tăng đồng hồ, giảm timer ca, nấu, ăn và kiên nhẫn. Chỉ tăng ready_ticks cho món đã ready ở đầu bước.
Xét bếp theo id. Món nấu xong chuyển ready với ready_ticks = 0. Dùng burn_s: null.
Di chuyển rồi xét tối đa một interact, chọn theo (khoảng cách, bếp trước bàn, id). Nếu đối tượng được chọn không tương tác được, bỏ lượt. Bếp idle lấy đơn reserved cũ nhất theo order_tick rồi id bàn, tiêu đúng nguyên liệu giữ, chốt giá và bắt đầu nấu. Bếp ready giao món cho tay trống và về idle. Bàn nhận đúng order_id thì khách ăn với timer đầy. Chốt boa bằng floor(tiền món × tip_rate) nếu tỷ lệ kiên nhẫn còn lại sau bước 1 đạt tip_min_patience_ratio, nếu thấp hơn thì boa 0. Phục vụ đúng tick kiên nhẫn về 0 hoặc hết ca vẫn hợp lệ.
Theo id bàn, khách ăn xong trả tiền rồi rời bàn ngay. Nếu ca còn giờ, khách waiting có kiên nhẫn 0 rời và uy tín đổi theo left_reputation_delta. Khi hết ca, khách còn ăn trả ngay (kể cả vừa được giao món), khách còn chờ rời với closing và không trừ uy tín. Dọn xong phát quan_end. Khi khách rời, nhả phần giữ thô, bỏ món của đơn đang nấu, ready hoặc trên tay. Nguyên liệu đã dùng không hoàn lại. Boa dương cộng tip_reputation khi thu tiền, kẹp uy tín theo tuning.
Nếu còn giờ, xét lượt khách theo first_customer_tick, rồi mỗi customer_interval_s × 60 tick. Không còn bàn thì bỏ lượt. Có bàn thì lấy bàn trống id nhỏ nhất. Chọn đều theo seed trong 3 món đủ nguyên liệu khả dụng (tồn vật lý trừ phần giữ). Không có món đủ thì phát no_dish. Khách mới giữ đúng công thức ngay, order_tick bằng phase_tick hiện tại, kiên nhẫn đầy và bắt đầu giảm từ bước sau.
G. File kho (hợp đồng tích hợp Lặn & Hái → Mở Quán)
{"items":{"bong_sung":2,"ca_loc":1}}
File chỉ có khóa items, object kind → số nguyên không âm. Kind vắng tính 0, bên ghi bỏ khóa có lượng 0. Kho rỗng {"items":{}}. Bên đọc từ chối sai schema, kind lạ và giá trị ngoài miền (mã 2). Trần giỏ không áp lên kho quán.
File chỉ chứa hàng trong giỏ khi có gather_end, và khớp object inventory trong event đó. gather --inventory-out ghi đúng một lần (ngất ghi rỗng). Chạm --ticks trước khi kết thúc buổi sáng thì không tạo hoặc ghi đè file. Ghi file tạm cùng thư mục rồi thay thế nguyên tử sau khi ghi thành công.
Quán độc lập thiếu cả inventory và scenario.quan.stock thì kho rỗng. Tiền và earned đầu lượt độc lập bằng 0. Uy tín theo tuning, trừ khi scenario quán có khai.
Smoke test hộp đen. Dùng preset ở A, tạo dock.json với {"gather":{"hold":["ca_loc","bong_sung","bong_sung"]}} và dock-inputs.json với {"frames":[{"tick":0,"interact":true}]}. Snapshot quán ở tick 0 phải có stock:{"bong_sung":2,"ca_loc":1}, đúng file tiến trình đầu ghi.

<headless_cmd> --mode gather --seed 42 --scenario dock.json --inputs dock-inputs.json --ticks 1 --out gather.jsonl --inventory-out catch.json
<headless_cmd> --mode quan --seed 42 --inventory catch.json --ticks 0 --out quan.jsonl

phase 2:
Phase 2 · hạn tag phase-2 lúc 1:55 · phát hành 10:19

TICKET-02 — Một ngày ở chợ nổi (Phase 2)
55 phút (1:00–1:55) · Test Contract v1.1 · Hạn đẩy tag phase-2 1:55.

Hai buổi đã nối được. Khách hàng chốt số liệu chuẩn và muốn chơi trọn một vòng ngày. Sáng, Út Sen xem thực đơn để biết cần tìm nguyên liệu gì. Tối, quán dùng phần mang về để phục vụ. Cuối ngày, người chơi dùng tiền mua nâng cấp cho lần lặn sau.

1. Lõi (mọi nhóm) — Số liệu chuẩn
Thay số đã chọn ở Phase 1 bằng các giá trị dưới đây. Cập nhật cấu hình, spec và test cùng lúc. Tiền tính theo nghìn đồng, mô phỏng chạy 60 tick/s.

1.1. Buổi sáng — Lặn & Hái
Hằng số	Giá trị chuẩn
Thời lượng	180 s (10.800 tick).
Vùng nước	x ∈ [0,100], d ∈ [0,30]. Chặn ở các mép. Mặt nước ở d ≤ 0.5. Các vùng gồm nông d < 10, giữa 10 ≤ d < 20, sâu d ≥ 20.
Bến và xuất phát	Bến tâm [2,0], bán kính 3 m. Xuất phát [2,0], hướng 0° (+x).
Bơi	4.0 m/s, đạt tốc độ hoặc dừng trong ≤ 0.1 s (6 tick).
Oxy và ngạt	Cơ sở 30 s (1.800 tick). Dưới nước −1 oxy/tick, mặt nước +6/tick, kẹp ở mức tối đa. Ở dưới nước với oxy bằng 0, mất 1 Máu mỗi 60 tick, tính cả bước vừa chạm 0. Reset nhịp khi oxy > 0 hoặc lên mặt nước. Ngạt xuyên bất tử và không làm rơi hàng.
Giỏ và hái	12 ô, mỗi nguyên liệu 1 ô. Hái ở mặt nước trong ≤ 2.0 m, lấy 1, mọc lại sau 20 s (1.200 tick). Xét bến trước nút hái.
Nút hái	Bông điên điển N1 [12,0], N2 [28,0] · Bông súng N3 [44,0], N4 [60,0] · Kèo nèo N5 [76,0], N6 [90,0].
Bắt cá	catch (Space), chỉ dưới nước, chọn đàn gần nhất trong ≤ 2.0 m, hòa theo id. Cần đủ chỗ cho cả đàn. Hồi 0.5 s (30 tick) tính từ lần bắt thành công. Yield cá linh 3, cá lóc 1, cá kèo 2.
Đàn cá bơi	1.5 m/s trong x ∈ [4,96]. Cá linh bơi ở d ∈ [3,12], cá lóc [8,20] và cá kèo [22,28]. Đổi hướng theo seed ở bước bơi thứ 120, 240… trước khi di chuyển. Tới mép thì phản xạ phần quãng đường còn lại và đảo thành phần hướng vuông góc với mép, chạm góc đảo cả hai.
Điểm sinh	x ∈ {15,30,45,60,75,90}. Cá linh sinh ở d ∈ {5,10}, cá lóc {10,16} và cá kèo {24,27}. Có 36 cặp loài–vị trí, trong đó 30 vị trí hình học khác nhau.
Sinh cá	Đầu ca 8 đàn ở 8 điểm khác nhau, trần 12 đàn. Tại phase_tick = 360·k (k ≥ 1), sau khi cá bơi, sinh tối đa một đàn nếu còn dưới trần và có điểm cách mọi đàn đang sống > 1 m. Bỏ lượt nếu hết điểm. Loài được chọn với trọng số linh 40%, lóc 30%, kèo 30%, chuẩn hóa lại theo các loài còn điểm hợp lệ. Sau đó chọn đều một điểm của loài và lấy hướng ban đầu theo seed. Cá mới tham gia từ bước sau.
Kết thúc	docked khi tương tác trong bán kính bến, time khi hết giờ ở bất kỳ độ sâu nào. Cả hai giữ phần còn trong giỏ. fainted khi Máu bằng 0, mất toàn bộ giỏ.
1.2. Cá Sấu Năm Chèo, Máu và ngất
Máu cơ sở 3, hồi đầy đầu mỗi Ngày. Cá Sấu ở d ∈ [10,30]. M1 tuần tra từ [60,24] đến [64,24]. M2 từ Ngày 3, tuần tra từ [85,18] đến [89,18]. Waypoint đầu là vị trí xuất phát. Trong gather độc lập, dùng bố trí Ngày 1.
patrol đi 1.0 m/s tới waypoint, đổi sang mục tiêu kia cho bước sau khi đến. Nếu người chơi ở d ≥ 10 và cách ≤ 10 m, chuyển chase và bơi về phía người chơi ở 3.0 m/s. Trở về patrol khi cách > 16 m hoặc người chơi lên d < 10. Chặn Cá Sấu theo biên map và dải độ sâu của loài.
Sau khi cả hai di chuyển, nếu khoảng cách ≤ 1.5 m, người chơi ở d ≥ 10 và hết bất tử, chạm làm mất 1 Máu, bỏ floor(số đang mang/2) nguyên liệu theo LIFO (nhặt sau mất trước) và đặt bất tử 90 tick. Mỗi bước tối đa một hit, chọn con gần nhất, hòa theo id. Trong thời gian bất tử không phát hit hay chuyển Cá Sấu sang recoil do chạm.
Con gây hit vào recoil 60 bước tính từ bước sau, lùi theo hướng xa người chơi đã chốt lúc chạm (trùng tâm dùng +x), mỗi bước 2/60 m trước chặn mép và không gây hit. Hết recoil về patrol, xét phát hiện/chạm từ bước kế. Máu chạm 0 thì ngất ngay và vẫn mở quán tối với kho bàn giao rỗng.
1.3. Buổi tối — Mở Quán
Hằng số	Giá trị chuẩn
Thời lượng	180 s (10.800 tick).
Phòng / xuất phát / đi	x ∈ [0,16], z ∈ [0,10] / [8,5] / 4.0 m/s, đạt tốc độ hoặc dừng trong ≤ 6 tick. Chặn biên và đi xuyên nội thất.
Bếp	B1 [2,8], B2 [5,8].
Bàn	T1 [9,2], T2 [13,2], T3 [9,6], T4 [13,6].
Tương tác	≤ 1.5 m. Chọn gần nhất, hòa ưu tiên bếp trước bàn rồi id. Tay cầm 1 món. Bếp lấy đơn reserved cũ nhất theo order_tick rồi id bàn.
Khách	Lượt đầu tick 120, sau đó 120 + 900·k (k ≥ 0), nếu có bàn trống. Đến ghế trống id nhỏ nhất, giữ nguyên liệu khi gọi món. Kiên nhẫn 60 s (3.600 tick), ăn 10 s (600 tick).
Boa và uy tín	Boa floor(giá × 0.2) nếu còn ≥ 50% kiên nhẫn (≥ 30 s) lúc giao. Khi thu boa dương, uy tín +0.2. Uy tín đầu game 3.0, kẹp [0,5]. Khách hết kiên nhẫn khi ca còn giờ làm giảm 0.5.
Đóng ca	Khách còn ăn trả ngay, khách còn chờ rời mà không trừ uy tín. Dọn món và phần giữ của đơn. burn_s: null trong lõi.
Điểm	earned + 100 × floor(reputation). earned là tổng thu, gồm tiền món và boa.
Thực đơn. Lưu công thức, thời gian nấu và giá dưới dạng dữ liệu. Hai nguyên liệu mới là ca_keo (cá kèo) và keo_neo (kèo nèo).

ID	Món	Công thức	Nấu	Giá
ca_loc_nuong_trui	Cá lóc nướng trui	ca_loc ×1	6 s	60
goi_bong_sung	Gỏi bông súng	bong_sung ×2	4 s	40
lau_ca_linh_dien_dien	Lẩu cá linh bông điên điển	ca_linh ×3 + bong_dien_dien ×1	10 s	120
canh_chua_ca_loc	Canh chua cá lóc bông điên điển	ca_loc ×1 + bong_dien_dien ×1	8 s	90
ca_keo_nuong	Cá kèo nướng muối ớt	ca_keo ×2	6 s	70
lau_mam	Lẩu mắm miền Tây	ca_linh ×2 + ca_keo ×1 + keo_neo ×1 + bong_dien_dien ×1	12 s	200
2. Lõi — Vòng ngày, kế hoạch và Shop
Vòng ngày và kế hoạch
DayIntro → gather → EveningIntro → quan → DayResult → Shop → DayIntro (hoặc tổng kết sau Ngày 5).

Đầu Ngày, Má Tư công bố món định nấu và tổng nguyên liệu cần lấy. HUD sáng hiển thị đã lấy/cần. Khi cập bến, hết giờ hoặc ngất, quán mở với kho bàn giao. Tiền, earned, uy tín và cấp nâng cấp giữ qua Ngày. Oxy và Máu hồi đầy theo cấp có hiệu lực, giỏ làm mới và kho dư bị bỏ sau Shop.
Trong day, khách chọn đều theo seed từ các id món trong kế hoạch có đủ nguyên liệu sau khi trừ phần đang giữ. Số suất trong kế hoạch dùng để tính mục tiêu thu gom. Khách có thể gọi tiếp món đủ nguyên liệu kể cả khi đã bán đủ số suất dự kiến. Quán chạy riêng dùng cả 6 món. Có bàn mà thiếu món thì no_dish. Không có thưởng riêng khi lấy đủ danh sách.
Ngày chỉ hoàn tất khi Shop đóng, kể cả Ngày cuối. Một Ngày không pause dài tối đa 22.200 tick. Shop có thể đóng sớm.
Ngày	Món và số suất kế hoạch	Nguyên liệu cần	Số ô cần (thực tế nếu bắt theo đàn)
D1	ca_loc_nuong_trui ×3, goi_bong_sung ×3	ca_loc ×3, bong_sung ×6	9
D2	ca_loc_nuong_trui ×2, lau_ca_linh_dien_dien ×2	ca_loc ×2, ca_linh ×6, bong_dien_dien ×2	10
D3	goi_bong_sung ×2, canh_chua_ca_loc ×2, ca_keo_nuong ×2	bong_sung ×4, ca_loc ×2, bong_dien_dien ×2, ca_keo ×4	12
D4	lau_mam ×1, ca_loc_nuong_trui ×2, goi_bong_sung ×1	ca_linh ×2, ca_keo ×1, keo_neo ×1, bong_dien_dien ×1, ca_loc ×2, bong_sung ×2	9 (11)
D5	lau_mam ×1, lau_ca_linh_dien_dien ×1, ca_loc_nuong_trui ×1	ca_linh ×5, ca_keo ×1, keo_neo ×1, bong_dien_dien ×2, ca_loc ×1	10 (12)
Shop và nâng cấp
ID	Nâng cấp	Cấp 1	Cấp 2
oxygen	Bình oxy	200 → 45 s (2.700 tick)	400 → 60 s (3.600 tick)
hp	Áo phao (thêm Máu)	250 → 4 Máu	500 → 5 Máu
Nâng cấp theo dữ liệu, mua cấp kế tiếp một lần mỗi cấp. Đủ đúng giá vẫn mua được. Trừ vào money, giữ earned và điểm. Cấp vừa mua hiển thị ngay, có hiệu lực từ Ngày kế tiếp. Không đủ tiền hoặc đã tối đa thì buy_failed, tiền và cấp giữ nguyên. Shop chờ shop_done hoặc tự đóng sau 600 tick hoạt động.

Menu, pause và HUD
Menu chính có Chơi và Thoát. DayIntro hiện Ngày và danh sách Má Tư đọc, tự chuyển sau 4 s hoặc khi nhấn phím. EveningIntro hiện số lượng nhập kho và món nấu được. DayResult hiện khách đã phục vụ/bỏ đi, tiền, boa và thay đổi uy tín. Summary hiện tổng tiền, tổng điểm, uy tín, món bán chạy.
Esc/P tạm dừng. Menu pause làm mờ nền, có Tiếp tục và Về menu, thêm Cài đặt nếu có mở rộng. Dừng đồng hồ và mọi timer gameplay, kể cả trong Shop.
HUD sáng có Máu, oxy (dưới 25% đổi màu/nhấp nháy), thời gian (đổi màu còn ≤ 30 s), độ sâu, giỏ theo loại, danh sách cần lấy và hồi bắt. Hiện gợi ý hái/cập bến khi đến gần, “Thủy quái!” cùng viền tím khi có thủy quái gần và “Hết hơi!” khi oxy cạn. HUD quán có đồng hồ ca, tiền ca và uy tín, món và kiên nhẫn tại từng bàn (đổi màu khi < 25%), tiến độ bếp/trạng thái món chín, món đang cầm và kho khả dụng. Chữ không chân ≥ 18 px ở 1280×720.
Trên máy chấm, headless một Ngày không pause (≤ 22.200 tick) chạy ≤ 20 s. Bản chơi thường đạt trung bình ≥ 30 FPS ở 1280×720.
3. Mở rộng
Kỳ vọng tính cả buổi lab. Nhóm 4 người không bắt buộc, nhóm 5 hoàn thành ít nhất 1 mục, nhóm 6 ít nhất 2 mục. Hoàn thành lõi trước. Ghi mục đã làm trong README, kèm bằng chứng. Với các mục có mã trong Test Contract, khai mã ở extensions tại gốc manifest.

Tự do sáng tạo. Khi lõi đã đúng, nhóm có thể thêm ý tưởng riêng, như món ăn hoặc câu chuyện. Tắt phần tự thêm ở headless hoặc giữ nguyên kết quả theo Test Contract. Ghi vào mục “Sáng tạo của nhóm” trong README.md, kèm bằng chứng ngắn cho thấy lõi vẫn đúng.

Mở rộng	Luật
Lao xua + weapon	Q (attack), cần mua cấp 1. Hồi 3 s (180 tick) từ lần dùng hợp lệ, kể cả không trúng. Cấp 1 giá 300, bán kính 4 m, choáng 2 s. Cấp 2 giá 600, bán kính 6 m, choáng 3 s. Duyệt mục tiêu theo id, đẩy mỗi con 3 m ra xa (chặn mép, trùng tâm dùng +x), choáng ghi đè recoil/choáng cũ. Đứng yên và không hit trong 120/180 bước kể cả bước bị Lao. Hết choáng về patrol ở vị trí sau đẩy.
Vợt hút cá + net	Cấp 1 giá 250, 4.0 m, tối đa 2 đàn/lần. Cấp 2 giá 500, 6.0 m, tối đa 3 đàn/lần. Từ cấp 1 duyệt theo id, đếm số đàn bắt thành công. Đàn thiếu chỗ phát hold_full và giữ lại, được xét đàn kế. Có đàn bắt thành công mới đặt hồi. Cấp 0 dùng luật gần nhất của lõi.
Rắn Hổ Mây (snake)	M3 từ Ngày 1, [72,14] ↔ [76,14], d ∈ [8,20]. Patrol 1.0 m/s, chase 3.5 m/s, phát hiện ≤ 8 m, rời chase khi > 16 m hoặc người chơi lên d < 8. Dùng luật chạm/recoil chung và ngưỡng độ sâu của loài.
Cháy món (burn)	burn_s: 20. Nếu ready_ticks > 1200, bỏ món, nguyên liệu mất, bếp rảnh ngay. Thử giữ lại ngay cho đơn. Đủ thì reserved, nếu thiếu thì unfulfillable, khách tiếp tục chờ tới hết kiên nhẫn. Đúng 1.200 tick vẫn bưng được.
Chợ Chú Sáu (vendor)	Trong Shop, bán cá lóc với giá 20, cá linh 8, cá kèo 10 và mỗi loại bông điên điển, bông súng, kèo nèo 5. Giá mua floor(giá bán × 1.5), hàng bán cho người chơi không giới hạn. Mỗi lệnh một đơn vị. Tiền bán cộng money và earned. Hàng mua chờ nhập thẳng vào kho quán tối Ngày kế, tách khỏi gather_end.inventory.
Sổ tay & Cá Hô (ca_ho)	Một con H1, 1.0 m/s. Chọn vị trí từ các điểm sinh chuẩn d ≥ 10 theo seed. Bơi trong x ∈ [4,96], d ∈ [10,30], phản xạ mép như cá thường. Một cạnh bắt hợp lệ trúng Cá Hô thì phát released sau event bắt cá thường, không thêm hàng và không tự đặt hồi. F (photo) trong ≤ 6 m cộng 0.5 uy tín, một lần/Ngày. Sổ tay ghi 8 loài đã gặp.
Settings & âm thanh	Âm lượng Master/Music/SFX lưu được giữa các lần mở game.
4. Test Contract v1.1 — Thay đổi từ v1.0
4.1. CLI và manifest
<headless_cmd> --mode gather|quan|day --seed <int>
  [--scenario <file.json>] [--inputs <file.json>]
  [--inventory <file.json>] [--inventory-out <file.json>]
  [--days <N>] --ticks <N> --out <file.jsonl> [--snapshot-every <N>]
--days chỉ với day, số nguyên từ 1 đến 5, mặc định 1. day tự bàn giao theo schema kho đếm ở v1.0, có thể truyền trong bộ nhớ. Hai cờ file kho vẫn dành cho hai mode độc lập.

Đặt contract_version: "1.1", dùng số chuẩn và dữ liệu mục 1–2. Bảng dưới liệt kê các khóa thêm hoặc đổi.

Phạm vi	Khóa
gather	fish_initial là số 8. Thêm fish_speed,fish_turn_ticks,fish_max,fish_spawn_ticks,fish_spawn_clearance,fish_x,fish_depths,fish_spawn_x,fish_spawn_depths,fish_weights. Các map theo loài và fish_yield có đủ 3 loài. fish_x là miền x, fish_spawn_x là danh sách x. Thêm nút N5/N6.
gather.monsters	species.ca_sau {patrol_speed,chase_speed,detect_radius,exit_radius,depths,hit_radius,recoil_ticks,recoil_dist}, spawns[] {id,kind,pos,waypoints,from_day} và invuln_ticks:90,loss_ratio:0.5.
quan, menu	Thêm B2, T2–T4 và 3 món mới.
day_plan	Mảng 5 object {day,dishes,ingredients}. dishes và ingredients là map id → số nguyên dương. Tính ingredients bằng tổng công thức nhân số suất.
shop	{max_ticks,upgrades}. upgrades.oxygen[] {level,price,oxygen_max_s}, upgrades.hp[] {level,price,hp_max}, mảng theo cấp.
Mở rộng	weapon: gather.weapon_cooldown_s, shop.upgrades.weapon[] {level,price,weapon_radius,stun_s} · net: shop.upgrades.net[] {level,price,catch_radius,max_schools} · snake: gather.monsters.species.ran cùng schema loài, thêm M3 vào spawns · burn: quan.burn_s hữu hạn · vendor: shop.vendor {buy_multiplier,sell_prices} · ca_ho: gather.ca_ho {count,speed,depths,photo_radius,reputation_bonus,bonus_per_day}.
4.2. Inputs và pause
Các nút boolean mới gồm pause ở cả ba mode, shop_done trong Shop, attack và photo trong gather khi bật mở rộng tương ứng. Chỉ tác động ở cạnh lên. Giữ nút qua đổi pha không tạo cạnh mới.
buy là chuỗi khác rỗng, chạy chỉ tại frame khai báo. Nhận oxygen, hp và các mở rộng weapon, net, buy:<kind>/sell:<kind> (Chợ). Shop phát buy_failed nếu gặp lệnh không hỗ trợ. Nút đúng kiểu nhưng sai pha hoặc mở rộng chưa bật thì bỏ qua.
Xét cạnh pause trước. Bước vào pause chỉ tăng tick ngoài, cập nhật chốt và phát paused. Khi còn pause, bỏ qua cạnh hành động và buy. sim_tick, phase_tick, lịch và timer đứng yên. Cạnh lên tiếp theo phát resumed, chạy gameplay ngay trong bước đó.
4.3. Scenario
day nhận gather và quan làm mẫu khởi tạo mỗi Ngày. Khối day {money,earned,reputation,upgrades,day_plan} dựng trạng thái xuyên Ngày. Mặc định tiền và earned 0, uy tín theo tuning, cấp là {} và kế hoạch theo preset. Cần 0 ≤ money ≤ earned, khai cả hai khi có tiền đầu kỳ. day.day_plan ghi đè theo số Ngày, mỗi mục có dishes. Tính lại ingredients và so với giá trị khai nếu có.
Cấm quan.stock và quan.reputation khi chạy day. Dùng gather.hold để dựng hàng. Kho, khách, bếp và món thuộc kế hoạch được kiểm trên kho thực lúc mở quán, mâu thuẫn → mã 2.
gather.player thêm invuln_ticks và attack_cd_ticks nếu bật Lao. gather.fish[] thêm age_ticks (mặc định 0), số bước cá đã tham gia bơi. random_fish:false tắt cá mặc định, bơi và sinh, cá fixture đứng yên. Khai fish khi cờ bật thì thay đàn ban đầu, vẫn bơi/sinh.
gather.monsters[] thay danh sách mặc định, nhận {id,kind,pos,waypoints,target_idx,state,state_ticks_left,recoil_dir}. Hai waypoint, target_idx 0 hoặc 1 (mặc định 1), state mặc định patrol. recoil_dir là vector đơn vị khi recoil, mặc định null ở trạng thái khác. recoil/stunned cần timer dương. Bỏ mảng thì dùng bố trí đúng Ngày.
Nếu bật Sổ tay, gather.ca_ho là {id,pos,heading_deg,photographed} hoặc null, thay con tự sinh. Mặc định hướng 0°, ảnh false. random_ho:false tắt sinh và di chuyển tự động. Nếu bật cháy, quan.stoves[].ready_ticks dựng tuổi món chín.
Ví dụ mở một Ngày đã có tiền và kho mang về. Tương tác lúc ở bến sẽ đóng ca sáng ngay.

{"day":{"money":200,"earned":200},"gather":{"hold":["ca_loc","bong_sung","bong_sung"],"random_fish":false}}
4.4. Output
Snapshot thêm state:"paused". Gather thêm monsters[], player.invuln_ticks, player.attack_cd_ticks nếu có Lao, ca_ho (object hoặc null) nếu có Sổ tay. Trong day, snapshot mọi pha có day,day_plan,upgrades,active_upgrades. Hai map cấp lần lượt là cấp đã mua và cấp đang áp dụng. phase là gather, quan hoặc shop. Snapshot Shop có stock dư từ ca và time_left_ticks tới lúc đóng. Snapshot đổi pha ghi pha mới với phase_tick:0. Event kết thúc mang pha cũ. Vỏ event bật chế độ day có thêm day.

name	data
monster_hit	monster_id,hp,lost,pos (vị trí người chơi, lost là mảng kind theo LIFO).
fish_spawned	id,kind,pos khi sinh theo lịch.
faint	Thêm cause:"monster" nếu do bị chạm, lost liệt kê phần giỏ còn lại, hp:0.
day_start, phase_start	{}.
day_plan	dishes,ingredients của Ngày đó.
paused, resumed	{}.
bought	upgrade,level,price,money.
buy_failed	action,reason (funds/max_level/out_of_stock/unknown).
shop_end	reason (done/time).
attack, monster_stunned (Lao)	pos,monster_ids (theo id) / monster_id,pos,stun_ticks sau đẩy.
photo, released (Sổ tay)	id,reputation sau cộng / id.
dish_burnt (Cháy)	stove_id,order_id,dish_id,order_status sau xử lý.
vendor_trade (Chợ)	action (buy/sell), kind,price,money.
{"type":"event","tick":0,"phase":"gather","day":1,"name":"day_plan","data":{"dishes":{"ca_loc_nuong_trui":3,"goi_bong_sung":3},"ingredients":{"ca_loc":3,"bong_sung":6}}}
Dòng end của day thêm days_completed (số Shop đã đóng). Hoàn thành đủ Ngày thì reason:"days_complete".

4.5. Thứ tự xử lý bổ sung
Gather. Đồng hồ, cooldown, giảm bất tử và hồi nút → bơi, oxy, ngạt → Lao nếu có, cập nhật quái theo id rồi xét tối đa một hit → tương tác (bến trước hái) → bắt cá theo vị trí cá trước khi bơi, rồi ảnh nếu có → xét hết giờ. Nếu còn giờ thì cá bơi, sinh thêm theo lịch, rồi cập nhật Cá Hô nếu bật. Khi Máu về 0, xử lý faint rồi gather_end(fainted) ngay sau choke hoặc monster_hit và bỏ các bước còn lại. Tại cùng tick, ngạt có thể đi trước hit rồi mới xét hết giờ. Cập bến vẫn ưu tiên trước bắt cá và hết giờ nếu còn Máu.
Quán. Giữ thứ tự v1.0. Nếu bật cháy, xét món chín/cháy theo id bếp trước di chuyển và tương tác. Trong day, lọc menu theo id món trong kế hoạch trước khi lọc nguyên liệu khả dụng.
Đổi pha. day_start → day_plan → phase_start(gather). Sau gather_end dựng quán và phát phase_start(quan) cùng tick, kể cả khi ngất. Sau quan_end dựng Shop và phát phase_start(shop) cùng tick. Pha mới chỉ chạy gameplay từ bước sau.
Shop. Xử lý một buy trước cạnh shop_done, kể cả bước cuối. Đóng bằng nút ở bước cuối phát shop_end(done). Tự hết giờ phát shop_end(time). Đóng Shop thì tăng days_completed, kết thúc hoặc dựng Ngày kế ngay tick đó. Chỉ khi dựng Ngày mới mới sao cấp đã mua sang active_upgrades.
5. Quy trình nhóm và lịch gợi ý
Nhóm tự chọn cách phối hợp và cùng commit vào fork chung bằng tài khoản GitHub của từng người. Gợi ý làm song song (1) số chuẩn và cá bơi/sinh, (2) Cá Sấu, Máu và ngất, (3) 2 bếp/4 bàn, 6 món và kế hoạch ngày, (4) day, Shop, pause, menu và HUD. Dùng fixture cố định để người làm day tích hợp sớm với hai buổi đang có. Có thể kiểm chéo các lát, pair và đổi vai. Ghi Co-authored-by: khi cùng làm một commit.

Phút trong phase	Việc
0–5	Lên lại kế hoạch. So số chuẩn với giả định cũ, chốt giao diện chuyển pha, chia người và phần phụ thuộc theo AC-P2-xx. Ghi ở nơi nhóm tiện theo dõi.
5–20	Build và kiểm thử bốn lát, cập nhật hợp đồng v1.1 và cấu hình/dữ liệu chuẩn. Chuẩn bị ca smoke.
20	Chạy smoke tích hợp theo luồng gather --inventory-out → quan --inventory, có thể pair/mob. Đối chiếu snapshot kho ở tick 0 và lưu docs/proof/phase-2/integration.*. Standup 2–3 phút và điều người đã xong sang lát trễ.
20–35	Build tiếp, phối hợp giữa các lát và chốt luồng day.
35–45	Chạy smoke day --days 1, chạy nhiều Ngày để kiểm cấp nâng cấp và chạy regression P1 với số chuẩn. Lưu bằng chứng, hoàn thiện docs/verification/phase-2.md và gắn tag.
45–50	Retro nhanh. Ghi điều tốt, điều vướng và một hành động có người nhận trong docs/retro.md.
50–55	Dự phòng. Đẩy tag phase-2 chậm nhất 1:55.
Ghi lý do nếu test cũ cần cập nhật vì luật mới. Trong docs/verification/phase-2.md, nối từng AC với bằng chứng và kết quả chạy trên commit bàn giao. Cập nhật docs/clarify.md và docs/ai-usage-log.md.

Định nghĩa hoàn thành (DoD)
 contract_version:"1.1", tuning chuẩn, đủ 6 nguyên liệu và 6 món theo dữ liệu. Cá bơi/sinh, Cá Sấu, Máu/ngất, 2 bếp/4 bàn hoạt động đúng.
 Chơi trọn vòng ngày với menu, pause và HUD. --mode day công bố đúng kế hoạch D1–D5, chốt Ngày khi Shop đóng và áp đúng cấp oxygen/hp từ Ngày kế.
 Smoke tích hợp có bằng chứng. Regression P1 còn hiệu lực đạt với số chuẩn, test thay đổi có ghi lý do. docs/verification/phase-2.md và bằng chứng khớp commit gắn tag.
 Công việc các lát đã tích hợp trong fork chung, có bằng chứng đóng góp của từng người. Ghi chép làm rõ, nhật ký AI và retro đã cập nhật.
 Nếu làm mở rộng, README khai mục đã làm và có test/bằng chứng.
 Đẩy phase-2 trỏ tới commit bàn giao trên main chậm nhất 1:55.

 phase 3:
 Phase 3 · hạn tag phase-3 lúc 2:30 · phát hành 10:59

TICKET-03 — Change Request “Mùa Nước Nổi” (Phase 3)
35 phút (1:55–2:30) · Test Contract v1.2 · Hạn đẩy tag phase-3 2:30.

Tháng Tám âm lịch, nước lũ về, cá linh nhiều. Trời nóng làm nguyên liệu mau ươn. Khách hàng muốn biết độ tươi của từng nguyên liệu, từ lúc Út Sen lấy được đến khi đưa vào bếp. [THAY THẾ] đánh dấu các luật đổi so với bản đang chạy.

1. Lõi (mọi nhóm) — Độ tươi
[THAY THẾ] Kho đếm theo loại → kho cá thể
{"items":[{"id":"I1","kind":"ca_linh","fresh":100},{"id":"I2","kind":"ca_loc","fresh":97.5}]}
File có đúng khóa gốc items, giá trị là mảng cá thể {id,kind,fresh}. Kho rỗng là {"items":[]}. id là chuỗi duy nhất, khác rỗng, kind thuộc danh mục nguyên liệu, fresh hữu hạn trong [0,100]. Cấp I1,I2,… theo thứ tự vào giỏ, tiếp tục tăng xuyên pha và Ngày, kể cả khi cá thể trước đó đã dùng hoặc bỏ. LIFO khi mất hàng vẫn theo thứ tự vào giỏ.
Bên đọc chọn schema theo contract_version. Contract v1.2 trả mã 2 cho file kho đếm hoặc sai schema, kind lạ, id trùng, fresh ngoài miền. Kho quán nhận nguyên số lượng, id và độ tươi, kể cả hàng ươn. Sức chứa giỏ chỉ áp lên giỏ.
gather --inventory-out ghi đúng một lần khi có gather_end. Dùng file tạm cùng thư mục rồi thay thế nguyên tử. Ngất ghi kho rỗng. Nếu chạm giới hạn --ticks trước gather_end, giữ nguyên đường dẫn đích. Xuất file theo id, đủ độ chính xác khi đọc lại để giữ giá trị và nhánh ở ngưỡng 30. gather_end.data.inventory theo cùng schema.
Trong day, bàn giao trong cùng tick chuyển pha, hàng không hao thêm, ca quán chạy từ bước sau. Nếu có Chợ Chú Sáu, hàng mua nhập riêng vào kho quán Ngày kế với fresh:100, tách khỏi gather_end.inventory và dùng id mới. Hàng thô ở Shop hoặc chờ nhập không hao tươi. Khi người chơi bán, lấy cá thể chưa ươn tươi nhất của loại, hòa theo id.
Độ tươi, giữ chỗ và giá
Quy tắc	Cách xử lý
Hàng mới	fresh = 100 lúc bắt/hái, bắt đầu hao từ bước sau.
Hao tươi	Giỏ giảm 0.5/s, kho quán giảm 0.25/s kể cả hàng đang giữ chỗ. Mỗi giây 60 tick, kẹp đáy 0. Pause dừng hao tươi. Món chín không hao.
Ươn	fresh < 30, vẫn chiếm ô, không dùng nấu. Phát spoiled đúng một lần khi đi từ ≥ 30 xuống < 30. Nếu nhiều cá thể cùng vượt ngưỡng, phát theo id. So ngưỡng trước làm tròn.
[THAY THẾ] Giữ theo lượng → giữ theo id	Mỗi loại trong công thức lấy các cá thể khả dụng tươi nhất, hòa theo id. Nếu phần giữ có cá thể vừa ươn, nhả toàn bộ phần giữ của đơn và thử giữ lại đúng một lần. Xử lý các đơn bị ảnh hưởng theo order_tick rồi id bàn. Không đủ thì đơn thường chuyển unfulfillable, khách chờ tới hạn.
[THAY THẾ] Giá niêm yết → giá theo tươi	Khi bắt đầu nấu, tiêu đúng các id đang giữ và chốt base_price = floor(giá niêm yết × trung bình fresh của các cá thể dùng / 100). Nếu đủ điều kiện boa, áp floor(tiền món × 0.2) trên giá đã chốt. Điểm vẫn là earned + 100 × floor(reputation).
HUD	Cho người chơi đọc được độ tươi hoặc nhận ra hàng ươn bằng số, thanh, nhãn hoặc biểu tượng.
Dùng phép tính đủ chính xác ở ngưỡng 30 và phép floor. Ví dụ có thể dùng 240 đơn vị mỗi điểm tươi với các fixture biểu diễn chính xác, trừ 2 đơn vị/tick ở gather và 1 đơn vị/tick ở quán.

Thứ tự trong tick
Gather. Đồng hồ, cooldown, hồi nút và độ tươi của hàng có sẵn ở đầu bước → lịch dòng lũ nếu bật → bơi, oxy và ngạt → Lao nếu có, rồi thủy quái/hit → bến trước hái → bắt cá rồi ảnh nếu có → xét hết giờ, nếu còn giờ mới cập nhật cá và sinh thêm. Rơi hàng theo LIFO. Khi ngất, bỏ toàn bộ phần còn lại theo LIFO rồi phát faint, gather_end(fainted).
Quán. Đồng hồ và timer → hao tươi kho thô, phát hết spoiled theo id rồi mới xử lý giữ chỗ bị ươn → xét món chín/cháy nếu có theo id bếp → di chuyển và tối đa một tương tác → thanh toán, kiên nhẫn/đóng ca → nếu còn giờ, xử lý đặt trước nếu có rồi tới khách thường. Giao đúng tick kiên nhẫn chạm 0 vẫn hợp lệ. Giao đúng tick kết thúc ca được trả ngay.
Contract v1.2
[THAY THẾ] Đặt contract_version:"1.2". Thêm freshness {initial,gather_decay_per_s,quan_decay_per_s,spoiled_below} với các giá trị lần lượt 100, 0.5, 0.25 và 30.

Scenario. gather.hold và quan.stock là mảng cá thể. Trong day, Ngày đầu giữ nguyên id trong mẫu gather.hold, các Ngày kế cấp id mới theo thứ tự mảng với kind/fresh ban đầu. customers[].reserved là mảng id cá thể. Id vật lý duy nhất giữa các nơi chứa. Phần giữ phải trỏ tới cá thể chưa ươn trong kho, đủ công thức và không dùng chung với đơn khác. Bỏ reserved cho đơn reserved thì cấp theo order_tick rồi id bàn, lấy tươi nhất rồi id nhỏ. Sai hoặc mâu thuẫn → mã 2. Payload món giữ cấu trúc, base_price là giá đã chốt theo fresh.
JSONL. Snapshot hold, stock (quán và Shop) và customers[].reserved theo schema trên. cook_started.data.items là mảng cá thể sắp theo kind rồi id. lost trong monster_hit/faint là mảng cá thể theo thứ tự bỏ LIFO. Event mới spoiled có item_id,kind,location (hold/stock). Dung sai quan sát độ tươi ±0.01. Dùng trạng thái/event để kiểm nhánh ở ngưỡng. Tick của event biên phải chính xác.
Dùng scenario sau để kiểm ngưỡng khi chạy gather một bước không input. Cá thể bắt đầu đúng fresh 30 nên ươn ở bước đầu.

{"gather":{"hold":[{"id":"I1","kind":"ca_linh","fresh":30}],"random_fish":false,"monsters":[]}}
{"type":"event","tick":1,"phase":"gather","name":"spoiled","data":{"item_id":"I1","kind":"ca_linh","location":"hold"}}
Để smoke bàn giao file, dùng cùng mẫu trên với fresh:100 và interact:true ở frame 0 để cập bến. Mở quan --inventory với file vừa ghi và --ticks 0. So chính xác id, kind và độ tươi của snapshot quán với file sau lần hao ở bước gather.

2. Mở rộng
Kỳ vọng tính cả buổi lab. Nhóm 4 người không bắt buộc, nhóm 5 hoàn thành ít nhất 1 mục, nhóm 6 ít nhất 2 mục. Chọn sau khi độ tươi và bàn giao kho đã chạy ổn. Nếu làm, khai mã trong extensions và ghi test/bằng chứng trong README.

Tự do sáng tạo. Khi lõi đã đúng, nhóm có thể thêm ý tưởng riêng, như khu vực hoặc sự kiện. Tắt phần tự thêm ở headless hoặc giữ nguyên kết quả theo Test Contract. Ghi vào mục “Sáng tạo của nhóm” trong README.md, kèm bằng chứng ngắn cho thấy lõi vẫn đúng.

Dòng nước lũ (current)
Quy tắc	Cách xử lý
Lịch	Với t = 1800·k (k ≥ 1), báo trước ở t−120 bằng chữ, biểu tượng và âm thanh. Bắt đầu trước di chuyển ở t và kéo dài 480 tick (8 s), từ t đến t+479.
Hướng và lực	Chọn đều +x hoặc −x theo seed khi bắt đầu. Cộng 1.5 m/s vào người chơi nếu d đầu bước ≥ 10, rồi chặn mép. Đàn cá và thủy quái giữ chuyển động riêng, lực dòng không tích lũy vào player.vel.
Kết thúc	Phát current_end(elapsed) trước di chuyển ở t+480. Nếu ca kết thúc trước, phát current_end(phase_end) trước faint nếu có và trước gather_end. Bước bắt đầu dòng trùng bước cuối ca vẫn có lực. Giới hạn CLI chỉ cắt mô phỏng tại trạng thái hiện có.
Manifest thêm gather.current {interval_ticks,duration_ticks,warning_ticks,min_depth,speed}. Scenario nhận gather.random_current:false để tắt lịch hoặc current_direction:-1/1 để khóa hướng khi chạy lịch. Snapshot gather có current:null hoặc {direction,ticks_left}, đếm cả tick hoạt động vừa chụp.

Event	data
current_warning	starts_at_phase_tick.
current_start	direction,duration_ticks.
current_end	direction,reason (elapsed/phase_end).
Khách đặt trước (reservations)
Mỗi Ngày công bố 2 đơn R1,R2 sau phase_start(gather) theo id. HUD sáng hiện hai đơn. Chọn hai bàn khác nhau, món trong kế hoạch, tick đến theo seed trong [1800,10799], có thể cùng tick. Quán độc lập công bố lúc dựng pha và dùng menu đầy đủ.
Trạng thái scheduled → holding → waiting → served hoặc failed. Giữ bàn từ max(0, arrival_tick − 1800). Nếu giữ từ tick 0, thể hiện ngay trong snapshot dựng quán. Khách thường đang ngồi có thể ở lại, khách mới không ngồi bàn giữ. Khi còn giờ, cập nhật giữ bàn và xử lý khách đặt theo id trước lượt khách thường.
Đến giờ mà bàn còn khách thì fail occupied. Bàn trống nhưng thiếu kho thì fail stock. Đến thành công giữ nguyên liệu ngay, phát reservation_arrived rồi customer_arrived. Kiên nhẫn 60 s. Giá cuối floor(giá đã chốt theo fresh × 1.5), rồi mới tính boa. Giao thành công phát served rồi reservation_served.
Lỡ đơn do stock, occupied, burnt, patience hoặc closing thì nhả hàng/bàn, hủy món, uy tín −1 đúng một lần. reservation_failed thay nhánh rời do thất bại, không cộng phạt khách thường. Nếu phần giữ vừa ươn và giữ lại không đủ thì fail stock. Nếu món cháy, phát dish_burnt với order_status:"failed" trước reservation_failed. Khi đóng ca, fail các đơn chưa phục vụ/chưa fail theo id đặt. served và failed là trạng thái cuối.
Manifest thêm reservations {count,table_hold_s,price_multiplier,failed_reputation_delta} lần lượt 2, 30, 1.5, −1. Scenario nhận quan.reservations[] {id,table_id,dish_id,arrival_tick}. Mảng tường minh thay toàn bộ danh sách, tối đa hai đơn, bàn khác nhau, tick đến nguyên dương nhỏ hơn thời lượng ca chuẩn, có thể sau giờ đóng nếu fixture rút ngắn ca. quan.random_reservations:false tắt tự sinh. Snapshot gather trong day và quán có reservations[] kèm state. Snapshot quán thêm customers[].reservation_id và tables[].reservation_id, dùng null khi không có.

Event	data
reservation_announced	reservation_id,table_id,dish_id,arrival_tick.
reservation_arrived	reservation_id,order_id.
reservation_served	reservation_id,order_id,base_price đã nhân hệ số và làm tròn xuống.
reservation_failed	reservation_id,reason,reputation.
3. Quy trình nhóm
Nhóm tự chọn cách phối hợp và cùng commit vào fork chung bằng tài khoản GitHub của từng người. Ghi Co-authored-by: khi cùng làm một commit.

Gợi ý dùng 7 phút đầu để lên lại kế hoạch và chia lát. Phân tích tác động lên module, file và test. Ghi quyết định đổi schema kho, cách chuyển và thứ tự tích hợp để main vẫn chạy được. Có thể ghi trong README.md, docs/clarify.md, ADR hoặc nơi khác trong repo chung. Dưới đây là mẫu ghi tác động.

Module	File cần đổi	Test bị ảnh hưởng	Người phụ trách
Adapter, Lặn, Quán, day, HUD hoặc QA	Ghi file thực tế	Ghi test giữ, đổi hoặc thêm	Ghi người nhận
Gợi ý tích hợp schema/adapter và test migration trước. Làm Lặn, Quán và HUD song song theo schema đã chốt. Có thể hỗ trợ hai phiên bản nội bộ trong lúc chuyển và bật v1.2 khi cả hai đầu bàn giao đã sẵn sàng. Khi chạy v1.2, file kho đếm trả mã 2.

Gợi ý chạy smoke bàn giao kho trên bản tích hợp ở phút 20, có thể pair. Standup 2–3 phút để điều người đã xong sang lát đang trễ. Nếu có retro nhanh, ghi điều rút ra từ lần đổi kho trong docs/retro.md.

Ghi breaking change, schema mới và cách cập nhật fixture vào CHANGELOG.md. Trên main, kiểm cả file và day, rồi chạy lại regression P1–P2 còn hiệu lực. Ghi lý do nếu test cũ bị thay bởi luật mới. Lưu bằng chứng trong docs/proof/phase-3/ và ghi AC-P3-xx → bằng chứng → kết quả trong docs/verification/phase-3.md. Cập nhật docs/clarify.md và docs/ai-usage-log.md.

Lịch gợi ý
Phút trong phase	Việc
0–7	Phân tích tác động, ghi quyết định đổi schema, chốt thứ tự tích hợp và chia lại việc.
7–25	Viết schema/adapter, Lặn, Quán và HUD song song. Tích hợp theo thứ tự đã chốt. Phút 20 chạy smoke kho, standup và hỗ trợ lát trễ.
25–32	Bật v1.2 trên bản tích hợp, smoke hai tiến trình và day, chạy regression, chốt CHANGELOG, bằng chứng và tag. Retro nhanh.
32–35	Dự phòng. Đẩy phase-3 chậm nhất 2:30.
Định nghĩa hoàn thành (DoD)
 Contract v1.2 bàn giao kho cá thể qua file và trong day. Kho đếm trả mã 2. Id, độ tươi, hàng ươn, giữ chỗ, giá và JSONL đúng luật.
 HUD cho thấy độ tươi hoặc hàng ươn. Có test qua ngưỡng, thử giữ lại khi hàng vừa ươn, chốt giá và bàn giao.
 Có ghi tác động, quyết định đổi schema và thứ tự tích hợp giữ main chạy được. Các lát đã tích hợp trong fork chung, có bằng chứng đóng góp của từng người.
 CHANGELOG.md ghi breaking change, regression còn hiệu lực đạt, test thay đổi có lý do. docs/verification/phase-3.md và bằng chứng khớp commit gắn tag. Ghi chép làm rõ và nhật ký AI đã cập nhật.
 Nếu làm mở rộng, có test và bằng chứng cho từng mục.
 Đẩy phase-3 trỏ tới commit bàn giao trên main chậm nhất 2:30.

 phase 4:
 Phase 4 · hạn tag phase-4 lúc 3:00 · phát hành 11:29

TICKET-04 — Phát hành v1.0.0 (Phase 4)
30 phút (2:30–3:00) · Test Contract v1.3 · Hạn đẩy tag phase-4 và công bố GitHub Release v1.0.0 3:00.

Đo hiệu năng của cảnh lặn, kiểm tra cách người chơi nhận cảnh báo, bàn giao bản chạy được từ repo sạch và tổng kết cách nhóm đã làm việc.

1. Lõi (mọi nhóm)
Benchmark có render
<bench_cmd> --seed 42 --duration 30 --out bench.json
Cấu hình	Giá trị
Cảnh đo	Buổi sáng lõi với độ tươi, cá bơi, Cá Sấu Năm Chèo và hiệu ứng mặc định. Út Sen đứng yên ở bến.
Seed	42.
Cửa sổ	1280×720.
Làm nóng / đo	Làm nóng 3 s, sau đó đo 30 s.
Runner gọi <bench_cmd> --seed <int> --duration <giây> --out <bench.json>. Xuất năm trường JSON. Các số sau minh họa định dạng.

{"avg_fps":72,"p1_low_fps":38,"frames":2160,"measured_s":30,"load_ms":2400}
Trường	Cách tính
frames,measured_s	Số khung hình và số giây thực tế trong khoảng đo sau làm nóng.
avg_fps	frames / measured_s.
p1_low_fps	Chọn max(1,ceil(0.01 × frames)) khung chậm nhất rồi lấy nghịch đảo thời gian trung bình của chúng, tính thời gian theo giây.
load_ms	Mili giây từ lúc khởi chạy đến khung hình đầu tiên của cảnh đo.
Điểm phần benchmark dựa trên việc chạy được lệnh và tạo đúng bench.json. Mốc avg ≥ 60 FPS, 1% low ≥ 30 FPS và load ≤ 10 s dùng để báo cáo. Lưu artifact từ commit nộp trong docs/proof/phase-4/.

Cảnh báo dễ nhận biết
Dùng chữ hoặc biểu tượng để người chơi nhận ra thủy quái gần, oxy sắp hết và khách sắp giận. Thêm chế độ tương phản cao và chơi thử cả ba cảnh báo ở chế độ đó.

Đóng gói và phát hành
Từ clone sạch, chạy được bản có giao diện theo README.md trong tối đa 3 lệnh trên macOS hoặc Linux. Ghi yêu cầu môi trường, điều khiển, lệnh test, lệnh headless và benchmark.
Đính kèm bản đóng gói chạy được ở GitHub Release v1.0.0. Release notes do nhóm viết, nêu điểm mới, cách chạy và giới hạn đã biết. CHANGELOG.md ghi theo từng phase. Rà CREDITS.md và LICENSE cho tài sản đã dùng.
Đặt contract_version:"1.3", khai bench_cmd và soak_cmd ở gốc game.contract.json. Gameplay, tuning, kho và JSONL theo v1.2.
2. Soak headless (giảng viên chạy để báo cáo)
<soak_cmd> --seed 7 --days 10 --out soak.json
Lệnh nhận --seed <int> --days <N> --out <soak.json>. Giảng viên chạy 10 Ngày trong một tiến trình headless bằng script input hoặc bot tất định. Mỗi Ngày đi qua gather → quan → shop. Kế hoạch D1–D5 lặp ở Ngày 6–10. Tiền, tổng thu, uy tín, cấp nâng cấp, số Ngày và id cá thể tiếp tục xuyên suốt.

soak.json có days,days_completed,crashes,results,duration_s. Mỗi phần tử results[] có day,earned,reputation,score tại lúc Shop đóng.
Phép thử đạt khi days_completed = days và crashes = 0. So tính lặp ở các trường gameplay, bỏ số đo thời gian thực khi so. Không chấm ngưỡng bộ nhớ.
3. Mở rộng
Kỳ vọng tính cả buổi lab. Nhóm 4 người không bắt buộc, nhóm 5 hoàn thành ít nhất 1 mục, nhóm 6 ít nhất 2 mục. Nếu làm, ghi vào README và lưu bằng chứng.

Tự do sáng tạo. Khi lõi đã đúng, nhóm có thể hoàn thiện ý tưởng riêng, như đồ họa, âm nhạc hoặc giao diện. Tắt phần tự thêm ở headless hoặc giữ nguyên kết quả theo Test Contract. Ghi vào mục “Sáng tạo của nhóm” trong README.md, kèm bằng chứng ngắn cho thấy lõi vẫn đúng.

Bảng xếp hạng cục bộ (leaderboard)
Khai leaderboard trong extensions. Lưu bền vững top 10 cục bộ. Chỉ ghi một mục cho mỗi lượt chuẩn đủ 5 Ngày. Sắp điểm giảm dần, hòa thì mục ghi trước đứng trước, kể cả sau khi mở lại.
<run_cmd> --export-leaderboard <out.json> [--leaderboard <store.json>] xuất bảng đã sắp. Mỗi mục có name,score,days_completed,seed. Tên Unicode khác rỗng.
{"entries":[{"name":"Út Sen","score":300,"days_completed":5,"seed":42}]}
Headless mode day nhận cặp --leaderboard <store.json> --player-name <name>. Ghi đúng một mục khi chạy đủ 5 Ngày chuẩn, không scenario và reason:"days_complete". Thiếu một cờ trong cặp hoặc sai mode thì mã 2. Chạy test với store riêng. File xếp hạng không đổi JSONL. Soak không ghi xếp hạng.
Phụ đề SFX
Hiện phụ đề cho các hiệu ứng âm thanh đã triển khai. Chơi thử với âm thanh tắt để kiểm phụ đề có hiện đúng lúc.

4. Quy trình nhóm
Nhóm tự chọn cách phối hợp và cùng commit vào fork chung bằng tài khoản GitHub của từng người. Ghi Co-authored-by: khi cùng làm một commit.

Lên lại kế hoạch theo việc còn lại. Có thể chia hoặc kiêm các vai dưới đây và ghi phân công ở nơi nhóm tiện theo dõi.

Vai	Việc
Đóng gói	Thử từ clone sạch, ghi lệnh chạy, tạo bản phát hành.
Bench/QA	Chạy bench và regression, lưu artifact và ma trận ở docs/verification/phase-4.md.
Release/Integrator	Kiểm commit bàn giao, viết release notes, rà CHANGELOG, gắn tag và công bố Release.
Điều phối retro	Rà hành động đã chốt ở retro P2 và tổng hợp bằng chứng đóng góp.
Ghi AC-P4-xx → bằng chứng → kết quả chạy trên commit bàn giao trong docs/verification/phase-4.md. Cập nhật docs/clarify.md và docs/ai-usage-log.md.

Mở đầu retro bằng việc rà lại hành động đã chốt ở P2, xem nhóm đã làm gì, còn vướng gì và vì sao. Ghi điều làm tốt, điều cần sửa và hành động tiếp theo trong docs/retro.md. Nêu một lỗi AI đã mắc và cách nhóm xác minh.

Mỗi người viết docs/members/<handle>.md (≤ 200 từ), nêu phần mình làm, đã giúp ai, AI sai ở đâu và bài học. Dẫn commit hoặc bằng chứng liên quan trong repo chung. Đánh giá cá nhân dựa trên bằng chứng đóng góp, phản tư và đánh giá chéo. Số PR và lượt review không dùng để chấm cá nhân.

Đẩy phase-4 và công bố Release v1.0.0 từ cùng commit bàn giao trên main trước khi hết giờ build.

Lịch gợi ý
Phút trong phase	Việc
0–15	Đo bench, cập nhật cảnh báo và tương phản, thử clone sạch, chạy regression và chuẩn bị Release song song.
15–25	Retro và phản tư cá nhân. Phút 20 standup, rà vướng mắc và điều người đã xong sang hỗ trợ. Có thể pair chạy smoke trên bản tích hợp.
25–30	Dự phòng và kiểm commit, artifact, tag, Release. Hạn đẩy phase-4 và công bố v1.0.0 3:00.
Định nghĩa hoàn thành (DoD)
 Contract v1.3 khai đúng lệnh. bench_cmd chạy cảnh chuẩn và tạo bench.json đúng cấu trúc. soak_cmd sẵn sàng cho runner lớp.
 Clone sạch chạy bằng tối đa 3 lệnh. Ba cảnh báo có chữ hoặc biểu tượng và chế độ tương phản cao hoạt động.
 Regression P1–P3 còn hiệu lực đạt. docs/verification/phase-4.md và bằng chứng khớp commit gắn tag. Ghi chép làm rõ và nhật ký AI đã cập nhật.
 CHANGELOG.md, release notes và bản đóng gói đầy đủ. Tag phase-4 và GitHub Release v1.0.0 cùng trỏ tới commit trên main, chậm nhất 3:00.
 Retro đã rà hành động P2 và chốt việc tiếp theo. Có phản tư cá nhân đủ người và bằng chứng đóng góp của từng người trong repo chung để đánh giá chéo.
 Nếu làm mở rộng, có bài kiểm và bằng chứng cho từng mục.
Demo sau giờ build
Sau 3:00, demo trực tiếp hoặc nộp video .mp4 dưới 5 phút. Cả hai hình thức dùng cùng checklist.

 Chơi một Ngày từ Lặn & Hái qua Mở Quán đến khi đóng Shop.
 Chạy test và cho thấy kết quả đạt.
 Chỉ ra bằng chứng chia việc, phối hợp và đóng góp của từng người trong repo chung.
 Mở ma trận truy vết và chỉ ra bằng chứng tương ứng.