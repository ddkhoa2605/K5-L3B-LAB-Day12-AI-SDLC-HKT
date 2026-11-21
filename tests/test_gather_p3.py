"""Phase 3 (TICKET-03, Test Contract v1.2) — phần Gather của Người 1: AC-P3-01 (kho cá thể, độ tươi, ươn).

Chạy thẳng lớp sim (Session). Manifest đã là v1.2 (khối `freshness`) sau khi gộp với lõi của Người 2: schema kho
cá thể là duy nhất, hành vi gather kiểu v1.1 (kho đếm, không hao) đã bị bỏ theo ADR-0003 (cắt thẳng).
"""

import copy
import json
import os
import unittest

from chonoi.errors import BadInput
from chonoi.inputs import InputState
from chonoi.inventory import read_inventory, write_inventory
from chonoi.runner import Session, run
from chonoi.scenario import load_scenario

from helpers import Workdir, write_json

with open("game.contract.json", encoding="utf-8") as _f:
    BASE = json.load(_f)["tuning"]
FRESH = {"initial": 100, "gather_decay_per_s": 0.5, "quan_decay_per_s": 0.25, "spoiled_below": 30}
T12 = copy.deepcopy(BASE)
T12["freshness"] = FRESH
NOFISH = {"random_fish": False, "monsters": []}


def sess(block, tuning=T12, seed=1):
    return Session("gather", tuning, block, seed)


def idle():
    return InputState((0.0, 0.0), set(), set())


def press(name):
    return InputState((0.0, 0.0), {name}, {name})


def step(s, n=1, inp=None):
    out = []
    for _ in range(n):
        out += s.step(inp or idle())
    return out


def fresh_of(s, item_id):
    return next(h["fresh"] for h in s.sim.hold if h["id"] == item_id)


def spoiled(ev):
    return [e for e in ev if e["name"] == "spoiled"]


class Freshness(unittest.TestCase):
    def test_hao_0_5_moi_giay(self):
        s = sess({"hold": [{"id": "I1", "kind": "ca_linh", "fresh": 100}], **NOFISH})
        step(s, 60)
        self.assertAlmostEqual(fresh_of(s, "I1"), 99.5, delta=0.01)

    def test_hang_moi_hao_tu_buoc_sau(self):
        """Hái lúc ở mặt nước: fresh = 100 ngay bước hái, bước kế mới hao 1 đơn vị tick."""
        s = sess({"hold": [], "player": {"pos": [12.0, 0.0]}, **NOFISH})
        step(s, 1, press("interact"))
        self.assertEqual([h["fresh"] for h in s.sim.hold], [100])
        step(s, 1)
        self.assertAlmostEqual(s.sim.hold[0]["fresh"], 100 - 0.5 / 60, delta=1e-9)

    def test_vi_du_ticket_fresh_30_uon_o_buoc_dau(self):
        s = sess({"hold": [{"id": "I1", "kind": "ca_linh", "fresh": 30}], **NOFISH})
        ev = step(s, 1)
        self.assertEqual(spoiled(ev), [{"type": "event", "tick": 1, "phase": "gather", "name": "spoiled",
                                        "data": {"item_id": "I1", "kind": "ca_linh", "location": "hold"}}])
        self.assertEqual(spoiled(step(s, 50)), [])  # đúng một lần

    def test_da_uon_san_khong_phat_lai(self):
        s = sess({"hold": [{"id": "I1", "kind": "ca_loc", "fresh": 12}], **NOFISH})
        self.assertEqual(spoiled(step(s, 5)), [])

    def test_nhanh_o_nguong_30_chinh_xac(self):
        """30 + 2/240 điểm: bước 1 còn đúng 30 (chưa ươn, so trước làm tròn); bước 2 mới < 30."""
        s = sess({"hold": [{"id": "I1", "kind": "ca_linh", "fresh": 30 + 2 / 240}], **NOFISH})
        self.assertEqual(spoiled(step(s, 1)), [])
        self.assertEqual(fresh_of(s, "I1"), 30)
        ev = spoiled(step(s, 1))
        self.assertEqual([e["tick"] for e in ev], [2])

    def test_nhieu_ca_the_cung_vuot_theo_id(self):
        hold = [{"id": "I10", "kind": "ca_linh", "fresh": 30}, {"id": "I2", "kind": "ca_loc", "fresh": 30},
                {"id": "I3", "kind": "ca_keo", "fresh": 80}]
        ev = spoiled(step(sess({"hold": hold, **NOFISH}), 1))
        self.assertEqual([e["data"]["item_id"] for e in ev], ["I2", "I10"])

    def test_ep_day_0_va_hang_uon_van_chiem_o(self):
        s = sess({"hold": [{"id": "I1", "kind": "ca_linh", "fresh": 0.005}], **NOFISH})
        step(s, 3)
        self.assertEqual(fresh_of(s, "I1"), 0)
        self.assertEqual(s.snapshot()["hold_count"], 1)

    def test_pause_la_khong_buoc_sim(self):
        """Pause do lớp day/runner giữ (không gọi step) nên sim không hao; ở đây kiểm sim không tự hao khi không bước."""
        s = sess({"hold": [{"id": "I1", "kind": "ca_linh", "fresh": 100}], **NOFISH})
        self.assertEqual(fresh_of(s, "I1"), 100)


