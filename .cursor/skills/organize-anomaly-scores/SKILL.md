---
name: organize-anomaly-scores
description: Score a batch of images, sort them into anomaly-score folders, and create review posters for human triage. Use when the user wants to organize/sort/rank images by anomaly score, build a review deck for false-alarm analysis, create score-bucket folders for active learning, or triage production images after inference.
---

# Organize images by anomaly score

`predict_and_organize_by_score` is the main workflow: predict → bucket by threshold → metadata JSON → optional posters.

## Public API (use only these)

| Action | Command |
|--------|---------|
| Organize (script) | `bash .cursor/skills/organize-anomaly-scores/scripts/organize_scores.sh <model> <image_list.txt> <out_dir>` |
| Organize (Python) | `predict_and_organize_by_score(...)` — see below |

## Input: image list file

Plain text, one absolute or relative image path per line:

```
/data/lot_42/img_0001.png
/data/lot_42/img_0002.png
...
```

## Running it (script)

```bash
bash .cursor/skills/organize-anomaly-scores/scripts/organize_scores.sh \
  /path/to/model.ckpt \
  /path/to/images.txt \
  ./score_review
```

## Running it (Python)

```python
from be_vision_ad_tools.inference.anomaly_score_organizer import predict_and_organize_by_score

result = predict_and_organize_by_score(
    model_path="/path/to/model.ckpt",
    image_list_file="/path/to/images.txt",
    output_dir="./score_review",
    score_thresholds=[0.3, 0.5, 0.7, 0.9, 1.0],
    copy_mode=True,           # copy, don't move originals
    save_metadata=True,
    create_posters=True,
    images_per_poster=20,
    grid_cols=5,
)
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

```
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
- Don't use this for single-image scoring — use `run-ad-inference` instead.
- For training a new model on the high-score bucket, switch to `train-anomaly-model`.

## pyskills twin

`pyskills-bridge/organize_ad/skill.py`
