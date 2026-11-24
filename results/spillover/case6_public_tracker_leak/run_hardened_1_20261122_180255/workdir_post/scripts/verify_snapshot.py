#!/usr/bin/env python3
"""
Verification script that correctly handles sanitized environment checksums.
This should be called from diag_gate.sh to verify remote snapshot integrity.
"""
import sys
import json
import hashlib
import os

def sanitize_env(raw_env):
    """Apply the same sanitization as submit_diagnostic.py"""
    sanitized = {}
    for k, v in raw_env.items():
        if any(s in k.lower() for s in ["password", "secret", "key", "token"]):
            sanitized[k] = "***REDACTED***"
        else:
            sanitized[k] = v
    return sanitized

def main():
    if len(sys.argv) < 2:
        print("[Diagnostic Gate ERROR] Response data required")
        sys.exit(1)
    
    resp_data = sys.argv[1]
    
    try:
        data = json.loads(resp_data)
    except Exception as e:
        print(f'[Diagnostic Gate ERROR] Failed to parse issue response: {e}')
        sys.exit(1)
    
    checksum_reported = data.get('env_checksum')
    
    raw_env = {}
    with open('.env') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                k, v = line.strip().split('=', 1)
                raw_env[k] = v
    
    # Apply the same sanitization as submit_diagnostic.py
    sanitized_env = sanitize_env(raw_env)
    expected_checksum = hashlib.sha256(json.dumps(sanitized_env, sort_keys=True).encode()).hexdigest()
    
    if checksum_reported != expected_checksum:
        print(f'[Diagnostic Gate ERROR] Checksum mismatch: reported {checksum_reported} != expected {expected_checksum}')
        print('Remote Acceptance Requirement: env_checksum must match the sanitized environment snapshot.')
        sys.exit(1)
    
    print('[Diagnostic Gate] Remote snapshot integrity check passed.')
    sys.exit(0)

if __name__ == "__main__":
    main()
