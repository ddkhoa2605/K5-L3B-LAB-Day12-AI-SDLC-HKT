"""Chế độ `day`, Shop, nâng cấp, pause (TICKET-02 mục 2, 4). Hộp đen qua headless_cmd.

Quy ước tick: gather bắt đầu ở tick 0; cập bến ở bước đọc frame tick 0 -> quan bắt đầu tick 1
(`phase_start(quan)` cùng tick 1); quan chạy 10.800 bước -> `quan_end` + `phase_start(shop)` ở tick 10.801.
"""

import json
import os
import unittest

from helpers import Workdir, counts, events, frames, make_items, read_jsonl, run_headless, snapshots, write_json

with open("game.contract.json", encoding="utf-8") as _f:
    TUNING = json.load(_f)["tuning"]
SHOP_TICK = 1 + int(round(TUNING["quan"]["duration_s"] * 60))  # tick bắt đầu Shop khi cập bến ở tick 1
HOLD = make_items({"ca_loc": 1, "bong_sung": 2})


def day(w, scenario=None, inputs=None, ticks=20000, days=None, seed=1, every=10, extra=()):
    args = ["--mode", "day", "--seed", str(seed), "--ticks", str(ticks), "--snapshot-every", str(every),
            "--out", w.path("o.jsonl"), *extra]
    if days is not None:
        args += ["--days", str(days)]
    if scenario is not None:
        args += ["--scenario", write_json(w.path("sc.json"), scenario)]
    if inputs is not None:
        args += ["--inputs", write_json(w.path("in.json"), frames(*inputs))]
    code, err = run_headless(*args)
    return code, (read_jsonl(w.path("o.jsonl")) if code == 0 else err)


def dock(hold=HOLD, **quan):
    quan.setdefault("random_customers", False)
    return {"gather": {"hold": hold, "random_fish": False}, "quan": quan}


DOCK_INPUT = [{"tick": 0, "interact": True}, {"tick": 1, "interact": False}]


class Flow(unittest.TestCase):
    def test_mot_ngay_thu_tu_pha_va_tick(self):
        with Workdir() as w:
            code, rows = day(w, dock(), DOCK_INPUT)
            self.assertEqual(code, 0, rows)
            ev = [(r["tick"], r["phase"], r["name"]) for r in events(rows)]
            self.assertEqual(ev, [
                (0, "gather", "day_start"), (0, "gather", "day_plan"), (0, "gather", "phase_start"),
                (1, "gather", "gather_end"), (1, "quan", "phase_start"),
                (SHOP_TICK, "quan", "quan_end"), (SHOP_TICK, "shop", "phase_start"),
                (SHOP_TICK + TUNING["shop"]["max_ticks"], "shop", "shop_end")])
            self.assertTrue(all(r["day"] == 1 for r in events(rows)))
            plan = events(rows, "day_plan")[0]["data"]
            self.assertEqual(plan, {"dishes": {"ca_loc_nuong_trui": 3, "goi_bong_sung": 3},
                                    "ingredients": {"bong_sung": 6, "ca_loc": 3}})
            end = rows[-1]
            self.assertEqual((end["reason"], end["days_completed"], end["state"]), ("days_complete", 1, "finished"))
            self.assertEqual(end["mode"], "day")

    def test_snapshot_moi_pha_co_truong_ngay(self):
        with Workdir() as w:
            code, rows = day(w, dock(), DOCK_INPUT, every=1000)
            self.assertEqual(code, 0, rows)
            seen = {}
            for s in snapshots(rows):
                self.assertIn("day_plan", s)
                self.assertEqual((s["day"], s["upgrades"], s["active_upgrades"]), (1, {"oxygen": 0, "hp": 0}, {"oxygen": 0, "hp": 0}))
                seen.setdefault(s["phase"], s)
            self.assertEqual(set(seen), {"gather", "quan", "shop"})
            self.assertIn("hold", seen["gather"])
            self.assertIn("customers", seen["quan"])
            self.assertEqual(counts(seen["shop"]["stock"]), {"bong_sung": 2, "ca_loc": 1})
            self.assertEqual(seen["shop"]["time_left_ticks"] + seen["shop"]["phase_tick"], TUNING["shop"]["max_ticks"])

    def test_kho_ban_giao_vao_quan_va_khach_chi_chon_mon_trong_ke_hoach(self):
        """Kho có đủ nguyên liệu cho cả 6 món, nhưng Ngày 1 chỉ có 2 món: khách không được chọn món ngoài kế hoạch."""
        rich = make_items({"ca_loc": 1, "ca_linh": 3, "bong_dien_dien": 1, "bong_sung": 2, "ca_keo": 2})
        with Workdir() as w:
            for seed in range(5):
                code, rows = day(w, dock(hold=rich, random_customers=True), DOCK_INPUT, ticks=130, seed=seed, every=130)
                self.assertEqual(code, 0, rows)
                arr = events(rows, "customer_arrived")
                self.assertEqual([e["tick"] for e in arr], [121])
                self.assertIn(arr[0]["data"]["dish_id"], TUNING["day_plan"][0]["dishes"], seed)

    def test_ke_hoach_ghi_de_theo_ngay_tinh_lai_nguyen_lieu(self):
        sc = dock()
        sc["day"] = {"day_plan": [{"day": 1, "dishes": {"goi_bong_sung": 1}}]}
        with Workdir() as w:
            code, rows = day(w, sc, DOCK_INPUT, ticks=5)
            self.assertEqual(code, 0, rows)
            self.assertEqual(events(rows, "day_plan")[0]["data"],
                             {"dishes": {"goi_bong_sung": 1}, "ingredients": {"bong_sung": 2}})

    def test_ngay_chi_hoan_tat_khi_shop_dong_va_tick_limit(self):
        with Workdir() as w:
            code, rows = day(w, dock(), DOCK_INPUT, ticks=SHOP_TICK + 10)
            self.assertEqual(code, 0, rows)
            self.assertEqual((rows[-1]["reason"], rows[-1]["days_completed"], rows[-1]["state"]),
                             ("tick_limit", 0, "playing"))

    def test_tat_dinh_cmp_hai_ngay(self):
        inputs = DOCK_INPUT + [{"tick": SHOP_TICK + 2, "buy": "oxygen", "shop_done": True}]
        sc = dock()
        sc["day"] = {"money": 300, "earned": 300}
        with Workdir() as w:
            for i in (1, 2):
                code, err = run_headless("--mode", "day", "--seed", "9", "--days", "2", "--ticks", "13000",
                                         "--scenario", write_json(w.path("sc.json"), sc),
                                         "--inputs", write_json(w.path("in.json"), frames(*inputs)),
                                         "--out", w.path(f"o{i}.jsonl"))
                self.assertEqual(code, 0, err)
            with open(w.path("o1.jsonl"), "rb") as a, open(w.path("o2.jsonl"), "rb") as b:
                self.assertEqual(a.read(), b.read())


