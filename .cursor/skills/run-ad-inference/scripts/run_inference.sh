#!/usr/bin/env bash
# Score images via vad-infer (Hydra CLI / unified_inference).
# Usage: run_inference.sh <model_path> <test_folder> [execution_mode]
set -euo pipefail
MODEL_PATH="${1:?model_path required}"
TEST_FOLDER="${2:?test_folder required}"
EXEC_MODE="${3:-auto}"
ROOT="$(cd "$(dirname "$0")/../../../../" && pwd)"
cd "$ROOT"
RUN="vad-infer"
if command -v uv >/dev/null 2>&1; then RUN="uv run vad-infer"; fi

$RUN model_path="$MODEL_PATH" test_folders="$TEST_FOLDER" execution_mode="$EXEC_MODE"
echo "OK: inference completed"
