"""Test luật Quán (PRD-0 mục F/E/D), hộp đen qua headless_cmd. Số liệu mẫu lấy từ game.contract.json.

Chạy: PYTHONPATH=tests:. python3 -m unittest discover -s tests -v
"""

import json
import unittest

from helpers import Workdir, close, events, frames, read_jsonl, run_headless, snapshots, write_json

with open("game.contract.json", encoding="utf-8") as _f:
    TUNING = json.load(_f)["tuning"]
Q = TUNING["quan"]
MENU = TUNING["menu"]
PATIENCE = int(round(Q["patience_s"] * 60))
DISH = "ca_loc_nuong_trui"
PRICE = MENU[DISH]["price"]
COOK = int(round(MENU[DISH]["cook_s"] * 60))
EAT = int(round(Q["eat_s"] * 60))
B1, T1 = Q["stoves"][0]["pos"], Q["tables"][0]["pos"]


def quan(w, block, inputs=None, ticks=10, seed=1, every=1, inventory=None):
    """Chạy quan với fixture; trả (mã thoát, rows)."""
    sc = write_json(w.path("sc.json"), {"quan": block})
    args = ["--mode", "quan", "--seed", str(seed), "--ticks", str(ticks), "--scenario", sc,
            "--snapshot-every", str(every), "--out", w.path("o.jsonl")]
    if inputs is not None:
        args += ["--inputs", write_json(w.path("in.json"), frames(*inputs))]
    if inventory is not None:
        args += ["--inventory", inventory]
    code, err = run_headless(*args)
    return code, (read_jsonl(w.path("o.jsonl")) if code == 0 else err)


def waiting(cid="C1", **kw):
    c = {"id": cid, "table_id": "T1", "dish_id": DISH}
    c.update(kw)
    return c


class Arrival(unittest.TestCase):
    def test_khach_dau_tien_dung_lich_va_giu_cho(self):
        with Workdir() as w:
            code, rows = quan(w, {"stock": {"ca_loc": 1}}, ticks=Q["first_customer_tick"] + 5)
            self.assertEqual(code, 0, rows)
            ev = events(rows, "customer_arrived")
            self.assertEqual(len(ev), 1)
            self.assertEqual(ev[0]["tick"], Q["first_customer_tick"])
            self.assertEqual(ev[0]["data"], {"order_id": "C1", "table_id": "T1", "dish_id": DISH})
            s = snapshots(rows)[-1]
            self.assertEqual(s["stock"], {"ca_loc": 1}, "tồn vật lý không đổi, chỉ giữ chỗ")
            c = s["customers"][0]
            self.assertEqual((c["order_status"], c["reserved"], c["order_tick"]),
                             ("reserved", {"ca_loc": 1}, Q["first_customer_tick"]))
            self.assertEqual(c["patience_ticks_left"], PATIENCE - 5)
            self.assertEqual(s["tables"][0]["customer_id"], "C1")

    def test_khong_du_nguyen_lieu_no_dish(self):
        with Workdir() as w:
            code, rows = quan(w, {}, ticks=Q["first_customer_tick"] + 1)
            self.assertEqual(code, 0, rows)
            self.assertEqual([e["tick"] for e in events(rows, "no_dish")], [Q["first_customer_tick"]])
            self.assertEqual(events(rows, "customer_arrived"), [])
            self.assertEqual(snapshots(rows)[-1]["customers"], [])

    def test_random_customers_false_tat_khach_tu_sinh(self):
        with Workdir() as w:
            code, rows = quan(w, {"stock": {"ca_loc": 1}, "random_customers": False}, ticks=Q["first_customer_tick"] + 5)
            self.assertEqual(code, 0, rows)
            self.assertEqual(events(rows, "customer_arrived") + events(rows, "no_dish"), [])

    def test_khong_con_ban_bo_luot(self):
        with Workdir() as w:
            # v1.1 có 4 bàn: ngồi kín cả 4 thì khách mới bỏ lượt
            full = [waiting(f"C{i + 1}", table_id=tb["id"]) for i, tb in enumerate(Q["tables"])]
            code, rows = quan(w, {"stock": {"ca_loc": len(full) + 1}, "customers": full},
                              ticks=Q["first_customer_tick"] + 5)
            self.assertEqual(code, 0, rows)
            self.assertEqual(events(rows, "customer_arrived") + events(rows, "no_dish"), [])


