"""Buổi tối — Mở Quán (`quan`). Luật theo PRD-0 mục F (Quán) và mục E (event).

Nhìn từ trên xuống, vị trí `[x, z]`. Mỗi bước (tick k -> k+1), đúng thứ tự PRD-0:
  1. đồng hồ; giảm timer nấu / ăn / kiên nhẫn; chỉ tăng `ready_ticks` cho món đã ready từ đầu bước
  2. bếp theo id: nấu xong -> ready (`dish_ready`)
  3. di chuyển, rồi tối đa MỘT `interact` (khoảng cách, bếp trước bàn, id):
       bếp idle nhận đơn reserved cũ nhất (`cook_started`) · bếp ready -> tay trống (`dish_picked`)
       · bàn nhận đúng order (`served`)
  4. theo id bàn: ăn xong -> `paid`; hết kiên nhẫn -> `customer_left`; hết ca -> dọn bàn (`closing`) + `quan_end`
  5. còn giờ: khách mới theo lịch (`customer_arrived` / `no_dish`)
Số liệu chỉ đọc từ `tuning` (game.contract.json); ngẫu nhiên chỉ qua `Streams`.
"""

import math

from ..errors import BadInput
from ..ids import id_key, sort_by_id
from ..scenario import check_quan_state
from .ramp import ramp_velocity

TICK = 60.0
EPS = 1e-9


def _ticks(seconds):
    return int(round(seconds * TICK))


