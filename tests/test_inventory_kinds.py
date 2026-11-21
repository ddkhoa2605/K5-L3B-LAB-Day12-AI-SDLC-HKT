"""ADR-0001: kho nhận ca_keo, keo_neo (contract v1.1); kind lạ vẫn bị từ chối (mã 2)."""

import unittest

from helpers import Workdir, run_headless, write_json


class InventoryKinds(unittest.TestCase):
    def run_quan(self, w, items):
        inv = write_json(w.path("inv.json"), {"items": items})
        return run_headless("--mode", "quan", "--seed", "1", "--ticks", "0", "--inventory", inv,
                            "--out", w.path("q.jsonl"))[0]

    def test_kind_moi_hop_le(self):
        with Workdir() as w:
            self.assertEqual(self.run_quan(w, {"ca_keo": 2, "keo_neo": 1}), 0)

    def test_kind_la_van_bi_tu_choi(self):
        with Workdir() as w:
            self.assertEqual(self.run_quan(w, {"ca_la_lung": 1}), 2)

    def test_gather_hold_nhan_kind_moi(self):
        with Workdir() as w:
            sc = write_json(w.path("sc.json"), {"gather": {"hold": ["ca_keo", "keo_neo"]}})
            code, err = run_headless("--mode", "gather", "--seed", "1", "--ticks", "0", "--scenario", sc,
                                     "--out", w.path("g.jsonl"))
            self.assertEqual(code, 0, err)


if __name__ == "__main__":
    unittest.main()
