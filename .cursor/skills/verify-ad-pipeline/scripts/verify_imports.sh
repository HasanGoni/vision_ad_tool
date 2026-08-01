#!/usr/bin/env bash
# Smoke-test that core modules import (no GPU training).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"
RUN="python"
if command -v uv >/dev/null 2>&1; then RUN="uv run python"; fi

$RUN -c "
from be_vision_ad_tools.training.flexible_trainer import train_anomaly_model, FlexibleTrainingConfig
from be_vision_ad_tools.inference.unified_inference import unified_inference
from be_vision_ad_tools.inference.anomaly_score_organizer import predict_and_organize_by_score
print('OK: core imports succeeded')
"

SUBMIT="vad-train-submit"
if command -v uv >/dev/null 2>&1; then SUBMIT="uv run vad-train-submit"; fi
$SUBMIT --help >/dev/null
echo "OK: vad-train-submit --help"
