---
name: train-anomaly-model
description: Train an Anomalib-based anomaly detection model using be_vision_ad_tools (Padim, Patchcore, Fastflow, etc.) on a folder dataset with normal/abnormal splits. Use when the user asks to train/fit/build an AD model, anomaly detector, Patchcore/Padim model, or needs a new model checkpoint for X-ray/AOI defect detection — even if they don't name the library.
---

# Train an anomaly detection model

`vad-train` wraps `be_vision_ad_tools.training.flexible_trainer.train_anomaly_model` with Hydra config defaults in `be_vision_ad_tools/tutorials/conf/train.yaml`.

## Public API (use only these)

| Step | Command |
|------|---------|
| Train (Hydra CLI) | `vad-train data_root=<path> [model_name=patchcore] [class_name=...]` |
| Train (script) | `bash .cursor/skills/train-anomaly-model/scripts/train_model.sh <data_root> [model_name] [class_name]` |
| Verify after | use `verify-ad-pipeline` skill |

Do not invent other commands. Do not call raw Anomalib APIs unless the user explicitly asks to bypass the toolbox.

## Dataset layout

```
data_root/
├── good/        # normal images (default normal_dir)
└── bad/         # abnormal images (default abnormal_dir)
```

Override dir names via Hydra (`normal_dir=`, `abnormal_dir=`) or edit `conf/train.yaml`.

## Which model to use

| Model | When |
|-------|------|
| `padim` | Fast baseline, small datasets, quick iteration |
| `patchcore` | Strong default for industrial AD, memory-heavy |
| `fastflow` | Good speed/accuracy tradeoff |
| `efficientad` | Resource-constrained GPUs |

Default to `patchcore` for production X-ray/AOI, `padim` for smoke tests.

## Running it (Hydra CLI)

```bash
uv sync   # once, installs vad-train
vad-train data_root=/path/to/data model_name=patchcore class_name=my_product
```

## Running it (script)

```bash
bash .cursor/skills/train-anomaly-model/scripts/train_model.sh /path/to/data patchcore my_product
```

## Config overrides

Any field in `be_vision_ad_tools/tutorials/conf/train.yaml` can be overridden on the CLI:

```bash
vad-train data_root=/data/my_product max_epochs=50 backbone=wide_resnet50_2
```

## What "done" looks like (demonstration)

```text
Trained AD model:
- data: /data/my_product (good=120, bad=15)
- model: patchcore / resnet18
- checkpoint: /data/my_product/models/patchcore/...
- metrics: image_AUROC=0.97
- verified: verify-ad-pipeline passed
```

## What NOT to do

- Don't train without the preprocessing contract (p2/p98 norm, no silent 16→8-bit, no elastic aug).
- Don't hand-edit checkpoint files — retrain or fix `flexible_trainer` / notebook source in `nbs/`.
- Don't skip `verify-ad-pipeline` before claiming training works.

## pyskills twin

`pyskills-bridge/train_ad/skill.py`
