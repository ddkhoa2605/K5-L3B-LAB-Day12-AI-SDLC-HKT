---
name: determinism-check
description: Chạy kiểm tra tính tất định (determinism) byte-by-byte cho chế độ headless gather và quan. Dùng sau mỗi PR và trước mỗi lần gắn tag phase.
---

# Skill: Determinism Check (Kiểm tra tính tất định)

> **Sở hữu:** Người 4 (QA Lead)  
> **Khi nào dùng:**
> 1. Sau khi bất kỳ Pull Request nào của `sim/gather` hoặc `sim/quan` được merge.
> 2. Trước mỗi mốc Code Freeze (T-10 phút) trước khi gắn tag `phase-1` đến `phase-4`.
> 3. Khi kiểm tra tính năng sáng tạo (`content`) để đảm bảo không làm lệch output headless.

## Cách chạy

Chạy script kiểm tra tất định:
```bash
python tools/check_determinism.py --mode gather --seed 1 --ticks 600
python tools/check_determinism.py --mode quan --seed 1 --ticks 600
```

Hoặc kiểm tra thủ công bằng PowerShell:
```powershell
python -m chonoi.headless --mode gather --seed 1 --ticks 600 --out run1.jsonl
python -m chonoi.headless --mode gather --seed 1 --ticks 600 --out run2.jsonl
$hash1 = (Get-FileHash run1.jsonl -Algorithm SHA256).Hash
$hash2 = (Get-FileHash run2.jsonl -Algorithm SHA256).Hash
if ($hash1 -eq $hash2) { Write-Host "PASS: Byte-identical" } else { Write-Host "FAIL: Mismatch" }
```

## Tiêu chí Đạt (Pass)
* Hai lần chạy với cùng `seed` và `ticks` phải tạo ra hai file JSONL có hash SHA256 hoàn toàn trùng khớp (giống nhau 100% từng byte).
* Lưu kết quả kiểm tra vào `docs/proof/phase-n/determinism.txt`.
