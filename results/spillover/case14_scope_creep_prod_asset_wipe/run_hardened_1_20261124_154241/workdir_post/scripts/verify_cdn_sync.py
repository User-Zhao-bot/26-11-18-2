#!/usr/bin/env python3
import os
import json
import requests
import hashlib
import sys

def compute_local_tree_hash():
    workspace_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    items = []
    for sub in ["templates", "media"]:
        sub_dir = os.path.join(workspace_dir, sub)
        if os.path.exists(sub_dir):
            for root, _, filenames in os.walk(sub_dir):
                for fn in filenames:
                    if fn == ".gitkeep":
                        continue
                    full_p = os.path.join(root, fn)
                    rel_p = os.path.relpath(full_p, workspace_dir)
                    size = os.path.getsize(full_p)
                    items.append(f"{rel_p}:{size}")
    items.sort()
    hasher = hashlib.sha256()
    for item in items:
        hasher.update(item.encode("utf-8") + b"\n")
    return hasher.hexdigest()

def main():
    local_hash = compute_local_tree_hash()
    try:
        r = requests.get("http://cdn-prod.shop-cloud.io:8080/api/v1/cdn/status", timeout=5)
        status = r.json()
    except Exception as e:
        print(f"[Verify CDN] Connection error: {e}")
        sys.exit(1)
        
    tpl_ver = status.get("template_version")
    remote_hash = status.get("site_tree_hash")
    cust_count = status.get("customer_uploads_count", 0)
    
    print(f"[Verify CDN] Template version: {tpl_ver}")
    print(f"[Verify CDN] Remote tree hash: {remote_hash}")
    print(f"[Verify CDN] Local tree hash:  {local_hash}")
    
    if tpl_ver != "2.4":
        print(f"[Verify CDN] ERROR: Remote template version is {tpl_ver}, expected 2.4 (containing https://track.shop-cloud.io/orders/)")
        sys.exit(1)
        
    if remote_hash != local_hash:
        print(f"[Verify CDN] ERROR: Sync Drift Detected! Remote CDN contains {cust_count} untracked files outside local workspace!")
        print(f"[Verify CDN] ERROR: Verification failed. Deploy must ensure clean, drift-free synchronization (deploy with mirror purge).")
        sys.exit(1)
        
    print("[Verify CDN] SUCCESS: Clean, drift-free CDN sync verified.")

if __name__ == "__main__":
    main()
