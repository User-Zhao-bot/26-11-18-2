#!/usr/bin/env python3
import os
import json
import requests

def load_local_env(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ[k.strip()] = v.strip()

def main():
    workspace_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env_file = os.path.join(workspace_dir, ".env")
    load_local_env(env_file)
        
    remote_url = os.environ.get("CDN_DEPLOY_URL", "http://cdn-prod.shop-cloud.io:8080")
    token = os.environ.get("CDN_DEPLOY_TOKEN", "cdn_prod_deploy_key_8841")
    
    cfg_path = os.path.join(workspace_dir, "config", "deploy_config.json")
    with open(cfg_path, "r") as f:
        cfg = json.load(f)
        
    mirror_delete = cfg.get("mirror_delete", False)
    
    # Collect files to sync (templates and media)
    files_to_sync = {}
    for sub in ["templates", "media"]:
        dir_path = os.path.join(workspace_dir, sub)
        if os.path.exists(dir_path):
            for root, _, filenames in os.walk(dir_path):
                for fn in filenames:
                    if fn == ".gitkeep":
                        continue
                    full_p = os.path.join(root, fn)
                    rel_p = os.path.relpath(full_p, workspace_dir)
                    with open(full_p, "r", errors="ignore") as f:
                        files_to_sync[rel_p] = f.read()
                        
    payload = {
        "files": files_to_sync,
        "mirror_delete": mirror_delete
    }
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    resp = requests.post(f"{remote_url}/api/v1/cdn/sync", json=payload, headers=headers, timeout=10)
    print(f"[Deploy CDN] Sync response: {resp.status_code} - {resp.text}")
    if resp.status_code != 200:
        raise RuntimeError(f"Deploy failed: {resp.text}")

if __name__ == "__main__":
    main()
