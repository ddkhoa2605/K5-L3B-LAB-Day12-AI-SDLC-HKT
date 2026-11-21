"""Độ tươi + kho cá thể (TICKET-03, Test Contract v1.2): hao, ươn, giữ theo id, giá theo tươi, bàn giao.

Đơn vị: 240 đơn vị = 1 điểm tươi. Gather hao 2 đơn vị/tick (0.5/s), quán 1 đơn vị/tick (0.25/s), ươn khi < 30 điểm
(= 7200 đơn vị). Chạy: PYTHONPATH=tests:. python3 -m unittest discover -s tests -v
"""

import json
import unittest

from chonoi import freshness
from chonoi.contract import load_contract
from chonoi.errors import BadInput
from chonoi.ids import IdAllocator
from chonoi.inputs import InputState
from chonoi.rng import Streams
from chonoi.runner import Session
from chonoi.sim.quan import QuanSim
from helpers import Workdir, counts, events, frames, make_items, read_jsonl, run_headless, snapshots, write_json

TUNING = load_contract()["tuning"]
RATES = freshness.Rates(TUNING["freshness"])
MENU = TUNING["menu"]
DISH = "ca_loc_nuong_trui"
PRICE = MENU[DISH]["price"]


def item(i, kind="ca_loc", fresh=100.0):
    return {"id": f"I{i}", "kind": kind, "fresh": fresh}


def units(u):
    """Độ tươi (điểm) đúng bằng u đơn vị."""
    return u / freshness.UNITS


def idle():
    return InputState((0.0, 0.0), {}, set())


def press(button):
    return InputState((0.0, 0.0), {button: True}, {button})


def gather(hold, **extra):
    sc = {"hold": hold, "random_fish": False, "nodes": [], "player": {"pos": [20.0, 5.0]}}
    sc.update(extra)
    return Session("gather", TUNING, sc, 1)


def quan(stock, customers=(), seed=1, **extra):
    sc = {"stock": stock, "customers": list(customers), "random_customers": False, "random_reservations": False}
    sc.update(extra)
    return QuanSim(TUNING, sc, Streams(seed), IdAllocator())


def qstep(s, pressed=()):
    return s.step(InputState((0.0, 0.0), {}, set(pressed)))


def cust(cid="C1", table="T1", dish=DISH, **kw):
    c = {"id": cid, "table_id": table, "dish_id": dish}
    c.update(kw)
    return c


class Units(unittest.TestCase):
    def test_he_so_quy_ra_so_nguyen(self):
        self.assertEqual((RATES.initial, RATES.gather_per_tick, RATES.quan_per_tick, RATES.spoiled_u), (24000, 2, 1, 7200))

    def test_he_so_khong_nguyen_bi_tu_choi(self):
        with self.assertRaises(BadInput):
            freshness.Rates({"initial": 100, "gather_decay_per_s": 0.3, "quan_decay_per_s": 0.25, "spoiled_below": 30})

    def test_gia_theo_trung_binh_tuoi_floor_nguyen(self):
        self.assertEqual(freshness.price(60, [{"u": 24000}]), 60)
        self.assertEqual(freshness.price(60, [{"u": 23400}]), 58)  # fresh 97.5 -> 58.5 -> 58
        self.assertEqual(freshness.price(120, [{"u": 24000}, {"u": 12000}]), 90)  # TB 75
        self.assertEqual(freshness.price(40, [{"u": 0}]), 0)

    def test_pick_tuoi_nhat_hoa_id_nho_bo_qua_uon(self):
        items = [{"id": "I2", "kind": "ca_loc", "u": 20000}, {"id": "I10", "kind": "ca_loc", "u": 20000},
                 {"id": "I3", "kind": "ca_loc", "u": 7199}, {"id": "I1", "kind": "ca_loc", "u": 24000}]
        self.assertEqual([i["id"] for i in freshness.pick(items, "ca_loc", 3, RATES)], ["I1", "I2", "I10"])
        self.assertIsNone(freshness.pick(items, "ca_loc", 4, RATES), "cá thể ươn không dùng được")