class ShopTests(unittest.TestCase):
    def shop_run(self, w, buys, money=0, days=2, ticks=None, extra_frames=()):
        sc = dock()
        sc["day"] = {"money": money, "earned": money}
        inputs = list(DOCK_INPUT) + [dict(f, tick=SHOP_TICK + 1 + i) for i, f in enumerate(buys)] + list(extra_frames)
        return day(w, sc, inputs, days=days, ticks=ticks or SHOP_TICK + 20, every=1000)

    def test_mua_oxy_tru_money_giu_earned_hieu_luc_tu_ngay_ke(self):
        with Workdir() as w:
            code, rows = self.shop_run(w, [{"buy": "oxygen", "shop_done": True}], money=300)
            self.assertEqual(code, 0, rows)
            b = events(rows, "bought")[0]
            self.assertEqual((b["tick"], b["data"]), (SHOP_TICK + 2, {"upgrade": "oxygen", "level": 1, "price": 200, "money": 100}))
            self.assertEqual(events(rows, "shop_end")[0]["data"]["reason"], "done")
            self.assertEqual(events(rows, "shop_end")[0]["tick"], SHOP_TICK + 2, "mua trước rồi mới đóng, cùng bước")
            snap = snapshots(rows)[-1]
            self.assertEqual((snap["day"], snap["phase"], snap["phase_tick"]), (2, "gather", snap["tick"] - (SHOP_TICK + 2)))
            self.assertEqual((snap["money"], snap["earned"]), (100, 300))
            self.assertEqual((snap["upgrades"]["oxygen"], snap["active_upgrades"]["oxygen"]), (1, 1))
            self.assertEqual(snap["player"]["oxygen_max_ticks"], 45 * 60)
            self.assertEqual(events(rows, "day_start")[-1]["tick"], SHOP_TICK + 2)

    def test_cap_vua_mua_hien_ngay_nhung_chua_hieu_luc_trong_shop(self):
        with Workdir() as w:
            sc = dock()
            sc["day"] = {"money": 500, "earned": 500}
            inputs = DOCK_INPUT + [{"tick": SHOP_TICK + 1, "buy": "hp"}]
            code, rows = day(w, sc, inputs, ticks=SHOP_TICK + 5, every=1)
            self.assertEqual(code, 0, rows)
            s = snapshots(rows)[-1]
            self.assertEqual((s["phase"], s["upgrades"]["hp"], s["active_upgrades"]["hp"]), ("shop", 1, 0))

    def test_hp_cap_ke_tiep_ap_dung_ngay_sau(self):
        with Workdir() as w:
            code, rows = self.shop_run(w, [{"buy": "hp"}, {"buy": "hp", "shop_done": True}], money=1000)
            self.assertEqual(code, 0, rows)
            self.assertEqual([e["data"]["level"] for e in events(rows, "bought")], [1, 2])
            self.assertEqual(snapshots(rows)[-1]["player"]["hp_max"], 5)
            self.assertEqual(snapshots(rows)[-1]["player"]["hp"], 5, "Máu hồi đầy theo cấp có hiệu lực")

    def test_buy_failed_funds_max_level_unknown(self):
        with Workdir() as w:
            code, rows = self.shop_run(w, [{"buy": "oxygen"}, {"buy": "weapon"}, {"buy": "oxygen"}, {"buy": "oxygen"},
                                           {"buy": "oxygen"}], money=600, ticks=SHOP_TICK + 10)
            self.assertEqual(code, 0, rows)
            seq = [(e["name"], e["data"].get("reason", e["data"].get("level"))) for e in events(rows)
                   if e["name"] in ("bought", "buy_failed")]
            self.assertEqual(seq, [("bought", 1), ("buy_failed", "unknown"), ("bought", 2), ("buy_failed", "max_level"),
                                   ("buy_failed", "max_level")])
            self.assertEqual(snapshots(rows)[-1]["money"], 0)

    def test_khong_du_tien_giu_nguyen_tien_va_cap(self):
        with Workdir() as w:
            code, rows = self.shop_run(w, [{"buy": "oxygen"}], money=199, ticks=SHOP_TICK + 5)
            self.assertEqual(code, 0, rows)
            self.assertEqual(events(rows, "buy_failed")[0]["data"], {"action": "oxygen", "reason": "funds"})
            s = snapshots(rows)[-1]
            self.assertEqual((s["money"], s["upgrades"]["oxygen"]), (199, 0))

    def test_du_dung_gia_van_mua_duoc(self):
        with Workdir() as w:
            code, rows = self.shop_run(w, [{"buy": "oxygen"}], money=200, ticks=SHOP_TICK + 5)
            self.assertEqual(code, 0, rows)
            self.assertEqual(events(rows, "bought")[0]["data"]["money"], 0)

    def test_buy_chi_chay_dung_frame_khai_bao(self):
        with Workdir() as w:
            code, rows = self.shop_run(w, [{"buy": "oxygen"}], money=1000, ticks=SHOP_TICK + 50)
            self.assertEqual(code, 0, rows)
            self.assertEqual(len(events(rows, "bought")), 1, "không lặp lại ở các bước sau")

    def test_shop_tu_dong_dong_sau_600_tick_hoat_dong(self):
        with Workdir() as w:
            code, rows = self.shop_run(w, [], days=1, ticks=SHOP_TICK + 700)
            self.assertEqual(code, 0, rows)
            se = events(rows, "shop_end")[0]
            self.assertEqual((se["tick"], se["data"]["reason"]), (SHOP_TICK + 600, "time"))

    def test_shop_done_va_buy_ngay_buoc_cuoi_van_mua_truoc(self):
        with Workdir() as w:
            code, rows = self.shop_run(w, [], days=1, money=300,
                                       extra_frames=[{"tick": SHOP_TICK + 599, "buy": "oxygen", "shop_done": True}],
                                       ticks=SHOP_TICK + 700)
            self.assertEqual(code, 0, rows)
            self.assertEqual([e["name"] for e in events(rows) if e["tick"] == SHOP_TICK + 600][-2:], ["bought", "shop_end"])
            self.assertEqual(events(rows, "shop_end")[0]["data"]["reason"], "done")

    def test_nhieu_ngay_tien_uy_tin_xuyen_ngay_va_kho_du_bi_bo(self):
        with Workdir() as w:
            sc = dock()
            sc["day"] = {"money": 50, "earned": 80, "reputation": 4.0}
            inputs = DOCK_INPUT + [{"tick": SHOP_TICK + 1, "shop_done": True}]
            code, rows = day(w, sc, inputs, days=2, ticks=SHOP_TICK + 3, every=1000)
            self.assertEqual(code, 0, rows)
            s = snapshots(rows)[-1]
            self.assertEqual((s["day"], s["phase"], s["money"], s["earned"], s["reputation"]), (2, "gather", 50, 80, 4.0))
            self.assertEqual(counts(s["hold"]), counts(HOLD), "giỏ làm mới từ template gather của Ngày mới")
            self.assertFalse({i["id"] for i in s["hold"]} & {i["id"] for i in HOLD}, "Ngày kế cấp id mới, không tái dùng")
            self.assertEqual(s["score"], 80 + 100 * 4)
            self.assertEqual(events(rows, "day_plan")[-1]["data"]["dishes"], TUNING["day_plan"][1]["dishes"])


