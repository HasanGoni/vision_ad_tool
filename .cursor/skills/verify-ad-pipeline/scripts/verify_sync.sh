#!/usr/bin/env bash
# Install/sync project dependencies.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"
if command -v uv >/dev/null 2>&1; then
  uv sync
else
  pip install -e .
fi
echo "OK: dependencies synced in $ROOT"
