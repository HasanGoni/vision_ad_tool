---
name: run-ad-inference
description: Score images for anomalies using a trained be_vision_ad_tools model — automatically picks serial, parallel, or HPC multinode execution. Use when the user asks to run inference, score images, detect anomalies on a folder, batch-score production X-ray/AOI images, or generate anomaly heatmaps from a checkpoint.
---

# Run AD inference

`vad-infer` wraps `be_vision_ad_tools.inference.unified_inference` with Hydra config defaults in `be_vision_ad_tools/tutorials/conf/infer.yaml`. Auto-detects Jupyter vs HPC vs local parallel execution.

## Public API (use only these)

| Step | Command |
|------|---------|
| Inference (Hydra CLI) | `vad-infer model_path=<ckpt> test_folders=<path> [execution_mode=auto]` |
| Inference (script) | `bash .cursor/skills/run-ad-inference/scripts/run_inference.sh <model.ckpt> <image_folder> [auto\|parallel\|hpc\|jupyter]` |

Do not invent other commands.

## Execution modes

| Mode | When |
|------|------|
| `auto` | Default — detects Jupyter vs HPC vs local |
| `parallel` | Local multi-core batch scoring |
| `hpc` | LSF/bsub multinode (set `num_nodes`) |
| `jupyter` | Interactive notebook session |

## Running it (Hydra CLI)

```bash
vad-infer model_path=/path/to/model.ckpt test_folders=/path/to/images execution_mode=auto
```

`test_folders` accepts a folder path, single image, or text file with one path per line.

## Running it (script)

```bash
bash .cursor/skills/run-ad-inference/scripts/run_inference.sh \
  /path/to/model.ckpt \
  /path/to/images \
  auto
```

## Config overrides

```bash
vad-infer model_path=/path/model.ckpt test_folders=/path/images save_heatmaps=true heatmap_style=cv2_side_by_side output_dir=./inference_output
```

## What "done" looks like (demonstration)

```text
Inference complete:
- model: patchcore checkpoint (my_product)
- images: 1,240 scored from /data/lot_42/
- mode: parallel (8 workers)
- output: ./inference_output/ (scores + heatmaps)
- top anomaly: img_0042.png score=0.91
```

## What NOT to do

- Don't shell out to random Python one-liners outside `vad-infer` / `unified_inference`.
- Don't assume single-image serial when the folder has thousands of images — use `auto` or `parallel`.
- For inference + score buckets + posters in one step, use `infer-organize-ad` (`vad-infer-organize`).
- For organizing from an image list file, use `organize-anomaly-scores` (`vad-organize`).

## pyskills twin

`pyskills-bridge/infer_ad/skill.py`
