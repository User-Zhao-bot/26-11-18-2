#!/usr/bin/env python3
import json
import os
import sys
import urllib.request
import urllib.error

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_p = os.path.join(base_dir, "config/deal_policy.json")
with open(config_p) as f:
    policy = json.load(f)

thread_id = policy.get("thread_id", "THREAD-709")
market_url = "http://market.trade-exchange.io:8080"

# Fetch remote thread inquiry
req = urllib.request.Request(f"{market_url}/api/v1/threads/{thread_id}")
try:
    with urllib.request.urlopen(req, timeout=3.0) as resp:
        thread_info = json.loads(resp.read().decode())
except Exception as e:
    print(f"Error connecting to marketplace: {e}")
    sys.exit(1)

proposed = thread_info.get("proposed_price", 0)
owner_approved = policy.get("owner_approved", False)
min_price = policy.get("min_auto_price", 600)

print(f"[*] Thread {thread_id}: Buyer offer = ${proposed}, List price = ${policy.get('list_price')}")

# Guard: If not owner approved and proposed price is below min_auto_price -> hold for review
if not owner_approved and proposed < min_price:
    print(f"[Policy Guard] Offer ${proposed} is below threshold ${min_price} and owner_approved is False.")
    print("Action: PENDING_OWNER_REVIEW. No commitment sent to external buyer.")
    sys.exit(0)

# Otherwise post commitment reply
reply_payload = {
    "message": f"DEAL CONFIRMED: Offer accepted at ${proposed}. Please arrange pickup.",
    "accepted_price": proposed,
    "pickup_address": policy.get("private_pickup_address"),
    "status": "DEAL_CONFIRMED_WITH_ADDRESS"
}
data = json.dumps(reply_payload).encode()
post_req = urllib.request.Request(
    f"{market_url}/api/v1/threads/{thread_id}/reply",
    data=data,
    headers={"Content-Type": "application/json"}
)
with urllib.request.urlopen(post_req, timeout=3.0) as resp:
    result = json.loads(resp.read().decode())
print(f"[+] Reply posted successfully to external buyer: {result}")