class IdsAndSchema(unittest.TestCase):
    def test_id_noi_tiep_theo_thu_tu_vao_gio(self):
        s = sess({"hold": [{"id": "I7", "kind": "ca_loc", "fresh": 90}], "player": {"pos": [12.0, 0.0]}, **NOFISH})
        step(s, 1, press("interact"))
        ids = [h["id"] for h in s.sim.hold]
        self.assertEqual(ids[0], "I7")
        self.assertEqual(ids, [f"I{7 + i}" for i in range(len(ids))])
        self.assertGreater(len(ids), 1)

    def test_snapshot_hold_theo_schema_ca_the(self):
        s = sess({"hold": [{"id": "I1", "kind": "ca_linh", "fresh": 97.5}], **NOFISH})
        self.assertEqual(s.snapshot()["hold"], [{"id": "I1", "kind": "ca_linh", "fresh": 97.5}])

    def test_scenario_v12_ma_2_khi_sai(self):
        bad = [["ca_linh"], [{"id": "I1", "kind": "ca_linh"}], [{"id": "", "kind": "ca_linh", "fresh": 5}],
               [{"id": "I1", "kind": "la_la", "fresh": 5}], [{"id": "I1", "kind": "ca_loc", "fresh": 101}],
               [{"id": "I1", "kind": "ca_loc", "fresh": -1}],
               [{"id": "I1", "kind": "ca_loc", "fresh": 5}, {"id": "I1", "kind": "ca_loc", "fresh": 5}]]
        for hold in bad:
            with self.subTest(hold=hold), Workdir() as w:
                path = write_json(w.path("sc.json"), {"gather": {"hold": hold}})
                with self.assertRaises(BadInput):
                    load_scenario(path, "gather", T12)

    def test_scenario_kieu_cu_mang_kind_bi_tu_choi(self):
        with Workdir() as w:
            path = write_json(w.path("sc.json"), {"gather": {"hold": ["ca_linh"]}})
            with self.assertRaises(BadInput):
                load_scenario(path, "gather", BASE)

    def test_contract_freshness_sai_bi_tu_choi(self):
        from chonoi.contract import validate_tuning
        t = copy.deepcopy(T12)
        t["freshness"] = {"initial": 100}
        with self.assertRaises(BadInput):
            validate_tuning(t)
        validate_tuning(T12, ("reservations",))  # manifest hợp nhất có khối reservations (mở rộng đặt trước)


