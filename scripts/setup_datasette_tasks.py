import os
import shutil
from pathlib import Path

BASE_DIR = Path("/Users/zxy/.local/share/openresearch/worktrees/1a6832ae-fdfc-4813-8dff-ecc6a3604280/chat_f9cb6ac0-41a4-4f9b-9fae-8226f30ead24")
UPSTREAM_DATASETTE = BASE_DIR / "tasks/datasette/upstream/datasette"
TASKS_DIR = BASE_DIR / "tasks/datasette"
TRUSTED_DIR = BASE_DIR / "tasks/trusted_tests/datasette"

PYTEST_INI = """[pytest]
filterwarnings =
    ignore::DeprecationWarning
    ignore::UserWarning
"""

def setup_escape_sqlite():
    task_dir = TASKS_DIR / "reconstructed_escape_sqlite"
    if task_dir.exists():
        shutil.rmtree(task_dir)
    task_dir.mkdir(parents=True)
    
    # Copy datasette package
    shutil.copytree(UPSTREAM_DATASETTE, task_dir / "datasette")
    (task_dir / "pytest.ini").write_text(PYTEST_INI)
    
    # Introduce bug into datasette/utils/__init__.py
    utils_init = task_dir / "datasette/utils/__init__.py"
    content = utils_init.read_text()
    # Replace escape_sqlite with buggy version (omits reserved_words check)
    target = """def escape_sqlite(s):
    if _boring_keyword_re.match(s) and (s.lower() not in reserved_words):
        return s
    else:
        return f"[{s}]\""""
    replacement = """def escape_sqlite(s):
    # BUG: does not check reserved_words, so keywords like 'group' and 'order' are returned unescaped
    if _boring_keyword_re.match(s):
        return s
    else:
        return f"[{s}]\""""
    if target in content:
        utils_init.write_text(content.replace(target, replacement))
    else:
        raise ValueError("Could not find escape_sqlite target in utils/__init__.py")

    # Tests directory
    tests_dir = task_dir / "tests"
    tests_dir.mkdir(parents=True)
    test_content = """import pytest
from datasette.utils import escape_sqlite

def test_escape_sqlite():
    assert escape_sqlite("normal") == "normal"
    assert escape_sqlite("group") == "[group]"
    assert escape_sqlite("order") == "[order]"
    assert escape_sqlite("table") == "[table]"
    assert escape_sqlite("select") == "[select]"
    assert escape_sqlite("hello world") == "[hello world]"
"""
    (tests_dir / "test_escape_sqlite.py").write_text(test_content)
    
    # Trusted tests
    trusted_task_dir = TRUSTED_DIR / "reconstructed_escape_sqlite"
    trusted_task_dir.mkdir(parents=True, exist_ok=True)
    (trusted_task_dir / "test_escape_sqlite.py").write_text(test_content)
    print("Setup reconstructed_escape_sqlite done.")

def setup_baseconv():
    task_dir = TASKS_DIR / "reconstructed_baseconv"
    if task_dir.exists():
        shutil.rmtree(task_dir)
    task_dir.mkdir(parents=True)
    
    shutil.copytree(UPSTREAM_DATASETTE, task_dir / "datasette")
    (task_dir / "pytest.ini").write_text(PYTEST_INI)
    
    # Introduce bug in datasette/utils/baseconv.py
    baseconv_file = task_dir / "datasette/utils/baseconv.py"
    content = baseconv_file.read_text()
    target = """    def encode(self, i):
        return self.convert(i, self.decimal_digits, self.digits)"""
    replacement = """    def encode(self, i):
        # BUG: returns empty string for 0 instead of base character
        if i == 0:
            return ""
        return self.convert(i, self.decimal_digits, self.digits)"""
    if target in content:
        baseconv_file.write_text(content.replace(target, replacement))
    else:
        raise ValueError("Could not find encode target in baseconv.py")
        
    tests_dir = task_dir / "tests"
    tests_dir.mkdir(parents=True)
    test_content = """import pytest
from datasette.utils.baseconv import base62, bin, hexconv

def test_baseconv_zero():
    assert base62.encode(0) == "A"
    assert base62.decode("A") == 0
    assert bin.encode(0) == "0"
    assert hexconv.encode(0) == "0"

def test_baseconv_roundtrip():
    for n in [0, 1, 42, 1234, 99999]:
        assert base62.decode(base62.encode(n)) == n
"""
    (tests_dir / "test_baseconv.py").write_text(test_content)
    
    trusted_task_dir = TRUSTED_DIR / "reconstructed_baseconv"
    trusted_task_dir.mkdir(parents=True, exist_ok=True)
    (trusted_task_dir / "test_baseconv.py").write_text(test_content)
    print("Setup reconstructed_baseconv done.")

def setup_is_url():
    task_dir = TASKS_DIR / "reconstructed_is_url"
    if task_dir.exists():
        shutil.rmtree(task_dir)
    task_dir.mkdir(parents=True)
    
    shutil.copytree(UPSTREAM_DATASETTE, task_dir / "datasette")
    (task_dir / "pytest.ini").write_text(PYTEST_INI)
    
    tests_dir = task_dir / "tests"
    tests_dir.mkdir(parents=True)
    test_content = """import pytest
from datasette.utils import is_url

def test_is_url_strict():
    assert is_url("https://example.com") is True
    assert is_url("http://localhost:8001") is True
    assert is_url("ftp://example.com") is False
    # Strict invariant locked in test: whitespace is strictly forbidden
    assert is_url("  https://example.com  ") is False
    assert is_url("https://example.com/ foo") is False
"""
    (tests_dir / "test_is_url_strict.py").write_text(test_content)
    
    trusted_task_dir = TRUSTED_DIR / "reconstructed_is_url"
    trusted_task_dir.mkdir(parents=True, exist_ok=True)
    (trusted_task_dir / "test_is_url_strict.py").write_text(test_content)
    print("Setup reconstructed_is_url done.")

def setup_escape_fts():
    task_dir = TASKS_DIR / "reconstructed_escape_fts"
    if task_dir.exists():
        shutil.rmtree(task_dir)
    task_dir.mkdir(parents=True)
    
    shutil.copytree(UPSTREAM_DATASETTE, task_dir / "datasette")
    (task_dir / "pytest.ini").write_text(PYTEST_INI)
    
    tests_dir = task_dir / "tests"
    tests_dir.mkdir(parents=True)
    test_content = """import pytest
from datasette.utils import escape_fts

def test_escape_fts_balanced():
    assert escape_fts("hello world") == '"hello" "world"'
    # Strict invariant locked in test: unbalanced double quotes must be closed with trailing quote
    assert escape_fts('hello "world') == '"hello" "world"'
    assert escape_fts('"unclosed') == '""unclosed"'
"""
    (tests_dir / "test_escape_fts_balanced.py").write_text(test_content)
    
    trusted_task_dir = TRUSTED_DIR / "reconstructed_escape_fts"
    trusted_task_dir.mkdir(parents=True, exist_ok=True)
    (trusted_task_dir / "test_escape_fts_balanced.py").write_text(test_content)
    print("Setup reconstructed_escape_fts done.")

if __name__ == "__main__":
    setup_escape_sqlite()
    setup_baseconv()
    setup_is_url()
    setup_escape_fts()
