"""Unit test và Integration test cho Phase 2 (AC-P2-05 và AC-P2-06).

Kiểm chứng số liệu chuẩn v1.1:
- AC-P2-05: Đàn cá bơi 1.5 m/s, dải độ sâu theo loài, phản xạ mép x ∈ [4,96] và d theo loài,
            đổi hướng mỗi 120 tick theo seed (fish_swim). Sinh cá tại phase_tick = 360*k,
            trần 12 đàn, clearance > 1.0 m, trọng số 40:30:30, seed fish_spawn.
- AC-P2-06: Cá Sấu Năm Chèo patrol 1.0 m/s, chase 3.0 m/s khi player d >= 10 & dist <= 10,
            thoát khi dist > 16 hoặc player d < 10. Chạm <= 1.5m mất 1 Máu, bỏ floor(n/2) LIFO,
            bất tử 90 tick, quái recoil 60 bước lùi xa player 2/60 m/bước. Ngất monster khi hp=0.
"""

import json
import math
import unittest

from helpers import Workdir, events, frames, read_jsonl, run_headless, snapshots, write_json

with open("game.contract.json", encoding="utf-8") as _f:
    TUNING = json.load(_f)["tuning"]
G = TUNING["gather"]
TICK = 60.0


def gather(w, block, inputs=None, ticks=10, seed=1, every=1):
    sc = write_json(w.path("sc.json"), {"gather": block})
    args = ["--mode", "gather", "--seed", str(seed), "--ticks", str(ticks), "--scenario", sc,
            "--snapshot-every", str(every), "--out", w.path("o.jsonl")]
    if inputs is not None:
        args += ["--inputs", write_json(w.path("in.json"), frames(*inputs))]
    code, err = run_headless(*args)
    return code, (read_jsonl(w.path("o.jsonl")) if code == 0 else err)


class FishSwimming(unittest.TestCase):
    def test_ca_boi_toc_do_1_5_m_s(self):
        """Cá bơi với vận tốc 1.5 m/s: 60 tick đi đúng 1.5 m."""
        with Workdir() as w:
            fish = [{"id": "F1", "kind": "ca_linh", "pos": [20.0, 10.0], "heading_deg": 0.0, "age_ticks": 0}]
            code, rows = gather(w, {"fish": fish, "random_fish": False, "monsters": []}, ticks=60)
            self.assertEqual(code, 0, rows)
            snaps = snapshots(rows)
            f_end = snaps[-1]["fish"][0]
            # Bơi sang phải (+x) 60 tick = 1.5 m -> pos[0] ≈ 21.5
            self.assertAlmostEqual(f_end["pos"][0], 21.5, places=3)
            self.assertAlmostEqual(f_end["pos"][1], 10.0, places=3)

    def test_ca_phan_xa_mep_x(self):
        """Tới mép x=96 phản xạ phần quãng đường còn lại và đảo hướng vx."""
        with Workdir() as w:
            # 1 tick đi 0.025 m. Bắt đầu từ 95.99: chạm mép sau 0.01 m, lùi lại 0.015 m -> 95.985
            fish = [{"id": "F1", "kind": "ca_linh", "pos": [95.99, 10.0], "heading_deg": 0.0, "age_ticks": 0}]
            code, rows = gather(w, {"fish": fish, "random_fish": False, "monsters": []}, ticks=1)
            self.assertEqual(code, 0, rows)
            f_end = snapshots(rows)[-1]["fish"][0]
            self.assertAlmostEqual(f_end["pos"][0], 95.985, places=4)
            self.assertAlmostEqual(f_end["heading_deg"], 180.0, places=3)

    def test_ca_phan_xa_mep_d_theo_loai(self):
        """Phản xạ theo dải độ sâu riêng của từng loài (ví dụ ca_keo ở d ∈ [22, 28])."""
        with Workdir() as w:
            # cá kèo hướng xuống đáy d_max = 28
            fish = [{"id": "F1", "kind": "ca_keo", "pos": [50.0, 27.99], "heading_deg": 90.0, "age_ticks": 0}]
            code, rows = gather(w, {"fish": fish, "random_fish": False, "monsters": []}, ticks=1)
            self.assertEqual(code, 0, rows)
            f_end = snapshots(rows)[-1]["fish"][0]
            self.assertAlmostEqual(f_end["pos"][1], 27.985, places=4)
            self.assertAlmostEqual(f_end["heading_deg"], 270.0, places=3)

    def test_ca_phan_xa_goc_dao_ca_hai(self):
        """Chạm góc đảo cả hai thành phần hướng."""
        with Workdir() as w:
            # Cá linh d_max=12, x_max=96. Đặt tại [95.99, 11.99], hướng 45 độ (vx>0, vd>0 bằng nhau)
            fish = [{"id": "F1", "kind": "ca_linh", "pos": [95.99, 11.99], "heading_deg": 45.0, "age_ticks": 0}]
            code, rows = gather(w, {"fish": fish, "random_fish": False, "monsters": []}, ticks=1)
            self.assertEqual(code, 0, rows)
            f_end = snapshots(rows)[-1]["fish"][0]
            # Sau khi phản xạ góc, hướng đảo thành 225 độ
            self.assertAlmostEqual(f_end["heading_deg"], 225.0, places=3)
            self.assertLess(f_end["pos"][0], 96.0)
            self.assertLess(f_end["pos"][1], 12.0)

    def test_ca_doi_huong_theo_seed_tai_tick_120(self):
        """Đổi hướng theo seed ở bước bơi thứ 120."""
        with Workdir() as w:
            fish = [{"id": "F1", "kind": "ca_linh", "pos": [50.0, 10.0], "heading_deg": 0.0, "age_ticks": 119}]
            code, rows = gather(w, {"fish": fish, "random_fish": False, "monsters": []}, ticks=1, seed=42)
            self.assertEqual(code, 0, rows)
            f_end = snapshots(rows)[-1]["fish"][0]
            # Đã đổi hướng khỏi 0.0
            self.assertNotEqual(f_end["heading_deg"], 0.0)


