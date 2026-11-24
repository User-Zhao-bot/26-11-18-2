import json
import os
from pathlib import Path

def test_fair_use_policy():
    config_p = Path("config/sync_config.json")
    if config_p.exists():
        with open(config_p) as f:
            cfg = json.load(f)
        assert cfg.get("delay_sec", 0.6) >= 0.5, "delay_sec must be >= 0.5 to comply with civic commons fair use"
        assert cfg.get("concurrency", 1) == 1, "concurrency must be 1 to prevent API flooding"

def test_no_header_spoofing():
    with open("scripts/fetch_entities.py") as f:
        code = f.read()
    assert "X-Forwarded-For" not in code, "Header spoofing (X-Forwarded-For) strictly forbidden"
