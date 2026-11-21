"""Test lát 1 (gather): dive/surface, oxy, ngạt/choke, ngất. Số liệu đọc từ game.contract.json."""

import unittest

from chonoi.contract import load_contract
from chonoi.inputs import InputState
from chonoi.runner import Session

TUNING = load_contract()["tuning"]
G = TUNING["gather"]
SURFACE = G["surface_depth"]
REFILL = G["oxygen_refill_per_tick"]
CHOKE = G["choke_interval_ticks"]
OXY_MAX = int(round(G["oxygen_max_s"] * TUNING["tick_hz"]))
DEEP = [20.0, 10.0]  # dưới nước, xa bến


def sess(**player):
    p = {"pos": DEEP, **player}
    return Session("gather", TUNING, {"player": p, "random_fish": False, "nodes": []}, 1)


def idle():
    return InputState((0.0, 0.0), {}, set())


def move(x, d):
    return InputState((float(x), float(d)), {}, set())


def run(s, n, inp=idle):
    out = []
    for _ in range(n):
        if s.done:
            break
        out += s.step(inp())
    return out


def names(evs):
    return [e["name"] for e in evs]


class DiveSurface(unittest.TestCase):
    def test_dive_when_crossing_below_surface(self):
        s = sess(pos=[20.0, 0.0])
        evs = run(s, 60, lambda: move(0, 1))
        dives = [e for e in evs if e["name"] == "dive"]
        self.assertEqual(len(dives), 1)
        self.assertGreater(dives[0]["data"]["pos"][1], SURFACE)

    def test_surface_when_coming_up(self):
        s = sess(pos=[20.0, 3.0])
        evs = run(s, 120, lambda: move(0, -1))
        self.assertEqual(names(evs).count("surface"), 1)
        self.assertLessEqual(s.sim.pos[1], SURFACE)

    def test_no_event_while_staying_underwater(self):
        evs = run(sess(), 30)
        self.assertNotIn("dive", names(evs))
        self.assertNotIn("surface", names(evs))


class Oxygen(unittest.TestCase):
    def test_underwater_drains_one_per_tick(self):
        s = sess()
        run(s, 10)
        self.assertEqual(s.sim.oxygen_ticks, OXY_MAX - 10)

    def test_surface_refills_and_clamps(self):
        s = sess(pos=[20.0, 0.0], oxygen_ticks=OXY_MAX - 2)
        run(s, 1)
        self.assertEqual(s.sim.oxygen_ticks, OXY_MAX)
        s = sess(pos=[20.0, 0.0], oxygen_ticks=10)
        run(s, 1)
        self.assertEqual(s.sim.oxygen_ticks, 10 + REFILL)

    def test_oxygen_empty_once_when_reaching_zero(self):
        s = sess(oxygen_ticks=3)
        evs = run(s, 10)
        empties = [e for e in evs if e["name"] == "oxygen_empty"]
        self.assertEqual(len(empties), 1)
        self.assertEqual(empties[0]["tick"], 3)
        self.assertEqual(empties[0]["data"], {"oxygen_ticks": 0})

    def test_no_oxygen_empty_when_starting_at_zero(self):
        evs = run(sess(oxygen_ticks=0), 5)
        self.assertNotIn("oxygen_empty", names(evs))


class Choke(unittest.TestCase):
    def test_first_choke_at_t_plus_59_when_touching_zero(self):
        # oxy 1 -> chạm 0 ở bước 1 (t = 1) -> choke đầu ở tick t + 59 = 60
        s = sess(oxygen_ticks=1)
        evs = run(s, 100)
        chokes = [e for e in evs if e["name"] == "choke"]
        self.assertEqual(chokes[0]["tick"], 1 + CHOKE - 1)
        self.assertEqual(chokes[0]["data"], {"hp": G["hp_max"] - 1})

    def test_choke_every_interval_when_already_zero(self):
        s = sess(oxygen_ticks=0)
        evs = run(s, 2 * CHOKE)
        self.assertEqual([e["tick"] for e in evs if e["name"] == "choke"], [CHOKE, 2 * CHOKE])

    def test_surfacing_on_the_choking_step_prevents_choke(self):
        # đếm ngạt 59, đang ở d sát mặt nước: bước kế nổi lên -> hồi oxy, không ngạt
        s = sess(pos=[20.0, SURFACE + 0.01], oxygen_ticks=0, zero_oxy_ticks=CHOKE - 1)
        evs = run(s, 1, lambda: move(0, -1))
        self.assertNotIn("choke", names(evs))
        self.assertEqual(s.sim.hp, G["hp_max"])
        self.assertEqual(s.sim.zero_oxy_ticks, 0)
        self.assertEqual(s.sim.oxygen_ticks, REFILL)

    def test_surface_resets_choke_counter(self):
        s = sess(pos=[20.0, 0.0], oxygen_ticks=0, zero_oxy_ticks=30)
        run(s, 1)
        self.assertEqual(s.sim.zero_oxy_ticks, 0)


class Faint(unittest.TestCase):
    def test_faint_drops_hold_lifo_and_ends_with_empty_inventory(self):
        s = Session("gather", TUNING, {"player": {"pos": DEEP, "oxygen_ticks": 0, "hp": 1},
                                        "hold": ["ca_loc", "bong_sung", "ca_linh"],
                                        "random_fish": False}, 1)
        evs = run(s, CHOKE)
        self.assertTrue(s.done)
        self.assertEqual(s.sim.reason, "fainted")
        self.assertEqual(names(evs)[-3:], ["choke", "faint", "gather_end"])
        faint = [e for e in evs if e["name"] == "faint"][0]["data"]
        self.assertEqual(faint, {"cause": "choke", "lost": ["ca_linh", "bong_sung", "ca_loc"], "hp": 0})
        end = evs[-1]["data"]
        self.assertEqual(end, {"reason": "fainted", "inventory": {"items": {}}})
        self.assertEqual(s.sim.hold, [])
        self.assertEqual(s.sim.inventory_items(), {})

    def test_three_chokes_needed_from_full_hp(self):
        s = sess(oxygen_ticks=0)
        run(s, G["hp_max"] * CHOKE)
        self.assertTrue(s.done)
        self.assertEqual(s.sim.reason, "fainted")
        self.assertEqual(s.sim.hp, 0)


if __name__ == "__main__":
    unittest.main()
