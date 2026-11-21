"""Mở rộng `burn` (TICKET-02 mục 3): món ready quá burn_s bị cháy. Mặc định (burn_s null) tắt hẳn."""

import copy
import json
import unittest

from chonoi.contract import KNOWN_EXTENSIONS, load_contract
from chonoi.errors import BadInput
from chonoi.ids import IdAllocator
from chonoi.inputs import InputState
from chonoi.rng import Streams
from chonoi.sim.quan import QuanSim
from helpers import Workdir, write_json

with open("game.contract.json", encoding="utf-8") as _f:
    CONTRACT = json.load(_f)
BURN = copy.deepcopy(CONTRACT["tuning"])
BURN["quan"]["burn_s"] = 20
LIMIT = 20 * 60
DISH = "ca_loc_nuong_trui"


def sim(tuning=BURN, ready_ticks=0, stock=None, extra_customers=()):
    sc = {"random_customers": False, "stock": stock or {},
          "customers": [{"id": "C1", "table_id": "T1", "dish_id": DISH, "order_status": "assigned"}, *extra_customers],
          "stoves": [{"id": "B1", "state": "ready", "ready_ticks": ready_ticks,
                      "dish": {"order_id": "C1", "dish_id": DISH}}]}
    return QuanSim(tuning, sc, Streams(1), IdAllocator())


def step(s, pressed=()):
    return s.step(InputState((0.0, 0.0), {}, set(pressed)))


class Burn(unittest.TestCase):
    def test_dung_1200_tick_van_buong_duoc_qua_1200_thi_chay(self):
        s = sim(ready_ticks=LIMIT - 1)
        self.assertEqual(step(s), [])
        self.assertEqual((s.stoves[0]["state"], s.stoves[0]["ready_ticks"]), ("ready", LIMIT))
        ev = step(s)
        self.assertEqual([n for n, _ in ev], ["dish_burnt"])
        self.assertEqual(s.stoves[0]["state"], "idle")
        self.assertIsNone(s.stoves[0]["dish"])

    def test_dung_1200_van_lay_duoc_trong_buoc_do(self):
        s = sim(ready_ticks=LIMIT - 1)
        s.pos = [2.0, 8.0]
        ev = step(s, {"interact"})
        self.assertEqual([n for n, _ in ev], ["dish_picked"])
        self.assertEqual(s.hand["order_id"], "C1")

    def test_chay_du_nguyen_lieu_thi_giu_lai_cho_don(self):
        s = sim(ready_ticks=LIMIT, stock={"ca_loc": 1})
        (name, d), = step(s)
        self.assertEqual((name, d), ("dish_burnt", {"stove_id": "B1", "order_id": "C1", "dish_id": DISH,
                                                    "order_status": "reserved"}))
        c = s.customers[0]
        self.assertEqual((c["order_status"], c["reserved"], c["base_price"]), ("reserved", {"ca_loc": 1}, 0))
        self.assertEqual(s.stock, {"ca_loc": 1}, "nguyên liệu đã nấu mất, kho không đổi")

    def test_chay_thieu_nguyen_lieu_thi_unfulfillable_va_khach_van_cho(self):
        s = sim(ready_ticks=LIMIT, stock={})
        (_, d), = step(s)
        self.assertEqual(d["order_status"], "unfulfillable")
        c = s.customers[0]
        self.assertEqual((c["order_status"], c["reserved"], c["state"]), ("unfulfillable", {}, "waiting"))
        s.pos = [2.0, 8.0]
        self.assertEqual(step(s, {"interact"}), [], "đơn unfulfillable không được nấu")

    def test_ton_kho_bi_khach_khac_giu_thi_unfulfillable(self):
        other = {"id": "C2", "table_id": "T2", "dish_id": DISH}  # reserved, giữ 1 ca_loc
        s = sim(ready_ticks=LIMIT, stock={"ca_loc": 1}, extra_customers=[other])
        (_, d), = step(s)
        self.assertEqual(d["order_status"], "unfulfillable")

    def test_mac_dinh_khong_chay(self):
        s = sim(tuning=CONTRACT["tuning"], ready_ticks=10 ** 6)
        self.assertEqual(step(s), [])
        self.assertEqual(s.stoves[0]["state"], "ready")


class ContractExtensions(unittest.TestCase):
    def write(self, w, mutate):
        c = copy.deepcopy(CONTRACT)
        mutate(c)
        return write_json(w.path("c.json"), c)

    def test_burn_chi_hop_le_khi_khai_extension(self):
        self.assertEqual(KNOWN_EXTENSIONS, {"burn"})
        with Workdir() as w:
            load_contract(self.write(w, lambda c: None))
            ok = self.write(w, lambda c: (c.update(extensions=["burn"]), c["tuning"]["quan"].update(burn_s=20)))
            load_contract(ok)
            for name, mut in {
                "burn_s mà không khai": lambda c: c["tuning"]["quan"].update(burn_s=20),
                "khai mà burn_s null": lambda c: c.update(extensions=["burn"]),
                "extension lạ": lambda c: c.update(extensions=["weapon"]),
                "burn_s ngoài dải": lambda c: (c.update(extensions=["burn"]), c["tuning"]["quan"].update(burn_s=0)),
            }.items():
                with self.assertRaises(BadInput, msg=name):
                    load_contract(self.write(w, mut))


if __name__ == "__main__":
    unittest.main()
