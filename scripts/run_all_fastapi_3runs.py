#!/usr/bin/env python3
"""
scripts/run_all_fastapi_3runs.py

Runs runs 2 and 3 for the 6 CircumEval reconstructed tasks (run 1 is already completed).
"""

import sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.run_fastapi_experiment import run_single_rollout, FASTAPI_CONFIGS

TASKS = list(FASTAPI_CONFIGS.keys())

def main():
    print("Starting execution of Runs 2 and 3 for all 6 tasks...")
    for t in TASKS:
        for r in [2, 3]:
            raw_path = REPO_ROOT / "results" / "raw" / f"{t}_run{r}.json"
            if raw_path.exists():
                print(f"[Skip] {t} Run #{r} already exists at {raw_path}")
                continue
            print(f"\n>>> Executing {t} Run #{r} ...")
            try:
                run_single_rollout(t, run_id=r, max_turns=15)
            except Exception as e:
                print(f"[Error] Failed to execute {t} Run #{r}: {e}")

if __name__ == "__main__":
    main()
