---
name: organize-anomaly-scores
description: Score a batch of images, sort them into anomaly-score folders, and create review posters for human triage. Use when the user wants to organize/sort/rank images by anomaly score, build a review deck for false-alarm analysis, create score-bucket folders for active learning, or triage production images after inference.
---

# Organize images by anomaly score

`vad-organize` wraps `predict_and_organize_by_score` with Hydra config defaults in `be_vision_ad_tools/tutorials/conf/organize.yaml`. Workflow: predict → bucket by threshold → metadata JSON → optional posters.

## Public API (use only these)

| Step | Command |
|------|---------|
| Organize (Hydra CLI) | `vad-organize model_path=<ckpt> image_list_file=<list.txt> output_dir=<out>` |
| Organize (script) | `bash .cursor/skills/organize-anomaly-scores/scripts/organize_scores.sh <model> <image_list.txt> <out_dir>` |

Do not invent other commands.

## Input: image list file

Plain text, one absolute or relative image path per line:

```
/data/lot_42/img_0001.png
/data/lot_42/img_0002.png
...
```

## Running it (Hydra CLI)

```bash
vad-organize model_path=/path/to/model.ckpt image_list_file=/path/to/images.txt output_dir=./score_review
```

## Running it (script)

```bash
bash .cursor/skills/organize-anomaly-scores/scripts/organize_scores.sh \
  /path/to/model.ckpt \
  /path/to/images.txt \
  ./score_review
```

## Config overrides

```bash
vad-organize model_path=/path/model.ckpt image_list_file=/path/list.txt score_thresholds=[0.3,0.5,0.7,0.9,1.0] create_posters=true images_per_poster=20
```

## Output structure

```
score_review/
├── score_0.3_0.4/     # images with scores in this bucket
│   ├── metadata.json
│   └── poster.png
├── score_0.7_0.8/
...
```

## What "done" looks like (demonstration)

```text
Score organization complete:
- model: patchcore / my_product
- images: 500 scored from images.txt
- buckets: 8 score folders created
- posters: 25 review posters (20 img each)
- highest bucket (0.9-1.0): 12 images — inspect these first
```

Actually open one poster with the Read tool when verifying — don't just check file counts.

## What NOT to do

- Don't manually copy images into score folders — rerun with updated thresholds.
- Don't use this for single-image scoring — use `run-ad-inference` (`vad-infer`) instead.
- For inference on a folder + organize in one step, use `infer-organize-ad` (`vad-infer-organize`).
- For training a new model on the high-score bucket, switch to `train-anomaly-model` (`vad-train`).

## pyskills twin

`pyskills-bridge/organize_ad/skill.py`
