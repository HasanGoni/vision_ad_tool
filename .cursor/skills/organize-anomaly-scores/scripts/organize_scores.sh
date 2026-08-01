#!/usr/bin/env bash
# Predict and organize images by anomaly score.
# Usage: organize_scores.sh <model_path> <image_list.txt> <output_dir>
set -euo pipefail
export MODEL_PATH="${1:?model_path required}"
export IMAGE_LIST="${2:?image_list_file required}"
export OUTPUT_DIR="${3:?output_dir required}"
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"
RUN="python"
if command -v uv >/dev/null 2>&1; then RUN="uv run python"; fi

$RUN <<'PY'
import os
from be_vision_ad_tools.inference.anomaly_score_organizer import predict_and_organize_by_score

result = predict_and_organize_by_score(
    model_path=os.environ["MODEL_PATH"],
    image_list_file=os.environ["IMAGE_LIST"],
    output_dir=os.environ["OUTPUT_DIR"],
    create_posters=True,
    save_metadata=True,
)
print("OK: organization completed")
stats = result.get("organization_stats", result)
print(stats)
PY
