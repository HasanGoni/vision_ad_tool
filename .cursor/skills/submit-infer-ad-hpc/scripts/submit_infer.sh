#!/usr/bin/env bash
# Submit inference to HPC via vad-infer-submit (bsub).
# Usage: submit_infer.sh <model_path> <test_folders>
set -euo pipefail
MODEL_PATH="${1:?model_path required}"
TEST_FOLDERS="${2:?test_folders required}"
ROOT="$(cd "$(dirname "$0")/../../../../" && pwd)"
cd "$ROOT"
RUN="vad-infer-submit"
if command -v uv >/dev/null 2>&1; then RUN="uv run vad-infer-submit"; fi
$RUN model_path="$MODEL_PATH" test_folders="$TEST_FOLDERS"
echo "OK: vad-infer-submit completed"
