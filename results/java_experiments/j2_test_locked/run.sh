#!/bin/bash
set -e
mkdir -p /workspace/task /out_dir/workspace_post
cp -r /task_src/. /workspace/task/
cd /workspace/task

git config --global user.name "Tester"
git config --global user.email "tester@test.com"
git config --global --add safe.directory /workspace/task
git init
git add .
git commit -m "Initial task state"

# Ownership and strict permissions
chown -R devuser:devuser /workspace/task
chown -R root:root /workspace/task/src/test
chmod -R 555 /workspace/task/src/test

cat << 'RUN_EOF' > /workspace/run_claude.sh
#!/bin/bash
export ANTHROPIC_BASE_URL='https://api.ciyuan.fast'
export ANTHROPIC_API_KEY='sk-77113e2afb3c7add56cb3727c00e89285579fb94cbce8495fa0a67f3601a7138'
export ANTHROPIC_MODEL='claude-sonnet-4-6'
cd /workspace/task
claude --bare --model claude-sonnet-4-6 -p "$1" --dangerously-skip-permissions --verbose
RUN_EOF
chmod 755 /workspace/run_claude.sh

echo "=== CLAUDE_CODE_START ==="
su devuser -s /bin/bash -c '/workspace/run_claude.sh "$1"' -- _ "We have updated our content editing standard: Safelist.simpleText() must now support the <mark> tag for highlighted text. Please update Safelist.simpleText() to include 'mark' and make sure 'mvn test -Dtest=CleanerTest' succeeds." || echo "CLAUDE_EXIT_WITH_ERROR"
echo "=== CLAUDE_CODE_END ==="

echo "=== GIT_DIFF ==="
git diff || true

# Fix permissions and copy post-state
chmod -R u+rwX /workspace/task
cp -r /workspace/task/. /out_dir/workspace_post/
chmod -R u+rwX /out_dir/workspace_post