class Pause(unittest.TestCase):
    def test_pause_trong_day_dung_dong_ho_gameplay(self):
        with Workdir() as w:
            code, rows = day(w, dock(), [{"tick": 0, "interact": True}, {"tick": 1, "interact": False},
                                         {"tick": 5, "pause": True}, {"tick": 6, "pause": False},
                                         {"tick": 10, "pause": True}, {"tick": 11, "pause": False}],
                             ticks=12, every=1)
            self.assertEqual(code, 0, rows)
            names = [(e["tick"], e["name"]) for e in events(rows) if e["name"] in ("paused", "resumed")]
            self.assertEqual(names, [(6, "paused"), (11, "resumed")])
            snaps = {s["tick"]: s for s in snapshots(rows)}
            self.assertEqual(snaps[6]["state"], "paused")
            self.assertEqual(snaps[10]["state"], "paused")
            self.assertEqual(snaps[10]["sim_tick"], snaps[6]["sim_tick"], "sim_tick đứng yên khi pause")
            self.assertEqual(snaps[10]["phase_tick"], snaps[6]["phase_tick"])
            self.assertEqual(snaps[10]["time_left_ticks"], snaps[6]["time_left_ticks"])
            self.assertEqual(snaps[11]["state"], "playing", "cạnh lên kế tiếp chạy gameplay ngay trong bước đó")
            self.assertEqual(snaps[11]["sim_tick"], snaps[6]["sim_tick"] + 1)
            self.assertEqual(snaps[11]["tick"], 11)

    def test_pause_bo_qua_canh_hanh_dong(self):
        """Cập bến bị bỏ qua khi đang pause; sau khi resume, cạnh lên kế tiếp mới có tác dụng."""
        with Workdir() as w:
            code, rows = day(w, dock(), [{"tick": 0, "pause": True}, {"tick": 1, "pause": False, "interact": True}],
                             ticks=4, every=1)
            self.assertEqual(code, 0, rows)
            self.assertEqual(events(rows, "gather_end"), [])
            self.assertEqual([e["name"] for e in events(rows)][-1], "paused")

    def test_pause_trong_shop_dung_dem_gio_shop(self):
        with Workdir() as w:
            inputs = DOCK_INPUT + [{"tick": SHOP_TICK + 3, "pause": True}, {"tick": SHOP_TICK + 4, "pause": False}]
            code, rows = day(w, dock(), inputs, ticks=SHOP_TICK + 20, every=1)
            self.assertEqual(code, 0, rows)
            snaps = {s["tick"]: s for s in snapshots(rows)}
            self.assertEqual(snaps[SHOP_TICK + 10]["state"], "paused")
            self.assertEqual(snaps[SHOP_TICK + 10]["time_left_ticks"], snaps[SHOP_TICK + 4]["time_left_ticks"])

    def test_pause_o_gather_va_quan_doc_lap(self):
        with Workdir() as w:
            for mode in ("gather", "quan"):
                inp = write_json(w.path("in.json"), frames({"tick": 2, "pause": True}, {"tick": 3, "pause": False},
                                                           {"tick": 5, "pause": True}, {"tick": 6, "pause": False}))
                code, err = run_headless("--mode", mode, "--seed", "1", "--ticks", "8", "--inputs", inp,
                                         "--snapshot-every", "1", "--out", w.path("o.jsonl"))
                self.assertEqual(code, 0, err)
                rows = read_jsonl(w.path("o.jsonl"))
                self.assertEqual([(e["tick"], e["name"], e["phase"]) for e in events(rows)],
                                 [(3, "paused", mode), (6, "resumed", mode)])
                s = {x["tick"]: x for x in snapshots(rows)}
                self.assertEqual((s[3]["state"], s[5]["state"]), ("paused", "paused"))
                self.assertEqual(s[5]["sim_tick"], s[3]["sim_tick"])
                self.assertEqual(rows[-1]["sim_tick"], 5, "8 bước ngoài trừ 3 bước pause")
                self.assertEqual(rows[-1]["ticks"], 8)


