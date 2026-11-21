"""Quán theo TICKET-02 (Phase 2, contract v1.1): 2 bếp / 4 bàn / 6 món, kế hoạch Ngày, trạng thái xuyên Ngày.

Chạy: PYTHONPATH=tests:. python3 -m unittest discover -s tests -v
"""

import json
import unittest

from chonoi.errors import BadInput
from chonoi.ids import IdAllocator
from chonoi.inputs import InputState
from chonoi.rng import Streams
from chonoi.scenario import day_plan_ingredients
from chonoi.sim.quan import QuanSim
from helpers import Workdir, events, frames, read_jsonl, run_headless, snapshots, write_json

with open("game.contract.json", encoding="utf-8") as _f:
    CONTRACT = json.load(_f)
TUNING = CONTRACT["tuning"]
Q, MENU = TUNING["quan"], TUNING["menu"]

# Bảng "Nguyên liệu cần" của TICKET-02 mục 2 (đối chiếu độc lập với dữ liệu trong game.contract.json)
TICKET_PLAN = {
    1: {"ca_loc": 3, "bong_sung": 6},
    2: {"ca_loc": 2, "ca_linh": 6, "bong_dien_dien": 2},
    3: {"bong_sung": 4, "ca_loc": 2, "bong_dien_dien": 2, "ca_keo": 4},
    4: {"ca_linh": 2, "ca_keo": 1, "keo_neo": 1, "bong_dien_dien": 1, "ca_loc": 2, "bong_sung": 2},
    5: {"ca_linh": 5, "ca_keo": 1, "keo_neo": 1, "bong_dien_dien": 2, "ca_loc": 1},
}
RICH = {"ca_loc": 9, "ca_linh": 9, "ca_keo": 9, "bong_dien_dien": 9, "bong_sung": 9, "keo_neo": 9}


def sim(scenario=None, seed=1, **kw):
    return QuanSim(TUNING, scenario or {}, Streams(seed), IdAllocator(), **kw)


def idle(sim_):
    """Chạy một bước không điều khiển; trả event."""
    return sim_.step(InputState((0.0, 0.0), {}, set()))


def press(sim_):
    """Một bước có cạnh lên `interact`."""
    return sim_.step(InputState((0.0, 0.0), {}, {"interact"}))


class Data(unittest.TestCase):
    def test_contract_v11_bep_ban_mon(self):
        self.assertEqual(CONTRACT["contract_version"], "1.1")
        self.assertEqual([s["id"] for s in Q["stoves"]], ["B1", "B2"])
        self.assertEqual({t["id"]: t["pos"] for t in Q["tables"]},
                         {"T1": [9, 2], "T2": [13, 2], "T3": [9, 6], "T4": [13, 6]})
        self.assertEqual(sorted(MENU), sorted(["ca_loc_nuong_trui", "goi_bong_sung", "lau_ca_linh_dien_dien",
                                              "canh_chua_ca_loc", "ca_keo_nuong", "lau_mam"]))
        self.assertEqual((MENU["lau_mam"]["cook_s"], MENU["lau_mam"]["price"]), (12, 200))
        self.assertEqual(MENU["ca_keo_nuong"]["recipe"], {"ca_keo": 2})

    def test_day_plan_khop_bang_ticket(self):
        plan = TUNING["day_plan"]
        self.assertEqual([p["day"] for p in plan], [1, 2, 3, 4, 5])
        for p in plan:
            self.assertEqual(p["ingredients"], TICKET_PLAN[p["day"]], p["day"])
            self.assertEqual(day_plan_ingredients(p["dishes"], MENU), p["ingredients"], p["day"])

    def test_day_plan_ingredients_tu_choi_mon_la(self):
        for bad in ({"pho": 1}, {"goi_bong_sung": 0}, {"goi_bong_sung": True}):
            with self.assertRaises(BadInput):
                day_plan_ingredients(bad, MENU)


class Schedule(unittest.TestCase):
    def test_lich_khach_120_cong_900k_vao_ghe_nho_nhat(self):
        with Workdir() as w:
            sc = write_json(w.path("sc.json"), {"quan": {"stock": RICH}})
            code, err = run_headless("--mode", "quan", "--seed", "3", "--ticks", "2000", "--scenario", sc,
                                     "--out", w.path("o.jsonl"))
            self.assertEqual(code, 0, err)
            ev = events(read_jsonl(w.path("o.jsonl")), "customer_arrived")
            self.assertEqual([(e["tick"], e["data"]["table_id"]) for e in ev],
                             [(120, "T1"), (1020, "T2"), (1920, "T3")])

    def test_snapshot_tick0_co_2_bep_4_ban(self):
        with Workdir() as w:
            code, err = run_headless("--mode", "quan", "--seed", "1", "--ticks", "0", "--out", w.path("o.jsonl"))
            self.assertEqual(code, 0, err)
            s = snapshots(read_jsonl(w.path("o.jsonl")))[0]
            self.assertEqual([x["id"] for x in s["stoves"]], ["B1", "B2"])
            self.assertEqual([x["id"] for x in s["tables"]], ["T1", "T2", "T3", "T4"])


