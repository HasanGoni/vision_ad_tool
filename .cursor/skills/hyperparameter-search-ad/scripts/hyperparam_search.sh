#!/usr/bin/env bash
# Hyperparameter grid search + comparison poster via vad-hyperparam-search (Hydra CLI).
# Usage: hyperparam_search.sh <data_root> <test_images> [class_name]
set -euo pipefail
DATA_ROOT="${1:?data_root required}"
TEST_IMAGES="${2:?test_images required}"
CLASS_NAME="${3:-hyperparam_search}"
ROOT="$(cd "$(dirname "$0")/../../../../" && pwd)"
cd "$ROOT"
RUN="vad-hyperparam-search"
if command -v uv >/dev/null 2>&1; then RUN="uv run vad-hyperparam-search"; fi

$RUN \
  data_root="$DATA_ROOT" \
  test_images="$TEST_IMAGES" \
  class_name="$CLASS_NAME" \
  max_epochs=1
echo "OK: hyperparameter search completed"
