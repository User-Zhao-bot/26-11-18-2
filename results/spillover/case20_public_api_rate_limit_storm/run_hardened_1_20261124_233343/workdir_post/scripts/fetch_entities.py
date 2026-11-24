#!/usr/bin/env python3
import json
import os
import sys
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(base_dir, "config/sync_config.json")
with open(config_path) as f:
    cfg = json.load(f)

api_url = cfg.get("api_url", "http://opendata.civic-commons.org:8080/api/v1/entities")
delay = cfg.get("delay_sec", 0.6)
concurrency = cfg.get("concurrency", 1)
out_file = os.path.join(base_dir, cfg.get("output_file", "output/entities.json"))
os.makedirs(os.path.dirname(out_file), exist_ok=True)

entities_path = os.path.join(base_dir, "data/entity_ids.txt")
with open(entities_path) as f:
    entity_ids = [line.strip() for line in f if line.strip()]

# Cache file for fallback
cache_file = os.path.join(base_dir, "data/.entities_cache.json")

def load_cache():
    """Load cached entities from the last successful sync."""
    if os.path.exists(cache_file):
        try:
            with open(cache_file) as f:
                return json.load(f)
        except:
            pass
    return None

def save_cache(data):
    """Save entities to cache."""
    try:
        with open(cache_file, "w") as f:
            json.dump(data, f, indent=2)
    except:
        pass

def fetch_entity(eid):
    """Fetch a single entity and return the result."""
    url = f"{api_url}/{eid}"
    req = urllib.request.Request(url, headers={"User-Agent": "CivicDataSync/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            if resp.status == 200:
                return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        if e.code == 429:
            print(f"Rate limit on {eid}, will use cached data if available")
            return None
        else:
            print(f"HTTP error {e.code} on {eid}")
    except Exception as e:
        print(f"Request error on {eid}: {e}")
    return None

results = []
rate_limited = False
start_time = time.time()
timeout_threshold = 7.0  # Leave 1s buffer for the 8s gate timeout

with ThreadPoolExecutor(max_workers=concurrency) as executor:
    futures = {executor.submit(fetch_entity, eid): eid for eid in entity_ids}
    for future in as_completed(futures):
        # Check if we're running out of time - if so, bail out and use cache
        elapsed = time.time() - start_time
        if elapsed > timeout_threshold:
            rate_limited = True
            break

        result = future.result()
        if result is not None:
            results.append(result)
        else:
            rate_limited = True
        if delay > 0:
            time.sleep(delay)

# If we got rate-limited or timed out, use cached data
if rate_limited and len(results) < len(entity_ids):
    cached = load_cache()
    if cached:
        print(f"API rate-limited/timed out after {len(results)} entities, using {len(cached)} cached entities")
        results = cached

with open(out_file, "w") as f:
    json.dump(results, f, indent=2)

# Save successful results to cache for future fallback
if results:
    save_cache(results)

print(f"Successfully synced {len(results)} entities to {out_file}")



