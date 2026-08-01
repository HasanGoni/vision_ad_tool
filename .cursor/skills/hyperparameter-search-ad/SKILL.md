---
name: hyperparameter-search-ad
description: Run hyperparameter grid search across Padim/Patchcore model combinations and generate a side-by-side comparison poster on test images. Use when the user wants to compare AD models/backbones/features, tune hyperparameters, diff training parameters, or produce a hyperparam comparison poster for X-ray/AOI defect detection.
---

# Hyperparameter search + comparison poster

`vad-hyperparam-search` wraps `be_vision_ad_tools.training.hyperparameter_search.diff_parameter_and_save_poster` with Hydra config defaults in `be_vision_ad_tools/tutorials/conf/hyperparam_search.yaml`. Trains a grid of model combinations, then builds a comparison poster with heatmaps.

## Public API (use only these)

| Step | Command |
|------|---------|
| Hyperparam search (Hydra CLI) | `vad-hyperparam-search data_root=<path> test_images=<path> [model_names=[padim,patchcore]]` |
| Hyperparam search (script) | `bash .cursor/skills/hyperparameter-search-ad/scripts/hyperparam_search.sh <data_root> <test_images> [class_name]` |
| Verify after | use `verify-ad-pipeline` skill |

Do not invent other commands. Do not call raw Anomalib APIs unless the user explicitly asks to bypass the toolbox.

## Dataset layout

```
data_root/
├── good/        # normal images (default normal_dir)
└── bad/         # abnormal images (default abnormal_dir)
```

`test_images` accepts a folder, single image, or list of paths.

## Which parameters to tune

| Parameter | When |
|-----------|------|
| `model_names` | Compare Padim vs Patchcore vs Fastflow |
| `backbones` | Try resnet18 vs wide_resnet50_2 |
| `n_features_list` | Patchcore memory / feature count |
| `layers` | Which ResNet layers to extract features from |
| `max_models` | Limit poster columns (top N successful models) |
| `max_test_images` | Limit poster rows |

Default to a small grid for smoke tests (`max_epochs=1`, few combinations).

## Running it (Hydra CLI)

```bash
uv sync   # once, installs vad-hyperparam-search
vad-hyperparam-search \
  data_root=/path/to/data \
  test_images=/path/to/test \
  model_names=[padim,patchcore] \
  backbones=[resnet18] \
  max_epochs=1 \
  max_models=4 \
  output_file=./comparison_poster.png
```

## Running it (script)

```bash
bash .cursor/skills/hyperparameter-search-ad/scripts/hyperparam_search.sh \
  /path/to/data \
  /path/to/test_images \
  my_product
```

## Config overrides

Any field in `be_vision_ad_tools/tutorials/conf/hyperparam_search.yaml` can be overridden on the CLI:

```bash
vad-hyperparam-search \
  data_root=/data/my_product \
  test_images=/data/lot_42 \
  layers='[[layer1,layer2],[layer1,layer2,layer3]]' \
  n_features_list=[64,128] \
  show_original=true \
  device=cuda
```

## What "done" looks like (demonstration)

```text
Hyperparameter search complete:
- data: /data/my_product (good=120, bad=15)
- grid: 4 combinations (padim+resnet18, patchcore+resnet18, ...)
- successful trainings: 3/4
- poster: ./comparison_poster.png (3 models x 6 test images)
- results JSON: /data/my_product/test_hyperparameter_results/hyperparameter_search_results_*.json
- models saved: /data/my_product/test_hyperparameter_models/
```

## What NOT to do

- Don't run full `max_epochs` grids on large datasets without scoping down first.
- Don't hand-edit poster PNGs — rerun with different `max_models` / `max_test_images`.
- Don't skip `verify-ad-pipeline` before claiming library changes work.

## pyskills twin

`pyskills-bridge/hyperparameter_search_ad/skill.py`