class Cooking(unittest.TestCase):
    def test_bep_nhan_don_cu_nhat_tieu_nguyen_lieu(self):
        with Workdir() as w:
            code, rows = quan(w, {"player": {"pos": B1}, "stock": {"ca_loc": 1}, "random_customers": False,
                                  "customers": [waiting()]}, inputs=[{"tick": 0, "interact": True}], ticks=1)
            self.assertEqual(code, 0, rows)
            ev = events(rows, "cook_started")[0]
            self.assertEqual(ev["tick"], 1)
            self.assertEqual(ev["data"], {"stove_id": "B1", "order_id": "C1", "dish_id": DISH,
                                          "items": ["ca_loc"], "base_price": PRICE})
            s = snapshots(rows)[-1]
            self.assertEqual(s["stock"], {})
            self.assertEqual(s["stoves"][0]["state"], "cooking")
            self.assertEqual(s["stoves"][0]["cook_ticks_left"], COOK)
            self.assertEqual((s["customers"][0]["order_status"], s["customers"][0]["reserved"]), ("assigned", {}))

    def test_mon_chin_dung_tick(self):
        with Workdir() as w:
            code, rows = quan(w, {"player": {"pos": B1}, "stock": {"ca_loc": 1}, "random_customers": False,
                                  "customers": [waiting()]}, inputs=[{"tick": 0, "interact": True}, {"tick": 1, "interact": False}],
                              ticks=COOK + 5, every=COOK)
            self.assertEqual(code, 0, rows)
            self.assertEqual([e["tick"] for e in events(rows, "dish_ready")], [1 + COOK])

    def test_lay_mon_khi_tay_trong(self):
        with Workdir() as w:
            blk = {"player": {"pos": B1}, "random_customers": False, "customers": [waiting(order_status="assigned")],
                   "stoves": [{"id": "B1", "state": "ready", "dish": {"order_id": "C1", "dish_id": DISH}}]}
            code, rows = quan(w, blk, inputs=[{"tick": 0, "interact": True}], ticks=1)
            self.assertEqual(code, 0, rows)
            self.assertEqual(events(rows, "dish_picked")[0]["data"], {"stove_id": "B1", "order_id": "C1", "dish_id": DISH})
            s = snapshots(rows)[-1]
            self.assertEqual(s["hand"], {"order_id": "C1", "dish_id": DISH, "base_price": PRICE})
            self.assertEqual(s["stoves"][0]["state"], "idle")

    def test_ready_ticks_chi_tang_tu_dau_buoc(self):
        with Workdir() as w:
            blk = {"random_customers": False, "customers": [waiting(order_status="assigned")],
                   "stoves": [{"id": "B1", "state": "ready", "dish": {"order_id": "C1", "dish_id": DISH}}]}
            code, rows = quan(w, blk, ticks=3)
            self.assertEqual(code, 0, rows)
            self.assertEqual([s["stoves"][0]["ready_ticks"] for s in snapshots(rows)], [0, 1, 2, 3])


class Serving(unittest.TestCase):
    def serve(self, patience):
        with Workdir() as w:
            blk = {"player": {"pos": T1}, "random_customers": False, "hand": {"order_id": "C1", "dish_id": DISH},
                   "customers": [waiting(order_status="assigned", patience_ticks_left=patience)]}
            code, rows = quan(w, blk, inputs=[{"tick": 0, "interact": True}], ticks=1)
            self.assertEqual(code, 0, rows)
            return rows

    def test_boa_khi_con_du_kien_nhan(self):
        rows = self.serve(PATIENCE - 1)
        d = events(rows, "served")[0]["data"]
        self.assertEqual((d["base_price"], d["tip"]), (PRICE, int(PRICE * Q["tip_rate"])))
        s = snapshots(rows)[-1]
        self.assertIsNone(s["hand"])
        c = s["customers"][0]
        self.assertEqual((c["state"], c["order_status"], c["eat_ticks_left"]), ("eating", "served", EAT))

    def test_khong_boa_khi_kien_nhan_thap(self):
        rows = self.serve(int(Q["tip_min_patience_ratio"] * PATIENCE) - 10)
        self.assertEqual(events(rows, "served")[0]["data"]["tip"], 0)

    def test_phuc_vu_dung_tick_kien_nhan_ve_0_van_hop_le(self):
        rows = self.serve(1)  # sau bước 1 còn 0
        self.assertEqual(len(events(rows, "served")), 1)
        self.assertEqual(events(rows, "customer_left"), [])

    def test_hai_khach_cung_ban_exit_2(self):
        with Workdir() as w:
            blk = {"stock": {"ca_loc": 2}, "customers": [waiting("C1"), waiting("C2")]}
            self.assertEqual(quan(w, blk, ticks=1)[0], 2)


