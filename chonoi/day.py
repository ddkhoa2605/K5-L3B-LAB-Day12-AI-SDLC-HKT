"""Chế độ `day` (Test Contract v1.1, TICKET-02 mục 2, 4): một vòng ngày
DayIntro -> gather -> quan -> Shop -> (Ngày kế | tổng kết), tối đa 5 Ngày.

Không có luật mới ở đây: `DaySession` chỉ ghép `GatherSim`, `QuanSim` và Shop, giữ trạng thái xuyên Ngày
(money, earned, uy tín, cấp nâng cấp) và chuyển pha đúng thứ tự mục 4.5. Số liệu đọc từ `game.contract.json`
(`day_plan`, `shop`). Giao diện (DayIntro, menu, HUD) chỉ ĐỌC snapshot.

Thứ tự một bước ngoài: pause -> (gameplay của pha hiện tại) -> chuyển pha nếu pha kết thúc.
Chuyển pha: sau `gather_end` dựng quán và phát `phase_start(quan)` CÙNG tick (kể cả khi ngất); sau `quan_end`
dựng Shop và phát `phase_start(shop)` cùng tick; pha mới chỉ chạy gameplay từ bước sau.
"""

import copy
import json
import math

from . import freshness
from .errors import BadInput
from .ids import IdAllocator
from .inputs import InputPlayer
from .jsonl import JsonlWriter
from .pause import PauseGate
from .rng import Streams
from .scenario import GATHER_KEYS, QUAN_KEYS, _validate_gather, _validate_quan, day_plan_ingredients
from .sim.gather import GatherSim
from .sim.quan import QuanSim, announce_events, plan_reservations

DAY_KEYS = {"money", "earned", "reputation", "upgrades", "day_plan"}
MAX_DAYS = 5


# --- scenario -------------------------------------------------------------------------------------
def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _nonneg_int(name, v):
    if isinstance(v, bool) or not isinstance(v, int) or v < 0:
        raise BadInput(f"{name} phải là số nguyên không âm")


def preset_plan(tuning):
    """day_plan của preset -> {số Ngày: {"dishes", "ingredients"}}."""
    plan = {}
    for p in tuning["day_plan"]:
        plan[p["day"]] = {"dishes": dict(p["dishes"]), "ingredients": dict(p["ingredients"])}
    return plan


def load_day_scenario(path, tuning):
    """Đọc scenario cho `--mode day`. Trả {"day": {...đã chuẩn hóa}, "gather": {...}, "quan": {...}}."""
    data = {}
    if path is not None:
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, ValueError) as e:
            raise BadInput(f"không đọc được scenario {path}: {e}")
        if not isinstance(data, dict) or not set(data) <= {"day", "gather", "quan"}:
            raise BadInput("scenario của day chỉ được có khối 'day', 'gather', 'quan'")
    out = {"gather": _block("gather", data.get("gather", {}), tuning, GATHER_KEYS, _validate_gather),
           "quan": _block("quan", data.get("quan", {}), tuning, QUAN_KEYS, _validate_quan)}
    if {"stock", "reputation"} & set(out["quan"]):
        raise BadInput("khi chạy day cấm quan.stock và quan.reputation (dùng gather.hold và day.reputation)")
    out["day"] = _day_block(data.get("day", {}), tuning)
    return out


def _block(mode, block, tuning, allowed, validate):
    if not isinstance(block, dict):
        raise BadInput(f"khối {mode} phải là object")
    extra = set(block) - allowed
    if extra:
        raise BadInput(f"trường lạ/chưa hỗ trợ trong {mode}: {sorted(extra)}")
    if "time_left_ticks" in block:
        dur = int(round(tuning[mode]["duration_s"] * 60))
        t = block["time_left_ticks"]
        if isinstance(t, bool) or not isinstance(t, int) or not (1 <= t <= dur):
            raise BadInput(f"time_left_ticks phải là số nguyên trong [1, {dur}]")
    validate(block, tuning)
    return block


