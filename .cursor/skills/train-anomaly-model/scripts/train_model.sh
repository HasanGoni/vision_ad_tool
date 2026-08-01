#!/usr/bin/env bash
# Train an anomaly detection model via flexible_trainer.
# Usage: train_model.sh <data_root> [model_name] [class_name]
set -euo pipefail
export DATA_ROOT="${1:?data_root required}"
export MODEL_NAME="${2:-padim}"
export CLASS_NAME="${3:-anomaly_detection}"
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"
RUN="python"
if command -v uv >/dev/null 2>&1; then RUN="uv run python"; fi

$RUN <<'PY'
import os
from be_vision_ad_tools.training.flexible_trainer import FlexibleTrainingConfig, train_anomaly_model

config = FlexibleTrainingConfig(
    data_root=os.environ["DATA_ROOT"],
    class_name=os.environ["CLASS_NAME"],
    model_name=os.environ["MODEL_NAME"],
    backbone="resnet18",
    max_epochs=1,
)
result = train_anomaly_model(config)
print("OK: training completed")
print(result)
PY
