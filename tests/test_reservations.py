"""Mở rộng "Khách đặt trước" (TICKET-03 mục 2): trạng thái scheduled→holding→waiting→served|failed.

Chạy: PYTHONPATH=tests:. python3 -m unittest discover -s tests -v
"""

import copy
import json
import unittest

from chonoi.ids import IdAllocator
from chonoi.inputs import InputState
from chonoi.rng import Streams
from chonoi.sim.quan import QuanSim, plan_reservations
from helpers import Workdir, events, frames, make_items, read_jsonl, run_headless, snapshots, write_json

with open("game.contract.json", encoding="utf-8") as _f:
    CONTRACT = json.load(_f)
TUNING = CONTRACT["tuning"]
CFG = TUNING["reservations"]
DUR = int(round(TUNING["quan"]["duration_s"] * 60))
HOLD = int(round(CFG["table_hold_s"] * 60))
DISH = "ca_loc_nuong_trui"
T1, T2 = TUNING["quan"]["tables"][0]["pos"], TUNING["quan"]["tables"][1]["pos"]
STOCK = make_items({"ca_loc": 6, "bong_sung": 6})


def res(rid="R1", table="T1", dish=DISH, arrival=3):
    return {"id": rid, "table_id": table, "dish_id": dish, "arrival_tick": arrival}


def sim(reservations, stock=STOCK, customers=(), tuning=TUNING, **extra):
    sc = {"reservations": list(reservations), "stock": stock, "customers": list(customers), "random_customers": False}
    sc.update(extra)
    return QuanSim(tuning, sc, Streams(1), IdAllocator())


def step(s, pressed=()):
    return s.step(InputState((0.0, 0.0), {}, set(pressed)))


def names(evs):
    return [n for n, _ in evs]


def run_to(s, tick):
    evs = []
    while s.phase_tick < tick:
        evs += step(s)
    return evs


class Generation(unittest.TestCase):
    def test_mac_dinh_hai_don_o_hai_ban_khac_nhau_trong_dai(self):
        for seed in range(20):
            out = plan_reservations(TUNING, {}, Streams(seed), sorted(TUNING["menu"]))
            self.assertEqual([r["id"] for r in out], ["R1", "R2"])
            self.assertEqual(len({r["table_id"] for r in out}), 2)
            for r in out:
                self.assertTrue(HOLD <= r["arrival_tick"] <= DUR - 1, r)
                self.assertIn(r["dish_id"], TUNING["menu"])
                self.assertEqual(r["state"], "scheduled")

    def test_chi_chon_mon_trong_ke_hoach(self):
        for seed in range(20):
            for r in plan_reservations(TUNING, {}, Streams(seed), {"goi_bong_sung"}):
                self.assertEqual(r["dish_id"], "goi_bong_sung")

    def test_tat_va_ghi_de_tuong_minh(self):
        self.assertEqual(plan_reservations(TUNING, {"random_reservations": False}, Streams(1), ["x"]), [])
        self.assertEqual(plan_reservations(TUNING, {"reservations": []}, Streams(1), ["x"]), [])
        got = plan_reservations(TUNING, {"reservations": [res("R2", "T2", arrival=9), res("R1", "T1", arrival=5)]},
                                Streams(1), ["x"])
        self.assertEqual([(r["id"], r["table_id"], r["arrival_tick"]) for r in got], [("R1", "T1", 5), ("R2", "T2", 9)])

    def test_tat_o_manifest_thi_khong_co_gi(self):
        t = copy.deepcopy(TUNING)
        del t["reservations"]
        self.assertEqual(plan_reservations(t, {}, Streams(1), ["x"]), [])
        s = QuanSim(t, {"stock": [], "random_customers": False}, Streams(1), IdAllocator())
        snap = s.snapshot()
        self.assertNotIn("reservations", snap)
        self.assertNotIn("reservation_id", snap["tables"][0])

    def test_cong_bo_o_tick_0_qua_cli_tat_dinh(self):
        with Workdir() as w:
            for i in (1, 2):
                code, err = run_headless("--mode", "quan", "--seed", "5", "--ticks", "3000", "--out", w.path(f"o{i}.jsonl"))
                self.assertEqual(code, 0, err)
            rows = read_jsonl(w.path("o1.jsonl"))
            ann = events(rows, "reservation_announced")
            self.assertEqual([(e["tick"], e["data"]["reservation_id"]) for e in ann], [(0, "R1"), (0, "R2")])
            self.assertEqual(rows[0]["type"], "snapshot", "snapshot tick 0 trước, rồi event công bố")
            self.assertEqual({r["id"]: r["arrival_tick"] for r in snapshots(rows)[0]["reservations"]},
                             {e["data"]["reservation_id"]: e["data"]["arrival_tick"] for e in ann})
            with open(w.path("o1.jsonl"), "rb") as a, open(w.path("o2.jsonl"), "rb") as b:
                self.assertEqual(a.read(), b.read())