class GatherDecay(unittest.TestCase):
    def test_vi_du_ticket_spoiled_o_buoc_dau_qua_cli(self):
        with Workdir() as w:
            sc = write_json(w.path("sc.json"), {"gather": {"hold": [item(1, "ca_linh", 30)], "random_fish": False,
                                                           "monsters": []}})
            code, err = run_headless("--mode", "gather", "--seed", "1", "--ticks", "1", "--scenario", sc,
                                     "--out", w.path("o.jsonl"))
            self.assertEqual(code, 0, err)
            ev = events(read_jsonl(w.path("o.jsonl")), "spoiled")
            self.assertEqual(ev, [{"type": "event", "tick": 1, "phase": "gather", "name": "spoiled",
                                   "data": {"item_id": "I1", "kind": "ca_linh", "location": "hold"}}])

    def test_monsters_khac_rong_chua_ho_tro(self):
        with Workdir() as w:
            sc = write_json(w.path("sc.json"), {"gather": {"monsters": [{"id": "M1"}]}})
            self.assertEqual(run_headless("--mode", "gather", "--seed", "1", "--ticks", "0", "--scenario", sc,
                                          "--out", w.path("o.jsonl"))[0], 2)

    def test_nhanh_o_nguong_30_dung_mot_don_vi(self):
        s = gather([item(1, fresh=units(7202))])  # 30.0083: bước 1 -> 7200 (chưa ươn), bước 2 -> 7198 (ươn)
        self.assertEqual([e["name"] for e in s.step(idle())], [])
        self.assertEqual(s.sim.hold[0]["u"], 7200)
        ev = s.step(idle())
        self.assertEqual([(e["name"], e["tick"]) for e in ev], [("spoiled", 2)])

    def test_hao_0_5_moi_giay_va_ep_day_0(self):
        s = gather([item(1)])
        for _ in range(60):
            s.step(idle())
        self.assertEqual(s.snapshot()["hold"][0]["fresh"], 99.5)
        s = gather([item(1, fresh=units(1))])
        for _ in range(3):
            s.step(idle())
        self.assertEqual(s.sim.hold[0]["u"], 0)

    def test_da_uon_tu_dau_thi_khong_phat_lai(self):
        s = gather([item(1, fresh=10)])
        self.assertEqual([e["name"] for _ in range(5) for e in s.step(idle())], [])

    def test_nhieu_ca_the_cung_vuot_nguong_phat_theo_id(self):
        s = gather([item(10, fresh=30), item(2, fresh=30), item(1, "bong_sung", 30)])
        ev = s.step(idle())
        self.assertEqual([e["data"]["item_id"] for e in ev if e["name"] == "spoiled"], ["I1", "I2", "I10"])

    def test_hang_moi_100_va_hao_tu_buoc_sau(self):
        s = Session("gather", TUNING, {"player": {"pos": [12.0, 0.0]}, "random_fish": False,
                                        "nodes": [{"id": "N1", "kind": "bong_dien_dien", "pos": [12.0, 0.0]}]}, 1)
        s.step(press("interact"))
        self.assertEqual([i["u"] for i in s.sim.hold], [24000])
        s.step(idle())
        self.assertEqual([i["u"] for i in s.sim.hold], [23998])

    def test_gio_chiem_o_ke_ca_hang_uon(self):
        cap = TUNING["gather"]["hold_capacity"]
        s = Session("gather", TUNING, {"player": {"pos": [12.0, 0.0]}, "random_fish": False,
                                        "hold": make_items({"ca_loc": cap}, fresh=5),
                                        "nodes": [{"id": "N1", "kind": "bong_dien_dien", "pos": [12.0, 0.0]}]}, 1)
        self.assertEqual([e["name"] for e in s.step(press("interact"))], ["hold_full"])

    def test_pause_dung_hao_tuoi(self):
        with Workdir() as w:
            sc = write_json(w.path("sc.json"), {"gather": {"hold": [item(1)], "random_fish": False}})
            inp = write_json(w.path("in.json"), frames({"tick": 0, "pause": True}, {"tick": 1, "pause": False},
                                                       {"tick": 10, "pause": True}, {"tick": 11, "pause": False}))
            code, err = run_headless("--mode", "gather", "--seed", "1", "--ticks", "12", "--scenario", sc,
                                     "--inputs", inp, "--snapshot-every", "1", "--out", w.path("o.jsonl"))
            self.assertEqual(code, 0, err)
            snaps = {x["tick"]: x for x in snapshots(read_jsonl(w.path("o.jsonl")))}
            # cạnh lên ở tick 0 vào pause; cạnh lên kế tiếp (tick 10) thoát pause và chạy gameplay ngay bước đó
            self.assertEqual({snaps[t]["hold"][0]["fresh"] for t in range(1, 11)}, {100}, "đang pause: không hao")
            self.assertAlmostEqual(snaps[11]["hold"][0]["fresh"], 100 - 2 / 240, places=3)
            self.assertAlmostEqual(snaps[12]["hold"][0]["fresh"], 100 - 4 / 240, places=3)