class Payment(unittest.TestCase):
    def test_tra_tien_boa_va_uy_tin(self):
        with Workdir() as w:
            blk = {"player": {"pos": T1}, "random_customers": False, "hand": {"order_id": "C1", "dish_id": DISH},
                   "customers": [waiting(order_status="assigned")]}
            code, rows = quan(w, blk, inputs=[{"tick": 0, "interact": True}], ticks=EAT + 5, every=EAT + 5)
            self.assertEqual(code, 0, rows)
            paid = events(rows, "paid")[0]
            tip = int(PRICE * Q["tip_rate"])
            self.assertEqual(paid["tick"], 1 + EAT)
            self.assertEqual(paid["data"], {"order_id": "C1", "table_id": "T1", "base_price": PRICE, "tip": tip,
                                            "amount": PRICE + tip, "reason": "finished_eating"})
            s = snapshots(rows)[-1]
            self.assertEqual((s["money"], s["earned"], s["customers"]), (PRICE + tip, PRICE + tip, []))
            self.assertTrue(close(s["reputation"], Q["reputation_initial"] + Q["tip_reputation"], 0.01))
            self.assertEqual(s["score"], PRICE + tip + 100 * int(s["reputation"]))

    def test_het_kien_nhan_roi_va_tru_uy_tin(self):
        with Workdir() as w:
            code, rows = quan(w, {"stock": {"ca_loc": 1}, "random_customers": False, "customers": [waiting(patience_ticks_left=3)]}, ticks=5)
            self.assertEqual(code, 0, rows)
            ev = events(rows, "customer_left")
            self.assertEqual((ev[0]["tick"], ev[0]["data"]["reason"]), (3, "patience"))
            self.assertTrue(close(ev[0]["data"]["reputation"], Q["reputation_initial"] + Q["left_reputation_delta"], 0.01))
            self.assertEqual(snapshots(rows)[-1]["customers"], [])

    def test_khach_roi_bo_mon_dang_nau(self):
        with Workdir() as w:
            blk = {"random_customers": False, "customers": [waiting(order_status="assigned", patience_ticks_left=2)],
                   "stoves": [{"id": "B1", "state": "cooking", "cook_ticks_left": 100,
                               "dish": {"order_id": "C1", "dish_id": DISH}}]}
            code, rows = quan(w, blk, ticks=3)
            self.assertEqual(code, 0, rows)
            self.assertEqual(snapshots(rows)[-1]["stoves"][0]["state"], "idle")

    def test_het_ca_don_ban_khong_tru_uy_tin(self):
        with Workdir() as w:
            blk = {"stock": {"ca_loc": 1}, "random_customers": False, "time_left_ticks": 5,
                   "customers": [waiting()]}
            code, rows = quan(w, blk, ticks=100)
            self.assertEqual(code, 0, rows)
            left = events(rows, "customer_left")[0]
            self.assertEqual((left["tick"], left["data"]["reason"]), (5, "closing"))
            self.assertEqual(left["data"]["reputation"], Q["reputation_initial"])
            qe = events(rows, "quan_end")[0]
            self.assertEqual((qe["tick"], qe["data"]["reason"]), (5, "time"))
            self.assertEqual(rows[-1]["reason"], "time")
            self.assertEqual(rows[-1]["state"], "finished")
            self.assertEqual([r["name"] for r in events(rows)][-2:], ["customer_left", "quan_end"])

    def test_het_ca_khach_dang_an_tra_ngay(self):
        with Workdir() as w:
            blk = {"random_customers": False, "time_left_ticks": 3,
                   "customers": [waiting(state="eating", eat_ticks_left=500, base_price=PRICE, tip=12)]}
            code, rows = quan(w, blk, ticks=10)
            self.assertEqual(code, 0, rows)
            paid = events(rows, "paid")[0]["data"]
            self.assertEqual((paid["reason"], paid["amount"]), ("closing", PRICE + 12))
            qe = events(rows, "quan_end")[0]["data"]
            self.assertEqual((qe["money"], qe["earned"], qe["shift_earned"]), (PRICE + 12,) * 3)


