#!/usr/bin/env bash
# Submit full pipeline to HPC via vad-full-submit (bsub).
# Usage: submit_full.sh <data_root> <test_folders> [model_name]
set -euo pipefail
DATA_ROOT="${1:?data_root required}"
TEST_FOLDERS="${2:?test_folders required}"
MODEL_NAME="${3:-patchcore}"
ROOT="$(cd "$(dirname "$0")/../../../../" && pwd)"
cd "$ROOT"
RUN="vad-full-submit"
if command -v uv >/dev/null 2>&1; then RUN="uv run vad-full-submit"; fi
$RUN train.data_root="$DATA_ROOT" train.model_name="$MODEL_NAME" infer_organize.test_folders="$TEST_FOLDERS"
echo "OK: vad-full-submit completed"
