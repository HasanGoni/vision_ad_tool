---
name: train-infer-ad
description: Train an anomaly detection model, then immediately run inference and create validation posters from the new checkpoint. Use when the user wants to train a model and see validation results in one step, smoke-test training with visual output, or run train-then-infer without manual checkpoint handoff.
---

# Train then infer (validation posters)

`vad-train-infer` chains `train_anomaly_model` with `run_inference_after_training` using Hydra config defaults in `tutorials/end2end_tutorial/conf/train_infer.yaml`. Automatically passes the trained checkpoint to inference — no manual `model_path` lookup.

## Public API (use only these)

| Step | Command |
|------|---------|
| Train + infer (Hydra CLI) | `vad-train-infer train.data_root=<path> infer_after_training.validation_images=<path>` |
| Train + infer (script) | `bash .cursor/skills/train-infer-ad/scripts/train_infer.sh <data_root> <validation_images> [model_name]` |

Do not invent other commands.

## When to use this vs other skills

| Need | Skill / CLI |
|------|-------------|
| Train only | `train-anomaly-model` / `vad-train` |
| Train + infer on test folder + score buckets | `full-ad-pipeline` / `vad-full` |
| Train + validation posters | **this skill** / `vad-train-infer` |
| Infer on existing checkpoint | `run-ad-inference` / `vad-infer` |

## Dataset layout (training)

```
data_root/
├── good/        # normal images
└── bad/         # abnormal images
```

`validation_images` can be a folder or image path for post-training inference posters.

## Running it (Hydra CLI)

```bash
vad-train-infer train.data_root=/path/to/data infer_after_training.validation_images=/path/to/val
```

## Running it (script)

```bash
bash .cursor/skills/train-infer-ad/scripts/train_infer.sh \
  /path/to/data \
  /path/to/validation_images \
  patchcore
```

## Config overrides

```bash
vad-train-infer \
  train.data_root=/data/my_product train.model_name=patchcore train.max_epochs=50 \
  infer_after_training.validation_images=/data/val infer_after_training.poster_rows=4 infer_after_training.poster_cols=4
```

## What "done" looks like (demonstration)

```text
Train-infer complete:
- data: /data/my_product (good=120, bad=15)
- model: patchcore / resnet18
- checkpoint: /data/my_product/models/patchcore/...
- validation: 48 images scored from /data/val/
- posters: validation_posters/ (4×4 grid, 3 pages)
- metrics: image_AUROC=0.97
```

Open at least one validation poster when verifying.

## What NOT to do

- Don't manually find the checkpoint path after training — this workflow passes it automatically.
- Don't use this for production batch scoring with score buckets — use `vad-full` or `vad-infer-organize`.
- Don't skip `verify-ad-pipeline` before claiming the training leg works.

## pyskills twin

`pyskills-bridge/train_infer_ad/skill.py` (if present)
