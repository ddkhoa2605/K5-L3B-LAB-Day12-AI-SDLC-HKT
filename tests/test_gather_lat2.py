"""Test lát 2 (gather): hái, bắt cá, giỏ đầy (hold_full), cập bến xét trước hái, hết giờ.
Số liệu đọc từ game.contract.json.
"""

import json
import math
import unittest

from chonoi.contract import load_contract
from chonoi.inputs import InputState
from chonoi.runner import Session

TUNING = load_contract()["tuning"]
G = TUNING["gather"]
SURFACE = G["surface_depth"]
TICK = float(TUNING["tick_hz"])
INTERACT_R = G["interact_radius"]
CATCH_R = G["catch_radius"]
REGROW_TICKS = int(round(G["regrow_s"] * TICK))
CATCH_CD_TICKS = int(round(G["catch_cooldown_s"] * TICK))
CAPACITY = G["hold_capacity"]


def idle():
    return InputState((0.0, 0.0), {}, set())


def press(button):
    return InputState((0.0, 0.0), {button: True}, {button})


def run(s, n, inp=idle):
    out = []
    for _ in range(n):
        if s.done:
            break
        out += s.step(inp())
    return out


def names(evs):
    return [e["name"] for e in evs]


class GatherInteract(unittest.TestCase):
    def test_gather_ready_node_at_surface(self):
        scenario = {
            "player": {"pos": [12.0, 0.0]},
            "nodes": [{"id": "N1", "kind": "bong_dien_dien", "pos": [12.0, 0.0]}],
            "random_fish": False,
        }
        s = Session("gather", TUNING, scenario, 1)
        evs = s.step(press("interact"))
        gathers = [e for e in evs if e["name"] == "gather"]
        self.assertEqual(len(gathers), 1)
        self.assertEqual(gathers[0]["data"], {"node_id": "N1", "kind": "bong_dien_dien", "amount": 1})
        self.assertEqual(s.sim.hold, ["bong_dien_dien"])
        self.assertEqual(s.sim.nodes[0]["regrow_ticks"], REGROW_TICKS)

    def test_gather_tie_break_by_id(self):
        # 2 nút cách đều 1.0 (ở x=19 và x=21, player ở x=20)
        scenario = {
            "player": {"pos": [20.0, 0.0]},
            "nodes": [
                {"id": "N2", "kind": "bong_sung", "pos": [21.0, 0.0]},
                {"id": "N1", "kind": "bong_dien_dien", "pos": [19.0, 0.0]},
            ],
            "random_fish": False,
        }
        s = Session("gather", TUNING, scenario, 1)
        evs = s.step(press("interact"))
        gathers = [e for e in evs if e["name"] == "gather"]
        self.assertEqual(len(gathers), 1)
        self.assertEqual(gathers[0]["data"]["node_id"], "N1")

    def test_gather_exact_radius_boundary(self):
        # đúng mép bán kính INTERACT_R (2.0) và trong dung sai float EPS (1e-9)
        scenario = {
            "player": {"pos": [10.0, 0.0]},
            "nodes": [{"id": "N1", "kind": "bong_dien_dien", "pos": [10.0 + INTERACT_R + 1e-10, 0.0]}],
            "random_fish": False,
        }
        s = Session("gather", TUNING, scenario, 1)
        evs = s.step(press("interact"))
        self.assertIn("gather", names(evs))

        # vượt mép ngoài dung sai EPS -> không hái được
        scenario_out = {
            "player": {"pos": [10.0, 0.0]},
            "nodes": [{"id": "N1", "kind": "bong_dien_dien", "pos": [10.0 + INTERACT_R + 0.01, 0.0]}],
            "random_fish": False,
        }
        s2 = Session("gather", TUNING, scenario_out, 1)
        evs2 = s2.step(press("interact"))
        self.assertNotIn("gather", names(evs2))

    def test_node_regrown_after_1200_steps(self):
        scenario = {
            "player": {"pos": [12.0, 0.0]},
            "nodes": [{"id": "N1", "kind": "bong_dien_dien", "pos": [12.0, 0.0]}],
            "random_fish": False,
        }
        s = Session("gather", TUNING, scenario, 1)
        s.step(press("interact"))
        self.assertEqual(s.sim.nodes[0]["regrow_ticks"], REGROW_TICKS)

        # chạy 1199 bước idle
        run(s, REGROW_TICKS - 1)
        self.assertEqual(s.sim.nodes[0]["regrow_ticks"], 1)

        # bước thứ 1200: nút mọc lại và hái được ngay trong cùng bước
        evs = s.step(press("interact"))
        self.assertEqual(names(evs), ["node_regrown", "gather"])
        self.assertEqual(evs[0]["data"], {"node_id": "N1"})
        self.assertEqual(evs[1]["data"]["node_id"], "N1")

    def test_no_gather_when_underwater(self):
        # player ở d = 1.0 > surface_depth (0.5), xa bến
        scenario = {
            "player": {"pos": [12.0, 1.0]},
            "nodes": [{"id": "N1", "kind": "bong_dien_dien", "pos": [12.0, 0.0]}],
            "random_fish": False,
        }
        s = Session("gather", TUNING, scenario, 1)
        evs = s.step(press("interact"))
        self.assertNotIn("gather", names(evs))

    def test_hold_full_on_gather_keeps_node(self):
        scenario = {
            "player": {"pos": [12.0, 0.0]},
            "hold": ["ca_loc"] * CAPACITY,
            "nodes": [{"id": "N1", "kind": "bong_dien_dien", "pos": [12.0, 0.0]}],
            "random_fish": False,
        }
        s = Session("gather", TUNING, scenario, 1)
        evs = s.step(press("interact"))
        self.assertNotIn("gather", names(evs))
        fulls = [e for e in evs if e["name"] == "hold_full"]
        self.assertEqual(len(fulls), 1)
        self.assertEqual(fulls[0]["data"], {"action": "gather", "node_id": "N1", "required": 1, "free": 0})
        self.assertEqual(s.sim.nodes[0]["regrow_ticks"], 0)
        self.assertEqual(len(s.sim.hold), CAPACITY)


