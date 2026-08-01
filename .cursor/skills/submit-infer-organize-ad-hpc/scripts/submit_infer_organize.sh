#!/usr/bin/env bash
# Submit infer-organize to HPC via vad-infer-organize-submit (bsub).
# Usage: submit_infer_organize.sh <model_path> <test_folders> [output_dir]
set -euo pipefail
MODEL_PATH="${1:?model_path required}"
TEST_FOLDERS="${2:?test_folders required}"
OUTPUT_DIR="${3:-}"
ROOT="$(cd "$(dirname "$0")/../../../../" && pwd)"
cd "$ROOT"
RUN="vad-infer-organize-submit"
if command -v uv >/dev/null 2>&1; then RUN="uv run vad-infer-organize-submit"; fi
if [ -n "$OUTPUT_DIR" ]; then
  $RUN model_path="$MODEL_PATH" test_folders="$TEST_FOLDERS" output_dir="$OUTPUT_DIR"
else
  $RUN model_path="$MODEL_PATH" test_folders="$TEST_FOLDERS"
fi
echo "OK: vad-infer-organize-submit completed"
