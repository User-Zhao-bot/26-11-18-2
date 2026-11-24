#!/usr/bin/env python3
"""
scripts/run_all_codex_cases.py

Runs all 6 CircumEval reconstructed tasks under Codex CLI harness:
1. reconstructed_encoder_exclude_none (already done)
2. reconstructed_oauth_expiry
3. reconstructed_status_204
4. reconstructed_encoder_lookup
5. reconstructed_exclude_none
6. reconstructed_sa_filter
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.run_codex_fastapi_experiment import run_codex_on_task

TASKS = [
    "reconstructed_oauth_expiry",
    "reconstructed_status_204",
    "reconstructed_encoder_lookup",
    "reconstructed_exclude_none",
    "reconstructed_sa_filter",
]

def main():
    print("Starting execution of remaining CircumEval tasks under Codex CLI...")
    for t in TASKS:
        print(f"\n>>>>>>>> Running task: {t} <<<<<<<<")
        try:
            res = run_codex_on_task(t, run_id=1, timeout=900)
            print(f"Task {t} finished. Status: {res.get('oracle', {}).get('run_status')}")
        except Exception as e:
            print(f"Task {t} encountered error: {e}")

if __name__ == "__main__":
    main()
