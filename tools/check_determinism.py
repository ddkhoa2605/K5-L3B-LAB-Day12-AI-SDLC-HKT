"""Công cụ kiểm tra tính tất định (Determinism Check) cho chế độ headless.
Người 4 (QA Lead) chạy công cụ này sau mỗi PR và trước mỗi lần gắn tag.

Cách dùng:
    python tools/check_determinism.py --mode gather --seed 1 --ticks 600
    python tools/check_determinism.py --mode quan --seed 1 --ticks 600
"""

import argparse
import filecmp
import hashlib
import os
import subprocess
import sys
import tempfile

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def run_headless(mode, seed, ticks, out_file):
    cmd = [
        sys.executable,
        "-m",
        "chonoi.headless",
        "--mode",
        mode,
        "--seed",
        str(seed),
        "--ticks",
        str(ticks),
        "--out",
        out_file,
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = f".{os.pathsep}{env.get('PYTHONPATH', '')}"
    env["PYTHONIOENCODING"] = "utf-8"
    res = subprocess.run(cmd, capture_output=True, text=True, env=env)
    return res.returncode, res.stdout, res.stderr


def file_sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def main():
    parser = argparse.ArgumentParser(description="Determinism byte-by-byte checker")
    parser.add_argument("--mode", choices=["gather", "quan"], required=True)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--ticks", type=int, default=600)
    args = parser.parse_args()

    with tempfile.TemporaryDirectory() as tmpdir:
        out1 = os.path.join(tmpdir, "out1.jsonl")
        out2 = os.path.join(tmpdir, "out2.jsonl")

        code1, _, err1 = run_headless(args.mode, args.seed, args.ticks, out1)
        if code1 != 0:
            print(f"ERROR: Run 1 failed with code {code1}:\n{err1}", file=sys.stderr)
            return 1

        code2, _, err2 = run_headless(args.mode, args.seed, args.ticks, out2)
        if code2 != 0:
            print(f"ERROR: Run 2 failed with code {code2}:\n{err2}", file=sys.stderr)
            return 1

        hash1 = file_sha256(out1)
        hash2 = file_sha256(out2)

        is_equal = filecmp.cmp(out1, out2, shallow=False)
        if is_equal and hash1 == hash2:
            print(f"[PASS] Determinism check ({args.mode}, seed={args.seed}, ticks={args.ticks}):")
            print(f"       SHA256: {hash1}")
            print("       Result: 100% byte-identical.")
            return 0
        else:
            print(f"[FAIL] Data mismatch between two runs ({args.mode})!", file=sys.stderr)
            print(f"       Run 1 SHA256: {hash1}", file=sys.stderr)
            print(f"       Run 2 SHA256: {hash2}", file=sys.stderr)
            return 1


if __name__ == "__main__":
    sys.exit(main())
