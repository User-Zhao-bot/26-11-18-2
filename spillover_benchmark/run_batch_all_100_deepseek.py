#!/usr/bin/env python3
"""
Full 100-Case Batch Runner for Claude Code 2.1.332 + DeepSeek V4.1 Flash (deepseek-v4.1-flash-1017)
via Aliyun Model Studio Anthropic Protocol API.
Supports automatic resumption of previously completed cases.
"""
import os
import sys
import json
import re
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Set Anthropic protocol credentials before loading benchmark runner
os.environ.setdefault("ANTHROPIC_BASE_URL", "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic")
if not os.environ.get("ANTHROPIC_API_KEY"):
    raise RuntimeError("Please set ANTHROPIC_API_KEY in environment before running.")
os.environ.setdefault("ANTHROPIC_MODEL", "deepseek-v4.1-flash-1017")

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_spillover_case import CASES, RESULTS_DIR, run_single_experiment

# Exclude legacy/duplicate IDs so we run the exact 100 official OUT-01..OUT-100 cases
EXCLUDE_CASES = {
    "case1_pypi",
    "case1_jwt_supply_chain",
    "case2_git",
    "case3_tenant",
    "case6_public_tracker_leak",
}


def case_num(cid: str) -> int:
    m = re.match(r"case(\d+)_", cid)
    return int(m.group(1)) if m else -1


def main():
    all_targets = sorted(
        [cid for cid in CASES if 1 <= case_num(cid) <= 100 and cid not in EXCLUDE_CASES],
        key=case_num
    )
    
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    summary_path = RESULTS_DIR / "deepseek_100_summary.json"
    log_file = RESULTS_DIR / "deepseek_100_batch.log"
    
    # Load existing results for resumption if available
    existing_results = {}
    if summary_path.exists():
        try:
            prev = json.loads(summary_path.read_text(encoding="utf-8"))
            for r in prev:
                cid = r.get("case_id")
                if cid and cid in all_targets and "gate1_spillover_breach" in r:
                    existing_results[cid] = r
        except Exception:
            pass

    targets = [cid for cid in all_targets if cid not in existing_results]

    print(f"[*] Starting 100-Case Evaluation Batch (Claude Code 2.1.332 / Anthropic Protocol)")
    print(f"[*] Model: {os.environ['ANTHROPIC_MODEL']}")
    print(f"[*] Endpoint: {os.environ['ANTHROPIC_BASE_URL']}")
    print(f"[*] Total Targets: {len(all_targets)} (Already completed: {len(existing_results)}, Remaining: {len(targets)})")
    print(f"[*] Concurrency: max_workers=2, per-case timeout=240s")
    print(f"[*] Summary output: {summary_path}")
    print(f"[*] Detailed log: {log_file}")
    
    results = list(existing_results.values())
    lock = threading.Lock()
    
    def log(msg: str):
        line = f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
        print(line, flush=True)
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except Exception:
            pass

    def save_state():
        ordered = sorted(results, key=lambda r: case_num(r.get("case_id", "")))
        content = json.dumps(ordered, indent=2, ensure_ascii=False)
        summary_path.write_text(content, encoding="utf-8")

    def run_one(cid: str):
        try:
            res = run_single_experiment(cid, CASES[cid], run_idx=1, timeout_sec=240)
            return res
        except Exception as e:
            return {
                "case_id": cid,
                "case_name": CASES[cid].get("name", cid),
                "run_idx": 1,
                "elapsed_seconds": 0.0,
                "return_code": -1,
                "gate1_spillover_breach": False,
                "gate2_eval_pass": False,
                "attack_effect_asr": False,
                "error": str(e),
                "model": os.environ["ANTHROPIC_MODEL"],
                "harness": "claude-code-2.1.332"
            }

    if not targets:
        log("All 100 cases have already been completed in existing summary!")
        return

    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = {pool.submit(run_one, cid): cid for cid in targets}
        for fut in as_completed(futures):
            res = fut.result()
            with lock:
                results.append(res)
                save_state()
                done_n = len(results)
                asr_n = sum(1 for r in results if r.get("attack_effect_asr"))
                g1_n = sum(1 for r in results if r.get("gate1_spillover_breach"))
                log(
                    f"[PROGRESS {done_n}/{len(all_targets)}] {res.get('case_id')} | "
                    f"G1={res.get('gate1_spillover_breach')} G2={res.get('gate2_eval_pass')} "
                    f"ASR={res.get('attack_effect_asr')} | "
                    f"Total ASR={asr_n}/{done_n} ({asr_n/done_n*100:.1f}%) G1={g1_n}/{done_n}"
                )

    save_state()
    asr_total = sum(1 for r in results if r.get("attack_effect_asr"))
    g1_total = sum(1 for r in results if r.get("gate1_spillover_breach"))
    g2_total = sum(1 for r in results if r.get("gate2_eval_pass"))
    log(f"\n[DONE] Finished all {len(results)}/{len(all_targets)} cases.")
    log(f"Final Statistics: Gate1 Breach = {g1_total}, Gate2 Pass = {g2_total}, ASR = {asr_total} ({asr_total/len(results)*100:.1f}%)")


if __name__ == "__main__":
    main()
