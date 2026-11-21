"""Buổi tối — Mở Quán (`quan`). Luật theo PRD-0 mục F (Quán) và mục E (event).

Nhìn từ trên xuống, vị trí `[x, z]`. Mỗi bước (tick k -> k+1), đúng thứ tự PRD-0:
  1. đồng hồ; giảm timer nấu / ăn / kiên nhẫn; chỉ tăng `ready_ticks` cho món đã ready từ đầu bước
  2. bếp theo id: nấu xong -> ready (`dish_ready`)
  3. di chuyển, rồi tối đa MỘT `interact` (khoảng cách, bếp trước bàn, id):
       bếp idle nhận đơn reserved cũ nhất (`cook_started`) · bếp ready -> tay trống (`dish_picked`)
       · bàn nhận đúng order (`served`)
  4. theo id bàn: ăn xong -> `paid`; hết kiên nhẫn -> `customer_left`; hết ca -> dọn bàn (`closing`) + `quan_end`
  5. còn giờ: khách mới theo lịch (`customer_arrived` / `no_dish`)
v1.2 (độ tươi): kho là mảng CÁ THỂ {id,kind,u}; giữ chỗ theo id (tươi nhất, hòa id nhỏ); sau bước 1 kho thô hao
1 đơn vị/tick (kể cả hàng đang giữ), phát `spoiled` theo id rồi xử lý đơn có phần giữ vừa ươn (nhả hết, thử giữ lại
đúng một lần theo order_tick rồi id bàn); giá chốt khi nấu = floor(giá × TB fresh / 100).
Số liệu chỉ đọc từ `tuning` (game.contract.json); ngẫu nhiên chỉ qua `Streams`.
"""

import math