class CatchFish(unittest.TestCase):
    def test_catch_fish_success_and_cooldown(self):
        scenario = {
            "player": {"pos": [15.0, 5.0]},
            "fish": [{"id": "F1", "kind": "ca_linh", "pos": [15.0, 5.0], "heading_deg": 0}],
            "random_fish": False,
        }
        s = Session("gather", TUNING, scenario, 1)
        evs = s.step(press("catch"))
        catches = [e for e in evs if e["name"] == "fish_caught"]
        self.assertEqual(len(catches), 1)
        self.assertEqual(catches[0]["data"], {"fish_id": "F1", "kind": "ca_linh", "yield": 3})
        self.assertEqual(s.sim.hold, ["ca_linh", "ca_linh", "ca_linh"])
        self.assertEqual(s.sim.fish, [])
        self.assertEqual(s.sim.catch_cd_ticks, CATCH_CD_TICKS)

    def test_catch_cooldown_blocks_second_catch(self):
        scenario = {
            "player": {"pos": [15.0, 5.0]},
            "fish": [
                {"id": "F1", "kind": "ca_loc", "pos": [15.0, 5.0], "heading_deg": 0},
                {"id": "F2", "kind": "ca_loc", "pos": [15.0, 5.5], "heading_deg": 0},
            ],
            "random_fish": False,
        }
        s = Session("gather", TUNING, scenario, 1)
        s.step(press("catch"))
        self.assertEqual(len(s.sim.hold), 1)

        # bước tiếp theo bấm catch ngay -> bị chặn bởi cooldown
        evs = s.step(press("catch"))
        self.assertNotIn("fish_caught", names(evs))
        self.assertEqual(len(s.sim.hold), 1)

    def test_catch_available_after_30_ticks(self):
        scenario = {
            "player": {"pos": [15.0, 5.0]},
            "fish": [
                {"id": "F1", "kind": "ca_loc", "pos": [15.0, 5.0], "heading_deg": 0},
                {"id": "F2", "kind": "ca_loc", "pos": [15.0, 5.5], "heading_deg": 0},
            ],
            "random_fish": False,
        }
        s = Session("gather", TUNING, scenario, 1)
        s.step(press("catch"))
        self.assertEqual(s.sim.catch_cd_ticks, 30)

        # chạy 29 bước idle
        run(s, 29)
        self.assertEqual(s.sim.catch_cd_ticks, 1)

        # bước thứ 30: cd giảm về 0 và bấm catch thành công
        evs = s.step(press("catch"))
        self.assertIn("fish_caught", names(evs))
        self.assertEqual(len(s.sim.hold), 2)

    def test_catch_tie_break_by_id(self):
        # 2 đàn cá cách đều
        scenario = {
            "player": {"pos": [20.0, 6.0]},
            "fish": [
                {"id": "F10", "kind": "ca_loc", "pos": [20.0, 7.0], "heading_deg": 0},
                {"id": "F2", "kind": "ca_loc", "pos": [20.0, 5.0], "heading_deg": 0},
            ],
            "random_fish": False,
        }
        s = Session("gather", TUNING, scenario, 1)
        evs = s.step(press("catch"))
        catches = [e for e in evs if e["name"] == "fish_caught"]
        self.assertEqual(len(catches), 1)
        self.assertEqual(catches[0]["data"]["fish_id"], "F2")

    def test_catch_hold_full_no_partial_no_cooldown(self):
        # hold 10 món, trống 2; ca_linh yield 3 -> thiếu chỗ
        scenario = {
            "player": {"pos": [15.0, 5.0]},
            "hold": ["ca_loc"] * 10,
            "fish": [{"id": "F1", "kind": "ca_linh", "pos": [15.0, 5.0], "heading_deg": 0}],
            "random_fish": False,
        }
        s = Session("gather", TUNING, scenario, 1)
        evs = s.step(press("catch"))
        self.assertNotIn("fish_caught", names(evs))
        fulls = [e for e in evs if e["name"] == "hold_full"]
        self.assertEqual(len(fulls), 1)
        self.assertEqual(fulls[0]["data"], {"action": "catch", "fish_id": "F1", "required": 3, "free": 2})
        self.assertEqual(len(s.sim.hold), 10)
        self.assertEqual(len(s.sim.fish), 1)
        self.assertEqual(s.sim.catch_cd_ticks, 0)

    def test_catch_at_surface_ignored(self):
        # player ở mặt nước (d = 0.2 <= 0.5)
        scenario = {
            "player": {"pos": [15.0, 0.2]},
            "fish": [{"id": "F1", "kind": "ca_loc", "pos": [15.0, 1.0], "heading_deg": 0}],
            "random_fish": False,
        }
        s = Session("gather", TUNING, scenario, 1)
        evs = s.step(press("catch"))
        self.assertNotIn("fish_caught", names(evs))
        self.assertNotIn("hold_full", names(evs))
        self.assertEqual(s.sim.catch_cd_ticks, 0)

    def test_catch_exact_radius_boundary_and_tolerance(self):
        # cá ở đúng mép bán kính CATCH_R (2.0) cộng dung sai float EPS (1e-10 < 1e-9)
        scenario = {
            "player": {"pos": [15.0, 5.0]},
            "fish": [{"id": "F1", "kind": "ca_loc", "pos": [15.0 + CATCH_R + 1e-10, 5.0], "heading_deg": 0}],
            "random_fish": False,
        }
        s = Session("gather", TUNING, scenario, 1)
        evs = s.step(press("catch"))
        self.assertIn("fish_caught", names(evs))

        # vượt mép ngoài dung sai EPS -> không bắt được
        scenario_out = {
            "player": {"pos": [15.0, 5.0]},
            "fish": [{"id": "F1", "kind": "ca_loc", "pos": [15.0 + CATCH_R + 0.01, 5.0], "heading_deg": 0}],
            "random_fish": False,
        }
        s2 = Session("gather", TUNING, scenario_out, 1)
        evs2 = s2.step(press("catch"))
        self.assertNotIn("fish_caught", names(evs2))

    def test_catch_no_fish_in_radius(self):
        scenario = {
            "player": {"pos": [50.0, 10.0]},
            "fish": [{"id": "F1", "kind": "ca_loc", "pos": [15.0, 5.0], "heading_deg": 0}],
            "random_fish": False,
        }
        s = Session("gather", TUNING, scenario, 1)
        evs = s.step(press("catch"))
        self.assertNotIn("fish_caught", names(evs))
        self.assertEqual(s.sim.catch_cd_ticks, 0)


