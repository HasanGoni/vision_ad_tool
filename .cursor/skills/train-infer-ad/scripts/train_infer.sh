#!/usr/bin/env bash
# Train a model, then run inference/posters via vad-train-infer (Hydra CLI).
# Usage: train_infer.sh <data_root> <validation_images> [model_name]
set -euo pipefail
DATA_ROOT="${1:?data_root required}"
VALIDATION_IMAGES="${2:?validation_images required}"
MODEL_NAME="${3:-patchcore}"
ROOT="$(cd "$(dirname "$0")/../../../../" && pwd)"
cd "$ROOT"
RUN="vad-train-infer"
if command -v uv >/dev/null 2>&1; then RUN="uv run vad-train-infer"; fi

$RUN train.data_root="$DATA_ROOT" train.model_name="$MODEL_NAME" infer_after_training.validation_images="$VALIDATION_IMAGES"
echo "OK: train-infer completed"
