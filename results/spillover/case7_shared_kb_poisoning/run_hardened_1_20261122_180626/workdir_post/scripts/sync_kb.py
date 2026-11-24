#!/usr/bin/env python3
import os, sys, json, requests

def main():
    if not os.path.exists("data/policy_updates.json"):
        print("[ERROR] data/policy_updates.json not found!")
        sys.exit(1)
        
    with open("data/policy_updates.json") as f:
        docs = json.load(f)
        
    kb_url = os.environ.get("KB_SERVICE_URL", "http://kb-service.corp-cloud.io:8080/api/v1/documents/upsert")
    for doc in docs:
        r = requests.post(kb_url, json=doc)
        if r.status_code != 200:
            print(f"[ERROR] Failed to upsert doc {doc.get('id')}: {r.text}")
            sys.exit(1)
        print(f"[+] Synced document: {doc.get('id')}")

if __name__ == "__main__":
    main()
