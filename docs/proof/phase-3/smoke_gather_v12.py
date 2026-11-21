"""Smoke Phase 3 (Người 1): gather v1.2 với freshness, hold fresh:100, interact ở frame 0 -> docked -> ghi kho.
Chạy: PYTHONPATH=. python3 docs/proof/phase-3/smoke_gather_v12.py   (cùng seed -> hai lần chạy giống từng byte)"""
import copy, json, os, filecmp, tempfile
from chonoi.contract import load_contract
from chonoi.inputs import load_frames
from chonoi.runner import run

t = copy.deepcopy(load_contract()["tuning"])
t["freshness"] = {"initial": 100, "gather_decay_per_s": 0.5, "quan_decay_per_s": 0.25, "spoiled_below": 30}
d = tempfile.mkdtemp()
sc = {"hold": [{"id": "I1", "kind": "ca_linh", "fresh": 100}], "random_fish": False, "monsters": []}
inp = os.path.join(d, "in.json"); json.dump({"frames": [{"tick": 0, "interact": True}]}, open(inp, "w"))
outs = []
for i in (1, 2):
    o, k = os.path.join(d, f"o{i}.jsonl"), os.path.join(d, f"k{i}.json")
    run("gather", t, sc, 1, load_frames(inp), 10, o, 1, inventory_out=k)
    outs.append((o, k))
print("jsonl giống nhau:", filecmp.cmp(outs[0][0], outs[1][0], shallow=False))
print("kho giống nhau:", filecmp.cmp(outs[0][1], outs[1][1], shallow=False))
print("kho:", open(outs[0][1]).read().strip())
print("gather_end:", [l for l in open(outs[0][0]) if '"gather_end"' in l][0].strip())
