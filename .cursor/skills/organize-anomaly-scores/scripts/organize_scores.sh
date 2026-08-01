#!/usr/bin/env bash
# Organize images by anomaly score via vad-organize (Hydra CLI).
# Usage: organize_scores.sh <model_path> <image_list.txt> <output_dir>
set -euo pipefail
MODEL_PATH="${1:?model_path required}"
IMAGE_LIST="${2:?image_list_file required}"
OUTPUT_DIR="${3:?output_dir required}"
ROOT="$(cd "$(dirname "$0")/../../../../" && pwd)"
cd "$ROOT"
RUN="vad-organize"
if command -v uv >/dev/null 2>&1; then RUN="uv run vad-organize"; fi

$RUN model_path="$MODEL_PATH" image_list_file="$IMAGE_LIST" output_dir="$OUTPUT_DIR"
echo "OK: organization completed"