def _day_block(d, tuning):
    if not isinstance(d, dict) or set(d) - DAY_KEYS:
        raise BadInput(f"khối day chỉ có các khóa {sorted(DAY_KEYS)}")
    q, shop = tuning["quan"], tuning["shop"]
    out = {}
    if ("money" in d) != ("earned" in d):
        raise BadInput("day.money và day.earned phải khai cùng nhau")
    if "money" in d:
        _nonneg_int("day.money", d["money"])
        _nonneg_int("day.earned", d["earned"])
        if d["money"] > d["earned"]:
            raise BadInput("day.money không được lớn hơn day.earned")
        out["money"], out["earned"] = d["money"], d["earned"]
    if "reputation" in d:
        if not (_num(d["reputation"]) and q["reputation_min"] <= d["reputation"] <= q["reputation_max"]):
            raise BadInput("day.reputation phải trong [reputation_min, reputation_max]")
        out["reputation"] = d["reputation"]
    ups = d.get("upgrades", {})
    if not isinstance(ups, dict):
        raise BadInput("day.upgrades phải là object {nâng cấp: cấp}")
    for k, lv in ups.items():
        if k not in shop["upgrades"]:
            raise BadInput(f"day.upgrades: nâng cấp lạ {k!r}")
        if isinstance(lv, bool) or not isinstance(lv, int) or not (0 <= lv <= len(shop["upgrades"][k])):
            raise BadInput(f"day.upgrades.{k}: cấp phải là số nguyên trong [0, {len(shop['upgrades'][k])}]")
    out["upgrades"] = dict(ups)
    plan = preset_plan(tuning)
    seen = set()
    for p in d.get("day_plan", []):
        if not isinstance(p, dict) or not set(p) <= {"day", "dishes", "ingredients"} or "dishes" not in p:
            raise BadInput("day.day_plan[]: cần {day, dishes[, ingredients]}")
        n = p.get("day")
        if isinstance(n, bool) or not isinstance(n, int) or not (1 <= n <= MAX_DAYS) or n in seen:
            raise BadInput("day.day_plan[].day phải là số nguyên 1..5, không trùng")
        seen.add(n)
        if not isinstance(p["dishes"], dict) or not p["dishes"]:
            raise BadInput("day.day_plan[].dishes phải là object không rỗng")
        ing = day_plan_ingredients(p["dishes"], tuning["menu"])
        if "ingredients" in p and p["ingredients"] != ing:
            raise BadInput(f"day.day_plan[{n}].ingredients không khớp công thức × số suất: cần {ing}")
        plan[n] = {"dishes": dict(p["dishes"]), "ingredients": ing}
    out["day_plan"] = plan
    return out


# --- phiên chơi ------------------------------------------------------------------------------------
class _SimView:
    """Mặt nạ tương thích với `chonoi.live` (cần `.sim.done/.reason`)."""

    def __init__(self, s):
        self._s = s

    @property
    def done(self):
        return self._s.done

    @property
    def reason(self):
        return self._s.reason

    @done.setter
    def done(self, v):
        self._s.done = v

    @reason.setter
    def reason(self, v):
        self._s.reason = v