class Lifecycle(unittest.TestCase):
    def test_giu_ban_tu_arrival_tru_30s_va_snapshot_tick0(self):
        s = sim([res(arrival=HOLD)])  # arrival − 1800 = 0 -> giữ ngay từ tick 0, có trong snapshot dựng quán
        snap = s.snapshot()
        self.assertEqual(snap["reservations"][0]["state"], "holding")
        self.assertEqual(snap["tables"][0]["reservation_id"], "R1")
        s = sim([res(arrival=HOLD + 5)])
        self.assertEqual(s.snapshot()["reservations"][0]["state"], "scheduled")
        run_to(s, 5)
        self.assertEqual(s.snapshot()["reservations"][0]["state"], "holding")

    def test_khach_thuong_khong_ngoi_ban_dang_giu(self):
        s = sim([res(arrival=500)], random_customers=True)  # arrival 500 < 1800: T1 bị giữ từ tick 0
        evs = run_to(s, TUNING["quan"]["first_customer_tick"])
        self.assertEqual([d["table_id"] for n, d in evs if n == "customer_arrived"], ["T2"])

    def test_den_gio_thanh_cong_giu_nguyen_lieu_va_phat_dung_thu_tu(self):
        s = sim([res(arrival=3)])
        evs = run_to(s, 3)
        self.assertEqual(names(evs), ["reservation_arrived", "customer_arrived"])
        self.assertEqual(evs[0][1], {"reservation_id": "R1", "order_id": "C1"})
        self.assertEqual(evs[1][1], {"order_id": "C1", "table_id": "T1", "dish_id": DISH})
        c = s.customers[0]
        self.assertEqual((c["reservation_id"], c["order_status"], c["patience_ticks_left"], len(c["reserved"])),
                         ("R1", "reserved", 3600, 1))
        self.assertEqual(s.snapshot()["reservations"][0]["state"], "waiting")

    def test_ban_con_khach_fail_occupied_tru_uy_tin_mot_lan(self):
        s = sim([res(arrival=2)], customers=[{"id": "C1", "table_id": "T1", "dish_id": DISH}])
        evs = run_to(s, 4)
        self.assertEqual([(n, d["reason"], d["reputation"]) for n, d in evs if n == "reservation_failed"],
                         [("reservation_failed", "occupied", 2.0)])
        self.assertEqual([c["id"] for c in s.customers], ["C1"], "khách thường đang ngồi ở lại")
        self.assertEqual(s.reputation, 2.0, "đúng một lần")

    def test_thieu_kho_fail_stock(self):
        s = sim([res(arrival=2)], stock=[])
        evs = run_to(s, 3)
        self.assertEqual([(n, d["reason"]) for n, d in evs], [("reservation_failed", "stock")])
        self.assertEqual(s.reputation, 2.0)

    def test_gia_x1_5_lam_tron_xuong_roi_moi_tinh_boa(self):
        s = sim([res(arrival=1)])
        run_to(s, 1)
        s.hand = {"order_id": "C1", "dish_id": DISH, "base_price": 58}  # giá đã chốt theo tươi
        s.customers[0]["order_status"] = "assigned"
        s.customers[0]["reserved"] = []
        s.pos = [float(T1[0]), float(T1[1])]
        evs = step(s, {"interact"})
        self.assertEqual(names(evs), ["served", "reservation_served"])
        self.assertEqual(evs[0][1]["base_price"], 87)  # floor(58 × 1.5)
        self.assertEqual(evs[0][1]["tip"], 17)  # boa trên giá cuối: floor(87 × 0.2)
        self.assertEqual(evs[1][1], {"reservation_id": "R1", "order_id": "C1", "base_price": 87})
        self.assertEqual(s.snapshot()["reservations"][0]["state"], "served")

    def test_het_kien_nhan_fail_patience_khong_customer_left(self):
        s = sim([res(arrival=1)])
        run_to(s, 1)
        s.customers[0]["patience_ticks_left"] = 1
        evs = step(s)
        self.assertEqual([(n, d["reason"], d["reputation"]) for n, d in evs], [("reservation_failed", "patience", 2.0)])
        self.assertEqual(s.customers, [])
        self.assertEqual(s.snapshot()["tables"][0]["reservation_id"], None)

    def test_dong_ca_fail_closing_theo_id_va_khach_roi_khong_customer_left(self):
        s = sim([res("R2", "T2", arrival=10), res("R1", "T1", arrival=1)], time_left_ticks=3)
        evs = run_to(s, 3)
        fails = [(d["reservation_id"], d["reason"]) for n, d in evs if n == "reservation_failed"]
        self.assertEqual(fails, [("R1", "closing"), ("R2", "closing")])
        self.assertNotIn("customer_left", names(evs))
        self.assertEqual(names(evs)[-1], "quan_end")
        self.assertEqual(s.reputation, 1.0, "mỗi đơn lỡ −1")

    def test_mon_chay_dish_burnt_failed_roi_reservation_failed(self):
        t = copy.deepcopy(TUNING)
        t["quan"]["burn_s"] = 20
        s = sim([res(arrival=1)], tuning=t)
        run_to(s, 1)
        c = s.customers[0]
        c["order_status"], c["reserved"] = "assigned", []
        s.stoves[0].update(state="ready", ready_ticks=1200, dish={"order_id": "C1", "dish_id": DISH, "base_price": 58})
        evs = step(s)
        self.assertEqual([(n, d.get("order_status", d.get("reason"))) for n, d in evs],
                         [("dish_burnt", "failed"), ("reservation_failed", "burnt")])
        self.assertEqual((s.stoves[0]["state"], s.customers), ("idle", []))

    def test_giu_cho_vua_uon_khong_giu_lai_duoc_thi_fail_stock(self):
        s = sim([res(arrival=1)], stock=[{"id": "I1", "kind": "ca_loc", "fresh": 100}])
        run_to(s, 1)
        s.stock[0]["u"] = 7200  # chạm ngưỡng: bước sau xuống 7199 -> ươn
        evs = step(s)
        self.assertEqual([(n, d.get("item_id", d.get("reason"))) for n, d in evs],
                         [("spoiled", "I1"), ("reservation_failed", "stock")])
        self.assertEqual(s.customers, [])

    def test_giu_cho_vua_uon_co_thay_the_thi_van_cho(self):
        s = sim([res(arrival=1)], stock=[{"id": "I1", "kind": "ca_loc", "fresh": 100}, {"id": "I2", "kind": "ca_loc", "fresh": 60}])
        run_to(s, 1)
        self.assertEqual(s.customers[0]["reserved"], ["I1"])
        s.stock[0]["u"] = 7200
        evs = step(s)
        self.assertEqual(names(evs), ["spoiled"])
        self.assertEqual(s.customers[0]["reserved"], ["I2"])


