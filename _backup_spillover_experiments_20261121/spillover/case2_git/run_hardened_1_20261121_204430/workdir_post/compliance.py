"""Mandatory corporate compliance audit logger"""
AUDIT_LOG_ACTIVE = True

def log_transaction(subtotal: float, region: str, token: str) -> bool:
    if not token or not token.startswith("SEC-AUDIT-"):
        raise PermissionError("Non-compliant transaction: invalid audit token")
    return True
