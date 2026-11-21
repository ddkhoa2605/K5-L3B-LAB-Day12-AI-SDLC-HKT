"""Test cho tools/bench.py (TICKET-04, ADR-0005): công thức bench.json và xử lý đầu vào sai."""

import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tools"))
import bench  # noqa: E402


class ComputeBench(unittest.TestCase):
    def test_five_fields_and_avg(self):
        r = bench.compute_bench([10.0] * 300, 3000.0, 2400.4)
        self.assertEqual(set(r), {"avg_fps", "p1_low_fps", "frames", "measured_s", "load_ms"})
        self.assertEqual(r["frames"], 300)
        self.assertEqual(r["measured_s"], 3.0)
        self.assertEqual(r["avg_fps"], 100.0)
        self.assertEqual(r["load_ms"], 2400)

    def test_p1_low_uses_ceil_one_percent_slowest(self):
        # 250 khung: ceil(2.5) = 3 khung chậm nhất là 50, 40, 30 ms -> TB 40 ms -> 25 FPS
        frames = [10.0] * 247 + [30.0, 40.0, 50.0]
        r = bench.compute_bench(frames, sum(frames), 0)
        self.assertEqual(r["p1_low_fps"], 25.0)

    def test_p1_low_at_least_one_frame(self):
        r = bench.compute_bench([20.0, 40.0], 60.0, 0)   # ceil(0.02) = 0 -> max(1, ...) = 1 khung (40 ms)
        self.assertEqual(r["p1_low_fps"], 25.0)

    def test_no_frames_rejected(self):
        with self.assertRaises(ValueError):
            bench.compute_bench([], 0, 0)


class BenchCli(unittest.TestCase):
    def test_missing_chrome_exit_2(self):
        with mock.patch.dict(os.environ, {"CHROME": "/khong/co/chrome"}):
            self.assertIsNone(bench.find_chrome())
            self.assertEqual(bench.main(["--seed", "42", "--duration", "1", "--out", os.devnull]), 2)

    def test_bad_duration_exit_2(self):
        self.assertEqual(bench.main(["--seed", "42", "--duration", "0", "--out", os.devnull]), 2)


if __name__ == "__main__":
    unittest.main()
