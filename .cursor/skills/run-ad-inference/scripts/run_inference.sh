#!/usr/bin/env bash
# Run unified inference on image folder(s).
# Usage: run_inference.sh <model_path> <test_folder> [execution_mode]
set -euo pipefail
export MODEL_PATH="${1:?model_path required}"
export TEST_FOLDER="${2:?test_folder required}"
export EXEC_MODE="${3:-auto}"
ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
cd "$ROOT"
RUN="python"
if command -v uv >/dev/null 2>&1; then RUN="uv run python"; fi

$RUN <<'PY'
import os
from be_vision_ad_tools.inference.unified_inference import unified_inference

result = unified_inference(
    model_path=os.environ["MODEL_PATH"],
    test_folders=os.environ["TEST_FOLDER"],
    execution_mode=os.environ["EXEC_MODE"],
    save_heatmaps=True,
)
print("OK: inference completed")
print(result)
PY