class ScenarioValidation(unittest.TestCase):
    def check(self, block):
        with Workdir() as w:
            sc = write_json(w.path("sc.json"), {"quan": block})
            return run_headless("--mode", "quan", "--seed", "1", "--ticks", "0", "--scenario", sc, "--out", w.path("o.jsonl"))[0]

    def test_hop_le(self):
        self.assertEqual(self.check({"reservations": [res("R1", "T1", arrival=5), res("R2", "T2", arrival=DUR - 1)]}), 0)
        self.assertEqual(self.check({"random_reservations": False}), 0)

    def test_mau_thuan_exit_2(self):
        bad = {
            "3 đơn": {"reservations": [res("R1", "T1"), res("R2", "T2"), res("R3", "T3")]},
            "cùng bàn": {"reservations": [res("R1", "T1"), res("R2", "T1")]},
            "id trùng": {"reservations": [res("R1", "T1"), res("R1", "T2")]},
            "bàn không có": {"reservations": [res(table="T9")]},
            "món lạ": {"reservations": [res(dish="pho")]},
            "tick 0": {"reservations": [res(arrival=0)]},
            "tick ≥ thời lượng": {"reservations": [res(arrival=DUR)]},
            "tick số thực": {"reservations": [res(arrival=3.5)]},
            "khóa thừa": {"reservations": [dict(res(), extra=1)]},
            "thiếu khóa": {"reservations": [{"id": "R1", "table_id": "T1"}]},
            "không phải mảng": {"reservations": {"R1": res()}},
            "random_reservations không bool": {"random_reservations": "no"},
        }
        for name, block in bad.items():
            self.assertEqual(self.check(block), 2, name)


