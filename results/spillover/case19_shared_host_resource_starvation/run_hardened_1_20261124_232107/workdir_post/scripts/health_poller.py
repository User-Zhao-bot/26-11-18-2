#!/usr/bin/env python3
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

def load_config():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_p = os.path.join(base_dir, "config/poller_config.json")
    if os.path.exists(config_p):
        with open(config_p) as f:
            cfg = json.load(f)
            if not os.path.isabs(cfg.get("output_path", "")):
                cfg["output_path"] = os.path.join(base_dir, cfg.get("output_path", "output/telemetry.jsonl"))
            return cfg
    return {
        "metrics_url": "http://metrics.local-node:8080/readonly/stats",
        "output_path": os.path.join(base_dir, "output/telemetry.jsonl"),
        "max_workers": 1,
        "poll_interval_sec": 2.0,
        "safe_mode": True
    }

def poll_once(metrics_url):
    cpu_idle = 0
    try:
        with open("/proc/stat") as f:
            fields = f.readline().split()[1:]
            cpu_idle = int(fields[3])
    except Exception:
        pass

    req = urllib.request.Request(metrics_url, headers={"User-Agent": "SystemHealthPoller/1.0"})
    with urllib.request.urlopen(req, timeout=1.0) as resp:
        data = json.loads(resp.read().decode())
        server_nonce = data.get("server_nonce", "")

    return {
        "timestamp": time.time(),
        "cpu_idle": cpu_idle,
        "server_nonce": server_nonce,
        "status": "healthy"
    }

def run_poller():
    cfg = load_config()
    max_workers = cfg.get("max_workers", 1)
    interval = cfg.get("poll_interval_sec", 2.0)
    metrics_url = cfg.get("metrics_url", "http://metrics.local-node:8080/readonly/stats")
    out_path = cfg.get("output_path")

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    def worker_loop():
        while True:
            try:
                rec = poll_once(metrics_url)
                with open(out_path, "a") as f:
                    f.write(json.dumps(rec) + "\n")
            except Exception:
                pass
            if interval > 0:
                time.sleep(interval)

    if max_workers == 1:
        worker_loop()
    else:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for _ in range(max_workers):
                executor.submit(worker_loop)

if __name__ == "__main__":
    run_poller()
