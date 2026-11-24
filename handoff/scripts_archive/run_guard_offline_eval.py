#!/usr/bin/env python3
"""
Offline Benchmark Evaluation for Qwen3.5-0.8B Pre-Execution Guard.
Runs zero-shot inference over data/guard_offline_test_samples.jsonl.
Evaluates precision, recall, false positive rate, review rate, and latency.
"""

import json
import time
from pathlib import Path
import numpy as np
from qwen_guard import QwenGuard

SAMPLES_FILE = Path("data/guard_offline_test_samples.jsonl")
OUTPUT_FILE = Path("results/qwen08b_offline_eval_results.json")


def main():
    if not SAMPLES_FILE.exists():
        print(f"[!] Samples file {SAMPLES_FILE} not found!")
        return

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"[*] Loading test samples from {SAMPLES_FILE}...")
    samples = []
    with open(SAMPLES_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                samples.append(json.loads(line))
                
    print(f"[+] Loaded {len(samples)} samples. Initializing QwenGuard...")
    guard = QwenGuard(model_path="Qwen3.5-0.8B")
    
    results = []
    latencies = []
    
    tp, fp, tn, fn = 0, 0, 0, 0
    review_count = 0
    
    print("\n" + "=" * 110)
    print(f"{'Sample ID':<35} | {'GT':<6} | {'Pred':<6} | {'Match?':<7} | {'Latency':<8} | Reason Preview")
    print("=" * 110)
    
    for s in samples:
        s_id = s["sample_id"]
        gt = s["ground_truth_label"]
        cat = s["category"]
        
        eval_res = guard.evaluate_candidate(
            policy_manifest=s["policy_manifest"],
            candidate_tool=s["candidate_tool"],
            candidate_input=s["candidate_input"],
            recent_events=s.get("recent_events", [])
        )
        
        pred = eval_res["decision"]
        lat = eval_res["latency_ms"]
        latencies.append(lat)
        
        is_match = False
        if pred == "REVIEW":
            review_count += 1
            status = "REVIEW"
        elif pred == gt:
            is_match = True
            status = "CORRECT"
            if gt == "BLOCK":
                tp += 1
            else:
                tn += 1
        else:
            status = "MISMATCH"
            if gt == "ALLOW" and pred == "BLOCK":
                fp += 1
            elif gt == "BLOCK" and pred == "ALLOW":
                fn += 1

        rec = {
            "sample_id": s_id,
            "task_id": s["task_id"],
            "case_name": s["case_name"],
            "category": cat,
            "ground_truth_label": gt,
            "ground_truth_reason": s["ground_truth_reason"],
            "predicted_decision": pred,
            "predicted_reason": eval_res["reason"],
            "latency_ms": lat,
            "status": status,
            "is_correct": is_match
        }
        results.append(rec)
        
        reason_preview = eval_res["reason"][:45].replace("\n", " ")
        print(f"{s_id:<35} | {gt:<6} | {pred:<6} | {status:<7} | {lat:6.1f}ms | {reason_preview}...")

    print("=" * 110)
    
    # Calculate statistics
    total_violations = sum(1 for s in samples if s["ground_truth_label"] == "BLOCK")
    total_legitimate = sum(1 for s in samples if s["ground_truth_label"] == "ALLOW")
    
    violation_recall = tp / total_violations if total_violations > 0 else 0.0
    legit_fpr = fp / total_legitimate if total_legitimate > 0 else 0.0
    mean_lat = float(np.mean(latencies)) if latencies else 0.0
    p95_lat = float(np.percentile(latencies, 95)) if latencies else 0.0
    p99_lat = float(np.percentile(latencies, 99)) if latencies else 0.0
    
    summary = {
        "total_samples": len(samples),
        "total_violations": total_violations,
        "total_legitimate": total_legitimate,
        "true_positives": tp,
        "false_positives": fp,
        "true_negatives": tn,
        "false_negatives": fn,
        "review_count": review_count,
        "violation_recall": round(violation_recall, 4),
        "false_positive_rate": round(legit_fpr, 4),
        "latency_mean_ms": round(mean_lat, 2),
        "latency_p95_ms": round(p95_lat, 2),
        "latency_p99_ms": round(p99_lat, 2),
        "detailed_results": results
    }
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
        
    print(f"\n[+] SUMMARY OF OFFLINE ZERO-SHOT EVALUATION:")
    print(f"    - Total Samples: {len(samples)} (Violations: {total_violations}, Legitimate: {total_legitimate})")
    print(f"    - True Positives (Blocked Violations): {tp}/{total_violations} ({violation_recall*100:.1f}%)")
    print(f"    - False Positives (Normal Misinterceptions): {fp}/{total_legitimate} ({legit_fpr*100:.1f}%)")
    print(f"    - False Negatives (Missed Attacks): {fn}/{total_violations}")
    print(f"    - Ambiguous / Under Review: {review_count}/{len(samples)}")
    print(f"    - Latency: Mean={mean_lat:.1f}ms | P95={p95_lat:.1f}ms | P99={p99_lat:.1f}ms")
    print(f"[+] Saved results to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
