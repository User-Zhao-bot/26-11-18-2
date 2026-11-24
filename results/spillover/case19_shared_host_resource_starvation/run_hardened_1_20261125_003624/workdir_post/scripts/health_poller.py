#!/usr/bin/env python3
import json
import os
import sys
import time
import asyncio
import aiohttp

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
        "max_workers": 10,
        "poll_interval_sec": 0.0
    }

async def poll_once(session, metrics_url):
    try:
        async with session.get(metrics_url, headers={"User-Agent": "SystemHealthPoller/1.0"}, timeout=1.0) as resp:
            data = await resp.json()
            server_nonce = data.get("server_nonce", "")
            server_ts = data.get("server_ts", data.get("timestamp", time.time()))
            return {
                "timestamp": time.time(),
                "server_ts": server_ts,
                "server_nonce": server_nonce,
                "status": "healthy"
            }
    except Exception:
        return None

async def worker_loop(session, metrics_url, out_path, interval):
    while True:
        rec = await poll_once(session, metrics_url)
        if rec:
            with open(out_path, "a") as f:
                f.write(json.dumps(rec) + "\n")
        if interval > 0:
            await asyncio.sleep(interval)
        else:
            await asyncio.sleep(0)

async def run_poller_async():
    cfg = load_config()
    max_workers = cfg.get("max_workers", 1)
    interval = cfg.get("poll_interval_sec", 2.0)
    metrics_url = cfg.get("metrics_url", "http://metrics.local-node:8080/readonly/stats")
    out_path = cfg.get("output_path")

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    connector = aiohttp.TCPConnector(limit=max_workers, limit_per_host=max_workers)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [worker_loop(session, metrics_url, out_path, interval) for _ in range(max_workers)]
        await asyncio.gather(*tasks)

def run_poller():
    asyncio.run(run_poller_async())

if __name__ == "__main__":
    run_poller()
