#!/usr/bin/env bash
# Submit organize to HPC via vad-organize-submit (bsub).
# Usage: submit_organize.sh <model_path> <image_list_file> [output_dir]
set -euo pipefail
MODEL_PATH="${1:?model_path required}"
IMAGE_LIST="${2:?image_list_file required}"
OUTPUT_DIR="${3:-./score_review}"
ROOT="$(cd "$(dirname "$0")/../../../../" && pwd)"
cd "$ROOT"
RUN="vad-organize-submit"
if command -v uv >/dev/null 2>&1; then RUN="uv run vad-organize-submit"; fi
$RUN model_path="$MODEL_PATH" image_list_file="$IMAGE_LIST" output_dir="$OUTPUT_DIR"
echo "OK: vad-organize-submit completed"
