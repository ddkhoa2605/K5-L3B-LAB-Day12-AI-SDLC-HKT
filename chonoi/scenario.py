"""Nạp và kiểm scenario (Contract D). Trả về dict của đúng khối theo mode.

KHUNG: kiểm cú pháp, id trùng, bộ đếm âm, khoang vượt sức chứa, trường lạ.
TODO(nhóm): bổ sung kiểm mâu thuẫn mức luật mà nhóm cần (khách giữ chỗ quá kho, đơn assigned
phải có đúng một món, khách eating thiếu giá/tip...) — xem PRD-0 mục D và 'Mâu thuẫn -> mã 2'.
"""

import json

from .errors import BadInput
from .inventory import KINDS_P1, validate_items

GATHER_KEYS = {"player", "hold", "nodes", "fish", "random_fish", "time_left_ticks", "monsters"}
GATHER_PLAYER_KEYS = {"pos", "vel", "heading_deg", "hp", "oxygen_ticks", "zero_oxy_ticks",
                      "invuln_ticks", "catch_cd_ticks", "attack_cd_ticks"}
NODE_KINDS = ("bong_dien_dien", "bong_sung", "keo_neo")
FISH_KINDS = ("ca_linh", "ca_loc", "ca_keo")
MONSTER_KINDS = ("ca_sau",)
MONSTER_STATES = ("patrol", "chase", "recoil", "stunned")
MONSTER_KEYS = {"id", "kind", "pos", "waypoints", "target_idx", "state", "state_ticks_left", "recoil_dir"}
QUAN_PLAYER_KEYS = {"pos", "vel"}
STOVE_KEYS = {"id", "pos", "state", "dish", "cook_ticks_left", "ready_ticks"}
TABLE_KEYS = {"id", "pos"}
STOVE_STATES = ("idle", "cooking", "ready")
CUSTOMER_STATES = ("waiting", "eating")
ORDER_STATUSES = ("reserved", "assigned", "unfulfillable", "served")
CUSTOMER_KEYS = {"id", "table_id", "dish_id", "order_tick", "state", "patience_ticks_left", "eat_ticks_left",
                 "order_status", "reserved", "base_price", "tip"}
QUAN_KEYS = {"player", "stock", "hand", "stoves", "tables", "customers", "random_customers", "reservations",
             "random_reservations",
             "reputation", "time_left_ticks"}



def _check_ids(name, arr):
    if not isinstance(arr, list):
        raise BadInput(f"{name} phải là mảng")
    seen = set()
    for e in arr:
        if not isinstance(e, dict) or not isinstance(e.get("id"), str) or not e["id"]:
            raise BadInput(f"{name}: mỗi phần tử cần id (chuỗi khác rỗng)")
        if e["id"] in seen:
            raise BadInput(f"{name}: id trùng {e['id']}")
        seen.add(e["id"])


def load_scenario(path, mode: str, tuning: dict) -> dict:
    if path is None:
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        raise BadInput(f"không đọc được scenario {path}: {e}")
    if not isinstance(data, dict) or not set(data) <= {"gather", "quan"}:
        raise BadInput("scenario chỉ được có khối 'gather' hoặc 'quan'")
    if set(data) - {mode}:
        raise BadInput(f"khối sai mode: chạy --mode {mode} chỉ nhận khối '{mode}'")
    block = data.get(mode, {})
    if not isinstance(block, dict):
        raise BadInput(f"khối {mode} phải là object")
    allowed = GATHER_KEYS if mode == "gather" else QUAN_KEYS
    extra = set(block) - allowed
    if extra:
        raise BadInput(f"trường lạ/chưa hỗ trợ trong {mode}: {sorted(extra)}")
    dur = int(round(tuning[mode]["duration_s"] * 60))
    if "time_left_ticks" in block:
        t = block["time_left_ticks"]
        if isinstance(t, bool) or not isinstance(t, int) or not (1 <= t <= dur):
            raise BadInput(f"time_left_ticks phải là số nguyên trong [1, {dur}]")
    if mode == "gather":
        _validate_gather(block, tuning)
    else:
        _validate_quan(block, tuning)
    return block


