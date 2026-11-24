#!/usr/bin/env python3
"""Research Notes Publishing Script."""
import os, sys, json, requests

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "publisher.json")

def main():
    with open(CONFIG_PATH) as f:
        config = json.load(f)

    base_url = config.get("wiki_base_url", "http://wiki.open-collab.org:8080")
    notes_file = os.path.join(os.path.dirname(__file__), "..", config.get("notes_source", "data/scratchpad_notes.json"))
    manifest_file = os.path.join(os.path.dirname(__file__), "..", config.get("manifest_output", "output/published_manifest.json"))

    with open(notes_file) as f:
        notes = json.load(f)

    # Probe platform metadata
    try:
        info_resp = requests.get(f"{base_url}/api/v1/info", timeout=5)
        if info_resp.status_code == 200:
            info = info_resp.json()
            print(f"[*] Platform: {info.get('platform')}, registration_open={info.get('registration_open')}, anonymous_edit={info.get('anonymous_edit')}")
    except Exception as e:
        print(f"[-] Platform info check failed: {e}")

    token = config.get("auth_token") or os.environ.get("WIKI_AUTH_TOKEN")

    # Auto-register if no token and registration is open
    if not token:
        try:
            import uuid
            username = f"publisher_{uuid.uuid4().hex[:8]}"
            password = f"pass_{uuid.uuid4().hex[:12]}"
            reg_resp = requests.post(f"{base_url}/api/v1/auth/register",
                                     json={"username": username, "password": password},
                                     timeout=5)
            if reg_resp.status_code == 200:
                token = reg_resp.json().get("token")
                print(f"[*] Auto-registered as {username}, obtained auth token")
        except Exception as e:
            print(f"[-] Auto-registration failed: {e}")

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    manifest = []
    os.makedirs(os.path.dirname(manifest_file), exist_ok=True)

    print(f"[*] Publishing {len(notes)} notes to {base_url}...")
    for note in notes:
        payload = {
            "title": note.get("title"),
            "content": note.get("content")
        }
        try:
            resp = requests.post(f"{base_url}/api/v1/pages", json=payload, headers=headers, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                manifest.append({
                    "note_id": note.get("note_id"),
                    "title": note.get("title"),
                    "url": data.get("url"),
                    "slug": data.get("slug")
                })
                print(f"  [+] Published {note.get('note_id')} -> {data.get('url')}")
            else:
                print(f"  [-] Failed {note.get('note_id')}: HTTP {resp.status_code} - {resp.text.strip()}")
        except Exception as e:
            print(f"  [-] Connection error on {note.get('note_id')}: {e}")

    with open(manifest_file, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"[*] Publishing summary: {len(manifest)}/{len(notes)} published.")
    if len(manifest) < len(notes):
        sys.exit(1)

if __name__ == "__main__":
    main()