class QuanSim:
    mode = "quan"
    phase = "quan"

    def __init__(self, tuning, scenario, streams, ids, inventory=None):
        t = tuning["quan"]
        self.t = t
        self.menu = tuning["menu"]
        self.rng = streams
        self.ids = ids
        self.patience_total = _ticks(t["patience_s"])
        self.eat_total = _ticks(t["eat_s"])
        self.interval_ticks = _ticks(t["customer_interval_s"])
        self.random_customers = scenario.get("random_customers", True)
        p = scenario.get("player", {})
        self.pos = [float(c) for c in p.get("pos", t["start_pos"])]
        self.vel = [float(c) for c in p.get("vel", [0.0, 0.0])]
        self._tgt = None
        self._ramp_left = 0
        # kho: --inventory HOẶC scenario.stock (cả hai -> headless đã báo mã 2)
        self.stock = dict(inventory if inventory is not None else scenario.get("stock", {}))
        self.time_left_ticks = scenario.get("time_left_ticks", _ticks(t["duration_s"]))
        self.reputation = scenario.get("reputation", t["reputation_initial"])
        self.phase_tick = 0
        self.stoves = [self._new_stove(s) for s in self._merge(t["stoves"], scenario.get("stoves", []))]
        self.tables = self._merge(t["tables"], scenario.get("tables", []))
        self.customers = [self._new_customer(c) for c in scenario.get("customers", [])]
        self.hand = self._payload(scenario.get("hand"))
        for c in self.customers:
            ids.reserve(c["id"])
        check_quan_state(self, tuning)
        self.money = 0
        self.earned = 0
        self.shift_earned = 0
        self.done = False
        self.reason = None

    # --- dựng trạng thái từ scenario (giá trị mặc định theo PRD-0 mục D) ---------------------
    @staticmethod
    def _merge(defaults, updates):
        by_id = {d["id"]: dict(d) for d in defaults}
        for u in updates:
            if u["id"] not in by_id:
                raise BadInput(f"id bếp/bàn không tồn tại: {u['id']}")
            by_id[u["id"]].update(u)
        return sort_by_id(list(by_id.values()))

    def _payload(self, d):
        if d is None:
            return None
        return {"order_id": d["order_id"], "dish_id": d["dish_id"],
                "base_price": d.get("base_price", self.menu[d["dish_id"]]["price"])}

    def _new_stove(self, s):
        return {"id": s["id"], "pos": [float(c) for c in s["pos"]], "state": s.get("state", "idle"),
                "dish": self._payload(s.get("dish")), "cook_ticks_left": s.get("cook_ticks_left", 0),
                "ready_ticks": s.get("ready_ticks", 0)}

    def _new_customer(self, c):
        status = c.get("order_status", "served" if c.get("state") == "eating" else "reserved")
        dish = self.menu[c["dish_id"]]
        if "reserved" in c:
            reserved = dict(c["reserved"])
        elif status == "reserved":
            reserved = dict(dish["recipe"])
        else:
            reserved = {}
        return {"id": c["id"], "table_id": c["table_id"], "dish_id": c["dish_id"],
                "order_tick": c.get("order_tick", 0), "state": c.get("state", "waiting"),
                "patience_ticks_left": c.get("patience_ticks_left", self.patience_total),
                "eat_ticks_left": c.get("eat_ticks_left", 0), "order_status": status,
                "reserved": reserved,
                "base_price": c.get("base_price", 0 if status == "reserved" else dish["price"]),
                "tip": c.get("tip", 0)}

    # --- giao diện cho runner ---------------------------------------------------------------
    def snapshot(self) -> dict:
        occupied = {c["table_id"]: c["id"] for c in self.customers}
        return {
            "player": {"pos": self.pos, "vel": self.vel},
            "stock": {k: self.stock[k] for k in sorted(self.stock) if self.stock[k] > 0},
            "hand": self.hand,
            "stoves": [{k: s[k] for k in ("id", "pos", "state", "dish", "cook_ticks_left", "ready_ticks")}
                       for s in self.stoves],
            "tables": [{"id": tb["id"], "pos": tb["pos"], "customer_id": occupied.get(tb["id"])}
                       for tb in self.tables],
            "customers": sort_by_id(self.customers),
        }

    # --- một bước -----------------------------------------------------------------------------
    def step(self, inp):
        events = []
        self.phase_tick += 1
        # 1. đồng hồ, nấu, ăn, kiên nhẫn
        self.time_left_ticks = max(0, self.time_left_ticks - 1)
        for s in self.stoves:
            if s["state"] == "ready":
                s["ready_ticks"] += 1
            elif s["state"] == "cooking":
                s["cook_ticks_left"] = max(0, s["cook_ticks_left"] - 1)
        for c in self.customers:
            if c["state"] == "waiting":
                c["patience_ticks_left"] = max(0, c["patience_ticks_left"] - 1)
            else:
                c["eat_ticks_left"] = max(0, c["eat_ticks_left"] - 1)
        # 2. bếp theo id
        for s in sort_by_id(self.stoves):
            if s["state"] == "cooking" and s["cook_ticks_left"] == 0:
                s["state"], s["ready_ticks"] = "ready", 0
                events.append(("dish_ready", self._stove_data(s)))
        # 3. di chuyển rồi tối đa một interact
        self._move(inp)
        if inp.pressed("interact"):
            self._interact(events)
        # 4. thu tiền / khách rời / hết ca
        closing = self.time_left_ticks <= 0
        for tb in sort_by_id(self.tables):
            c = self._customer_at(tb["id"])
            if c is None:
                continue
            if c["state"] == "eating" and (c["eat_ticks_left"] == 0 or closing):
                self._pay(c, "closing" if c["eat_ticks_left"] > 0 else "finished_eating", events)
            elif c["state"] == "waiting" and (c["patience_ticks_left"] == 0 or closing):
                # hết kiên nhẫn chỉ tính khi ca còn giờ; hết ca thì rời "closing", không trừ uy tín
                self._leave(c, "closing" if closing else "patience", events)
        if closing:
            self.done = True
            self.reason = "time"
            events.append(("quan_end", {"reason": "time", "money": self.money, "earned": self.earned,
                                        "shift_earned": self.shift_earned, "reputation": self.reputation}))
            return events
        # 5. khách mới theo lịch
        first = self.t["first_customer_tick"]
        if (self.random_customers and self.phase_tick >= first
                and (self.phase_tick - first) % self.interval_ticks == 0):
            self._spawn(events)
        return events

    # --- tiện ích -----------------------------------------------------------------------------
    @staticmethod
    def _stove_data(s):
        return {"stove_id": s["id"], "order_id": s["dish"]["order_id"], "dish_id": s["dish"]["dish_id"]}

    def _customer_at(self, table_id):
        for c in self.customers:
            if c["table_id"] == table_id:
                return c
        return None

    def _customer(self, order_id):
        for c in self.customers:
            if c["id"] == order_id:
                return c
        return None

    def _available(self):
        """Tồn vật lý trừ phần đã giữ cho khách."""
        avail = dict(self.stock)
        for c in self.customers:
            for k, n in c["reserved"].items():
                avail[k] = avail.get(k, 0) - n
        return avail

    def _set_reputation(self, value):
        self.reputation = round(min(self.t["reputation_max"], max(self.t["reputation_min"], value)), 6)

    def _interact(self, events):
        radius = self.t["interact_radius"]
        cand = []
        for s in self.stoves:
            cand.append((math.dist(self.pos, s["pos"]), 0, id_key(s["id"]), "stove", s))
        for tb in self.tables:
            cand.append((math.dist(self.pos, tb["pos"]), 1, id_key(tb["id"]), "table", tb))
        cand = [c for c in cand if c[0] <= radius + EPS]
        if not cand:
            return
        _, _, _, kind, obj = min(cand, key=lambda c: c[:3])
        if kind == "stove":
            if obj["state"] == "idle":
                self._start_cooking(obj, events)
            elif obj["state"] == "ready" and self.hand is None:
                self.hand, obj["dish"] = obj["dish"], None
                obj["state"], obj["cook_ticks_left"], obj["ready_ticks"] = "idle", 0, 0
                events.append(("dish_picked", {"stove_id": obj["id"], "order_id": self.hand["order_id"],
                                               "dish_id": self.hand["dish_id"]}))
        else:
            c = self._customer_at(obj["id"])
            if c and c["state"] == "waiting" and self.hand and self.hand["order_id"] == c["id"]:
                self._serve(c, events)

    def _start_cooking(self, stove, events):
        pending = [c for c in self.customers if c["order_status"] == "reserved"]
        if not pending:
            return
        c = min(pending, key=lambda c: (c["order_tick"], id_key(c["table_id"])))
        dish = self.menu[c["dish_id"]]
        for k, n in c["reserved"].items():
            self.stock[k] = self.stock.get(k, 0) - n
        items = [k for k in sorted(c["reserved"]) for _ in range(c["reserved"][k])]
        c["reserved"], c["order_status"], c["base_price"] = {}, "assigned", dish["price"]
        stove["state"], stove["cook_ticks_left"], stove["ready_ticks"] = "cooking", _ticks(dish["cook_s"]), 0
        stove["dish"] = {"order_id": c["id"], "dish_id": c["dish_id"], "base_price": c["base_price"]}
        data = self._stove_data(stove)
        data.update(items=items, base_price=c["base_price"])
        events.append(("cook_started", data))

    def _serve(self, c, events):
        pay = self.hand
        self.hand = None
        c["state"], c["order_status"] = "eating", "served"
        c["eat_ticks_left"] = self.eat_total
        enough = c["patience_ticks_left"] >= self.t["tip_min_patience_ratio"] * self.patience_total
        c["base_price"] = pay["base_price"]
        c["tip"] = math.floor(c["base_price"] * self.t["tip_rate"]) if enough else 0
        events.append(("served", {"order_id": c["id"], "table_id": c["table_id"], "dish_id": c["dish_id"],
                                  "patience_ticks_left": c["patience_ticks_left"],
                                  "base_price": c["base_price"], "tip": c["tip"]}))

    def _pay(self, c, reason, events):
        amount = c["base_price"] + c["tip"]
        self.money += amount
        self.earned += amount
        self.shift_earned += amount
        if c["tip"] > 0:
            self._set_reputation(self.reputation + self.t["tip_reputation"])
        events.append(("paid", {"order_id": c["id"], "table_id": c["table_id"], "base_price": c["base_price"],
                                "tip": c["tip"], "amount": amount, "reason": reason}))
        self.customers.remove(c)

    def _leave(self, c, reason, events):
        if reason == "patience":
            self._set_reputation(self.reputation + self.t["left_reputation_delta"])
        for s in self.stoves:  # bỏ món của đơn đang nấu / ready; nguyên liệu đã dùng không hoàn lại
            if s["dish"] and s["dish"]["order_id"] == c["id"]:
                s["state"], s["dish"], s["cook_ticks_left"], s["ready_ticks"] = "idle", None, 0, 0
        if self.hand and self.hand["order_id"] == c["id"]:
            self.hand = None
        events.append(("customer_left", {"order_id": c["id"], "table_id": c["table_id"], "reason": reason,
                                         "reputation": self.reputation}))
        self.customers.remove(c)  # phần giữ thô đi cùng khách

    def _spawn(self, events):
        taken = {c["table_id"] for c in self.customers}
        free = [tb for tb in sort_by_id(self.tables) if tb["id"] not in taken]
        if not free:
            return
        avail = self._available()
        ok = [d for d in sorted(self.menu)
              if all(avail.get(k, 0) >= n for k, n in self.menu[d]["recipe"].items())]
        if not ok:
            events.append(("no_dish", {}))
            return
        dish_id = ok[self.rng.get("customer_dish").randrange(len(ok))]
        cid = self.ids.new("C")
        self.customers.append({
            "id": cid, "table_id": free[0]["id"], "dish_id": dish_id, "order_tick": self.phase_tick,
            "state": "waiting", "patience_ticks_left": self.patience_total, "eat_ticks_left": 0,
            "order_status": "reserved", "reserved": dict(self.menu[dish_id]["recipe"]),
            "base_price": 0, "tip": 0})
        events.append(("customer_arrived", {"order_id": cid, "table_id": free[0]["id"], "dish_id": dish_id}))

    def _move(self, inp):
        speed = self.t["walk_speed"]
        mx, mz = inp.move
        self.vel = ramp_velocity(self, (mx * speed, mz * speed), int(self.t.get("ramp_max_ticks", 6)))
        b = self.t["bounds"]
        for i, axis in enumerate(("x", "z")):
            self.pos[i] += self.vel[i] / TICK
            lo, hi = b[axis]
            if self.pos[i] <= lo:
                self.pos[i], self.vel[i] = lo, max(0.0, self.vel[i])
            elif self.pos[i] >= hi:
                self.pos[i], self.vel[i] = hi, min(0.0, self.vel[i])
