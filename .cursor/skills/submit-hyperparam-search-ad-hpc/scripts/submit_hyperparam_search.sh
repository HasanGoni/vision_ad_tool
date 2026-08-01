#!/usr/bin/env bash
# Submit hyperparam search to HPC via vad-hyperparam-search-submit (bsub).
# Usage: submit_hyperparam_search.sh <data_root> <test_images> [class_name]
set -euo pipefail
DATA_ROOT="${1:?data_root required}"
TEST_IMAGES="${2:?test_images required}"
CLASS_NAME="${3:-hyperparam_search}"
ROOT="$(cd "$(dirname "$0")/../../../../" && pwd)"
cd "$ROOT"
RUN="vad-hyperparam-search-submit"
if command -v uv >/dev/null 2>&1; then RUN="uv run vad-hyperparam-search-submit"; fi
$RUN data_root="$DATA_ROOT" test_images="$TEST_IMAGES" class_name="$CLASS_NAME"
echo "OK: vad-hyperparam-search-submit completed"
