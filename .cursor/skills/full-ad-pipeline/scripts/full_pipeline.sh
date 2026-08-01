#!/usr/bin/env bash
# Full train + infer-organize pipeline via vad-full (Hydra CLI).
# Usage: full_pipeline.sh <data_root> <test_folders> [model_name]
set -euo pipefail
DATA_ROOT="${1:?data_root required}"
TEST_FOLDERS="${2:?test_folders required}"
MODEL_NAME="${3:-patchcore}"
ROOT="$(cd "$(dirname "$0")/../../../../" && pwd)"
cd "$ROOT"
RUN="vad-full"
if command -v uv >/dev/null 2>&1; then RUN="uv run vad-full"; fi

$RUN train.data_root="$DATA_ROOT" train.model_name="$MODEL_NAME" infer_organize.test_folders="$TEST_FOLDERS"
echo "OK: full pipeline completed"
