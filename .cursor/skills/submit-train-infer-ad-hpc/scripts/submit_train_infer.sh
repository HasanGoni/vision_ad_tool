#!/usr/bin/env bash
# Submit train-infer to HPC via vad-train-infer-submit (bsub).
# Usage: submit_train_infer.sh <data_root> <validation_images> [model_name]
set -euo pipefail
DATA_ROOT="${1:?data_root required}"
VAL_IMAGES="${2:?validation_images required}"
MODEL_NAME="${3:-patchcore}"
ROOT="$(cd "$(dirname "$0")/../../../../" && pwd)"
cd "$ROOT"
RUN="vad-train-infer-submit"
if command -v uv >/dev/null 2>&1; then RUN="uv run vad-train-infer-submit"; fi
$RUN train.data_root="$DATA_ROOT" train.model_name="$MODEL_NAME" infer_after_training.validation_images="$VAL_IMAGES"
echo "OK: vad-train-infer-submit completed"
