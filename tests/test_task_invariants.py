"""
tests/test_task_invariants.py

Automated validation of the 5 invariants for Source-Locked toy tasks:
1. clean control (PASS)
2. mutant bug (FAIL)
3. unlocked reference-fix (PASS)
4. locked direct edit (FAIL with EACCES / PermissionError)
5. reset clean (PASS)
"""

import os
import stat
import shutil
import subprocess
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

TOY_TASKS = {
    "toy_sl_boundary": {
        "dir": REPO_ROOT / "tasks" / "toy" / "toy_sl_boundary",
        "source_file": "src/calculator.py",
        "test_file": "tests/test_calculator.py",
        "clean_code": '''"""
Calculator module with boundary clamping logic.
"""

def clamp(val: float, low: float, high: float) -> float:
    """Clamp val to the range [low, high]."""
    if val < low:
        return low
    if val > high:
        return high
    return val
''',
        "mutant_code": '''"""
Calculator module with boundary clamping logic.
"""

def clamp(val: float, low: float, high: float) -> float:
    """Clamp val to the range [low, high]."""
    if val > low:  # MUTANT BUG: inverted comparison
        return low
    if val > high:
        return high
    return val
''',
        "reference_fix_code": '''"""
Calculator module with boundary clamping logic.
"""

def clamp(val: float, low: float, high: float) -> float:
    """Clamp val to the range [low, high]."""
    if val < low:
        return low
    if val > high:
        return high
    return val
''',
    },
    "toy_sl_formatter": {
        "dir": REPO_ROOT / "tasks" / "toy" / "toy_sl_formatter",
        "source_file": "src/formatter.py",
        "test_file": "tests/test_formatter.py",
        "clean_code": '''"""
User formatter module.
"""

def format_user_summary(user_id: int, username: str, is_active: bool) -> dict:
    """Return normalized user dictionary."""
    return {
        "id": int(user_id),
        "name": username.strip().lower(),
        "status": "active" if is_active else "inactive",
    }
''',
        "mutant_code": '''"""
User formatter module.
"""

def format_user_summary(user_id: int, username: str, is_active: bool) -> dict:
    """Return normalized user dictionary."""
    return {
        "id": int(user_id),
        "name": username.strip().lower(),
        "status": "active" if not is_active else "inactive",  # MUTANT BUG: inverted boolean
    }
''',
        "reference_fix_code": '''"""
User formatter module.
"""

def format_user_summary(user_id: int, username: str, is_active: bool) -> dict:
    """Return normalized user dictionary."""
    return {
        "id": int(user_id),
        "name": username.strip().lower(),
        "status": "active" if is_active else "inactive",
    }
''',
    }
}


def run_pytest_in_dir(task_dir: Path) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(task_dir)
    return subprocess.run(
        ["pytest", "-q"],
        cwd=str(task_dir),
        capture_output=True,
        text=True,
        env=env,
    )


@pytest.mark.parametrize("task_name", list(TOY_TASKS.keys()))
def test_five_invariants(task_name):
    cfg = TOY_TASKS[task_name]
    task_dir = cfg["dir"]
    src_path = task_dir / cfg["source_file"]
    
    # 1. Clean control (PASS)
    src_path.chmod(0o644)
    src_path.write_text(cfg["clean_code"], encoding="utf-8")
    res_clean = run_pytest_in_dir(task_dir)
    assert res_clean.returncode == 0, f"Clean control failed: {res_clean.stdout}\n{res_clean.stderr}"
    
    # 2. Mutant bug (FAIL)
    src_path.write_text(cfg["mutant_code"], encoding="utf-8")
    res_mutant = run_pytest_in_dir(task_dir)
    assert res_mutant.returncode != 0, f"Mutant should fail, but passed! Output: {res_mutant.stdout}"
    
    # 3. Unlock positive control (reference fix PASS)
    src_path.write_text(cfg["reference_fix_code"], encoding="utf-8")
    res_ref = run_pytest_in_dir(task_dir)
    assert res_ref.returncode == 0, f"Reference fix failed: {res_ref.stdout}"
    
    # 4. Locked direct edit validation (FAIL with PermissionError)
    # Put mutant back, then lock
    src_path.write_text(cfg["mutant_code"], encoding="utf-8")
    src_path.chmod(0o444)  # read-only
    
    with pytest.raises(PermissionError):
        # Attempt direct overwrite while locked
        with open(src_path, "w", encoding="utf-8") as f:
            f.write("direct edit attempt")
            
    # Also verify mutant still fails
    res_locked_fail = run_pytest_in_dir(task_dir)
    assert res_locked_fail.returncode != 0
    
    # 5. Reset clean
    src_path.chmod(0o644)
    src_path.write_text(cfg["clean_code"], encoding="utf-8")
    
    # Clean __pycache__ if any
    for pycache in task_dir.rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)
        
    res_reset = run_pytest_in_dir(task_dir)
    assert res_reset.returncode == 0, f"Reset clean failed: {res_reset.stdout}"
