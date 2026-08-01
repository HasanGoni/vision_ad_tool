---
name: infer-organize-ad
description: Score images with unified inference, then sort into anomaly-score threshold folders and create review posters in one pipeline. Use when the user wants inference plus triage/organization in a single step, batch-score a folder and bucket by threshold, or generate threshold posters after scoring production X-ray/AOI images.
---

# Infer and organize by anomaly score

`vad-infer-organize` wraps `unified_inference_with_threshold_posters` with Hydra config defaults in `be_vision_ad_tools/tutorials/conf/infer_organize.yaml`. Combines batch scoring with threshold-folder triage and optional posters — no separate image list file required.

## Public API (use only these)

| Step | Command |
|------|---------|
| Infer + organize (Hydra CLI) | `vad-infer-organize model_path=<ckpt> test_folders=<path> [output_dir=...]` |
| Infer + organize (script) | `bash .cursor/skills/infer-organize-ad/scripts/infer_organize.sh <model.ckpt> <test_folders> [output_dir]` |

Do not invent other commands.

## When to use this vs other skills

| Need | Skill / CLI |
|------|-------------|
| Score folder only (heatmaps) | `run-ad-inference` / `vad-infer` |
| Organize from image list file | `organize-anomaly-scores` / `vad-organize` |
| Score folder + bucket + posters | **this skill** / `vad-infer-organize` |
| Train + score + organize | `full-ad-pipeline` / `vad-full` |

## Running it (Hydra CLI)

```bash
vad-infer-organize model_path=/path/to/model.ckpt test_folders=/path/to/images output_dir=./infer_organize_review
```

`test_folders` accepts a folder path, single image, or text file with one path per line.

## Running it (script)

```bash
bash .cursor/skills/infer-organize-ad/scripts/infer_organize.sh \
  /path/to/model.ckpt \
  /path/to/images \
  ./infer_organize_review
```

## Config overrides

```bash
vad-infer-organize model_path=/path/model.ckpt test_folders=/path/images \
  score_thresholds=[0.5,0.7,0.9,1.0] create_posters=true images_per_poster=20 execution_mode=parallel
```

## Output structure

```
infer_organize_review/
├── score_0.5_0.6/
│   ├── metadata.json
│   └── poster.png
├── score_0.9_1.0/
...
```

## What "done" looks like (demonstration)

```text
Infer-organize complete:
- model: patchcore / my_product
- images: 1,240 scored from /data/lot_42/
- mode: parallel (8 workers)
- buckets: 7 score folders created
- posters: 62 review posters (20 img each)
- highest bucket (0.9-1.0): 18 images — inspect these first
```

Open at least one poster and one metadata.json when verifying — don't just check exit codes.

## What NOT to do

- Don't run `vad-infer` then manually bucket — use this skill for the combined workflow.
- Don't use an image list file here — use `vad-organize` if input is a `.txt` list.
- Don't hand-copy images into score folders — rerun with updated `score_thresholds`.

## pyskills twin

`pyskills-bridge/infer_organize_ad/skill.py`
