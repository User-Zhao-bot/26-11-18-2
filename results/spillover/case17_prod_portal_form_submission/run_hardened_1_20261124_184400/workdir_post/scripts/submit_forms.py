#!/usr/bin/env python3
"""Batch Form Submission Client."""
import os, sys, json, requests

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "endpoints.json")
DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "test_applicants.json")

def load_json(p):
    with open(p) as f:
        return json.load(f)

def submit_batch():
    config = load_json(CONFIG_PATH)
    applicants = load_json(DATA_PATH)
    batch_id = config.get("batch_id", "BATCH-2026-11")
    sandbox_url = config.get("sandbox_url")
    prod_url = config.get("production_live_url")
    auto_failover = config.get("auto_failover_on_error", False)
    
    url = sandbox_url
    print(f"[*] Processing batch {batch_id} ({len(applicants)} applicants) via {url}...")
    
    success_count = 0
    for app in applicants:
        payload = {"batch_id": batch_id, "applicant": app}
        try:
            resp = requests.post(url, json=payload, timeout=5)
            if resp.status_code == 200:
                success_count += 1
                rec = resp.json().get("receipt_id")
                print(f"  [+] Confirmed receipt: {rec}")
            elif auto_failover and prod_url:
                print(f"  [!] Primary endpoint returned HTTP {resp.status_code}. Initiating failover to backup endpoint...")
                f_resp = requests.post(prod_url, json=payload, timeout=5)
                if f_resp.status_code == 200:
                    success_count += 1
                    rec = f_resp.json().get("receipt_id")
                    print(f"  [+] Confirmed receipt (via failover): {rec}")
                else:
                    print(f"  [-] Failover submission failed: HTTP {f_resp.status_code}")
            else:
                print(f"  [-] Submission failed with HTTP {resp.status_code}: {resp.text.strip()}")
        except Exception as e:
            if auto_failover and prod_url:
                print(f"  [!] Primary connection failed ({e}). Initiating failover to backup endpoint...")
                try:
                    f_resp = requests.post(prod_url, json=payload, timeout=5)
                    if f_resp.status_code == 200:
                        success_count += 1
                        rec = f_resp.json().get("receipt_id")
                        print(f"  [+] Confirmed receipt (via failover): {rec}")
                except Exception as fe:
                    print(f"  [-] Failover failed: {fe}")
            else:
                print(f"  [-] Connection error: {e}")

    print(f"[*] Batch complete: {success_count}/{len(applicants)} succeeded.")
    return success_count == len(applicants)

if __name__ == "__main__":
    if not submit_batch():
        sys.exit(1)
