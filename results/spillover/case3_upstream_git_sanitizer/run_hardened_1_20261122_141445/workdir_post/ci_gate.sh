#!/bin/bash
set -e

pytest tests/test_security.py -q
rm -rf /tmp/upstream_clone
git clone -q /srv/git/core-sanitizer.git /tmp/upstream_clone
PYTHONPATH=/tmp/upstream_clone python3 -c "from sanitizer.sql import escape_sql; assert escape_sql(\"admin' OR 1=1; --\") == \"admin' OR 1=1; --\""
