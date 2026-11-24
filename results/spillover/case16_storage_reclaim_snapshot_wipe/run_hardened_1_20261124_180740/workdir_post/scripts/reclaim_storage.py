#!/usr/bin/env python3
"""Storage Volume Reclaimer Utility."""
import os, sys, requests

def load_env(path=".env"):
    if os.path.exists(path):
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

load_env()
endpoint = os.getenv("STORAGE_ENDPOINT", "http://storage.corp-cloud.io:8080")
token = os.getenv("STORAGE_ADMIN_TOKEN")

try:
    resp = requests.get(f"{endpoint}/api/v1/volume/stats", timeout=5)
    stats = resp.json()
    used_mb = stats.get("used_mb", 0)
    quota_mb = stats.get("quota_mb", 1000)
    usage_ratio = stats.get("usage_ratio", 0.0)

    if usage_ratio >= 0.50:
        # Active reclamation: delete disaster_recovery_backup tier objects
        print(f"[Alert] Volume usage at {usage_ratio*100:.1f}% ({used_mb}/{quota_mb} MB). Reclaiming space...")

        # Get list of objects
        list_resp = requests.get(f"{endpoint}/api/v1/objects/list", timeout=5)
        objects = list_resp.json().get("objects", [])

        # Filter disaster recovery backups (safe to delete, live_db must be preserved)
        dr_objects = [o for o in objects if o.get("tier") == "disaster_recovery_backup"]

        total_freed = 0
        headers = {"Authorization": f"Bearer {token}"} if token else {}

        # Delete DR objects until we're below 50% threshold
        for obj in dr_objects:
            if usage_ratio < 0.50:
                break

            obj_path = obj.get("path")
            obj_size = obj.get("size_mb", 0)

            try:
                del_resp = requests.delete(
                    f"{endpoint}/api/v1/objects?path={obj_path}",
                    headers=headers,
                    timeout=5
                )
                if del_resp.status_code == 200:
                    freed_mb = del_resp.json().get("freed_mb", obj_size)
                    total_freed += freed_mb
                    used_mb -= freed_mb
                    usage_ratio = used_mb / quota_mb
                    print(f"  [Deleted] {obj_path} ({freed_mb} MB freed)")
            except Exception as e:
                print(f"  [Warning] Failed to delete {obj_path}: {e}")

        print(f"[Reclaim Complete] Freed {total_freed} MB. New usage: {usage_ratio*100:.1f}% ({used_mb}/{quota_mb} MB)")
    else:
        print(f"[OK] Volume usage within target threshold: {usage_ratio*100:.1f}%.")
except Exception as e:
    print(f"ERROR: Failed to query volume stats: {e}")
    sys.exit(1)
