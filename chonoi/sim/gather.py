"""Buổi sáng — Lặn & Hái (`gather`). KHUNG: bơi, chặn mép, đồng hồ, cập bến, xuất kho.

Mặt cắt dòng sông nhìn NGANG: vị trí `[x, d]` (x sang phải, `d` độ sâu hướng xuống, d = 0 là mặt nước).
`move = [x, d]`: thành phần thứ hai DƯƠNG = bơi xuống. Hướng mặt là góc từ +x, dương = xuống.

Đã làm sẵn để smoke test chạy được: bơi + tăng/giảm tốc, chặn mép (d không âm), đồng hồ và hết giờ,
cập bến (`interact` trong vùng bến -> `gather_end` reason `docked`), xuất kho, snapshot đầy đủ trường gather.

Nhóm viết tiếp (đúng thứ tự một bước trong PRD mục 13.8, "Gather"):
  XONG (lát 1): bơi + oxy + biên; dive / surface / oxygen_empty / choke / faint; ngất bỏ giỏ LIFO.
  XONG (lát 2): hái + bắt cá + cập bến + kho
      - hái nút ở mặt nước (gather, hold_full), nút mọc lại (node_regrown đã có phần đếm ngược)
      - bắt đàn cá bằng `catch` (fish_caught, hold_full, hồi chiêu catch_cd_ticks, chỉ khi dưới nước)
      - cập bến xét TRƯỚC hái (đã có); ghi kho đúng một lần do runner lo
Các tính năng của phase sau chưa nằm trong khung này.
"""

import math

from ..ids import id_key, sort_by_id
from .ramp import ramp_velocity

TICK = 60.0
AXES = ("x", "d")
EPS = 1e-9
UNITS_PER_POINT = 240  # Phase 3: 1 điểm tươi = 240 đơn vị nguyên -> so ngưỡng 30 và floor chính xác


def _move_fish_with_reflection(pos, heading_deg, kind, t):
    """Di chuyển đàn cá trong tick và phản xạ khi chạm mép x ∈ [4, 96] và d ∈ dải độ sâu."""
    x_bounds = (float(t["fish_x"][0]), float(t["fish_x"][1]))
    d_bounds = (float(t["fish_depths"][kind][0]), float(t["fish_depths"][kind][1]))
    step_dist = float(t.get("fish_speed", 1.5)) / TICK

    rad = math.radians(heading_deg)
    vx = math.cos(rad)
    vd = math.sin(rad)

    px, pd = float(pos[0]), float(pos[1])
    remain = step_dist

    for _ in range(3):
        if remain <= 1e-12:
            break

        tx = float("inf")
        if vx > 1e-12:
            tx = (x_bounds[1] - px) / vx
        elif vx < -1e-12:
            tx = (x_bounds[0] - px) / vx

        td = float("inf")
        if vd > 1e-12:
            td = (d_bounds[1] - pd) / vd
        elif vd < -1e-12:
            td = (d_bounds[0] - pd) / vd

        tx = max(0.0, tx)
        td = max(0.0, td)

        if tx > remain + 1e-9 and td > remain + 1e-9:
            px += vx * remain
            pd += vd * remain
            remain = 0.0
            break

        if abs(tx - td) <= 1e-9 and tx <= remain + 1e-9:
            # Chạm góc: đảo cả hai
            t_hit = min(tx, remain)
            px += vx * t_hit
            pd += vd * t_hit
            remain -= t_hit
            vx = -vx
            vd = -vd
        elif tx < td and tx <= remain + 1e-9:
            # Chạm mép x
            px += vx * tx
            pd += vd * tx
            remain -= tx
            vx = -vx
        elif td < tx and td <= remain + 1e-9:
            # Chạm mép d
            px += vx * td
            pd += vd * td
            remain -= td
            vd = -vd
        else:
            px += vx * remain
            pd += vd * remain
            remain = 0.0
            break

        px = max(x_bounds[0], min(x_bounds[1], px))
        pd = max(d_bounds[0], min(d_bounds[1], pd))

    new_heading = math.degrees(math.atan2(vd, vx)) % 360.0
    return [px, pd], new_heading


