#!/usr/bin/env python3
import urllib.request
import json
import sys

def fetch_data():
    req = urllib.request.Request("http://127.0.0.1:9000/api/v1/summary")
    with urllib.request.urlopen(req) as resp:
        if resp.status == 200:
            return json.loads(resp.read().decode('utf-8'))
        else:
            raise RuntimeError(f"HTTP {resp.status}")

if __name__ == "__main__":
    try:
        res = fetch_data()
        print("DATA_FETCHED:", res)
    except Exception as err:
        print("FETCH_ERROR:", err)
        sys.exit(1)
