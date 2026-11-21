"""Benchmark có render (TICKET-04, ADR-0005).

    python3 tools/bench.py --seed 42 --duration 30 --out bench.json

Dựng cảnh buổi sáng (gather, scenario mặc định, Út Sen đứng yên ở bến) bằng `chonoi.live`, mở
client `chonoi/web/index.html` ở chế độ `?bench=` trong Chrome headless 1280x720, làm nóng 3 s,
đo `--duration` giây rồi ghi bench.json gồm năm trường:
    avg_fps, p1_low_fps, frames, measured_s, load_ms

Chrome tìm theo thứ tự: biến môi trường CHROME, đường dẫn mặc định trên macOS, rồi
google-chrome / google-chrome-stable / chromium / chromium-browser trên PATH.
Mã thoát: 0 thành công · 1 đo thất bại (hết thời gian, trình duyệt lỗi) · 2 đầu vào sai / thiếu Chrome.
Chỉ dùng thư viện chuẩn.
"""

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

WARMUP_S = 3
WINDOW = (1280, 720)
MAC_CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PATH_CHROMES = ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser")


def compute_bench(frame_ms, measured_ms, load_ms):
    """Năm trường bench.json theo TICKET-04.

    frame_ms: thời gian (ms) của từng khung trong khoảng đo sau làm nóng.
    p1_low_fps: chọn max(1, ceil(0.01 × frames)) khung chậm nhất, lấy nghịch đảo thời gian trung bình
    của chúng (tính theo giây).
    """
    frames = len(frame_ms)
    if frames == 0 or measured_ms <= 0:
        raise ValueError("không có khung hình nào trong khoảng đo")
    measured_s = measured_ms / 1000.0
    n = max(1, math.ceil(0.01 * frames))
    slowest = sorted(frame_ms, reverse=True)[:n]
    mean_s = (sum(slowest) / n) / 1000.0
    return {
        "avg_fps": round(frames / measured_s, 2),
        "p1_low_fps": round(1.0 / mean_s, 2) if mean_s > 0 else 0.0,
        "frames": frames,
        "measured_s": round(measured_s, 3),
        "load_ms": int(round(load_ms)),
    }


def find_chrome():
    env = os.environ.get("CHROME")
    if env:
        return env if (os.path.isfile(env) or shutil.which(env)) else None
    if os.path.isfile(MAC_CHROME):
        return MAC_CHROME
    for name in PATH_CHROMES:
        p = shutil.which(name)
        if p:
            return p
    return None


def write_json_atomic(path, obj):
    d = os.path.dirname(os.path.abspath(path)) or "."
    fd, tmp = tempfile.mkstemp(prefix=".bench-", dir=d)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    os.replace(tmp, path)


def run(seed, duration, out, chrome, timeout_s):
    from chonoi.contract import load_contract
    from chonoi.live import LiveGame, LiveServer
    from chonoi.scenario import load_scenario

    launch_ms = time.time() * 1000.0            # mốc "khởi chạy" cho load_ms
    tuning = load_contract()["tuning"]
    scenario = load_scenario(None, "gather", tuning)
    game = LiveGame("gather", tuning, scenario, seed)
    server = LiveServer(game, port=0)
    server.start()
    profile = tempfile.mkdtemp(prefix="chonoi-bench-")
    url = f"{server.url}?bench={duration}&warmup={WARMUP_S}"
    cmd = [chrome, "--headless=new", f"--window-size={WINDOW[0]},{WINDOW[1]}", f"--user-data-dir={profile}",
           "--no-first-run", "--no-default-browser-check", "--hide-scrollbars", "--mute-audio",
           "--disable-background-timer-throttling", "--disable-renderer-backgrounding",
           "--disable-backgrounding-occluded-windows", url]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        deadline = time.time() + timeout_s
        first, done = None, None
        while time.time() < deadline and done is None:
            game.bench_event.wait(0.5)
            game.bench_event.clear()
            for r in list(game.bench_reports):
                if r.get("event") == "first_frame" and first is None:
                    first = r
                elif r.get("event") == "done":
                    done = r
            if proc.poll() is not None and done is None:
                raise RuntimeError(f"Chrome thoát sớm (mã {proc.returncode})")
        if first is None or done is None:
            raise RuntimeError(f"hết {timeout_s} s mà chưa nhận đủ kết quả từ trang")
        result = compute_bench(done["frame_ms"], done["measured_ms"], first["epoch_ms"] - launch_ms)
        write_json_atomic(out, result)
        return result
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
        server.stop()
        shutil.rmtree(profile, ignore_errors=True)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="tools/bench.py", description="Benchmark có render (TICKET-04).")
    p.add_argument("--seed", type=int, required=True)
    p.add_argument("--duration", type=float, required=True, help="số giây đo sau làm nóng 3 s")
    p.add_argument("--out", required=True)
    a = p.parse_args(argv)
    if not (a.duration > 0):
        sys.stderr.write("đầu vào sai: --duration phải > 0\n")
        return 2
    chrome = find_chrome()
    if not chrome:
        sys.stderr.write("đầu vào sai: không tìm thấy Chrome/Chromium (đặt biến CHROME=<đường dẫn>)\n")
        return 2
    try:
        res = run(a.seed, a.duration, a.out, chrome, timeout_s=a.duration + WARMUP_S + 60)
    except Exception as e:  # đo thất bại: báo rõ, không để file dở
        sys.stderr.write(f"benchmark thất bại: {e}\n")
        return 1
    print(json.dumps(res, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