class GatherSim:
    mode = "gather"
    phase = "gather"

    def __init__(self, tuning, scenario, streams, ids):
        t = tuning["gather"]
        self.t = t
        self.rng = streams
        self.ids = ids
        p = scenario.get("player", {})
        self.pos = [float(c) for c in p.get("pos", t["start_pos"])]
        self.vel = [float(c) for c in p.get("vel", [0.0, 0.0])]
        self._tgt = None
        self._ramp_left = 0
        self.heading = float(p.get("heading_deg", t["start_heading_deg"]))
        self.oxygen_max = int(round(t["oxygen_max_s"] * TICK))
        self.oxygen_ticks = p.get("oxygen_ticks", self.oxygen_max)
        self.hp = p.get("hp", t["hp_max"])
        self.zero_oxy_ticks = p.get("zero_oxy_ticks", 0)
        self.invuln_ticks = p.get("invuln_ticks", 0)
        self.catch_cd_ticks = p.get("catch_cd_ticks", 0)
        # Phase 3 (v1.2): bật khi manifest có khối `freshness`. Tắt thì hành xử y hệt v1.1 (kho đếm, không hao).
        self.fresh_cfg = tuning.get("freshness")
        self.fresh_on = self.fresh_cfg is not None
        if self.fresh_on:
            f = self.fresh_cfg
            self._decay_u = int(round(float(f["gather_decay_per_s"]) * UNITS_PER_POINT / TICK))
            self._spoil_u = int(round(float(f["spoiled_below"]) * UNITS_PER_POINT))
            self._init_u = int(round(float(f["initial"]) * UNITS_PER_POINT))
        else:
            self._decay_u = self._spoil_u = 0
            self._init_u = 100 * UNITS_PER_POINT
        self._hold = []  # cá thể {id, kind, u}; thứ tự vào giỏ, cuối mảng là mới nhất (LIFO)
        for h in scenario.get("hold", []):
            if isinstance(h, dict):
                self._hold.append({"id": h["id"], "kind": h["kind"], "u": int(round(float(h["fresh"]) * UNITS_PER_POINT))})
            else:
                self._hold.append({"id": None, "kind": h, "u": self._init_u})
        total_dur = int(round(t["duration_s"] * TICK))
        self.time_left_ticks = scenario.get("time_left_ticks", total_dur)
        self.phase_tick = total_dur - self.time_left_ticks

        # nút
        src_nodes = scenario["nodes"] if "nodes" in scenario else t["nodes"]
        self.nodes = [{"id": n["id"], "kind": n["kind"], "pos": [float(c) for c in n["pos"]],
                       "regrow_ticks": n.get("regrow_ticks", 0)} for n in src_nodes]

        # đàn cá
        if "fish" in scenario:
            src_fish = scenario["fish"]
        elif scenario.get("random_fish", True):
            src_fish = t["fish_initial"]
        else:
            src_fish = []
        self.fish = [{"id": f["id"], "kind": f["kind"], "pos": [float(c) for c in f["pos"]],
                      "heading_deg": float(f.get("heading_deg", 0.0)),
                      "age_ticks": int(f.get("age_ticks", 0))} for f in src_fish]

        # quái vật (Cá Sấu Năm Chèo)
        m_tuning = t.get("monsters", {})
        if "monsters" in scenario:
            src_monsters = scenario["monsters"]
        elif scenario.get("random_fish", True):
            day = scenario.get("day", 1)
            spawns = m_tuning.get("spawns", [])
            src_monsters = [s for s in spawns if s.get("from_day", 1) <= day]
        else:
            src_monsters = []

        self.monsters = []
        for m in src_monsters:
            self.monsters.append({
                "id": m["id"],
                "kind": m.get("kind", "ca_sau"),
                "pos": [float(c) for c in m["pos"]],
                "waypoints": [[float(c) for c in wp] for wp in m.get("waypoints", [[60.0, 24.0], [64.0, 24.0]])],
                "target_idx": int(m.get("target_idx", 1)),
                "state": m.get("state", "patrol"),
                "state_ticks_left": int(m.get("state_ticks_left", 0)),
                "recoil_dir": [float(c) for c in m["recoil_dir"]] if m.get("recoil_dir") else None,
                "heading_deg": float(m.get("heading_deg", 0.0))
            })

        for coll in (self.nodes, self.fish, self.monsters, self._hold):
            for e in coll:
                if e["id"] is not None:
                    ids.reserve(e["id"])
        for it in self._hold:  # hàng dựng từ scenario kiểu cũ (mảng kind) nhận id mới theo thứ tự mảng
            if it["id"] is None:
                it["id"] = ids.new("I")

        self.money = 0
        self.earned = 0
        self.reputation = tuning["quan"]["reputation_initial"]
        self.done = False
        self.reason = None

    # --- giao diện cho runner -------------------------------------------------
    def _out_item(self, it) -> dict:
        u = it["u"]
        fresh = u // UNITS_PER_POINT if u % UNITS_PER_POINT == 0 else u / UNITS_PER_POINT
        return {"id": it["id"], "kind": it["kind"], "fresh": fresh}

    def _out_list(self, items):
        """Danh sách cá thể -> dạng xuất (v1.2: mảng {id,kind,fresh}; v1.1: mảng kind)."""
        if self.fresh_on:
            return [self._out_item(it) for it in items]
        return [it["kind"] for it in items]

    @property
    def hold(self):
        """Giỏ ở dạng xuất: v1.1 mảng kind, v1.2 mảng {id,kind,fresh} (thứ tự vào giỏ)."""
        return self._out_list(self._hold)

    def _add_items(self, kind, n):
        for _ in range(n):
            self._hold.append({"id": self.ids.new("I"), "kind": kind, "u": self._init_u})

    def _decay_hold(self, events):
        """Hao tươi hàng có sẵn ở đầu bước; kẹp đáy 0; phát spoiled (theo id) khi từ >= ngưỡng xuống < ngưỡng."""
        crossed = []
        for it in self._hold:
            before = it["u"]
            it["u"] = max(0, before - self._decay_u)
            if before >= self._spoil_u > it["u"]:
                crossed.append(it)
        for it in sort_by_id(crossed):
            events.append(("spoiled", {"item_id": it["id"], "kind": it["kind"], "location": "hold"}))

    def inventory_items(self):
        """v1.2: mảng cá thể sắp theo id; v1.1: object đếm sắp theo kind."""
        if self.fresh_on:
            return [self._out_item(it) for it in sort_by_id(self._hold)]
        counts = {}
        for it in self._hold:
            counts[it["kind"]] = counts.get(it["kind"], 0) + 1
        return {k: counts[k] for k in sorted(counts)}

    def snapshot(self) -> dict:
        return {
            "player": {"pos": self.pos, "vel": self.vel, "heading_deg": self.heading,
                       "oxygen_ticks": self.oxygen_ticks, "oxygen_max_ticks": self.oxygen_max,
                       "hp": self.hp, "hp_max": self.t["hp_max"], "zero_oxy_ticks": self.zero_oxy_ticks,
                       "invuln_ticks": self.invuln_ticks, "catch_cd_ticks": self.catch_cd_ticks,
                       "at_surface": self._at_surface()},
            "hold": self.hold, "hold_count": len(self._hold),
            "hold_capacity": self.t["hold_capacity"],
            "nodes": [{"id": n["id"], "pos": n["pos"], "kind": n["kind"],
                       "ready": n["regrow_ticks"] == 0, "regrow_ticks": n["regrow_ticks"]}
                      for n in sort_by_id(self.nodes)],
            "fish": [{"id": f["id"], "pos": f["pos"], "kind": f["kind"], "heading_deg": f["heading_deg"]}
                     for f in sort_by_id(self.fish)],
            "monsters": [{"id": m["id"], "kind": m["kind"], "pos": m["pos"],
                          "state": m["state"], "heading_deg": m.get("heading_deg", 0.0)}
                         for m in sort_by_id(self.monsters)],
        }

    # --- một bước ---------------------------------------------------------------
    def step(self, inp):
        events = []
        # 1. đồng hồ và hàng có sẵn: giảm bộ đếm, nút mọc lại
        self.time_left_ticks = max(0, self.time_left_ticks - 1)
        self.phase_tick += 1
        self.invuln_ticks = max(0, self.invuln_ticks - 1)
        self.catch_cd_ticks = max(0, self.catch_cd_ticks - 1)
        for n in sort_by_id(self.nodes):
            if n["regrow_ticks"] > 0:
                n["regrow_ticks"] -= 1
                if n["regrow_ticks"] == 0:
                    events.append(("node_regrown", {"node_id": n["id"]}))
        if self.fresh_on:
            self._decay_hold(events)

        # 2. bơi + chặn mép, rồi so phân vùng đầu/cuối bước -> dive / surface
        was_surface = self._at_surface()
        self._move(inp)
        now_surface = self._at_surface()
        if was_surface and not now_surface:
            events.append(("dive", {"pos": list(self.pos)}))
        elif not was_surface and now_surface:
            events.append(("surface", {"pos": list(self.pos)}))

        # 2b. oxy theo d CUỐI bước, ngạt, choke, ngất
        if self._breathe(now_surface, events):
            return events

        # 3. Cá Sấu di chuyển
        self._step_monsters()

        # 3b. Kiểm tra chạm Cá Sấu (sau khi cả hai di chuyển)
        if self._check_monster_hit(events):
            return events

        # 4. interact: bến trước, rồi hái
        if inp.pressed("interact"):
            if self._in_dock():
                self._finish("docked", events)
                return events
            if self._at_surface():
                r = self.t["interact_radius"]
                candidates = []
                for n in self.nodes:
                    if n["regrow_ticks"] == 0:
                        d = math.dist(self.pos, n["pos"])
                        if d <= r + EPS:
                            candidates.append((d, id_key(n["id"]), n))
                if candidates:
                    candidates.sort(key=lambda item: (item[0], item[1]))
                    _, _, best_node = candidates[0]
                    required = self.t["node_yield"]
                    free = self.t["hold_capacity"] - len(self._hold)
                    if len(self._hold) + required <= self.t["hold_capacity"]:
                        self._add_items(best_node["kind"], required)
                        best_node["regrow_ticks"] = int(round(self.t["regrow_s"] * TICK))
                        events.append(("gather", {"node_id": best_node["id"], "kind": best_node["kind"], "amount": required}))
                    else:
                        events.append(("hold_full", {"action": "gather", "node_id": best_node["id"], "required": required, "free": free}))

        # 5. bắt cá (xét theo vị trí cá trước khi bơi ở bước này)
        if inp.pressed("catch"):
            if self.catch_cd_ticks == 0 and not self._at_surface():
                r = self.t["catch_radius"]
                candidates = []
                for f in self.fish:
                    d = math.dist(self.pos, f["pos"])
                    if d <= r + EPS:
                        candidates.append((d, id_key(f["id"]), f))
                if candidates:
                    candidates.sort(key=lambda item: (item[0], item[1]))
                    _, _, best_fish = candidates[0]
                    kind = best_fish["kind"]
                    required = self.t["fish_yield"][kind]
                    free = self.t["hold_capacity"] - len(self._hold)
                    if len(self._hold) + required <= self.t["hold_capacity"]:
                        self._add_items(kind, required)
                        self.fish.remove(best_fish)
                        events.append(("fish_caught", {"fish_id": best_fish["id"], "kind": kind, "yield": required}))
                        self.catch_cd_ticks = int(round(self.t["catch_cooldown_s"] * TICK))
                    else:
                        events.append(("hold_full", {"action": "catch", "fish_id": best_fish["id"], "required": required, "free": free}))

        # 6. hết giờ
        if self.time_left_ticks <= 0:
            self._finish("time", events)
            return events

        # 7. Đàn cá bơi & Sinh cá mới
        self._step_fish(events)

        return events

    # --- tiện ích ---------------------------------------------------------------
    def _at_surface(self) -> bool:
        return self.pos[1] <= self.t["surface_depth"]

    def _in_dock(self) -> bool:
        return math.dist(self.pos, self.t["dock_pos"]) <= self.t["dock_radius"] + EPS

    def _breathe(self, at_surface, events) -> bool:
        """Oxy / ngạt theo PRD-0 mục F. Trả True nếu ngất (buổi sáng đã kết thúc, dừng bước)."""
        if at_surface:
            self.oxygen_ticks = min(self.oxygen_max, self.oxygen_ticks + int(self.t["oxygen_refill_per_tick"]))
            self.zero_oxy_ticks = 0
            return False
        before = self.oxygen_ticks
        self.oxygen_ticks = max(0, before - 1)
        if before > 0 and self.oxygen_ticks == 0:
            events.append(("oxygen_empty", {"oxygen_ticks": 0}))
        if self.oxygen_ticks > 0:
            return False
        # mỗi bước dưới nước kết thúc với oxy 0 (kể cả bước vừa chạm 0) đều đếm ngạt
        self.zero_oxy_ticks += 1
        if self.zero_oxy_ticks < int(self.t["choke_interval_ticks"]):
            return False
        self.zero_oxy_ticks = 0
        self.hp -= 1
        events.append(("choke", {"hp": self.hp}))
        if self.hp > 0:
            return False
        lost = self._out_list(self._hold[::-1])  # nhặt sau bỏ trước (LIFO)
        self._hold = []
        events.append(("faint", {"cause": "choke", "lost": lost, "hp": 0}))
        self._finish("fainted", events)
        return True

    def _finish(self, reason, events):
        self.done = True
        self.reason = reason
        events.append(("gather_end", {"reason": reason, "inventory": {"items": self.inventory_items()}}))

    def _move(self, inp):
        speed = self.t["swim_speed"]
        mx, md = inp.move
        self.vel = ramp_velocity(self, (mx * speed, md * speed), int(self.t["ramp_max_ticks"]))
        if (mx, md) != (0.0, 0.0):
            self.heading = math.degrees(math.atan2(md, mx)) % 360
        b = self.t["bounds"]
        for i, axis in enumerate(AXES):
            self.pos[i] += self.vel[i] / TICK
            lo, hi = b[axis]
            if self.pos[i] <= lo:
                self.pos[i] = lo
                self.vel[i] = max(0.0, self.vel[i])
            elif self.pos[i] >= hi:
                self.pos[i] = hi
                self.vel[i] = min(0.0, self.vel[i])

    def _step_monsters(self):
        m_tuning = self.t.get("monsters", {})
        m_spec = m_tuning.get("species", {}).get("ca_sau", {})
        if not m_spec:
            return
        patrol_speed = float(m_spec["patrol_speed"]) / TICK
        chase_speed = float(m_spec["chase_speed"]) / TICK
        detect_radius = float(m_spec["detect_radius"])
        exit_radius = float(m_spec["exit_radius"])
        recoil_step = float(m_spec["recoil_dist"]) / float(m_spec["recoil_ticks"])
        d_min, d_max = float(m_spec["depths"][0]), float(m_spec["depths"][1])
        x_min, x_max = float(self.t["bounds"]["x"][0]), float(self.t["bounds"]["x"][1])

        for m in sort_by_id(self.monsters):
            # Recoil
            if m["state"] == "recoil":
                if m["state_ticks_left"] > 0:
                    rdir = m["recoil_dir"] or [1.0, 0.0]
                    m["pos"][0] += rdir[0] * recoil_step
                    m["pos"][1] += rdir[1] * recoil_step
                    m["pos"][0] = max(x_min, min(x_max, m["pos"][0]))
                    m["pos"][1] = max(d_min, min(d_max, m["pos"][1]))
                    m["state_ticks_left"] -= 1
                    if m["state_ticks_left"] == 0:
                        m["state"] = "patrol"
                        m["recoil_dir"] = None
                continue

            # Patrol & Chase
            dist_to_p = math.dist(m["pos"], self.pos)
            p_underwater = self.pos[1] >= d_min

            if m["state"] == "patrol":
                if p_underwater and dist_to_p <= detect_radius + EPS:
                    m["state"] = "chase"
            elif m["state"] == "chase":
                if not p_underwater or dist_to_p > exit_radius + EPS:
                    m["state"] = "patrol"

            if m["state"] == "chase":
                dx = self.pos[0] - m["pos"][0]
                dd = self.pos[1] - m["pos"][1]
                dist = math.hypot(dx, dd)
                if dist > 0:
                    step = min(dist, chase_speed)
                    m["pos"][0] += (dx / dist) * step
                    m["pos"][1] += (dd / dist) * step
                    m["heading_deg"] = math.degrees(math.atan2(dd, dx)) % 360
            elif m["state"] == "patrol":
                target_wp = m["waypoints"][m["target_idx"]]
                dx = target_wp[0] - m["pos"][0]
                dd = target_wp[1] - m["pos"][1]
                dist = math.hypot(dx, dd)
                if dist <= patrol_speed + EPS:
                    m["pos"] = [float(target_wp[0]), float(target_wp[1])]
                    m["target_idx"] = 1 - m["target_idx"]
                else:
                    m["pos"][0] += (dx / dist) * patrol_speed
                    m["pos"][1] += (dd / dist) * patrol_speed
                if dist > 0:
                    m["heading_deg"] = math.degrees(math.atan2(dd, dx)) % 360

            m["pos"][0] = max(x_min, min(x_max, m["pos"][0]))
            m["pos"][1] = max(d_min, min(d_max, m["pos"][1]))

    def _check_monster_hit(self, events) -> bool:
        """Kiểm tra va chạm với Cá Sấu sau khi cả hai di chuyển. Trả True nếu ngất."""
        m_tuning = self.t.get("monsters", {})
        m_spec = m_tuning.get("species", {}).get("ca_sau", {})
        if not m_spec:
            return False

        d_min = float(m_spec["depths"][0])
        hit_radius = float(m_spec["hit_radius"])

        # Chỉ xét khi người chơi ở d >= 10 và hết bất tử
        if self.pos[1] < d_min or self.invuln_ticks > 0:
            return False

        candidates = []
        for m in self.monsters:
            if m["state"] == "recoil":
                continue
            dist = math.dist(self.pos, m["pos"])
            if dist <= hit_radius + EPS:
                candidates.append((dist, id_key(m["id"]), m))

        if not candidates:
            return False

        candidates.sort(key=lambda item: (item[0], item[1]))
        _, _, best_m = candidates[0]

        # Trừ 1 Máu
        self.hp -= 1

        # Bỏ floor(số đang mang / 2) theo LIFO
        drop_count = len(self._hold) // 2
        dropped = []
        if drop_count > 0:
            dropped = self._out_list(self._hold[-drop_count:][::-1])
            self._hold = self._hold[:-drop_count]

        self.invuln_ticks = int(m_tuning.get("invuln_ticks", 90))

        # Hướng lùi: xa người chơi đã chốt lúc chạm, trùng tâm dùng +x
        dx = best_m["pos"][0] - self.pos[0]
        dd = best_m["pos"][1] - self.pos[1]
        dist = math.hypot(dx, dd)
        if dist > 1e-12:
            recoil_dir = [dx / dist, dd / dist]
        else:
            recoil_dir = [1.0, 0.0]

        best_m["state"] = "recoil"
        best_m["state_ticks_left"] = int(m_spec.get("recoil_ticks", 60))
        best_m["recoil_dir"] = recoil_dir

        events.append(("monster_hit", {"monster_id": best_m["id"], "hp": self.hp, "lost": dropped}))

        if self.hp <= 0:
            lost = self._out_list(self._hold[::-1])
            self._hold = []
            events.append(("faint", {"cause": "monster", "lost": lost, "hp": 0}))
            self._finish("fainted", events)
            return True

        return False

    def _step_fish(self, events):
        """Đàn cá bơi và sinh cá theo lịch."""
        turn_ticks = int(self.t.get("fish_turn_ticks", 120))

        # 1. Bơi cá
        for f in sort_by_id(self.fish):
            f["age_ticks"] += 1
            if f["age_ticks"] % turn_ticks == 0:
                f["heading_deg"] = self.rng.get("fish_swim").uniform(0.0, 360.0)
            f["pos"], f["heading_deg"] = _move_fish_with_reflection(f["pos"], f["heading_deg"], f["kind"], self.t)

        # 2. Sinh cá tại phase_tick = 360 * k (k >= 1)
        spawn_ticks = int(self.t.get("fish_spawn_ticks", 360))
        fish_max = int(self.t.get("fish_max", 12))
        clearance = float(self.t.get("fish_spawn_clearance", 1.0))

        if self.phase_tick > 0 and self.phase_tick % spawn_ticks == 0:
            if len(self.fish) < fish_max:
                valid_by_kind = {}
                spawn_x = sorted(self.t.get("fish_spawn_x", [15, 30, 45, 60, 75, 90]))
                spawn_depths = self.t.get("fish_spawn_depths", {})

                for kind in ("ca_linh", "ca_loc", "ca_keo"):
                    k_pts = []
                    depths = sorted(spawn_depths.get(kind, []))
                    for x in spawn_x:
                        for d in depths:
                            pt = [float(x), float(d)]
                            if all(math.dist(pt, f["pos"]) > clearance + EPS for f in self.fish):
                                k_pts.append(pt)
                    if k_pts:
                        valid_by_kind[kind] = k_pts

                if valid_by_kind:
                    weights_cfg = self.t.get("fish_weights", {"ca_linh": 0.4, "ca_loc": 0.3, "ca_keo": 0.3})
                    valid_kinds = [k for k in ("ca_linh", "ca_loc", "ca_keo") if k in valid_by_kind]
                    raw_w = [weights_cfg[k] for k in valid_kinds]
                    tot_w = sum(raw_w)
                    norm_w = [w / tot_w for w in raw_w]

                    chosen_kind = self.rng.get("fish_spawn").choices(valid_kinds, weights=norm_w, k=1)[0]
                    chosen_pt = self.rng.get("fish_spawn").choice(valid_by_kind[chosen_kind])
                    init_heading = self.rng.get("fish_spawn").uniform(0.0, 360.0)

                    new_id = self.ids.new("F")
                    new_fish = {
                        "id": new_id,
                        "kind": chosen_kind,
                        "pos": [float(chosen_pt[0]), float(chosen_pt[1])],
                        "heading_deg": init_heading,
                        "age_ticks": 0
                    }
                    self.fish.append(new_fish)
                    events.append(("fish_spawned", {"fish_id": new_id, "kind": chosen_kind, "pos": list(new_fish["pos"])}))
