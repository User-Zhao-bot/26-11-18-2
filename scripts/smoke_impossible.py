#!/usr/bin/env python3
"""
scripts/smoke_impossible.py

Reproducible runner for ImpossibleBench P0 Smoke tests:
- impossible_livecodebench: conflicting (limit=2), original (limit=2)
- impossible_swebench: conflicting (agent_type="tools", limit=1)

Outputs real .eval logs to results/raw/ and summary tables to results/tables/.
"""

import os
import sys
import json
import argparse
from pathlib import Path

# Load environment
import dotenv
dotenv.load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from inspect_ai import eval
from inspect_ai.log import read_eval_log
from impossiblebench import impossible_livecodebench, impossible_swebench



def run_livecodebench(split: str, limit: int = 2, agent_type: str = "minimal"):
    print(f"\n==========================================")
    print(f"Running LiveCodeBench: split={split}, limit={limit}, agent_type={agent_type}")
    print(f"==========================================")
    
    task = impossible_livecodebench(
        split=split,
        agent_type=agent_type,
        limit=limit,
    )
    
    model = os.environ.get("INSPECT_MODEL", "openai/deepseek-v4.1-flash")
    raw_dir = Path(__file__).resolve().parent.parent / "results" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    logs = eval(
        task,
        model=model,
        model_args={"client_timeout": 300.0},
        max_samples=1,
        max_subprocesses=1,
        log_dir=str(raw_dir),
    )
    return logs


def run_swebench(split: str = "conflicting", limit: int = 1, agent_type: str = "tools", instance_id: str = "django__django-10554"):
    print(f"\n==========================================")
    print(f"Running SWE-bench: split={split}, instance={instance_id}, limit={limit}, agent_type={agent_type}")
    print(f"==========================================")
    
    task = impossible_swebench(
        split=split,
        instance_ids=[instance_id] if instance_id else None,
        agent_type=agent_type,
        build_docker_images=False,
        docker_image_from_id=lambda id: "swebench/sweb.eval.x86_64.django_1776_django-10554:latest",
        max_attempts=3,
        limit=limit,
    )
    
    model = os.environ.get("INSPECT_MODEL", "openai/deepseek-v4.1-flash")
    raw_dir = Path(__file__).resolve().parent.parent / "results" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    logs = eval(
        task,
        model=model,
        model_args={"client_timeout": 300.0},
        max_samples=1,
        max_subprocesses=1,
        log_dir=str(raw_dir),
    )
    return logs


def parse_and_export_summary():
    raw_dir = Path(__file__).resolve().parent.parent / "results" / "raw"
    tables_dir = Path(__file__).resolve().parent.parent / "results" / "tables"
    tables_dir.mkdir(parents=True, exist_ok=True)
    
    eval_files = list(raw_dir.glob("*.eval"))
    print(f"\nFound {len(eval_files)} .eval files in {raw_dir}")
    
    all_results = []
    for f in eval_files:
        try:
            log = read_eval_log(str(f))
            task_name = log.eval.task
            model_name = log.eval.model
            created = log.eval.created
            
            for s in (log.samples or []):
                score_val = None
                if s.scores:
                    first_scorer = list(s.scores.values())[0]
                    score_val = first_scorer.value
                
                all_results.append({
                    "eval_file": f.name,
                    "task": task_name,
                    "sample_id": s.id,
                    "model": model_name,
                    "score": score_val,
                    "error": str(s.error) if s.error else None,
                    "created": created,
                })
        except Exception as e:
            print(f"Error parsing {f}: {e}")
            
    if all_results:
        import pandas as pd
        df = pd.DataFrame(all_results)
        csv_path = tables_dir / "p0_summary.csv"
        df.to_csv(csv_path, index=False)
        print(f"Saved summary to {csv_path}")
        print(df[["task", "sample_id", "model", "score", "error"]])
    else:
        print("No eval results parsed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run ImpossibleBench smoke evaluations")
    parser.add_argument("--mode", choices=["lcb", "swe", "all", "summary"], default="all")
    parser.add_argument("--lcb-split", choices=["conflicting", "original", "both"], default="both")
    parser.add_argument("--lcb-limit", type=int, default=2)
    parser.add_argument("--lcb-agent-type", choices=["minimal", "tools"], default="minimal")
    parser.add_argument("--swe-limit", type=int, default=1)
    
    args = parser.parse_args()
    
    if args.mode in ["lcb", "all"]:
        if args.lcb_split in ["conflicting", "both"]:
            run_livecodebench("conflicting", limit=args.lcb_limit, agent_type=args.lcb_agent_type)
        if args.lcb_split in ["original", "both"]:
            run_livecodebench("original", limit=args.lcb_limit, agent_type=args.lcb_agent_type)
            
    if args.mode in ["swe", "all"]:
        run_swebench("conflicting", limit=args.swe_limit, agent_type="tools")
        
    parse_and_export_summary()
