#!/usr/bin/env bash
# Train an anomaly detection model via vad-train (Hydra CLI).
# Usage: train_model.sh <data_root> [model_name] [class_name]
set -euo pipefail
DATA_ROOT="${1:?data_root required}"
MODEL_NAME="${2:-padim}"
CLASS_NAME="${3:-anomaly_detection}"
ROOT="$(cd "$(dirname "$0")/../../../../" && pwd)"
cd "$ROOT"
RUN="vad-train"
if command -v uv >/dev/null 2>&1; then RUN="uv run vad-train"; fi

$RUN data_root="$DATA_ROOT" model_name="$MODEL_NAME" class_name="$CLASS_NAME"
echo "OK: training completed"
