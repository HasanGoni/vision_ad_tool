---
name: full-ad-pipeline
description: Run the complete anomaly-detection pipeline — train a model, then score test images and organize into threshold folders with review posters. Use when the user wants end-to-end AD from scratch, train-and-test in one command, or a full production triage workflow without manual checkpoint handoff.
---

# Full AD pipeline (train + infer-organize)

`vad-full` chains training with `unified_inference_with_threshold_posters` using Hydra config defaults in `be_vision_ad_tools/tutorials/conf/full.yaml`. Trains a model, extracts the exported checkpoint, then scores and organizes test images into threshold buckets with posters.

## Public API (use only these)

| Step | Command |
|------|---------|
| Full pipeline (Hydra CLI) | `vad-full train.data_root=<path> infer_organize.test_folders=<path>` |
| Full pipeline (script) | `bash .cursor/skills/full-ad-pipeline/scripts/full_pipeline.sh <data_root> <test_folders> [model_name]` |
| Verify after | use `verify-ad-pipeline` skill |

Do not invent other commands.

## When to use this vs other skills

| Need | Skill / CLI |
|------|-------------|
| Train only | `train-anomaly-model` / `vad-train` |
| Train + validation posters | `train-infer-ad` / `vad-train-infer` |
| Infer-organize existing checkpoint | `infer-organize-ad` / `vad-infer-organize` |
| **Train + test triage end-to-end** | **this skill** / `vad-full` |

## Dataset layout (training)

```
data_root/
├── good/        # normal images
└── bad/         # abnormal images
```

`infer_organize.test_folders` accepts a folder, single image, or text file with one path per line.

## Running it (Hydra CLI)

```bash
vad-full train.data_root=/path/to/data infer_organize.test_folders=/path/to/test
```

## Running it (script)

```bash
bash .cursor/skills/full-ad-pipeline/scripts/full_pipeline.sh \
  /path/to/data \
  /path/to/test_images \
  patchcore
```

## Config overrides

```bash
vad-full \
  train.data_root=/data/my_product train.model_name=patchcore train.max_epochs=100 \
  infer_organize.test_folders=/data/lot_42 infer_organize.output_dir=./full_results \
  infer_organize.score_thresholds=[0.5,0.7,0.9,1.0] infer_organize.create_posters=true
```

## Output structure

```
full_pipeline_results/
├── score_0.5_0.7/
│   ├── metadata.json
│   └── poster.png
├── score_0.9_1.0/
...
```

## What "done" looks like (demonstration)

```text
Full AD pipeline complete:
- train data: /data/my_product (good=120, bad=15)
- model: patchcore / resnet18
- checkpoint: /data/my_product/models/patchcore/...
- test images: 1,240 scored from /data/lot_42/
- buckets: 4 score folders in ./full_pipeline_results/
- posters: 62 review posters
- highest bucket (0.9-1.0): 18 images — inspect these first
- metrics: image_AUROC=0.97
```

Open at least one poster and confirm the checkpoint path matches training output.

## What NOT to do

- Don't run `vad-train` then manually wire `model_path` into `vad-infer-organize` — use this skill.
- Don't use for quick training smoke tests — use `vad-train` or `vad-train-infer` instead.
- Don't skip `verify-ad-pipeline` before claiming library changes work.

## pyskills twin

`pyskills-bridge/full_ad/skill.py`