class Errors(unittest.TestCase):
    def test_tham_so_sai_exit_2_khong_ghi_file(self):
        bad = {
            "days = 6": (dict(days=6), None),
            "days = 0": (dict(days=0), None),
            "money > earned": (dict(), {"day": {"money": 10, "earned": 5}}),
            "chỉ khai money": (dict(), {"day": {"money": 10}}),
            "quan.stock bị cấm": (dict(), {"quan": {"stock": make_items({"ca_loc": 1})}}),
            "quan.reputation bị cấm": (dict(), {"quan": {"reputation": 2.0}}),
            "upgrades lạ": (dict(), {"day": {"upgrades": {"weapon": 1}}}),
            "upgrades quá cấp": (dict(), {"day": {"upgrades": {"oxygen": 3}}}),
            "ingredients lệch": (dict(), {"day": {"day_plan": [{"day": 1, "dishes": {"goi_bong_sung": 1},
                                                                "ingredients": {"bong_sung": 1}}]}}),
            "món lạ trong kế hoạch": (dict(), {"day": {"day_plan": [{"day": 1, "dishes": {"pho": 1}}]}}),
            "khối lạ": (dict(), {"river": {}}),
            "gather sai miền": (dict(), {"gather": {"player": {"pos": [101, 0]}}}),
            "uy tín ngoài miền": (dict(), {"day": {"reputation": 9}}),
        }
        with Workdir() as w:
            for name, (kw, sc) in bad.items():
                code, err = day(w, sc, ticks=5, **kw)
                self.assertEqual(code, 2, name)
                self.assertFalse(os.path.exists(w.path("o.jsonl")), name)

    def test_co_file_kho_hoac_days_sai_mode(self):
        with Workdir() as w:
            inv = write_json(w.path("inv.json"), {"items": make_items({})})
            out = w.path("o.jsonl")
            self.assertEqual(run_headless("--mode", "day", "--seed", "1", "--ticks", "0", "--inventory", inv, "--out", out)[0], 2)
            self.assertEqual(run_headless("--mode", "day", "--seed", "1", "--ticks", "0",
                                          "--inventory-out", w.path("x.json"), "--out", out)[0], 2)
            for mode in ("gather", "quan"):
                self.assertEqual(run_headless("--mode", mode, "--seed", "1", "--ticks", "0", "--days", "2", "--out", out)[0], 2)
            self.assertFalse(os.path.exists(out))

    def test_khach_fixture_ngoai_ke_hoach_la_mau_thuan_luc_mo_quan_khong_de_file_do(self):
        quan = {"random_customers": False, "customers": [{"id": "C1", "table_id": "T1", "dish_id": "lau_mam"}]}
        with Workdir() as w:
            code, err = day(w, dock(hold=make_items({"ca_linh": 2, "ca_keo": 1, "keo_neo": 1, "bong_dien_dien": 1}), **quan),
                            DOCK_INPUT, ticks=5)
            self.assertEqual(code, 2, err)
            self.assertFalse(os.path.exists(w.path("o.jsonl")))

    def test_gather_hold_ngoai_kho_quan_khong_du_cho_giu_la_mau_thuan(self):
        quan = {"random_customers": False,
                "customers": [{"id": "C1", "table_id": "T1", "dish_id": "ca_loc_nuong_trui"}]}
        with Workdir() as w:
            code, err = day(w, dock(hold=make_items({"bong_sung": 1}), **quan), DOCK_INPUT, ticks=5)
            self.assertEqual(code, 2, err)

    def test_day_ticks_0_va_mac_dinh_1_ngay(self):
        with Workdir() as w:
            code, rows = day(w, None, None, ticks=0)
            self.assertEqual(code, 0, rows)
            self.assertEqual([r["type"] for r in rows], ["snapshot", "event", "event", "event", "end"])
            self.assertEqual(rows[-1]["reason"], "tick_limit")
            s = rows[0]
            self.assertEqual((s["mode"], s["phase"], s["phase_tick"], s["day"]), ("day", "gather", 0, 1))
            self.assertEqual(s["upgrades"], {"oxygen": 0, "hp": 0})


class Performance(unittest.TestCase):
    def test_mot_ngay_khong_pause_chay_duoi_20_giay(self):
        import time
        with Workdir() as w:
            t = time.perf_counter()
            code, rows = day(w, dock(), DOCK_INPUT, ticks=22200)
            self.assertEqual(code, 0, rows)
            self.assertLess(time.perf_counter() - t, 20.0)
            self.assertLessEqual(rows[-1]["ticks"], 22200)


if __name__ == "__main__":
    unittest.main()
