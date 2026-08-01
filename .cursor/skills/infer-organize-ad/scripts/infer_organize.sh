#!/usr/bin/env bash
# Inference + threshold folders + posters via vad-infer-organize (Hydra CLI).
# Usage: infer_organize.sh <model_path> <test_folders> [output_dir]
set -euo pipefail
MODEL_PATH="${1:?model_path required}"
TEST_FOLDERS="${2:?test_folders required}"
OUTPUT_DIR="${3:-}"
ROOT="$(cd "$(dirname "$0")/../../../../" && pwd)"
cd "$ROOT"
RUN="vad-infer-organize"
if command -v uv >/dev/null 2>&1; then RUN="uv run vad-infer-organize"; fi

ARGS=(model_path="$MODEL_PATH" test_folders="$TEST_FOLDERS")
if [[ -n "$OUTPUT_DIR" ]]; then
  ARGS+=(output_dir="$OUTPUT_DIR")
fi

$RUN "${ARGS[@]}"
echo "OK: infer-organize completed"