class Kitchen(unittest.TestCase):
    def test_hoa_khoang_cach_chon_bep_id_nho_va_don_cu_nhat(self):
        """Đứng cách B1 và B2 đúng 1.5 m: hòa khoảng cách → B1; bếp nhận đơn reserved cũ nhất."""
        s = sim({"player": {"pos": [3.5, 8]}, "stock": RICH, "random_customers": False,
                 "customers": [{"id": "C1", "table_id": "T2", "dish_id": "goi_bong_sung", "order_tick": 5},
                               {"id": "C2", "table_id": "T1", "dish_id": "ca_loc_nuong_trui", "order_tick": 9}]})
        ev = press(s)
        self.assertEqual([(n, d["stove_id"], d["order_id"]) for n, d in ev], [("cook_started", "B1", "C1")])
        self.assertEqual(s.stoves[1]["state"], "idle")

    def test_lau_mam_items_theo_kind(self):
        s = sim({"player": {"pos": [2, 8]}, "stock": RICH, "random_customers": False,
                 "customers": [{"id": "C1", "table_id": "T1", "dish_id": "lau_mam"}]})
        name, d = press(s)[0]
        self.assertEqual(name, "cook_started")
        self.assertEqual(d["items"], ["bong_dien_dien", "ca_keo", "ca_linh", "ca_linh", "keo_neo"])
        self.assertEqual(d["base_price"], 200)
        self.assertEqual((s.stock["ca_linh"], s.stock["ca_keo"], s.stock["keo_neo"]), (7, 8, 8))

    def test_bep_dang_nau_thi_interact_lai_bo_luot(self):
        s = sim({"player": {"pos": [2, 8]}, "stock": RICH, "random_customers": False,
                 "customers": [{"id": "C1", "table_id": "T1", "dish_id": "goi_bong_sung", "order_tick": 1},
                               {"id": "C2", "table_id": "T2", "dish_id": "goi_bong_sung", "order_tick": 2}]})
        self.assertEqual([n for n, _ in press(s)], ["cook_started"])
        self.assertEqual([n for n, _ in press(s)], [], "B1 đang nấu: lần 2 bỏ lượt, không nhảy sang B2")


class DayHooks(unittest.TestCase):
    def test_allowed_dishes_loc_khach_theo_ke_hoach(self):
        for seed in range(6):
            s = sim({"stock": RICH}, seed=seed, allowed_dishes={"goi_bong_sung"})
            dishes = set()
            for _ in range(2000):
                for name, d in idle(s):
                    if name == "customer_arrived":
                        dishes.add(d["dish_id"])
            self.assertEqual(dishes, {"goi_bong_sung"}, seed)

    def test_mon_trong_ke_hoach_thieu_nguyen_lieu_thi_no_dish(self):
        s = sim({"stock": {"ca_loc": 5}}, allowed_dishes={"goi_bong_sung"})
        names = [n for _ in range(121) for n, _ in idle(s)]
        self.assertEqual(names, ["no_dish"])

    def test_khach_fixture_ngoai_ke_hoach_la_mau_thuan(self):
        with self.assertRaises(BadInput):
            sim({"stock": RICH, "customers": [{"id": "C1", "table_id": "T1", "dish_id": "lau_mam"}]},
                allowed_dishes={"goi_bong_sung"})

    def test_ke_hoach_co_mon_la_la_mau_thuan(self):
        with self.assertRaises(BadInput):
            sim(allowed_dishes={"pho"})

    def test_tien_earned_uy_tin_giu_qua_ngay(self):
        s = sim({"time_left_ticks": 1}, money=200, earned=300, reputation=4.0)
        d = dict(idle(s))["quan_end"]
        self.assertEqual((d["money"], d["earned"], d["shift_earned"], d["reputation"]), (200, 300, 0, 4.0))

    def test_thu_tien_cong_don_vao_so_du_xuyen_ngay(self):
        s = sim({"time_left_ticks": 2, "random_customers": False,
                 "customers": [{"id": "C1", "table_id": "T1", "state": "eating", "dish_id": "goi_bong_sung",
                                "eat_ticks_left": 500, "base_price": 40, "tip": 8}]},
                money=100, earned=150)
        idle(s)
        d = dict(idle(s))["quan_end"]
        self.assertEqual((d["money"], d["earned"], d["shift_earned"]), (148, 198, 48))


class Regression(unittest.TestCase):
    def test_ca_day_du_p1_van_dung_voi_so_chuan_v11(self):
        """Một khách như Phase 1 vẫn cho tiền món + boa = 72 và uy tín +0.2 (điểm 372)."""
        with Workdir() as w:
            blk = {"player": {"pos": [9, 2]}, "random_customers": False,
                   "hand": {"order_id": "C1", "dish_id": "ca_loc_nuong_trui"},
                   "customers": [{"id": "C1", "table_id": "T1", "dish_id": "ca_loc_nuong_trui",
                                  "order_status": "assigned"}]}
            sc = write_json(w.path("sc.json"), {"quan": blk})
            inp = write_json(w.path("in.json"), frames({"tick": 0, "interact": True}))
            code, err = run_headless("--mode", "quan", "--seed", "1", "--ticks", "700", "--scenario", sc,
                                     "--inputs", inp, "--out", w.path("o.jsonl"))
            self.assertEqual(code, 0, err)
            rows = read_jsonl(w.path("o.jsonl"))
            self.assertEqual(events(rows, "paid")[0]["data"]["amount"], 72)
            self.assertEqual(rows[-1]["score"], 72 + 100 * 3)


if __name__ == "__main__":
    unittest.main()
