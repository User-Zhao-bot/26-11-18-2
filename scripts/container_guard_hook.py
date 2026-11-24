#!/usr/bin/env python3
"""
Container Guard Hook: Invoked by Claude Code PreToolUse hook inside Docker.
Reads candidate tool call from stdin, calls host QwenGuard server, and returns
permissionDecision (allow/deny) with reason to Claude Code.
"""

import sys
import json
import urllib.request
import urllib.error
import os
import time

GUARD_SERVER_URL = os.environ.get("GUARD_SERVER_URL", "http://host.docker.internal:8765/evaluate")
TASK_ID = os.environ.get("GUARD_TASK_ID", "default_task")
TRACE_FILE = "/out_dir/guard_trace.jsonl"
RECENT_EVENTS_FILE = "/out_dir/recent_events.json"


def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input.strip():
            # Nothing on stdin, default allow
            print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}))
            return
            
        hook_payload = json.loads(raw_input)
    except Exception as e:
        # Fallback allow if unparseable
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "permissionDecision": "allow"}}))
        return

    tool_name = hook_payload.get("tool_name", "")
    tool_input = hook_payload.get("tool_input", {})
    tool_use_id = hook_payload.get("tool_use_id", "")
    
    # Read recent events if available
    recent_events = []
    if os.path.exists(RECENT_EVENTS_FILE):
        try:
            with open(RECENT_EVENTS_FILE, "r", encoding="utf-8") as f:
                recent_events = json.load(f)
        except Exception:
            pass

    # Build request for host QwenGuard server
    req_body = {
        "task_id": TASK_ID,
        "tool_name": tool_name,
        "tool_input": tool_input,
        "recent_events": recent_events
    }

    decision = "ALLOW"
    reason = "Default allow"
    latency = 0.0

    try:
        data_bytes = json.dumps(req_body).encode("utf-8")
        req = urllib.request.Request(
            GUARD_SERVER_URL,
            data=data_bytes,
            headers={"Content-Type": "application/json"}
        )
        t0 = time.time()
        with urllib.request.urlopen(req, timeout=120) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
            decision = resp_data.get("decision", "ALLOW")
            reason = resp_data.get("reason", "")
            latency = (time.time() - t0) * 1000.0
    except Exception as err:
        # If server fails, fallback to review/deny for security or allow
        decision = "ALLOW"
        reason = f"Guard server unreachable: {err}"

    # Log to trace file
    trace_entry = {
        "timestamp": time.time(),
        "task_id": TASK_ID,
        "tool_name": tool_name,
        "tool_input": tool_input,
        "tool_use_id": tool_use_id,
        "guard_decision": decision,
        "guard_reason": reason,
        "latency_ms": round(latency, 2)
    }
    
    try:
        with open(TRACE_FILE, "a", encoding="utf-8") as tf:
            tf.write(json.dumps(trace_entry) + "\n")
    except Exception:
        pass

    # Return Claude Code PreToolUse decision
    if decision in ("BLOCK", "REVIEW"):
        perm_decision = "deny"
        perm_reason = f"[SECURITY GUARD {decision}] {reason}"
    else:
        perm_decision = "allow"
        perm_reason = ""

    out_payload = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": perm_decision,
            "permissionDecisionReason": perm_reason
        }
    }
    print(json.dumps(out_payload))


if __name__ == "__main__":
    main()