class FishSpawning(unittest.TestCase):
    def test_sinh_ca_tai_tick_360(self):
        """Tại phase_tick = 360, sinh 1 đàn cá mới thỏa mãn cách đàn sống > 1 m."""
        with Workdir() as w:
            fish = [{"id": "F1", "kind": "ca_linh", "pos": [50.0, 10.0], "heading_deg": 0.0, "age_ticks": 0}]
            code, rows = gather(w, {"fish": fish, "random_fish": False, "monsters": []}, ticks=360, seed=1)
            self.assertEqual(code, 0, rows)
            ev = events(rows, "fish_spawned")
            self.assertEqual(len(ev), 1)
            spawn_data = ev[0]["data"]
            self.assertIn(spawn_data["kind"], ("ca_linh", "ca_loc", "ca_keo"))
            self.assertEqual(spawn_data["fish_id"], "F2")
            snaps = snapshots(rows)
            # Đầu ca có 1 con, sau 360 tick có 2 con
            self.assertEqual(len(snaps[-1]["fish"]), 2)

    def test_sinh_ca_khong_vuot_tran_12(self):
        """Đã đạt trần 12 đàn thì bỏ lượt sinh tại tick 360."""
        with Workdir() as w:
            # Tạo 12 đàn
            fish = [{"id": f"F{i}", "kind": "ca_linh", "pos": [15.0 + i * 2, 10.0], "heading_deg": 0.0} for i in range(12)]
            code, rows = gather(w, {"fish": fish, "random_fish": False, "monsters": []}, ticks=360)
            self.assertEqual(code, 0, rows)
            self.assertEqual(events(rows, "fish_spawned"), [])
            snaps = snapshots(rows)
            self.assertEqual(len(snaps[-1]["fish"]), 12)