class DaySession:
    mode = "day"

    def __init__(self, tuning, scenario, seed, days=1):
        if isinstance(days, bool) or not isinstance(days, int) or not (1 <= days <= MAX_DAYS):
            raise BadInput(f"--days phải là số nguyên trong [1, {MAX_DAYS}]")
        self.tuning = tuning
        self.scn = scenario
        self.days = days
        self.rng = Streams(seed)
        d = scenario["day"]
        self.plans = d["day_plan"]
        self.money = d.get("money", 0)
        self.earned = d.get("earned", 0)
        self.reputation = d.get("reputation", tuning["quan"]["reputation_initial"])
        self.upgrades = {k: 0 for k in tuning["shop"]["upgrades"]}
        self.upgrades.update(d["upgrades"])
        self.active = dict(self.upgrades)  # cấp khai ở scenario có hiệu lực ngay Ngày 1
        self.day = 1
        self.days_completed = 0
        self.tick = 0
        self.sim_tick = 0
        self.phase = "gather"
        self.phase_tick = 0
        self.gate = PauseGate()
        self.done = False
        self.reason = None
        self.sim = None
        self.shop_left = 0
        self.shop_stock = []
        self.sim_view = _SimView(self)
        self.res_day = []  # Khách đặt trước của Ngày hiện tại, công bố ở buổi sáng
        # một allocator cá thể `I` dùng chung xuyên pha và Ngày (không tái dùng id đã cấp)
        self.item_ids = IdAllocator()
        self.stats = {"day": self._new_day_stats(), "sold": {}, "served": 0, "left": 0, "tips": 0}
        self.initial = []
        self._begin_day(0, self.initial)

    # --- thống kê cho giao diện (DayResult, Summary); không nằm trong snapshot/JSONL -------------
    def _new_day_stats(self):
        return {"served": 0, "left": 0, "tips": 0, "earned": 0, "reputation_start": self.reputation}

    def _tally(self, rows):
        d, t = self.stats["day"], self.stats
        for r in rows:
            n, x = r["name"], r["data"]
            if n == "served":
                d["served"] += 1
                t["served"] += 1
                t["sold"][x["dish_id"]] = t["sold"].get(x["dish_id"], 0) + 1
            elif n == "customer_left":
                d["left"] += 1
                t["left"] += 1
            elif n == "paid":
                d["tips"] += x["tip"]
                d["earned"] += x["amount"]
                t["tips"] += x["tip"]

    # --- tiện ích -------------------------------------------------------------------------------
    def _row(self, tick, name, data, phase=None):
        return {"type": "event", "tick": tick, "phase": phase or self.phase, "day": self.day, "name": name,
                "data": data}

    def _plan(self):
        return self.plans[self.day]

    def _cur(self):
        if self.phase == "quan" and self.sim is not None:
            return self.sim.money, self.sim.earned, self.sim.reputation
        return self.money, self.earned, self.reputation

    def _gather_tuning(self):
        t = copy.deepcopy(self.tuning)
        g, shop = t["gather"], t["shop"]["upgrades"]
        for kind, key in (("oxygen", "oxygen_max_s"), ("hp", "hp_max")):
            lv = self.active.get(kind, 0)
            if lv > 0:
                g[key] = shop[kind][lv - 1][key]
        return t

    # --- chuyển pha -------------------------------------------------------------------------------
    def _begin_day(self, tick, rows):
        plan = self._plan()
        self.stats["day"] = self._new_day_stats()
        self.phase, self.phase_tick = "gather", 0
        rows.append(self._row(tick, "day_start", {}))
        rows.append(self._row(tick, "day_plan", {"dishes": plan["dishes"], "ingredients": plan["ingredients"]}))
        scn = copy.deepcopy(self.scn["gather"])
        if self.day > 1:  # Ngày 1 giữ id của mẫu; Ngày kế cấp id mới theo thứ tự mảng, kind/fresh ban đầu
            for d in scn.get("hold", []):
                d["id"] = self.item_ids.new("I")
        self.sim = GatherSim(self._gather_tuning(), scn, self.rng, IdAllocator(), item_ids=self.item_ids)
        rows.append(self._row(tick, "phase_start", {}))
        # mở rộng `reservations`: công bố 2 đơn R1, R2 SAU phase_start(gather), theo id
        self.res_day = plan_reservations(self.tuning, self.scn["quan"], self.rng, set(plan["dishes"]))
        for name, data in announce_events(self.res_day):
            rows.append(self._row(tick, name, data))

    def _to_quan(self, tick, rows):
        inv = self.sim.inventory_items()  # ngất -> kho rỗng
        self.phase, self.phase_tick = "quan", 0
        self.sim = QuanSim(self.tuning, copy.deepcopy(self.scn["quan"]), self.rng, IdAllocator(), inventory=inv,
                           allowed_dishes=set(self._plan()["dishes"]), money=self.money, earned=self.earned,
                           reputation=self.reputation, reservations=self.res_day)
        rows.append(self._row(tick, "phase_start", {}))

    def _to_shop(self, tick, rows):
        self.money, self.earned, self.reputation = self.sim.money, self.sim.earned, self.sim.reputation
        self.shop_stock = freshness.external_sorted(self.sim.stock)  # hàng thô ở Shop không hao tươi
        self.shop_left = int(self.tuning["shop"]["max_ticks"])
        self.phase, self.phase_tick = "shop", 0
        self.sim = None
        rows.append(self._row(tick, "phase_start", {}))

    def _shop_step(self, inp, tick, rows):
        self.shop_left = max(0, self.shop_left - 1)
        if inp.buy:
            self._buy(inp.buy, tick, rows)
        if inp.pressed("shop_done"):
            self._end_shop("done", tick, rows)
        elif self.shop_left <= 0:
            self._end_shop("time", tick, rows)

    def _buy(self, action, tick, rows):
        levels = self.tuning["shop"]["upgrades"].get(action)
        if levels is None:
            rows.append(self._row(tick, "buy_failed", {"action": action, "reason": "unknown"}))
            return
        cur = self.upgrades[action]
        if cur >= len(levels):
            rows.append(self._row(tick, "buy_failed", {"action": action, "reason": "max_level"}))
            return
        up = levels[cur]
        if self.money < up["price"]:
            rows.append(self._row(tick, "buy_failed", {"action": action, "reason": "funds"}))
            return
        self.money -= up["price"]  # trừ vào money, giữ earned và điểm
        self.upgrades[action] = up["level"]
        rows.append(self._row(tick, "bought", {"upgrade": action, "level": up["level"], "price": up["price"],
                                               "money": self.money}))

    def _end_shop(self, reason, tick, rows):
        rows.append(self._row(tick, "shop_end", {"reason": reason}))
        self.days_completed += 1
        if self.day >= self.days:
            self.done, self.reason = True, "days_complete"
            return
        self.day += 1
        self.active = dict(self.upgrades)  # cấp đã mua chỉ có hiệu lực từ Ngày kế
        self._begin_day(tick, rows)

    # --- vòng tick ---------------------------------------------------------------------------------
    def step(self, inp):
        """Một bước ngoài (tick k -> k+1); trả các dòng event (tick = k + 1)."""
        tick = self.tick + 1
        rows = []
        name, run = self.gate.handle(inp)
        if name:
            rows.append(self._row(tick, name, {}))
        if run:
            self.sim_tick += 1
            self.phase_tick += 1
            if self.phase == "shop":
                self._shop_step(inp, tick, rows)
            else:
                for n, data in self.sim.step(inp):
                    rows.append(self._row(tick, n, data))
                if self.sim.done:
                    (self._to_quan if self.phase == "gather" else self._to_shop)(tick, rows)
        self.tick = tick
        self._tally(rows)
        return rows

    def snapshot(self) -> dict:
        money, earned, rep = self._cur()
        mult = self.tuning["score"]["reputation_multiplier"]
        left = self.shop_left if self.phase == "shop" else self.sim.time_left_ticks
        state = "finished" if self.done else ("paused" if self.gate.paused else "playing")
        s = {"type": "snapshot", "tick": self.tick, "sim_tick": self.sim_tick, "mode": "day", "phase": self.phase,
             "phase_tick": self.phase_tick, "state": state, "time_left_ticks": left, "money": money,
             "earned": earned, "reputation": rep, "score": earned + mult * math.floor(rep),
             "day": self.day, "day_plan": {"dishes": self._plan()["dishes"],
                                           "ingredients": self._plan()["ingredients"]},
             "upgrades": dict(self.upgrades), "active_upgrades": dict(self.active)}
        s.update({"stock": self.shop_stock} if self.phase == "shop" else self.sim.snapshot())
        if self.phase == "gather" and self.tuning.get("reservations"):
            s["reservations"] = [{k: r[k] for k in ("id", "table_id", "dish_id", "arrival_tick", "state")}
                                for r in self.res_day]
        return s

    def end_row(self) -> dict:
        money, earned, rep = self._cur()
        mult = self.tuning["score"]["reputation_multiplier"]
        return {"type": "end", "ticks": self.tick, "sim_tick": self.sim_tick, "mode": "day",
                "state": "finished" if self.done else "playing",
                "reason": self.reason if self.done else "tick_limit", "money": money, "earned": earned,
                "reputation": rep, "score": earned + mult * math.floor(rep),
                "days_completed": self.days_completed}

    def write_inventory_if_done(self, _path):
        """Tương thích `chonoi.live`: chế độ day không dùng file kho."""


def run_day(tuning, scenario, seed, days, frames, ticks, out_path, snapshot_every):
    """Chạy `--mode day`. Gom toàn bộ dòng rồi mới ghi: lỗi mâu thuẫn lúc dựng pha (mã 2) không để lại file dở."""
    sess = DaySession(tuning, scenario, seed, days)
    player = InputPlayer(frames)
    rows = [sess.snapshot()] + sess.initial
    last = 0
    while sess.tick < ticks and not sess.done:
        rows.extend(sess.step(player.advance(sess.tick)))
        if sess.tick % snapshot_every == 0 or sess.done:
            rows.append(sess.snapshot())
            last = sess.tick
    if last != sess.tick:
        rows.append(sess.snapshot())
    rows.append(sess.end_row())
    w = JsonlWriter(out_path)
    try:
        for r in rows:
            w.write(r)
    finally:
        w.close()
    return sess
