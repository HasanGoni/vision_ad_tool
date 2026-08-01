---
name: train-anomaly-model
description: Train an Anomalib-based anomaly detection model using be_vision_ad_tools (Padim, Patchcore, Fastflow, etc.) on a folder dataset with normal/abnormal splits. Use when the user asks to train/fit/build an AD model, anomaly detector, Patchcore/Padim model, or needs a new model checkpoint for X-ray/AOI defect detection — even if they don't name the library.
---

# Train an anomaly detection model

`be_vision_ad_tools.training.flexible_trainer` wraps Anomalib v1.x with smart defaults for GPU/HPC environments.

## Public API (use only these)

| Action | Command |
|--------|---------|
| Train (CLI) | `bash .cursor/skills/train-anomaly-model/scripts/train_model.sh <data_root> [model] [class_name]` |
| Train (Python) | see below — `train_anomaly_model(config)` |
| Verify after | use `verify-ad-pipeline` skill |

Do not call raw Anomalib APIs unless the user explicitly asks to bypass the toolbox.

## Dataset layout

```
data_root/
├── good/        # normal images (default normal_dir)
└── bad/         # abnormal images (default abnormal_dir)
```

Override dir names via Python config (`normal_dir`, `abnormal_dir`).

## Which model to use

| Model | When |
|-------|------|
| `padim` | Fast baseline, small datasets, quick iteration |
| `patchcore` | Strong default for industrial AD, memory-heavy |
| `fastflow` | Good speed/accuracy tradeoff |
| `efficientad` | Resource-constrained GPUs |

Only ask the user which model if genuinely ambiguous — default to `patchcore` for production X-ray/AOI, `padim` for smoke tests.

## Running it (script)

```bash
bash .cursor/skills/train-anomaly-model/scripts/train_model.sh /path/to/data patchcore my_product
```

## Running it (Python)

```python
from be_vision_ad_tools.training.flexible_trainer import FlexibleTrainingConfig, train_anomaly_model

config = FlexibleTrainingConfig(
    data_root="/path/to/data",
    class_name="my_product",
    model_name="patchcore",
    backbone="resnet18",
    max_epochs=100,
)
result = train_anomaly_model(config)
# result contains model paths, metrics
```

Or from YAML:

```python
train_anomaly_model("/path/to/config.yaml")
```

## What "done" looks like (demonstration)

```
Trained AD model:
- data: /data/my_product (good=120, bad=15)
- model: patchcore / resnet18
- checkpoint: /data/my_product/results/patchcore/...
- metrics: image_AUROC=0.97
- verified: verify-ad-pipeline passed
```

## What NOT to do

- Don't train without the preprocessing contract (p2/p98 norm, no silent 16→8-bit, no elastic aug).
- Don't hand-edit checkpoint files — retrain or fix `flexible_trainer` / notebook source in `nbs/`.
- Don't skip `verify-ad-pipeline` before claiming training works.

## pyskills twin

`pyskills-bridge/train_ad/skill.py`
