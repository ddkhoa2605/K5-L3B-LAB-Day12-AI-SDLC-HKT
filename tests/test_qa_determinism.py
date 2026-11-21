"""Bộ test kiểm tra Tính tất định (Determinism) và Hợp đồng CLI do Người 4 (QA Lead) phụ trách.

Chạy:
    python -m unittest tests/test_qa_determinism.py -v
"""

import os
import subprocess
import sys
import unittest

from helpers import Workdir, frames, run_headless, write_json


class QADeterminismAndCliTests(unittest.TestCase):
    def test_gather_deterministic_byte_exact(self):
        """Kiểm tra Gather chạy cùng seed 1 cho ra output giống nhau 100% từng byte."""
        with Workdir() as w:
            out1 = w.path("g1.jsonl")
            out2 = w.path("g2.jsonl")
            code1, err1 = run_headless("--mode", "gather", "--seed", "1", "--ticks", "300", "--out", out1)
            self.assertEqual(code1, 0, err1)
            code2, err2 = run_headless("--mode", "gather", "--seed", "1", "--ticks", "300", "--out", out2)
            self.assertEqual(code2, 0, err2)

            with open(out1, "rb") as f1, open(out2, "rb") as f2:
                self.assertEqual(f1.read(), f2.read(), "Output Gather giữa 2 lần chạy cùng seed bị lệch byte!")

    def test_quan_deterministic_byte_exact(self):
        """Kiểm tra Quán chạy cùng seed 1 cho ra output giống nhau 100% từng byte."""
        with Workdir() as w:
            out1 = w.path("q1.jsonl")
            out2 = w.path("q2.jsonl")
            code1, err1 = run_headless("--mode", "quan", "--seed", "1", "--ticks", "300", "--out", out1)
            self.assertEqual(code1, 0, err1)
            code2, err2 = run_headless("--mode", "quan", "--seed", "1", "--ticks", "300", "--out", out2)
            self.assertEqual(code2, 0, err2)

            with open(out1, "rb") as f1, open(out2, "rb") as f2:
                self.assertEqual(f1.read(), f2.read(), "Output Quán giữa 2 lần chạy cùng seed bị lệch byte!")

    def test_gather_determinism_with_movement_inputs(self):
        """Kiểm tra tính tất định khi có input di chuyển bơi lội."""
        with Workdir() as w:
            inp = write_json(
                w.path("in.json"),
                frames(
                    {"tick": 0, "move": [1, 0]},
                    {"tick": 30, "move": [0, 1]},
                    {"tick": 60, "move": [-1, 0]},
                    {"tick": 90, "move": [0, -1]},
                ),
            )
            out1 = w.path("in_g1.jsonl")
            out2 = w.path("in_g2.jsonl")

            code1, err1 = run_headless(
                "--mode", "gather", "--seed", "42", "--ticks", "150", "--inputs", inp, "--out", out1
            )
            self.assertEqual(code1, 0, err1)
            code2, err2 = run_headless(
                "--mode", "gather", "--seed", "42", "--ticks", "150", "--inputs", inp, "--out", out2
            )
            self.assertEqual(code2, 0, err2)

            with open(out1, "rb") as f1, open(out2, "rb") as f2:
                self.assertEqual(f1.read(), f2.read(), "Output Gather có inputs bị lệch byte!")

    def test_negative_invalid_cli_arguments_exit_2(self):
        """Kiểm tra các tham số CLI sai bắt buộc thoát mã 2 và KHÔNG tạo file output."""
        with Workdir() as w:
            out = w.path("should_not_exist.jsonl")

            # 1. Ticks âm
            code, _ = run_headless("--mode", "gather", "--seed", "1", "--ticks", "-5", "--out", out)
            self.assertEqual(code, 2, "Ticks âm phải trả về mã thoát 2")
            self.assertFalse(os.path.exists(out), "File output không được sinh ra khi lỗi")

            # 2. Snapshot-every âm hoặc 0
            code, _ = run_headless(
                "--mode", "gather", "--seed", "1", "--ticks", "10", "--snapshot-every", "0", "--out", out
            )
            self.assertEqual(code, 2, "Snapshot-every <= 0 phải trả về mã thoát 2")
            self.assertFalse(os.path.exists(out))

            # 3. Trùng đường dẫn in/out
            sc = write_json(w.path("same.json"), {"gather": {}})
            code, _ = run_headless(
                "--mode", "gather", "--seed", "1", "--ticks", "10", "--scenario", sc, "--out", sc
            )
            self.assertEqual(code, 2, "Trùng đường dẫn scenario và out phải trả về mã thoát 2")

    def test_determinism_tool_script_passes(self):
        """Kiểm tra script check_determinism.py chạy thành công và trả về mã 0."""
        cmd = [sys.executable, "tools/check_determinism.py", "--mode", "gather", "--seed", "1", "--ticks", "120"]
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        res = subprocess.run(cmd, capture_output=True, text=True, env=env)
        self.assertEqual(res.returncode, 0, res.stderr)
        self.assertIn("[PASS]", res.stdout)


if __name__ == "__main__":
    unittest.main()