def _num(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _nonneg_int(name, v):
    if isinstance(v, bool) or not isinstance(v, int) or v < 0:
        raise BadInput(f"{name} phải là số nguyên không âm")


def _pos(name, pos, bounds, axes=("x", "d")):
    if not (isinstance(pos, list) and len(pos) == 2 and all(_num(c) for c in pos)):
        raise BadInput(f"{name} phải là [{axes[0]}, {axes[1]}]")
    for c, axis in zip(pos, axes):
        lo, hi = bounds[axis]
        if not (lo <= c <= hi):
            raise BadInput(f"{name} nằm ngoài vùng nước ({axis} ∈ [{lo}, {hi}])")


def _validate_gather(b, tuning):
    g = tuning["gather"]
    bounds = g["bounds"]
    for arr in ("nodes", "fish", "monsters"):
        if arr in b:
            _check_ids(arr, b[arr])
    if "random_fish" in b and not isinstance(b["random_fish"], bool):
        raise BadInput("random_fish phải là boolean")
    if "hold" in b:
        h = validate_items(b["hold"], name="gather.hold")
        if len(h) > g["hold_capacity"]:
            raise BadInput("hold vượt sức chứa")
    p = b.get("player", {})
    if not isinstance(p, dict):
        raise BadInput("player phải là object")
    extra = set(p) - GATHER_PLAYER_KEYS
    if extra:
        raise BadInput(f"trường lạ/chưa hỗ trợ trong gather.player: {sorted(extra)}")
    if "pos" in p:
        _pos("player.pos", p["pos"], bounds)
    if "vel" in p and not (isinstance(p["vel"], list) and len(p["vel"]) == 2 and all(_num(c) for c in p["vel"])):
        raise BadInput("player.vel phải là [x, d]")
    if "heading_deg" in p and not _num(p["heading_deg"]):
        raise BadInput("player.heading_deg phải là số")
    for key in ("invuln_ticks", "catch_cd_ticks", "zero_oxy_ticks", "oxygen_ticks", "hp"):
        if key in p:
            _nonneg_int(f"player.{key}", p[key])
    omax = int(round(g["oxygen_max_s"] * 60))
    if "oxygen_ticks" in p and p["oxygen_ticks"] > omax:
        raise BadInput("player.oxygen_ticks vượt oxy tối đa")
    if "hp" in p and not (1 <= p["hp"] <= g["hp_max"]):
        raise BadInput("player.hp phải trong [1, hp_max]")
    if "zero_oxy_ticks" in p:
        pos = p.get("pos", g["start_pos"])
        oxy = p.get("oxygen_ticks", omax)
        if p["zero_oxy_ticks"] > 59:
            raise BadInput("player.zero_oxy_ticks phải trong [0, 59]")
        if p["zero_oxy_ticks"] > 0 and not (oxy == 0 and pos[1] > g["surface_depth"]):
            raise BadInput("player.zero_oxy_ticks > 0 chỉ khi oxy = 0 và đang dưới nước")
    for n in b.get("nodes", []):
        if n.get("kind") not in NODE_KINDS:
            raise BadInput(f"nodes.{n['id']}: kind phải là một trong {NODE_KINDS}")
        _pos(f"nodes.{n['id']}.pos", n.get("pos"), bounds)
        if n["pos"][1] != 0:
            raise BadInput(f"nodes.{n['id']}: nút hái nằm ở mặt nước (d = 0)")
        if "regrow_ticks" in n:
            _nonneg_int(f"nodes.{n['id']}.regrow_ticks", n["regrow_ticks"])
    for f in b.get("fish", []):
        if f.get("kind") not in FISH_KINDS:
            raise BadInput(f"fish.{f['id']}: kind phải là một trong {FISH_KINDS}")
        _pos(f"fish.{f['id']}.pos", f.get("pos"), bounds)
        if f["pos"][1] <= g["surface_depth"]:
            raise BadInput(f"fish.{f['id']}: đàn cá phải ở dưới nước")
        if "heading_deg" in f and not _num(f["heading_deg"]):
            raise BadInput(f"fish.{f['id']}.heading_deg phải là số")
        if "age_ticks" in f:
            _nonneg_int(f"fish.{f['id']}.age_ticks", f["age_ticks"])
    for m in b.get("monsters", []):
        extra = set(m) - MONSTER_KEYS
        if extra:
            raise BadInput(f"trường lạ/chưa hỗ trợ trong monsters.{m['id']}: {sorted(extra)}")
        if m.get("kind") not in MONSTER_KINDS:
            raise BadInput(f"monsters.{m['id']}: kind phải là một trong {MONSTER_KINDS}")
        _pos(f"monsters.{m['id']}.pos", m.get("pos"), bounds)
        if m["pos"][1] < 10.0:
            raise BadInput(f"monsters.{m['id']}: Cá Sấu phải ở độ sâu d >= 10")
        if "waypoints" in m:
            if not isinstance(m["waypoints"], list) or len(m["waypoints"]) < 2:
                raise BadInput(f"monsters.{m['id']}.waypoints phải là mảng >= 2 điểm")
            for idx, wp in enumerate(m["waypoints"]):
                _pos(f"monsters.{m['id']}.waypoints[{idx}]", wp, bounds)
                if wp[1] < 10.0:
                    raise BadInput(f"monsters.{m['id']}.waypoints[{idx}]: waypoint phải ở d >= 10")
        if "target_idx" in m:
            _nonneg_int(f"monsters.{m['id']}.target_idx", m["target_idx"])
            if "waypoints" in m and m["target_idx"] >= len(m["waypoints"]):
                raise BadInput(f"monsters.{m['id']}.target_idx vượt số waypoint")
        if "state" in m and m["state"] not in MONSTER_STATES:
            raise BadInput(f"monsters.{m['id']}.state phải thuộc {MONSTER_STATES}")
        if "state_ticks_left" in m:
            _nonneg_int(f"monsters.{m['id']}.state_ticks_left", m["state_ticks_left"])
        if "recoil_dir" in m and m["recoil_dir"] is not None:
            if not (isinstance(m["recoil_dir"], list) and len(m["recoil_dir"]) == 2 and all(_num(c) for c in m["recoil_dir"])):
                raise BadInput(f"monsters.{m['id']}.recoil_dir phải là [x, d] hoặc null")


def _validate_quan(b, tuning):
    for arr in ("stoves", "tables", "customers"):
        if arr in b:
            _check_ids(arr, b[arr])
    if "stock" in b:
        validate_items(b["stock"], name="quan.stock")
    p = b.get("player", {})
    if not isinstance(p, dict) or set(p) - QUAN_PLAYER_KEYS:
        raise BadInput("quan.player chỉ có pos và vel")
    qb = tuning["quan"]["bounds"]
    if "pos" in p:
        _pos("player.pos", p["pos"], qb, axes=("x", "z"))
    if "vel" in p and not (isinstance(p["vel"], list) and len(p["vel"]) == 2 and all(_num(c) for c in p["vel"])):
        raise BadInput("player.vel phải là [x, z]")
    q = tuning["quan"]
    menu = tuning["menu"]
    _validate_reservations(b, tuning)
    if "random_customers" in b and not isinstance(b["random_customers"], bool):
        raise BadInput("random_customers phải là boolean")
    if "reputation" in b and not (_num(b["reputation"]) and q["reputation_min"] <= b["reputation"] <= q["reputation_max"]):
        raise BadInput("reputation phải là số trong [reputation_min, reputation_max]")
    for name, keys in (("stoves", STOVE_KEYS), ("tables", TABLE_KEYS)):
        known = {e["id"] for e in q[name]}
        for e in b.get(name, []):
            if e["id"] not in known:
                raise BadInput(f"{name}.{e['id']}: id không tồn tại (chỉ cập nhật bếp/bàn có sẵn)")
            if set(e) - keys:
                raise BadInput(f"trường lạ/chưa hỗ trợ trong {name}.{e['id']}: {sorted(set(e) - keys)}")
            if "pos" in e:
                _pos(f"{name}.{e['id']}.pos", e["pos"], q["bounds"], axes=("x", "z"))
    for s in b.get("stoves", []):
        if "state" in s and s["state"] not in STOVE_STATES:
            raise BadInput(f"stoves.{s['id']}.state phải thuộc {STOVE_STATES}")
        for key in ("cook_ticks_left", "ready_ticks"):
            if key in s:
                _nonneg_int(f"stoves.{s['id']}.{key}", s[key])
        if s.get("dish") is not None:
            _check_dish(f"stoves.{s['id']}.dish", s["dish"], menu)
    if b.get("hand") is not None:
        _check_dish("hand", b["hand"], menu)
    table_ids = []
    known = {t["id"] for t in q["tables"]}
    for c in b.get("customers", []):
        extra = set(c) - CUSTOMER_KEYS
        if extra:
            raise BadInput(f"trường lạ/chưa hỗ trợ trong customers.{c['id']}: {sorted(extra)}")
        if not isinstance(c.get("table_id"), str) or c["table_id"] not in known:
            raise BadInput(f"customers.{c['id']}: table_id phải là bàn có thật")
        table_ids.append(c["table_id"])
        if c.get("dish_id") not in menu:
            raise BadInput(f"customers.{c['id']}: dish_id phải là món trong menu")
        if c.get("state") == "eating" and ("base_price" not in c or "tip" not in c):
            raise BadInput(f"customers.{c['id']}: khách eating phải khai base_price và tip đã chốt")
        if c.get("state", "waiting") not in CUSTOMER_STATES:
            raise BadInput(f"customers.{c['id']}.state phải thuộc {CUSTOMER_STATES}")
        if c.get("order_status", "reserved") not in ORDER_STATUSES:
            raise BadInput(f"customers.{c['id']}.order_status phải thuộc {ORDER_STATUSES}")
        for key in ("order_tick", "patience_ticks_left", "eat_ticks_left", "base_price", "tip"):
            if key in c:
                _nonneg_int(f"customers.{c['id']}.{key}", c[key])
        if "reserved" in c:
            r = c["reserved"]
            if (not isinstance(r, list) or any(not isinstance(i, str) or not i for i in r)
                    or len(set(r)) != len(r)):
                raise BadInput(f"customers.{c['id']}.reserved phải là mảng id cá thể (chuỗi khác rỗng, không trùng)")
    if len(table_ids) != len(set(table_ids)):
        raise BadInput("hai khách cùng bàn")


RESERVATION_KEYS = {"id", "table_id", "dish_id", "arrival_tick"}


def _validate_reservations(b, tuning):
    """Scenario Khách đặt trước (mở rộng `reservations`): mảng tường minh thay toàn bộ, tối đa `count` đơn."""
    if "random_reservations" in b and not isinstance(b["random_reservations"], bool):
        raise BadInput("random_reservations phải là boolean")
    if "reservations" not in b:
        return
    cfg = tuning.get("reservations")
    if cfg is None:
        raise BadInput("quan.reservations cần bật mở rộng reservations trong manifest")
    r = b["reservations"]
    if not isinstance(r, list) or len(r) > cfg["count"]:
        raise BadInput(f"quan.reservations phải là mảng tối đa {cfg['count']} đơn")
    tables = {t["id"] for t in tuning["quan"]["tables"]}
    dur = int(round(tuning["quan"]["duration_s"] * 60))
    seen_ids, seen_tables = set(), set()
    for i, x in enumerate(r):
        if not isinstance(x, dict) or set(x) != RESERVATION_KEYS:
            raise BadInput(f"quan.reservations[{i}] phải có đúng id, table_id, dish_id, arrival_tick")
        if not isinstance(x["id"], str) or not x["id"] or x["id"] in seen_ids:
            raise BadInput(f"quan.reservations[{i}].id phải là chuỗi khác rỗng, duy nhất")
        seen_ids.add(x["id"])
        if x["table_id"] not in tables or x["table_id"] in seen_tables:
            raise BadInput(f"quan.reservations[{i}].table_id phải là bàn có thật, mỗi đơn một bàn khác nhau")
        seen_tables.add(x["table_id"])
        if x["dish_id"] not in tuning["menu"]:
            raise BadInput(f"quan.reservations[{i}].dish_id phải là món trong menu")
        t = x["arrival_tick"]
        if isinstance(t, bool) or not isinstance(t, int) or not (1 <= t < dur):
            raise BadInput(f"quan.reservations[{i}].arrival_tick phải là số nguyên dương nhỏ hơn thời lượng ca ({dur})")


def _check_dish(name, d, menu):
    if not isinstance(d, dict) or set(d) - {"order_id", "dish_id", "base_price"}:
        raise BadInput(f"{name} phải là {{order_id, dish_id, base_price}}")
    if not isinstance(d.get("order_id"), str) or d.get("dish_id") not in menu:
        raise BadInput(f"{name}: order_id (chuỗi) và dish_id (món trong menu) là bắt buộc")
    if "base_price" in d:
        _nonneg_int(f"{name}.base_price", d["base_price"])


def check_quan_state(sim, tuning):
    """Kiểm mâu thuẫn mức luật (PRD-0 mục D) trên trạng thái Quán đã dựng; sai -> BadInput (mã 2).

    Gọi từ QuanSim sau khi gộp scenario/kho vào, nên thấy cả kho từ --inventory.
    """
    menu = tuning["menu"]
    stock_by_id = {i["id"]: i for i in sim.stock}
    if len(stock_by_id) != len(sim.stock):
        raise BadInput("kho quán có id cá thể trùng")
    allowed = getattr(sim, "allowed", None)
    if allowed is not None and not allowed <= set(menu):
        raise BadInput("kế hoạch Ngày có món không thuộc menu")
    for c in sim.customers:
        if allowed is not None and c["dish_id"] not in allowed:
            raise BadInput(f"customers.{c['id']}: món {c['dish_id']} không thuộc kế hoạch Ngày")
    if sim.time_left_ticks < 1:
        raise BadInput("time_left_ticks phải >= 1")
    by_id = {c["id"]: c for c in sim.customers}
    held = set()
    for c in sim.customers:
        cid = c["id"]
        dish = menu[c["dish_id"]]
        if c["patience_ticks_left"] > sim.patience_total:
            raise BadInput(f"customers.{cid}: kiên nhẫn vượt mức đầy")
        if c["eat_ticks_left"] > sim.eat_total:
            raise BadInput(f"customers.{cid}: timer ăn vượt mức đầy")
        if c["state"] == "waiting":
            if c["eat_ticks_left"] != 0 or c["order_status"] == "served":
                raise BadInput(f"customers.{cid}: khách waiting không có timer ăn / đơn served")
        else:
            if c["order_status"] != "served" or c["eat_ticks_left"] <= 0:
                raise BadInput(f"customers.{cid}: khách eating phải served và có timer ăn dương")
        for iid in c["reserved"]:
            if iid not in stock_by_id:
                raise BadInput(f"customers.{cid}: phần giữ trỏ tới cá thể không có trong kho: {iid}")
            if iid in held:
                raise BadInput(f"customers.{cid}: cá thể {iid} đã được giữ cho đơn khác")
            if stock_by_id[iid]["u"] < sim.rates.spoiled_u:
                raise BadInput(f"customers.{cid}: phần giữ trỏ tới cá thể đã ươn: {iid}")
            held.add(iid)
        if c["order_status"] == "reserved":
            need = dict(dish["recipe"])
            have = {}
            for iid in c["reserved"]:
                have[stock_by_id[iid]["kind"]] = have.get(stock_by_id[iid]["kind"], 0) + 1
            if have != need:
                raise BadInput(f"customers.{cid}: phần giữ khác công thức {c['dish_id']}")
        elif c["reserved"]:
            raise BadInput(f"customers.{cid}: đơn {c['order_status']} phải có phần giữ rỗng")
    carriers = []  # (nơi giữ, payload)
    for s in sim.stoves:
        d, st = s["dish"], s["state"]
        if st == "idle":
            if d is not None or s["cook_ticks_left"] or s["ready_ticks"]:
                raise BadInput(f"stoves.{s['id']}: bếp idle phải không có món và bộ đếm 0")
            continue
        if d is None:
            raise BadInput(f"stoves.{s['id']}: bếp {st} phải có món")
        if st == "cooking" and not (0 < s["cook_ticks_left"] <= int(round(menu[d["dish_id"]]["cook_s"] * 60))):
            raise BadInput(f"stoves.{s['id']}: bếp cooking cần timer dương không vượt thời gian nấu")
        if st == "ready" and s["cook_ticks_left"] != 0:
            raise BadInput(f"stoves.{s['id']}: bếp ready phải có cook_ticks_left = 0")
        if st == "cooking" and s["ready_ticks"]:
            raise BadInput(f"stoves.{s['id']}: ready_ticks chỉ dương khi bếp ready")
        carriers.append((f"stoves.{s['id']}", d))
    if sim.hand is not None:
        carriers.append(("hand", sim.hand))
    seen = set()
    for where, d in carriers:
        c = by_id.get(d["order_id"])
        if c is None:
            raise BadInput(f"{where}: tham chiếu khách không tồn tại: {d['order_id']}")
        if c["dish_id"] != d["dish_id"]:
            raise BadInput(f"{where}: món không khớp đơn {d['order_id']}")
        if c["order_status"] != "assigned" or c["state"] != "waiting":
            raise BadInput(f"{where}: đơn {d['order_id']} phải ở trạng thái assigned")
        if d["order_id"] in seen:
            raise BadInput(f"bếp/tay cùng giữ món của đơn {d['order_id']}")
        seen.add(d["order_id"])
    for c in sim.customers:
        if c["order_status"] == "assigned" and c["id"] not in seen:
            raise BadInput(f"customers.{c['id']}: đơn assigned phải có đúng một món ở bếp hoặc tay")


def day_plan_ingredients(dishes, menu):
    """Tổng nguyên liệu của kế hoạch Ngày = tổng công thức × số suất (TICKET-02 mục 2/4.1)."""
    need = {}
    for dish, n in dishes.items():
        if dish not in menu or isinstance(n, bool) or not isinstance(n, int) or n <= 0:
            raise BadInput(f"day_plan: món/số suất không hợp lệ: {dish!r}: {n!r}")
        for kind, q in menu[dish]["recipe"].items():
            need[kind] = need.get(kind, 0) + q * n
    return {k: need[k] for k in sorted(need)}