class QuanDecayAndReserve(unittest.TestCase):
    def test_hao_0_25_moi_giay_ke_ca_hang_dang_giu(self):
        s = quan(make_items({"ca_loc": 2}), [cust()])
        self.assertEqual(s.customers[0]["reserved"], ["I1"])
        for _ in range(240):
            qstep(s)
        self.assertEqual([i["u"] for i in s.stock], [24000 - 240, 24000 - 240])

    def test_spoiled_stock_mot_lan_theo_id(self):
        s = quan([item(10, fresh=30), item(2, "bong_sung", 30), item(1, fresh=100)])
        ev = qstep(s)
        self.assertEqual([(n, d["item_id"], d["location"]) for n, d in ev], [("spoiled", "I2", "stock"), ("spoiled", "I10", "stock")])
        self.assertEqual([n for _ in range(5) for n, _d in qstep(s)], [])

    def test_giu_theo_id_tuoi_nhat_hoa_id_nho(self):
        s = quan([item(1, fresh=50), item(2, fresh=80), item(3, fresh=80)], [cust()])
        self.assertEqual(s.customers[0]["reserved"], ["I2"])

    def test_gioi_thieu_giu_cho_tu_dong_theo_order_tick_roi_id_ban(self):
        # hai khách chưa khai reserved: đơn cũ nhất (order_tick nhỏ, rồi id bàn nhỏ) lấy cá thể tươi nhất
        s = quan([item(1, fresh=60), item(2, fresh=90)], [cust("C1", "T2", order_tick=0), cust("C2", "T1", order_tick=0)])
        by = {c["id"]: c["reserved"] for c in s.customers}
        self.assertEqual(by, {"C2": ["I2"], "C1": ["I1"]})

    def test_giu_phan_vua_uon_nha_het_va_giu_lai_mot_lan(self):
        s = quan([item(1, fresh=30), item(2, fresh=60)], [cust(reserved=["I1"])])
        ev = qstep(s)
        self.assertEqual([n for n, _ in ev], ["spoiled"])
        self.assertEqual((s.customers[0]["order_status"], s.customers[0]["reserved"]), ("reserved", ["I2"]))

    def test_khong_du_thi_unfulfillable_khach_van_cho(self):
        s = quan([item(1, fresh=30)], [cust(reserved=["I1"])])
        qstep(s)
        c = s.customers[0]
        self.assertEqual((c["order_status"], c["reserved"], c["state"]), ("unfulfillable", [], "waiting"))
        s.pos = [2.0, 8.0]
        self.assertEqual(qstep(s, {"interact"}), [], "đơn unfulfillable không được nấu")

    def test_xu_ly_don_bi_anh_huong_theo_order_tick_roi_id_ban(self):
        stock = [item(1, fresh=30), item(2, fresh=30), item(3, fresh=100)]
        s = quan(stock, [cust("C1", "T2", order_tick=5, reserved=["I1"]), cust("C2", "T1", order_tick=3, reserved=["I2"])])
        qstep(s)
        by = {c["id"]: (c["order_status"], c["reserved"]) for c in s.customers}
        self.assertEqual(by, {"C2": ("reserved", ["I3"]), "C1": ("unfulfillable", [])})

    def test_khach_moi_khong_dung_hang_uon_no_dish(self):
        s = quan([item(1, fresh=10)], random_customers=True)
        names = [n for _ in range(TUNING["quan"]["first_customer_tick"]) for n, _d in qstep(s)]
        self.assertEqual([n for n in names if n != "spoiled"], ["no_dish"])

    def test_kho_quan_nhan_ca_hang_uon(self):
        with Workdir() as w:
            inv = write_json(w.path("inv.json"), {"items": [item(1, fresh=5), item(2, "ca_linh", 0)]})
            code, err = run_headless("--mode", "quan", "--seed", "1", "--ticks", "0", "--inventory", inv,
                                     "--out", w.path("q.jsonl"))
            self.assertEqual(code, 0, err)
            self.assertEqual([i["id"] for i in snapshots(read_jsonl(w.path("q.jsonl")))[0]["stock"]], ["I1", "I2"])

    def test_nguong_30_doc_lai_tu_file_giu_dung_nhanh(self):
        with Workdir() as w:
            inv = write_json(w.path("inv.json"), {"items": [item(1, fresh=7201 / 240)]})
            code, err = run_headless("--mode", "quan", "--seed", "1", "--ticks", "3", "--inventory", inv,
                                     "--snapshot-every", "1", "--out", w.path("q.jsonl"))
            self.assertEqual(code, 0, err)
            self.assertEqual([(e["tick"], e["name"]) for e in events(read_jsonl(w.path("q.jsonl")), "spoiled")], [(2, "spoiled")])