from .. import freshness
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

    def __init__(self, tuning, scenario, streams, ids, inventory=None, allowed_dishes=None,
                 money=0, earned=0, reputation=None):
        """`allowed_dishes`: tập id món của kế hoạch Ngày (chế độ day, TICKET-02 mục 4.5); None = cả menu.
        `money`, `earned`, `reputation`: trạng thái giữ qua Ngày (chế độ day); mặc định như quán chạy riêng."""
        t = tuning["quan"]
        self.t = t
        self.menu = tuning["menu"]
        self.rng = streams
        self.ids = ids
        self.patience_total = _ticks(t["patience_s"])
        self.eat_total = _ticks(t["eat_s"])
        self.interval_ticks = _ticks(t["customer_interval_s"])
        # mở rộng `burn` (TICKET-02 mục 3): burn_s hữu hạn -> món ready quá lâu bị cháy; null = lõi, không cháy
        self.burn_ticks = None if t.get("burn_s") is None else _ticks(t["burn_s"])
        self.random_customers = scenario.get("random_customers", True)
        p = scenario.get("player", {})
        self.pos = [float(c) for c in p.get("pos", t["start_pos"])]
        self.vel = [float(c) for c in p.get("vel", [0.0, 0.0])]
        self._tgt = None
        self._ramp_left = 0
        self.rates = freshness.Rates(tuning["freshness"])
        # kho: --inventory (cá thể nội bộ) HOẶC scenario.stock (mảng ngoài); cả hai -> headless đã báo mã 2
        src = inventory if inventory is not None else [freshness.from_external(d) for d in scenario.get("stock", [])]
        self.stock = [dict(i) for i in src]
        self.time_left_ticks = scenario.get("time_left_ticks", _ticks(t["duration_s"]))
        self.reputation = scenario.get("reputation", t["reputation_initial"] if reputation is None else reputation)
        self.allowed = None if allowed_dishes is None else set(allowed_dishes)
        self.phase_tick = 0
        self.stoves = [self._new_stove(s) for s in self._merge(t["stoves"], scenario.get("stoves", []))]
        self.tables = self._merge(t["tables"], scenario.get("tables", []))
        self.customers = [self._new_customer(c) for c in scenario.get("customers", [])]
        self.hand = self._payload(scenario.get("hand"))
        for c in self.customers:
            ids.reserve(c["id"])
        self._auto_reserve_fixtures()
        check_quan_state(self, tuning)
        self.money = money
        self.earned = earned
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
        # mảng id cá thể; None = chưa khai, đơn `reserved` sẽ được cấp tự động (order_tick rồi id bàn)
        reserved = sorted(c["reserved"], key=id_key) if "reserved" in c else ([] if status != "reserved" else None)
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
            "stock": freshness.external_sorted(self.stock),
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
        # 1b. độ tươi: hao kho thô (kể cả hàng đang giữ), spoiled theo id, rồi xử lý giữ chỗ bị ươn
        self._freshness(events)
        # 2. bếp theo id
        for s in sort_by_id(self.stoves):
            if s["state"] == "cooking" and s["cook_ticks_left"] == 0:
                s["state"], s["ready_ticks"] = "ready", 0
                events.append(("dish_ready", self._stove_data(s)))
            elif (self.burn_ticks is not None and s["state"] == "ready" and s["ready_ticks"] > self.burn_ticks):
                self._burn(s, events)
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

    def _held_ids(self, skip=None):
        """Id cá thể đang được giữ cho các đơn (trừ đơn `skip`)."""
        return {i for c in self.customers if c is not skip for i in (c["reserved"] or [])}

    def _pick(self, dish_id, skip=None):
        """Id cá thể chưa ươn, chưa bị giữ, đủ công thức (tươi nhất, hòa id nhỏ) hoặc None."""
        got = freshness.pick_recipe(self.stock, self.menu[dish_id]["recipe"], self.rates, self._held_ids(skip))
        return None if got is None else sorted(got, key=id_key)

    def _auto_reserve_fixtures(self):
        """Đơn `reserved` của scenario chưa khai `reserved`: cấp theo order_tick rồi id bàn (PRD v1.2 mục scenario)."""
        for c in sorted((c for c in self.customers if c["reserved"] is None),
                        key=lambda c: (c["order_tick"], id_key(c["table_id"]))):
            got = self._pick(c["dish_id"], skip=c)
            if got is None:
                raise BadInput(f"customers.{c['id']}: không đủ cá thể chưa ươn để giữ cho {c['dish_id']}")
            c["reserved"] = got

    def _freshness(self, events):
        by_id = {i["id"]: i for i in self.stock}
        spoiled = freshness.decay(self.stock, self.rates.quan_per_tick, self.rates)
        for iid in spoiled:
            events.append(("spoiled", {"item_id": iid, "kind": by_id[iid]["kind"], "location": "stock"}))
        hit = set(spoiled)
        affected = sorted((c for c in self.customers if hit & set(c["reserved"])),
                          key=lambda c: (c["order_tick"], id_key(c["table_id"])))
        for c in affected:
            self._rereserve(c)

    def _rereserve(self, c):
        """Nhả TOÀN BỘ phần giữ của đơn và thử giữ lại đúng một lần. Không đủ -> unfulfillable. Trả True nếu giữ được."""
        c["reserved"] = []
        got = self._pick(c["dish_id"], skip=c)
        if got is None:
            c["order_status"] = "unfulfillable"
            return False
        c["reserved"] = got
        return True

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
        used = [i for i in self.stock if i["id"] in set(c["reserved"])]
        self.stock = [i for i in self.stock if i["id"] not in set(c["reserved"])]
        items = [freshness.external(i) for i in sorted(used, key=lambda i: (i["kind"], id_key(i["id"])))]
        # giá chốt theo độ tươi của đúng các cá thể đã dùng
        c["reserved"], c["order_status"], c["base_price"] = [], "assigned", freshness.price(dish["price"], used)
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

    def _burn(self, stove, events):
        """Món ready quá `burn_s`: bỏ món, nguyên liệu mất, bếp rảnh ngay; thử giữ lại ngay cho đơn."""
        order_id, dish_id = stove["dish"]["order_id"], stove["dish"]["dish_id"]
        stove["state"], stove["dish"], stove["cook_ticks_left"], stove["ready_ticks"] = "idle", None, 0, 0
        c = self._customer(order_id)
        c["base_price"] = 0
        got = self._pick(dish_id, skip=c)  # nguyên liệu đã nấu mất; thử giữ lại cho đơn từ kho còn lại
        if got is None:
            c["reserved"], c["order_status"] = [], "unfulfillable"
        else:
            c["reserved"], c["order_status"] = got, "reserved"
        events.append(("dish_burnt", {"stove_id": stove["id"], "order_id": order_id, "dish_id": dish_id,
                                      "order_status": c["order_status"]}))

    def _spawn(self, events):
        taken = {c["table_id"] for c in self.customers}
        free = [tb for tb in sort_by_id(self.tables) if tb["id"] not in taken]
        if not free:
            return
        ok = [d for d in sorted(self.menu)
              if (self.allowed is None or d in self.allowed) and self._pick(d) is not None]
        if not ok:
            events.append(("no_dish", {}))
            return
        dish_id = ok[self.rng.get("customer_dish").randrange(len(ok))]
        cid = self.ids.new("C")
        self.customers.append({
            "id": cid, "table_id": free[0]["id"], "dish_id": dish_id, "order_tick": self.phase_tick,
            "state": "waiting", "patience_ticks_left": self.patience_total, "eat_ticks_left": 0,
            "order_status": "reserved", "reserved": self._pick(dish_id),
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