class DockAndTimeout(unittest.TestCase):
    def test_dock_checked_before_gather(self):
        # player ở bến [2.0, 0.0] có nút hái ngay đó
        scenario = {
            "player": {"pos": [2.0, 0.0]},
            "nodes": [{"id": "N1", "kind": "bong_dien_dien", "pos": [2.0, 0.0]}],
            "hold": ["ca_loc"],
            "random_fish": False,
        }
        s = Session("gather", TUNING, scenario, 1)
        evs = s.step(press("interact"))
        self.assertNotIn("gather", names(evs))
        ends = [e for e in evs if e["name"] == "gather_end"]
        self.assertEqual(len(ends), 1)
        self.assertEqual(ends[0]["data"]["reason"], "docked")
        self.assertEqual(ends[0]["data"]["inventory"], {"items": {"ca_loc": 1}})

    def test_interact_at_last_step_docked_wins_over_time(self):
        scenario = {
            "player": {"pos": [2.0, 0.0]},
            "time_left_ticks": 1,
            "hold": ["bong_sung"],
            "random_fish": False,
        }
        s = Session("gather", TUNING, scenario, 1)
        evs = s.step(press("interact"))
        self.assertTrue(s.done)
        self.assertEqual(s.sim.reason, "docked")

    def test_gather_at_last_step_included_in_time_inventory(self):
        scenario = {
            "player": {"pos": [12.0, 0.0]},
            "nodes": [{"id": "N1", "kind": "bong_dien_dien", "pos": [12.0, 0.0]}],
            "time_left_ticks": 1,
            "random_fish": False,
        }
        s = Session("gather", TUNING, scenario, 1)
        evs = s.step(press("interact"))
        self.assertTrue(s.done)
        self.assertEqual(s.sim.reason, "time")
        self.assertEqual(names(evs), ["gather", "gather_end"])
        self.assertEqual(evs[1]["data"]["inventory"], {"items": {"bong_dien_dien": 1}})


if __name__ == "__main__":
    unittest.main()
