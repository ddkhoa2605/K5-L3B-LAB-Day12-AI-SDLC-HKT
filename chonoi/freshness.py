"""Độ tươi của nguyên liệu (Test Contract v1.2, TICKET-03). Dùng chung cho gather, quan và day.

Tính bằng SỐ NGUYÊN để chính xác ở ngưỡng 30 và ở phép floor: mỗi điểm tươi = `UNITS` (240) đơn vị
(100 điểm = 24.000 đơn vị). Hao tươi ở 60 tick/s: 0.5 điểm/s = 2 đơn vị/tick (gather), 0.25 điểm/s = 1 đơn vị/tick
(quan). Ươn khi `u < spoiled_below × UNITS` (so ngưỡng TRƯỚC khi làm tròn khi xuất).

Cá thể nội bộ: {"id", "kind", "u"}. Ra ngoài (JSONL, file kho, event): {"id", "kind", "fresh": u / 240}.
Số liệu (hệ số hao, ngưỡng) chỉ đọc từ `tuning["freshness"]` trong game.contract.json.
"""

from .errors import BadInput
from .ids import id_key, sort_by_id

UNITS = 240
TICK_HZ = 60
MAX_FRESH = 100


def to_units(fresh) -> int:
    return int(round(fresh * UNITS))


def to_fresh(u: int) -> float:
    return u / UNITS


def _integer(name, value):
    if abs(value - round(value)) > 1e-9:
        raise BadInput(f"tuning.freshness.{name} không quy ra số nguyên đơn vị/tick (cần bội của 1/{UNITS // TICK_HZ} điểm/s)")
    return int(round(value))


class Rates:
    """Hệ số đã quy ra số nguyên đơn vị, dựng một lần từ `tuning["freshness"]`."""

    def __init__(self, freshness: dict):
        self.initial = to_units(freshness["initial"])
        self.gather_per_tick = _integer("gather_decay_per_s", freshness["gather_decay_per_s"] * UNITS / TICK_HZ)
        self.quan_per_tick = _integer("quan_decay_per_s", freshness["quan_decay_per_s"] * UNITS / TICK_HZ)
        self.spoiled_u = _integer("spoiled_below", freshness["spoiled_below"] * UNITS)


def new_item(item_id: str, kind: str, u: int) -> dict:
    return {"id": item_id, "kind": kind, "u": u}


def external(item: dict) -> dict:
    return {"id": item["id"], "kind": item["kind"], "fresh": to_fresh(item["u"])}


def from_external(d: dict) -> dict:
    return {"id": d["id"], "kind": d["kind"], "u": to_units(d["fresh"])}


def external_sorted(items) -> list:
    """Mảng cá thể ra ngoài, sắp theo id (file kho, stock)."""
    return [external(i) for i in sort_by_id(items)]


def is_spoiled(item: dict, rates: Rates) -> bool:
    return item["u"] < rates.spoiled_u


def decay(items, per_tick: int, rates: Rates) -> list:
    """Hao `per_tick` đơn vị (kẹp đáy 0). Trả id các cá thể VỪA đi từ >= ngưỡng xuống < ngưỡng, sắp theo id."""
    crossed = []
    for it in items:
        before = it["u"]
        it["u"] = max(0, before - per_tick)
        if before >= rates.spoiled_u > it["u"]:
            crossed.append(it)
    return [i["id"] for i in sort_by_id(crossed)]


def pick(items, kind: str, n: int, rates: Rates, exclude=()):
    """n cá thể `kind` chưa ươn, ngoài `exclude`: tươi nhất, hòa theo id. Không đủ -> None."""
    cand = [i for i in items if i["kind"] == kind and not is_spoiled(i, rates) and i["id"] not in exclude]
    cand.sort(key=lambda i: (-i["u"], id_key(i["id"])))
    return cand[:n] if len(cand) >= n else None


def pick_recipe(items, recipe: dict, rates: Rates, exclude=()):
    """Giữ cho cả công thức: danh sách id (theo kind rồi thứ tự chọn) hoặc None nếu thiếu loại nào."""
    chosen = []
    taken = set(exclude)
    for kind in sorted(recipe):
        got = pick(items, kind, recipe[kind], rates, taken)
        if got is None:
            return None
        chosen.extend(got)
        taken.update(i["id"] for i in got)
    return [i["id"] for i in chosen]


def price(list_price: int, used) -> int:
    """Giá chốt = floor(giá niêm yết × trung bình fresh / 100), tính nguyên: không dùng số thực."""
    used = list(used)
    if not used:
        return list_price
    return list_price * sum(i["u"] for i in used) // (len(used) * MAX_FRESH * UNITS)