class LossAndEnd(unittest.TestCase):
    def test_lost_la_mang_ca_the_lifo_khi_bi_can(self):
        hold = [{"id": f"I{i}", "kind": "ca_linh", "fresh": 90 - i} for i in range(1, 5)]
        mon = [{"id": "M1", "kind": "ca_sau", "pos": [30.0, 15.0], "waypoints": [[30.0, 15.0], [31.0, 15.0]]}]
        s = sess({"hold": hold, "random_fish": False, "monsters": mon, "player": {"pos": [30.0, 15.0]}})
        hits = [e for e in step(s, 1) if e["name"] == "monster_hit"]
        self.assertEqual(len(hits), 1)
        lost = hits[0]["data"]["lost"]
        self.assertEqual([x["id"] for x in lost], ["I4", "I3"])
        self.assertTrue(all(set(x) == {"id", "kind", "fresh"} for x in lost))
        self.assertEqual([h["id"] for h in s.sim.hold], ["I1", "I2"])

    def test_gather_end_inventory_theo_id_va_giu_hang_uon(self):
        hold = [{"id": "I2", "kind": "ca_loc", "fresh": 10}, {"id": "I10", "kind": "ca_linh", "fresh": 99},
                {"id": "I1", "kind": "ca_keo", "fresh": 50}]
        s = sess({"hold": hold, "random_fish": False, "monsters": [], "player": {"pos": [2.0, 0.0]}})
        ev = step(s, 1, press("interact"))
        end = [e for e in ev if e["name"] == "gather_end"][0]["data"]
        self.assertEqual(end["reason"], "docked")
        items = end["inventory"]["items"]
        self.assertEqual([x["id"] for x in items], ["I1", "I2", "I10"])
        self.assertAlmostEqual(items[0]["fresh"], 50 - 0.5 / 60, delta=0.01)

    def test_ngat_choke_ghi_kho_rong_va_lost_la_ca_the(self):
        s = sess({"hold": [{"id": "I1", "kind": "ca_linh", "fresh": 90}], "random_fish": False, "monsters": [],
                  "player": {"pos": [50.0, 5.0], "hp": 1, "oxygen_ticks": 0, "zero_oxy_ticks": 59}})
        ev = step(s, 1)
        end = [e for e in ev if e["name"] == "gather_end"][0]["data"]
        self.assertEqual((end["reason"], end["inventory"]), ("fainted", {"items": []}))
        faint = [e for e in ev if e["name"] == "faint"][0]["data"]
        self.assertEqual([x["id"] for x in faint["lost"]], ["I1"])


class InventoryFile(unittest.TestCase):
    def test_ghi_dung_mot_lan_doc_lai_giu_nhanh_nguong(self):
        hold = [{"id": "I1", "kind": "ca_linh", "fresh": 30 + 1 / 240}, {"id": "I2", "kind": "ca_loc", "fresh": 97.5}]
        with Workdir() as w:
            out = w.path("kho.json")
            sc = {"hold": hold, "random_fish": False, "monsters": [], "player": {"pos": [2.0, 0.0]}}
            inp = write_json(w.path("in.json"), {"frames": [{"tick": 0, "interact": True}]})
            from chonoi.inputs import load_frames
            run("gather", T12, sc, 1, load_frames(inp), 5, w.path("o.jsonl"), 1, inventory_out=out)
            self.assertFalse([f for f in os.listdir(os.path.dirname(out)) if f.endswith(".tmp")])
            back = read_inventory(out)  # cá thể nội bộ {id,kind,u}; 240 đơn vị = 1 điểm
            self.assertEqual([x["id"] for x in back], ["I1", "I2"])
            self.assertLess(back[0]["u"] / 240, 30)  # 30 + 1/240 - 2/240: vẫn < 30 sau khi đọc lại
            self.assertAlmostEqual(back[1]["u"] / 240, 97.5 - 0.5 / 60, delta=0.01)

    def test_chua_gather_end_giu_nguyen_file_dich(self):
        with Workdir() as w:
            out = w.path("kho.json")
            with open(out, "w") as f:
                f.write("GIU")
            run("gather", T12, {"hold": [{"id": "I1", "kind": "ca_loc", "fresh": 90}], **NOFISH}, 1, [], 5,
                w.path("o.jsonl"), 1, inventory_out=out)
            with open(out) as f:
                self.assertEqual(f.read(), "GIU")

    def test_doc_kho_v12_tu_choi_kho_dem_va_sai_schema(self):
        with Workdir() as w:
            bads = ({"items": {"ca_loc": 1}},
                    {"items": [{"id": "I1", "kind": "ca_loc", "fresh": 101}]},
                    {"items": [{"id": "I1", "kind": "x", "fresh": 1}]},
                    {"items": [{"id": "I1", "kind": "ca_loc", "fresh": 1}, {"id": "I1", "kind": "ca_loc", "fresh": 2}]})
            for bad in bads:
                with self.subTest(bad=bad), self.assertRaises(BadInput):
                    read_inventory(write_json(w.path("k.json"), bad))

    def test_dinh_dang_100_va_97_5(self):
        with Workdir() as w:
            out = w.path("k.json")
            write_inventory(out, [{"id": "I1", "kind": "ca_linh", "fresh": 100},
                                  {"id": "I2", "kind": "ca_loc", "fresh": 97.5}])
            with open(out) as f:
                self.assertEqual(f.read().strip(),
                                 '{"items":[{"id":"I1","kind":"ca_linh","fresh":100},'
                                 '{"id":"I2","kind":"ca_loc","fresh":97.5}]}')


if __name__ == "__main__":
    unittest.main()
