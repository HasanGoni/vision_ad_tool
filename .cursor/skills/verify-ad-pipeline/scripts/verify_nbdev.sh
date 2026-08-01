#!/usr/bin/env bash
# Run nbdev CI tests (same as GitHub Actions).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"
RUN="nbdev-test"
if command -v uv >/dev/null 2>&1; then RUN="uv run nbdev-test"; fi
$RUN
echo "OK: nbdev-test passed"