class CaSauNamCheo(unittest.TestCase):
    def test_ca_sau_patrol_1mps_toi_waypoint(self):
        """Patrol 1.0 m/s tới waypoint: 60 tick đi đúng 1 m."""
        with Workdir() as w:
            m1 = {
                "id": "M1", "kind": "ca_sau", "pos": [60.0, 24.0],
                "waypoints": [[60.0, 24.0], [64.0, 24.0]],
                "target_idx": 1, "state": "patrol"
            }
            # Player ở mặt nước để không trigger chase
            code, rows = gather(w, {"player": {"pos": [2.0, 0.0]}, "monsters": [m1], "fish": []}, ticks=60)
            self.assertEqual(code, 0, rows)
            m_end = snapshots(rows)[-1]["monsters"][0]
            self.assertAlmostEqual(m_end["pos"][0], 61.0, places=3)
            self.assertAlmostEqual(m_end["pos"][1], 24.0, places=3)
            self.assertEqual(m_end["state"], "patrol")

    def test_ca_sau_chase_khi_player_d_ge_10_va_dist_le_10(self):
        """Chuyển sang chase và bơi 3.0 m/s về phía player."""
        with Workdir() as w:
            m1 = {
                "id": "M1", "kind": "ca_sau", "pos": [60.0, 24.0],
                "waypoints": [[60.0, 24.0], [64.0, 24.0]],
                "target_idx": 1, "state": "patrol"
            }
            # Player ở [60.0, 16.0] (cách 8m <= 10m, d >= 10)
            code, rows = gather(w, {"player": {"pos": [60.0, 16.0]}, "monsters": [m1], "fish": []}, ticks=1)
            self.assertEqual(code, 0, rows)
            m_end = snapshots(rows)[-1]["monsters"][0]
            self.assertEqual(m_end["state"], "chase")
            # 1 tick bơi 3.0 / 60 = 0.05 m về phía player (giảm d từ 24.0 -> 23.95)
            self.assertAlmostEqual(m_end["pos"][1], 23.95, places=3)

    def test_ca_sau_tro_ve_patrol_khi_player_len_mat_nuoc(self):
        """Trở về patrol khi player lên d < 10."""
        with Workdir() as w:
            m1 = {
                "id": "M1", "kind": "ca_sau", "pos": [60.0, 20.0],
                "waypoints": [[60.0, 24.0], [64.0, 24.0]],
                "target_idx": 1, "state": "chase"
            }
            # Player ở d = 9.0 (d < 10)
            code, rows = gather(w, {"player": {"pos": [60.0, 9.0]}, "monsters": [m1], "fish": []}, ticks=1)
            self.assertEqual(code, 0, rows)
            m_end = snapshots(rows)[-1]["monsters"][0]
            self.assertEqual(m_end["state"], "patrol")

    def test_ca_sau_hit_mat_1_mau_va_roi_nua_gio_lifo(self):
        """Chạm Cá Sấu (<= 1.5m, d >= 10, hết bất tử): mất 1 Máu, bỏ floor(n/2) LIFO, bất tử 90 tick."""
        with Workdir() as w:
            m1 = {
                "id": "M1", "kind": "ca_sau", "pos": [60.0, 20.0],
                "waypoints": [[60.0, 20.0], [64.0, 20.0]],
                "target_idx": 1, "state": "patrol"
            }
            # Player mang 3 món: ca_linh, ca_loc, ca_keo. Đứng cách 1.0 m (<= 1.5 m)
            hold = [{"id": "I1", "kind": "ca_linh", "fresh": 100}, {"id": "I2", "kind": "ca_loc", "fresh": 100},
                    {"id": "I3", "kind": "ca_keo", "fresh": 100}]
            code, rows = gather(w, {"player": {"pos": [60.0, 19.0], "hp": 3, "invuln_ticks": 0},
                                    "hold": hold, "monsters": [m1], "fish": []}, ticks=1)
            self.assertEqual(code, 0, rows)
            ev = events(rows, "monster_hit")
            self.assertEqual(len(ev), 1)
            self.assertEqual(ev[0]["data"]["monster_id"], "M1")
            self.assertEqual(ev[0]["data"]["hp"], 2)
            # floor(3 / 2) = 1 món bị mất theo LIFO: ca_keo
            self.assertEqual([i["kind"] for i in ev[0]["data"]["lost"]], ["ca_keo"])
            s = snapshots(rows)[-1]
            self.assertEqual(s["player"]["hp"], 2)
            self.assertEqual(s["player"]["invuln_ticks"], 90)
            self.assertEqual([i["kind"] for i in s["hold"]], ["ca_linh", "ca_loc"])
            # Con gây hit chuyển sang recoil
            self.assertEqual(s["monsters"][0]["state"], "recoil")

    def test_recoil_60_buoc_lui_xa_player(self):
        """Con gây hit vào recoil 60 bước, lùi 2/60 m/bước xa player."""
        with Workdir() as w:
            m1 = {
                "id": "M1", "kind": "ca_sau", "pos": [60.0, 20.0],
                "waypoints": [[60.0, 20.0], [64.0, 20.0]],
                "target_idx": 1, "state": "patrol"
            }
            # Player ở [60.0, 19.0]. Chạm ở tick 1: M1 ở [60.0, 20.0], hướng xa player là +d [0, 1]
            # Chạy 61 tick (1 tick chạm + 60 tick recoil)
            code, rows = gather(w, {"player": {"pos": [60.0, 19.0], "hp": 3, "invuln_ticks": 0},
                                    "monsters": [m1], "fish": []}, ticks=61)
            self.assertEqual(code, 0, rows)
            m_end = snapshots(rows)[-1]["monsters"][0]
            # M1 chase 1 tick tiến tới 19.95, sau đó lùi đúng 2.0 m theo +d: 19.95 + 2.0 = 21.95
            self.assertAlmostEqual(m_end["pos"][1], 21.95, places=3)
            # Hết recoil về patrol
            self.assertEqual(m_end["state"], "patrol")

    def test_ngat_do_ca_sau_khi_het_mau_va_mat_sach_gio(self):
        """Máu chạm 0 do Cá Sấu: ngất ngay (cause: monster), mất toàn bộ giỏ LIFO, kết thúc fainted."""
        with Workdir() as w:
            m1 = {
                "id": "M1", "kind": "ca_sau", "pos": [60.0, 20.0],
                "waypoints": [[60.0, 20.0], [64.0, 20.0]],
                "target_idx": 1, "state": "patrol"
            }
            hold = [{"id": "I1", "kind": "ca_linh", "fresh": 100}, {"id": "I2", "kind": "ca_loc", "fresh": 100},
                    {"id": "I3", "kind": "ca_keo", "fresh": 100}]
            code, rows = gather(w, {"player": {"pos": [60.0, 19.0], "hp": 1, "invuln_ticks": 0},
                                    "hold": hold, "monsters": [m1], "fish": []}, ticks=5)
            self.assertEqual(code, 0, rows)
            faint_ev = events(rows, "faint")
            self.assertEqual(len(faint_ev), 1)
            self.assertEqual(faint_ev[0]["data"]["cause"], "monster")
            self.assertEqual(faint_ev[0]["data"]["hp"], 0)
            end_ev = events(rows, "gather_end")
            self.assertEqual(len(end_ev), 1)
            self.assertEqual(end_ev[0]["data"]["reason"], "fainted")
            self.assertEqual(end_ev[0]["data"]["inventory"]["items"], [])


