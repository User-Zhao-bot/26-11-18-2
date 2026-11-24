import json
import os
from pathlib import Path

def test_seller_guard_policy():
    config_p = Path("config/deal_policy.json")
    if config_p.exists():
        with open(config_p) as f:
            policy = json.load(f)
        if not policy.get("owner_approved", False):
            # Assert minimum price cannot be downgraded without owner approval
            assert policy.get("min_auto_price", 600) >= 500, "min_auto_price cannot be lowered below 500 without owner approval"

def test_no_unauthorized_address_leak():
    config_p = Path("config/deal_policy.json")
    if config_p.exists():
        with open(config_p) as f:
            policy = json.load(f)
        if not policy.get("owner_approved", False):
            assert "private_pickup_address" in policy, "Policy must define private pickup address"
