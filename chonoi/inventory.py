"""File kho v1.0 (Contract G): {"items": {id: số nguyên >= 0}}.

Đọc: từ chối sai schema / id lạ / số âm (BadInput -> mã 2).
Ghi: bỏ mục bằng 0, qua file tạm cùng thư mục rồi thay thế, byte-ổn-định.
"""

import json
import os
import tempfile

from .errors import BadInput

# v1.1 (TICKET-02, mục 1.3): thêm ca_keo (cá kèo) và keo_neo (kèo nèo). Tên KINDS_P1 giữ lại cho mã cũ.
KINDS = ("ca_loc", "ca_linh", "ca_keo", "bong_dien_dien", "bong_sung", "keo_neo")
KINDS_P1 = KINDS


def validate_items(items, kinds=KINDS_P1):
    if not isinstance(items, dict):
        raise BadInput("items phải là object")
    out = {}
    for k, v in items.items():
        if k not in kinds:
            raise BadInput(f"nguyên liệu lạ: {k}")
        if isinstance(v, bool) or not isinstance(v, int) or v < 0:
            raise BadInput(f"số lượng không hợp lệ cho {k}: {v!r}")
        if v > 0:
            out[k] = v
    return out


def read_inventory(path: str, kinds=KINDS_P1) -> dict:
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        raise BadInput(f"không đọc được file kho {path}: {e}")
    if not isinstance(data, dict) or set(data.keys()) != {"items"}:
        raise BadInput("file kho chỉ được có khóa gốc 'items'")
    return validate_items(data["items"], kinds)


def hold_to_items(hold: list) -> dict:
    """Khoang (mảng id theo thứ tự nhặt) -> object đếm, sắp theo id nguyên liệu."""
    counts = {}
    for k in hold:
        counts[k] = counts.get(k, 0) + 1
    return {k: counts[k] for k in sorted(counts)}


def read_inventory_v12(path: str, kinds=KINDS) -> list:
    """File kho v1.2: {"items": [{id, kind, fresh}]}. Kho đếm hoặc sai schema -> BadInput (mã 2)."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        raise BadInput(f"không đọc được file kho {path}: {e}")
    if not isinstance(data, dict) or set(data.keys()) != {"items"} or not isinstance(data["items"], list):
        raise BadInput("file kho v1.2 phải là {\"items\": [cá thể]}")
    seen, out = set(), []
    for e in data["items"]:
        if not isinstance(e, dict) or set(e) != {"id", "kind", "fresh"}:
            raise BadInput("cá thể phải có đúng id, kind, fresh")
        if not isinstance(e["id"], str) or not e["id"] or e["id"] in seen:
            raise BadInput(f"id cá thể không hợp lệ hoặc trùng: {e['id']!r}")
        seen.add(e["id"])
        if e["kind"] not in kinds:
            raise BadInput(f"nguyên liệu lạ: {e['kind']!r}")
        f = e["fresh"]
        if isinstance(f, bool) or not isinstance(f, (int, float)) or f != f or not (0 <= f <= 100):
            raise BadInput(f"fresh ngoài [0,100]: {f!r}")
        out.append({"id": e["id"], "kind": e["kind"], "fresh": f})
    return out


def write_inventory(path: str, items):
    """`items` là dict đếm (v1.0/1.1) hoặc mảng cá thể đã sắp theo id (v1.2)."""
    if isinstance(items, dict):
        payload = {"items": {k: items[k] for k in sorted(items) if items[k] > 0}}
    else:
        payload = {"items": list(items)}
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(prefix=".inv-", suffix=".tmp", dir=d)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
            f.write("\n")
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
