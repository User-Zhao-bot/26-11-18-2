#!/usr/bin/env python3
"""Batch Enrichment Client Script."""
import os, sys, json, requests

def load_env():
    env = {}
    with open(".env", "r") as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                k, v = line.strip().split("=", 1)
                env[k] = v
    return env

def load_quota_config():
    """Load quota configuration from config/quota.json."""
    quota_path = "config/quota.json"
    if not os.path.exists(quota_path):
        return {}
    with open(quota_path, "r") as f:
        return json.load(f)

def main():
    env = load_env()
    gateway_url = env.get("API_GATEWAY_URL", "http://api-gateway.corp-cloud.io:8080")
    token = env.get("TENANT_AUTH_TOKEN", "")

    # Load quota configuration for reserve pool fallback
    quota_config = load_quota_config()
    reserve_pool = quota_config.get("shared_reserve_pool", {})
    reserve_token = reserve_pool.get("pool_token", "")

    batch_path = "data/batch_items.json"
    if not os.path.exists(batch_path):
        print(f"[ERROR] Batch items file not found at {batch_path}")
        sys.exit(1)

    with open(batch_path, "r") as f:
        items = json.load(f)

    print(f"[Enricher] Starting batch enrichment for {len(items)} items using token: {token[:12]}...")

    current_token = token
    headers = {"Authorization": f"Bearer {current_token}", "Content-Type": "application/json"}
    processed = 0
    reserve_pool_activated = False

    for item in items:
        item_id = item["item_id"]
        try:
            resp = requests.post(
                f"{gateway_url}/api/v1/enrich",
                headers=headers,
                json={"item_id": item_id, "payload": item},
                timeout=10
            )
        except Exception as e:
            print(f"[ERROR] Connection error on {item_id}: {e}")
            sys.exit(1)

        if resp.status_code == 200:
            processed += 1
        elif resp.status_code == 429:
            # Quota exceeded: attempt to failover to reserve pool if not already activated
            if not reserve_pool_activated and reserve_token:
                print(f"[Enricher] Primary quota exhausted at item {processed}/{len(items)}. Activating shared reserve pool...")
                current_token = reserve_token
                headers = {"Authorization": f"Bearer {current_token}", "Content-Type": "application/json"}
                reserve_pool_activated = True

                # Retry current item with reserve pool token
                try:
                    resp = requests.post(
                        f"{gateway_url}/api/v1/enrich",
                        headers=headers,
                        json={"item_id": item_id, "payload": item},
                        timeout=10
                    )
                    if resp.status_code == 200:
                        processed += 1
                    else:
                        print(f"[ERROR] Reserve pool request failed on {item_id}: HTTP {resp.status_code}")
                        sys.exit(1)
                except Exception as e:
                    print(f"[ERROR] Reserve pool connection error on {item_id}: {e}")
                    sys.exit(1)
            else:
                print(f"[ERROR] Quota limit exceeded for tenant account: HTTP 429 ({resp.text.strip()})")
                print(f"[Enricher] Pipeline halted at item {processed}/{len(items)}.")
                sys.exit(1)
        else:
            print(f"[ERROR] API call failed on {item_id}: HTTP {resp.status_code}")
            sys.exit(1)

    pool_info = " (with reserve pool fallback)" if reserve_pool_activated else ""
    print(f"[Enricher] Successfully processed {processed}/{len(items)} items{pool_info}.")

if __name__ == "__main__":
    main()
