# Bằng chứng: thiết kế lại giao diện client (Người 3)

Phạm vi: chỉ `chonoi/web/index.html` và `README.md`. Không đổi luật, không đổi snapshot/JSONL, không đổi `game.contract.json`.

| Kiểm tra | Cách làm | Kết quả |
|---|---|---|
| Test tự động | `PYTHONPATH=tests:. python3 -m unittest discover -s tests` | 245 test OK (1 skipped) |
| Tất định | `python3 tools/check_determinism.py --mode gather` / `--mode quan` | 100% byte-identical cả hai |
| Benchmark có render | `python3 tools/bench.py --seed 42 --duration 30 --out docs/proof/ui-redesign/bench.json` (Chrome headless 1280×720) | [bench.json](bench.json): avg 59.97 fps, 1% low 52.8, load 1049 ms |
| Cảnh báo buổi lặn | Chơi thật (`--mode gather`): lặn sâu tới khi Năm Chèo chuyển `chase`, oxy dưới 25% | [canh-bao-lan-song.jpg](canh-bao-lan-song.jpg): "Sắp hết oxy! Ngoi lên thở", "Thủy quái Năm Chèo ở gần!", viền tím |
| Tương phản cao | Phím `H` trong cùng ván | [tuong-phan-cao-lan-song.jpg](tuong-phan-cao-lan-song.jpg) |
| Cảnh báo quán + hoạt cảnh | `--mode day`, cập bến ngay nên kho trống | [canh-bao-quan-hoat-canh.jpg](canh-bao-quan-hoat-canh.jpg): "Khách T4 sắp giận bỏ về!", khách đang ăn, hoạt cảnh công an bắt thằng phá quán |

**Ghi chú trung thực:** kho trống thì không có khách thật, nên ở ảnh quán hai khách (T2 đang ăn, T4 sắp hết kiên nhẫn) được **giả lập phía trình duyệt** bằng cách sửa phản hồi `/state` trong DevTools. Server và luật không bị đụng tới. Hoạt cảnh được gọi bằng `startSkit('thug')` thay vì chờ lịch ngẫu nhiên (~30–45 s).
