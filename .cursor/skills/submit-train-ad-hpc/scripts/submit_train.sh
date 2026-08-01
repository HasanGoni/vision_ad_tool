#!/usr/bin/env bash
# Submit training to HPC via vad-train-submit (bsub).
# Usage: submit_train.sh <data_root> [model_name] [class_name]
set -euo pipefail
DATA_ROOT="${1:?data_root required}"
MODEL_NAME="${2:-patchcore}"
CLASS_NAME="${3:-anomaly_detection}"
ROOT="$(cd "$(dirname "$0")/../../../../" && pwd)"
cd "$ROOT"
RUN="vad-train-submit"
if command -v uv >/dev/null 2>&1; then RUN="uv run vad-train-submit"; fi
$RUN data_root="$DATA_ROOT" model_name="$MODEL_NAME" class_name="$CLASS_NAME"
echo "OK: vad-train-submit completed"