class Determinism(unittest.TestCase):
    def test_cung_seed_cung_byte(self):
        with Workdir() as w:
            inp = write_json(w.path("in.json"), frames(
                {"tick": 0, "move": [0, 1]}, {"tick": 60, "move": [-1, 0], "interact": True},
                {"tick": 61, "interact": False}, {"tick": 200, "move": [1, -1]}))
            inv = write_json(w.path("inv.json"), {"items": {"ca_loc": 5, "bong_sung": 4, "ca_linh": 3, "bong_dien_dien": 2}})
            for i in (1, 2):
                code, err = run_headless("--mode", "quan", "--seed", "7", "--ticks", "3000", "--inputs", inp,
                                         "--inventory", inv, "--out", w.path(f"o{i}.jsonl"))
                self.assertEqual(code, 0, err)
            with open(w.path("o1.jsonl"), "rb") as a, open(w.path("o2.jsonl"), "rb") as b:
                self.assertEqual(a.read(), b.read())
            self.assertTrue(events(read_jsonl(w.path("o1.jsonl")), "customer_arrived"))

    def test_seed_khac_co_the_chon_mon_khac(self):
        with Workdir() as w:
            inv = write_json(w.path("inv.json"), {"items": {"ca_loc": 5, "bong_sung": 4, "ca_linh": 3, "bong_dien_dien": 2}})
            dishes = set()
            for seed in range(12):
                code, err = run_headless("--mode", "quan", "--seed", str(seed), "--ticks", str(Q["first_customer_tick"]),
                                         "--inventory", inv, "--out", w.path("o.jsonl"))
                self.assertEqual(code, 0, err)
                dishes |= {e["data"]["dish_id"] for e in events(read_jsonl(w.path("o.jsonl")), "customer_arrived")}
            self.assertGreater(len(dishes), 1)


class ScenarioContradictions(unittest.TestCase):
    """PRD-0 mục D: mâu thuẫn mức luật -> mã thoát 2, không ghi đầu ra."""

    def test_mau_thuan_exit_2(self):
        bad = {
            "giữ quá tồn": {"stock": {}, "customers": [waiting()]},
            "giữ khác công thức": {"stock": {"ca_loc": 5}, "customers": [waiting(reserved={"ca_loc": 2})]},
            "assigned không có món": {"customers": [waiting(order_status="assigned")]},
            "unfulfillable còn giữ chỗ": {"stock": {"ca_loc": 1}, "customers": [waiting(order_status="unfulfillable", reserved={"ca_loc": 1})]},
            "eating thiếu timer": {"customers": [waiting(state="eating")]},
            "waiting nhưng served": {"customers": [waiting(order_status="served")]},
            "dish_id lạ": {"customers": [waiting(dish_id="pho")]},
            "thiếu dish_id": {"customers": [{"id": "C1", "table_id": "T1"}]},
            "bếp id không tồn tại": {"stoves": [{"id": "B9"}]},
            "bàn id không tồn tại": {"tables": [{"id": "T9"}]},
            "bếp ngoài miền": {"stoves": [{"id": "B1", "pos": [99, 5]}]},
            "bếp cooking thiếu món": {"stoves": [{"id": "B1", "state": "cooking", "cook_ticks_left": 5}]},
            "bếp idle còn món": {"customers": [waiting(order_status="assigned")],
                                 "stoves": [{"id": "B1", "dish": {"order_id": "C1", "dish_id": DISH}}]},
            "món tham chiếu khách không có": {"stoves": [{"id": "B1", "state": "ready", "dish": {"order_id": "C9", "dish_id": DISH}}]},
            "món không khớp đơn": {"customers": [waiting(order_status="assigned")],
                                   "stoves": [{"id": "B1", "state": "ready", "dish": {"order_id": "C1", "dish_id": "goi_bong_sung"}}]},
            "bếp và tay cùng đơn": {"customers": [waiting(order_status="assigned")],
                                    "hand": {"order_id": "C1", "dish_id": DISH},
                                    "stoves": [{"id": "B1", "state": "ready", "dish": {"order_id": "C1", "dish_id": DISH}}]},
            "kho nguyên liệu lạ": {"stock": {"pho": 1}},
            "kho âm": {"stock": {"ca_loc": -1}},
            "uy tín ngoài miền": {"reputation": 9},
            "timer bếp âm": {"stoves": [{"id": "B1", "cook_ticks_left": -1}]},
            "kiên nhẫn quá đầy": {"stock": {"ca_loc": 1}, "customers": [waiting(patience_ticks_left=PATIENCE + 1)]},
            "trường lạ": {"customers": [waiting(mood="vui")]},
        }
        with Workdir() as w:
            for name, blk in bad.items():
                code, _ = quan(w, blk, ticks=1)
                self.assertEqual(code, 2, name)
                self.assertFalse(__import__("os").path.exists(w.path("o.jsonl")), name)

    def test_kho_inventory_thieu_cho_giu_exit_2(self):
        with Workdir() as w:
            inv = write_json(w.path("inv.json"), {"items": {}})
            code, _ = quan(w, {"customers": [waiting()]}, ticks=1, inventory=inv)
            self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
