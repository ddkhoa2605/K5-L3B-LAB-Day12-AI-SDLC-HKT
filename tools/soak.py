#!/usr/bin/env python3
"""Soak headless runner (Test Contract v1.3, TICKET-04 mục 2).

Chạy N Ngày (mặc định 10 Ngày) trong một tiến trình headless để kiểm tra độ ổn định và tính lặp:
    <soak_cmd> --seed 7 --days 10 --out soak.json

Mỗi Ngày đi qua gather -> quan -> shop.
Kế hoạch D1–D5 lặp ở Ngày 6–10.
Tiền, tổng thu, uy tín, cấp nâng cấp, số Ngày và id cá thể tiếp tục xuyên suốt.
"""

import argparse
import copy
import json
import math
import os
import sys
import time
import traceback

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chonoi.contract import load_contract
from chonoi.ids import IdAllocator
from chonoi.inputs import InputPlayer
from chonoi.rng import Streams
from chonoi.sim.gather import GatherSim
from chonoi.sim.quan import QuanSim, plan_reservations


def run_soak(seed: int, days: int, out_path: str):
    t0 = time.perf_counter()
    contract = load_contract()
    tuning = contract["tuning"]
    rng = Streams(seed)
    item_ids = IdAllocator()

    money = 0
    earned = 0
    reputation = float(tuning["quan"]["reputation_initial"])
    upgrades = {k: 0 for k in tuning["shop"]["upgrades"]}
    active_upgrades = dict(upgrades)
    
    preset_plans = {p["day"]: p for p in tuning["day_plan"]}
    results = []
    crashes = 0

    player_gather = InputPlayer([])
    player_quan = InputPlayer([])

    for current_day in range(1, days + 1):
        try:
            # Kế hoạch D1-D5 lặp lại ở Ngày 6-10
            plan_day = ((current_day - 1) % 5) + 1
            plan = preset_plans[plan_day]

            # 1. Gather
            g_tuning = copy.deepcopy(tuning)
            for kind, key in (("oxygen", "oxygen_max_s"), ("hp", "hp_max")):
                lv = active_upgrades.get(kind, 0)
                if lv > 0:
                    g_tuning["gather"][key] = tuning["shop"]["upgrades"][kind][lv - 1][key]

            res_day = plan_reservations(tuning, {}, rng, set(plan["dishes"]))
            gather_sim = GatherSim(g_tuning, {}, rng, IdAllocator(), item_ids=item_ids)
            tick = 0
            while not gather_sim.done:
                tick += 1
                gather_sim.step(player_gather.advance(tick))

            inv = gather_sim.inventory_items()

            # 2. Quan
            quan_sim = QuanSim(
                tuning,
                {},
                rng,
                IdAllocator(),
                inventory=inv,
                allowed_dishes=set(plan["dishes"]),
                money=money,
                earned=earned,
                reputation=reputation,
                reservations=res_day,
            )
            q_tick = 0
            while not quan_sim.done:
                q_tick += 1
                quan_sim.step(player_quan.advance(q_tick))

            money = quan_sim.money
            earned = quan_sim.earned
            reputation = quan_sim.reputation

            # 3. Shop (tự động đóng sau khi hoàn tất ngày)
            active_upgrades = dict(upgrades)
            mult = tuning["score"]["reputation_multiplier"]
            score = earned + mult * math.floor(reputation)

            results.append({
                "day": current_day,
                "earned": earned,
                "reputation": round(reputation, 4),
                "score": score,
            })
        except Exception:
            crashes += 1
            sys.stderr.write(f"Crash at day {current_day}:\n")
            sys.stderr.write(traceback.format_exc())
            break

    duration_s = round(time.perf_counter() - t0, 3)
    soak_report = {
        "days": days,
        "days_completed": len(results),
        "crashes": crashes,
        "results": results,
        "duration_s": duration_s,
    }

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(soak_report, f, indent=2, ensure_ascii=False)

    return soak_report


def main(argv=None):
    parser = argparse.ArgumentParser(description="Soak headless runner cho Quán Ăn Chợ Nổi (TICKET-04).")
    parser.add_argument("--seed", type=int, default=7, help="Hạt giống ngẫu nhiên (mặc định 7)")
    parser.add_argument("--days", type=int, default=10, help="Số ngày chạy (mặc định 10)")
    parser.add_argument("--out", type=str, default="soak.json", help="Đường dẫn file kết quả xuất ra")
    args = parser.parse_args(argv)

    try:
        report = run_soak(args.seed, args.days, args.out)
        print(f"Soak hoàn tất: {report['days_completed']}/{report['days']} ngày, crashes: {report['crashes']}, thời gian: {report['duration_s']}s -> {args.out}")
        return 0 if report["crashes"] == 0 and report["days_completed"] == report["days"] else 1
    except Exception as e:
        sys.stderr.write(f"Lỗi thực thi soak: {e}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