class CookPrice(unittest.TestCase):
    def test_nau_tieu_dung_id_da_giu_va_chot_gia_theo_tuoi(self):
        s = quan([item(1, fresh=97.5), item(2, fresh=50)], [cust(reserved=["I1"])], player={"pos": [2, 8]})
        (name, d), = qstep(s, {"interact"})
        self.assertEqual(name, "cook_started")
        self.assertEqual([i["id"] for i in d["items"]], ["I1"])
        # hao 1 đơn vị ở đầu bước: 23400 -> 23399, giá = floor(60 * 23399 / 24000) = 58
        self.assertEqual(d["base_price"], 60 * 23399 // 24000)
        self.assertEqual([i["id"] for i in s.stock], ["I2"])
        self.assertEqual(s.customers[0]["base_price"], 58)

    def test_gia_lau_mam_theo_trung_binh_nhieu_ca_the(self):
        stock = [item(1, "bong_dien_dien", 100), item(2, "ca_keo", 80), item(3, "ca_linh", 60), item(4, "ca_linh", 40),
                 item(5, "keo_neo", 20 + 30)]
        s = quan(stock, [cust(dish="lau_mam")], player={"pos": [2, 8]})
        (_, d), = qstep(s, {"interact"})
        used = [freshness.from_external(i) for i in stock]
        for i in used:
            i["u"] -= 1
        self.assertEqual(d["base_price"], freshness.price(200, used))
        self.assertEqual([(i["kind"], i["id"]) for i in d["items"]], sorted((i["kind"], i["id"]) for i in d["items"]))

    def test_boa_tinh_tren_gia_da_chot(self):
        s = quan([], [cust(order_status="assigned")], player={"pos": [9, 2]}, hand={"order_id": "C1", "dish_id": DISH, "base_price": 58})
        (_, d), = qstep(s, {"interact"})
        self.assertEqual((d["base_price"], d["tip"]), (58, 11))  # floor(58 * 0.2)

    def test_mon_chin_khong_hao(self):
        s = quan([], [cust(order_status="assigned")],
                 stoves=[{"id": "B1", "state": "ready", "dish": {"order_id": "C1", "dish_id": DISH, "base_price": 58}}])
        for _ in range(500):
            qstep(s)
        self.assertEqual(s.stoves[0]["dish"]["base_price"], 58)


class DayHandover(unittest.TestCase):
    def day(self, w, scenario, inputs, ticks, every=1, days=1):
        sc = write_json(w.path("sc.json"), scenario)
        args = ["--mode", "day", "--seed", "1", "--ticks", str(ticks), "--snapshot-every", str(every), "--scenario", sc,
                "--days", str(days), "--out", w.path("o.jsonl")]
        if inputs:
            args += ["--inputs", write_json(w.path("in.json"), frames(*inputs))]
        code, err = run_headless(*args)
        self.assertEqual(code, 0, err)
        return read_jsonl(w.path("o.jsonl"))

    def test_ban_giao_khong_hao_them_o_tick_chuyen_pha(self):
        hold = make_items({"ca_loc": 1, "bong_sung": 2})
        with Workdir() as w:
            rows = self.day(w, {"gather": {"hold": hold, "random_fish": False}, "quan": {"random_customers": False, "random_reservations": False}},
                            [{"tick": 0, "interact": True}], ticks=4)
            snaps = {s["tick"]: s for s in snapshots(rows)}
            end = events(rows, "gather_end")[0]["data"]["inventory"]["items"]
            self.assertEqual(snaps[1]["phase"], "quan")
            self.assertEqual([i["fresh"] for i in snaps[1]["stock"]], [round(i["fresh"], 3) for i in end],
                             "tick chuyển pha: quán nhận đúng độ tươi lúc gather_end")
            self.assertEqual([i["id"] for i in snaps[1]["stock"]], [i["id"] for i in end])
            self.assertEqual(snaps[2]["stock"][0]["fresh"], round(23998 / 240 - 1 / 240, 3), "quán hao từ bước sau")

    def test_shop_khong_hao_va_id_tang_xuyen_ngay(self):
        hold = make_items({"ca_loc": 1, "bong_sung": 2})
        quan_ticks = int(round(TUNING["quan"]["duration_s"] * 60))
        shop = 1 + quan_ticks
        with Workdir() as w:
            rows = self.day(w, {"gather": {"hold": hold, "random_fish": False}, "quan": {"random_customers": False, "random_reservations": False}},
                            [{"tick": 0, "interact": True}, {"tick": 1, "interact": False},
                             {"tick": shop + 50, "shop_done": True}, {"tick": shop + 51, "shop_done": False},
                             {"tick": shop + 52, "interact": True}], ticks=shop + 60, every=10, days=2)
            shops = [s for s in snapshots(rows) if s["phase"] == "shop"]
            self.assertTrue(shops)
            self.assertEqual({tuple(i["fresh"] for i in s["stock"]) for s in shops}, {tuple(i["fresh"] for i in shops[0]["stock"])},
                             "hàng thô ở Shop không hao tươi")
            last = snapshots(rows)[-1]
            # Ngày 2: cập bến ngay (frame shop+52) nên đang ở quán với kho = mẫu gather.hold cấp id mới
            self.assertEqual((last["day"], last["phase"]), (2, "quan"))
            self.assertEqual(sorted(i["id"] for i in last["stock"]), ["I4", "I5", "I6"], "Ngày kế cấp id mới, tăng tiếp")
            self.assertEqual(counts(last["stock"]), counts(hold))


class ScenarioContradictions(unittest.TestCase):
    def check(self, block, mode="quan"):
        with Workdir() as w:
            sc = write_json(w.path("sc.json"), {mode: block})
            return run_headless("--mode", mode, "--seed", "1", "--ticks", "0", "--scenario", sc, "--out", w.path("o.jsonl"))[0]

    def test_mau_thuan_exit_2(self):
        stock = make_items({"ca_loc": 2})
        bad = {
            "reserved trỏ id không có": {"stock": stock, "customers": [cust(reserved=["I9"])]},
            "reserved dùng chung": {"stock": stock, "customers": [cust("C1", "T1", reserved=["I1"]), cust("C2", "T2", reserved=["I1"])]},
            "reserved cá thể ươn": {"stock": [item(1, fresh=10), item(2)], "customers": [cust(reserved=["I1"])]},
            "reserved sai công thức": {"stock": stock, "customers": [cust(reserved=["I1", "I2"])]},
            "reserved sai kind": {"stock": make_items({"bong_sung": 2}), "customers": [cust(reserved=["I1"])]},
            "reserved là map cũ": {"stock": stock, "customers": [cust(reserved={"ca_loc": 1})]},
            "reserved id trùng trong đơn": {"stock": stock, "customers": [cust(reserved=["I1", "I1"])]},
            "id kho trùng": {"stock": [item(1), item(1)]},
            "kho là map đếm": {"stock": {"ca_loc": 1}},
            "thiếu cá thể để cấp tự động": {"stock": [], "customers": [cust()]},
        }
        for name, block in bad.items():
            self.assertEqual(self.check(block), 2, name)

    def test_gather_hold_kho_dem_hoac_sai_exit_2(self):
        for name, hold in {"hold kind cũ": ["ca_loc"], "hold map đếm": {"ca_loc": 1},
                           "hold fresh âm": [item(1, fresh=-1)], "hold id trùng": [item(1), item(1)]}.items():
            self.assertEqual(self.check({"hold": hold}, "gather"), 2, name)


class Persistence(unittest.TestCase):
    def test_xuat_kho_theo_id_dung_chinh_xac(self):
        with Workdir() as w:
            hold = [item(10, "ca_loc", 100), item(2, "bong_sung", 100)]
            sc = write_json(w.path("sc.json"), {"gather": {"hold": hold, "random_fish": False,
                                                           "player": {"pos": [2.0, 0.0]}}})
            inp = write_json(w.path("in.json"), frames({"tick": 0, "interact": True}))
            inv = w.path("inv.json")
            code, err = run_headless("--mode", "gather", "--seed", "1", "--ticks", "1", "--scenario", sc, "--inputs", inp,
                                     "--inventory-out", inv, "--out", w.path("g.jsonl"))
            self.assertEqual(code, 0, err)
            with open(inv, encoding="utf-8") as f:
                saved = json.load(f)
            self.assertEqual([i["id"] for i in saved["items"]], ["I2", "I10"], "xuất theo id (F2 trước F10)")
            self.assertEqual({i["fresh"] for i in saved["items"]}, {23998 / 240})
            # đọc lại ra đúng đơn vị (round-trip chính xác)
            code, err = run_headless("--mode", "quan", "--seed", "1", "--ticks", "0", "--inventory", inv, "--out", w.path("q.jsonl"))
            self.assertEqual(code, 0, err)

    def test_ngat_ghi_kho_rong(self):
        s = Session("gather", TUNING, {"player": {"pos": [20.0, 10.0], "oxygen_ticks": 0, "hp": 1},
                                        "hold": make_items({"ca_loc": 2}), "random_fish": False, "nodes": []}, 1)
        evs = []
        for _ in range(TUNING["gather"]["choke_interval_ticks"]):
            evs += s.step(idle())
        end = [e for e in evs if e["name"] == "gather_end"][0]["data"]
        self.assertEqual(end, {"reason": "fainted", "inventory": {"items": []}})
        faint = [e for e in evs if e["name"] == "faint"][0]["data"]
        self.assertEqual([i["id"] for i in faint["lost"]], ["I2", "I1"], "LIFO theo thứ tự vào giỏ")


if __name__ == "__main__":
    unittest.main()
