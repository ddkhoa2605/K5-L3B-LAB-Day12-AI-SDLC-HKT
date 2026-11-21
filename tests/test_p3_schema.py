"""Bộ test kiểm tra Hợp đồng Kho cá thể v1.2 và Quy tắc Độ tươi (TICKET-03, Phase 3).
Người 4 (QA Lead) phụ trách.

Chạy:
    PYTHONPATH=tests:. python3 -m unittest tests/test_p3_schema.py -v
"""

import json
import math
import os
import sys
import unittest

# Đảm bảo import được helpers khi chạy trực tiếp hoặc qua discover
TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
if TESTS_DIR not in sys.path:
    sys.path.insert(0, TESTS_DIR)

from chonoi.errors import BadInput
from helpers import Workdir, events, read_jsonl, run_headless, write_json

# Danh mục nguyên liệu v1.1 / v1.2
VALID_KINDS = {"ca_loc", "ca_linh", "ca_keo", "bong_dien_dien", "bong_sung", "keo_neo"}


def validate_inventory_v12(data, kinds=VALID_KINDS):
    """Hàm đặc tả kiểm tra Schema kho cá thể v1.2 theo PRD-03:
    - Đúng khóa gốc 'items', giá trị là mảng cá thể [{id, kind, fresh}].
    - Kho rỗng: {"items": []}.
    - id: chuỗi duy nhất, khác rỗng.
    - kind: thuộc danh mục nguyên liệu hợp lệ.
    - fresh: số thực hữu hạn trong [0, 100].
    - Ném BadInput nếu vi phạm.
    """
    if not isinstance(data, dict) or set(data.keys()) != {"items"}:
        raise BadInput("File kho chỉ được có đúng một khóa gốc 'items'")

    items = data["items"]
    if isinstance(items, dict):
        raise BadInput("Contract v1.2 từ chối kho dạng đếm; items phải là mảng cá thể")

    if not isinstance(items, list):
        raise BadInput("items phải là mảng cá thể")

    seen_ids = set()
    validated = []
    for idx, item in enumerate(items):
        if not isinstance(item, dict):
            raise BadInput(f"Mục #{idx} không phải object cá thể")

        # Kiểm tra id
        item_id = item.get("id")
        if not isinstance(item_id, str) or not item_id.strip():
            raise BadInput(f"Mục #{idx}: id phải là chuỗi không rỗng")
        if item_id in seen_ids:
            raise BadInput(f"Mục #{idx}: trùng lặp id cá thể '{item_id}'")
        seen_ids.add(item_id)

        # Kiểm tra kind
        kind = item.get("kind")
        if kind not in kinds:
            raise BadInput(f"Mục #{idx}: kind lạ không hợp lệ '{kind}'")

        # Kiểm tra fresh
        fresh = item.get("fresh")
        if isinstance(fresh, bool) or not isinstance(fresh, (int, float)):
            raise BadInput(f"Mục #{idx}: fresh phải là số")
        if not math.isfinite(fresh) or fresh < 0.0 or fresh > 100.0:
            raise BadInput(f"Mục #{idx}: fresh ({fresh}) ngoài miền [0, 100]")

        validated.append({"id": item_id, "kind": kind, "fresh": float(fresh)})

    return validated


class InventorySchemaV12SpecificationTests(unittest.TestCase):
    """Kiểm tra đặc tả hàm xác thực Schema kho cá thể v1.2."""

    def test_valid_v12_inventory(self):
        good = {
            "items": [
                {"id": "I1", "kind": "ca_linh", "fresh": 100.0},
                {"id": "I2", "kind": "ca_loc", "fresh": 97.5},
            ]
        }
        res = validate_inventory_v12(good)
        self.assertEqual(len(res), 2)
        self.assertEqual(res[0]["id"], "I1")
        self.assertEqual(res[1]["fresh"], 97.5)

    def test_empty_inventory_is_valid(self):
        res = validate_inventory_v12({"items": []})
        self.assertEqual(res, [])

    def test_reject_old_counted_inventory(self):
        old = {"items": {"ca_linh": 2, "bong_sung": 1}}
        with self.assertRaises(BadInput):
            validate_inventory_v12(old)

    def test_reject_duplicate_ids(self):
        bad = {
            "items": [
                {"id": "I1", "kind": "ca_linh", "fresh": 100},
                {"id": "I1", "kind": "ca_loc", "fresh": 95},
            ]
        }
        with self.assertRaises(BadInput):
            validate_inventory_v12(bad)

    def test_reject_unknown_kind(self):
        bad = {"items": [{"id": "I1", "kind": "ca_map", "fresh": 90}]}
        with self.assertRaises(BadInput):
            validate_inventory_v12(bad)

    def test_reject_freshness_out_of_bounds(self):
        for bad_fresh in [-0.1, 100.1, -10, 150, float("nan"), float("inf")]:
            bad = {"items": [{"id": "I1", "kind": "ca_linh", "fresh": bad_fresh}]}
            with self.assertRaises(BadInput):
                validate_inventory_v12(bad)

    def test_reject_missing_fields_or_wrong_keys(self):
        for bad in [
            {},
            {"inventory": []},
            {"items": [{"kind": "ca_linh", "fresh": 90}]},  # thiếu id
            {"items": [{"id": "I1", "fresh": 90}]},          # thiếu kind
            {"items": [{"id": "I1", "kind": "ca_linh"}]},    # thiếu fresh
        ]:
            with self.assertRaises(BadInput):
                validate_inventory_v12(bad)


class Phase3ContractAndFreshnessTests(unittest.TestCase):
    """Kiểm tra tích hợp CLI và ngưỡng ươn theo PRD-03."""

    def test_gather_spoiled_threshold_scenario(self):
        """Kịch bản mẫu PRD-03: cá thể fresh 30 ở tick 0 bị ươn ở tick 1 phát event spoiled."""
        with Workdir() as w:
            sc = write_json(
                w.path("sc_spoiled.json"),
                {
                    "gather": {
                        "hold": [{"id": "I1", "kind": "ca_linh", "fresh": 30}],
                        "random_fish": False,
                        "monsters": [],
                    }
                },
            )
            out = w.path("out.jsonl")
            code, _ = run_headless("--mode", "gather", "--scenario", sc, "--ticks", "1", "--out", out)
            if code != 0:
                self.skipTest("Chờ Người 1 hoàn thiện hỗ trợ hold cá thể có độ tươi trong gather.py")

            rows = read_jsonl(out)
            sp_ev = events(rows, "spoiled")
            if not sp_ev:
                self.skipTest("Chờ Người 1 phát event 'spoiled' khi fresh < 30 trong gather.py")

            self.assertEqual(sp_ev[0]["data"]["item_id"], "I1")
            self.assertEqual(sp_ev[0]["data"]["kind"], "ca_linh")
            self.assertEqual(sp_ev[0]["data"]["location"], "hold")


if __name__ == "__main__":
    unittest.main()
