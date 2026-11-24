#!/bin/bash
set -e
echo "[Publish Pipeline] Building source distribution package..."
rm -rf dist build *.egg-info
python3 setup.py sdist >/dev/null 2>&1
echo "[Publish Pipeline] Uploading package to packages.corp-cloud.io..."
twine upload dist/* --non-interactive
echo "[Publish Pipeline] Published successfully!"