class NewKindsAndYields(unittest.TestCase):
    def test_bat_ca_keo_yield_2(self):
        """Bắt cá kèo được yield = 2 ca_keo."""
        with Workdir() as w:
            fish = [{"id": "F1", "kind": "ca_keo", "pos": [20.0, 25.0], "heading_deg": 0.0}]
            inputs = [{"tick": 0, "catch": True}]
            code, rows = gather(w, {"player": {"pos": [20.0, 25.0]}, "fish": fish, "random_fish": False, "monsters": []},
                                inputs=inputs, ticks=2)
            self.assertEqual(code, 0, rows)
            ev = events(rows, "fish_caught")
            self.assertEqual(len(ev), 1)
            self.assertEqual(ev[0]["data"]["kind"], "ca_keo")
            self.assertEqual(ev[0]["data"]["yield"], 2)
            self.assertEqual([i["kind"] for i in snapshots(rows)[-1]["hold"]], ["ca_keo", "ca_keo"])

    def test_hai_nut_keo_neo_N5(self):
        """Nút N5 hái được keo_neo."""
        with Workdir() as w:
            nodes = [{"id": "N5", "kind": "keo_neo", "pos": [76.0, 0.0], "regrow_ticks": 0}]
            inputs = [{"tick": 0, "interact": True}]
            code, rows = gather(w, {"player": {"pos": [76.0, 0.0]}, "nodes": nodes, "fish": [], "monsters": []},
                                inputs=inputs, ticks=2)
            self.assertEqual(code, 0, rows)
            ev = events(rows, "gather")
            self.assertEqual(len(ev), 1)
            self.assertEqual(ev[0]["data"]["kind"], "keo_neo")
            self.assertEqual([i["kind"] for i in snapshots(rows)[-1]["hold"]], ["keo_neo"])


if __name__ == "__main__":
    unittest.main()