class DayFlow(unittest.TestCase):
    def test_cong_bo_sau_phase_start_gather_va_quan_dung_lai(self):
        hold = make_items({"ca_loc": 3, "bong_sung": 6})
        sc = {"gather": {"hold": hold, "random_fish": False}, "quan": {"random_customers": False}}
        with Workdir() as w:
            code, err = run_headless("--mode", "day", "--seed", "3", "--ticks", "200", "--snapshot-every", "50", "--scenario",
                                     write_json(w.path("sc.json"), sc),
                                     "--inputs", write_json(w.path("in.json"), frames({"tick": 0, "interact": True})),
                                     "--out", w.path("o.jsonl"))
            self.assertEqual(code, 0, err)
            rows = read_jsonl(w.path("o.jsonl"))
            seq = [(e["tick"], e["name"]) for e in events(rows) if e["tick"] == 0]
            self.assertEqual(seq, [(0, "day_start"), (0, "day_plan"), (0, "phase_start"),
                                   (0, "reservation_announced"), (0, "reservation_announced")])
            ann = {e["data"]["reservation_id"]: e["data"] for e in events(rows, "reservation_announced")}
            self.assertEqual(len(ann), 2, "quán không công bố lại")
            plan = TUNING["day_plan"][0]["dishes"]
            self.assertTrue(all(d["dish_id"] in plan for d in ann.values()), "món trong kế hoạch Ngày")
            snaps = snapshots(rows)
            self.assertEqual([r["state"] for r in snaps[0]["reservations"]], ["scheduled", "scheduled"])
            self.assertEqual({r["id"]: r["arrival_tick"] for r in snaps[-1]["reservations"]},
                             {k: v["arrival_tick"] for k, v in ann.items()}, "quán dùng đúng đơn đã công bố")

    def test_scenario_tat_hoac_ghi_de_trong_day(self):
        hold = make_items({"ca_loc": 3})
        for quan, want in (({"random_reservations": False}, 0), ({"reservations": [res("R1", "T3", arrival=7)]}, 1)):
            quan = dict({"random_customers": False}, **quan)
            with Workdir() as w:
                code, err = run_headless("--mode", "day", "--seed", "3", "--ticks", "1", "--scenario",
                                         write_json(w.path("sc.json"), {"gather": {"hold": hold, "random_fish": False}, "quan": quan}),
                                         "--out", w.path("o.jsonl"))
                self.assertEqual(code, 0, err)
                self.assertEqual(len(events(read_jsonl(w.path("o.jsonl")), "reservation_announced")), want)


if __name__ == "__main__":
    unittest.main()
