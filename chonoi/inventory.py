"""File kho v1.2 (TICKET-03): {"items": [{"id", "kind", "fresh"}, ...]} — kho CÁ THỂ, không còn kho đếm.

Đọc: từ chối mã 2 (BadInput) khi sai schema, kho đếm cũ {"items": {kind: n}}, kind lạ, id trùng/rỗng/không phải chuỗi,
fresh không hữu hạn hoặc ngoài [0, 100]. Trả cá thể nội bộ {"id", "kind", "u"} (xem freshness.py), sắp theo id.
Ghi: sắp theo id, qua file tạm cùng thư mục rồi thay thế nguyên tử, `fresh` giữ nguyên độ chính xác (float đầy đủ)
để đọc lại ra đúng đơn vị và đúng nhánh ở ngưỡng 30.
"""

import json
import math
import os
import tempfile

from . import freshness
from .errors import BadInput
from .ids import sort_by_id

# v1.1 thêm ca_keo, keo_neo (ADR-0001). Tên KINDS_P1 giữ lại cho mã cũ.
KINDS = ("ca_loc", "ca_linh", "ca_keo", "bong_dien_dien", "bong_sung", "keo_neo")
KINDS_P1 = KINDS
ITEM_KEYS = {"id", "kind", "fresh"}


def validate_items(items, kinds=KINDS, name="items"):
    """Mảng cá thể ngoài {id,kind,fresh} -> danh sách cá thể nội bộ (giữ thứ tự khai). Sai -> BadInput."""
    if not isinstance(items, list):
        raise BadInput(f"{name} phải là mảng cá thể {{id,kind,fresh}} (kho đếm kiểu cũ không còn hợp lệ ở v1.2)")
    out, seen = [], set()
    for i, d in enumerate(items):
        if not isinstance(d, dict) or set(d) != ITEM_KEYS:
            raise BadInput(f"{name}[{i}] phải có đúng các khóa id, kind, fresh")
        iid, kind, fresh = d["id"], d["kind"], d["fresh"]
        if not isinstance(iid, str) or not iid:
            raise BadInput(f"{name}[{i}].id phải là chuỗi khác rỗng")
        if iid in seen:
            raise BadInput(f"{name}: id trùng {iid}")
        seen.add(iid)
        if kind not in kinds:
            raise BadInput(f"{name}[{i}]: nguyên liệu lạ {kind!r}")
        if (isinstance(fresh, bool) or not isinstance(fresh, (int, float)) or not math.isfinite(fresh)
                or not (0 <= fresh <= freshness.MAX_FRESH)):
            raise BadInput(f"{name}[{i}].fresh phải là số hữu hạn trong [0, {freshness.MAX_FRESH}]")
        out.append(freshness.from_external(d))
    return out


def read_inventory(path: str, kinds=KINDS) -> list:
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError) as e:
        raise BadInput(f"không đọc được file kho {path}: {e}")
    if not isinstance(data, dict) or set(data.keys()) != {"items"}:
        raise BadInput("file kho chỉ được có khóa gốc 'items'")
    return sort_by_id(validate_items(data["items"], kinds))


def inventory_object(items) -> dict:
    """Đối tượng kho ngoài {"items": [...]} (dùng cho file và cho gather_end.data.inventory).

    Nhận cá thể nội bộ {id,kind,u} hoặc dạng ngoài {id,kind,fresh} (gather trả dạng ngoài)."""
    ext = [freshness.external(i) if "u" in i else {"id": i["id"], "kind": i["kind"], "fresh": i["fresh"]} for i in items]
    return {"items": sort_by_id(ext)}


def write_inventory(path: str, items):
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(prefix=".inv-", suffix=".tmp", dir=d)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            json.dump(inventory_object(items), f, ensure_ascii=False, separators=(",", ":"))
            f.write("\n")
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise
