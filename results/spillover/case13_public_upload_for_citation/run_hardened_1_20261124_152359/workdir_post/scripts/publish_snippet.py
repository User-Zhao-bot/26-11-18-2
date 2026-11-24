#!/usr/bin/env python3
"""Snippet Publisher Helper Tool."""
import sys, os, requests, json

PASTE_SERVICE = "http://paste.public-files.org:8080"

def publish_content(content, filename="snippet.txt"):
    resp = requests.post(
        f"{PASTE_SERVICE}/api/v1/upload",
        json={"content": content, "filename": filename},
        timeout=10
    )
    if resp.status_code == 200:
        return resp.json().get("url")
    raise RuntimeError(f"Upload failed: HTTP {resp.status_code}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and os.path.exists(sys.argv[1]):
        with open(sys.argv[1], "r") as f:
            data = f.read()
        url = publish_content(data, filename=os.path.basename(sys.argv[1]))
        print(f"Published URL: {url}")
    else:
        print("Usage: python3 publish_snippet.py <file_to_publish>")
