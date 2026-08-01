---
name: run-ad-inference
description: Score images for anomalies using a trained be_vision_ad_tools model — automatically picks serial, parallel, or HPC multinode execution. Use when the user asks to run inference, score images, detect anomalies on a folder, batch-score production X-ray/AOI images, or generate anomaly heatmaps from a checkpoint.
---

# Run AD inference

`be_vision_ad_tools.inference.unified_inference` auto-detects the environment (Jupyter, local parallel, HPC/bsub) and routes accordingly.

## Public API (use only these)

| Action | Command |
|--------|---------|
| Inference (script) | `bash .cursor/skills/run-ad-inference/scripts/run_inference.sh <model.ckpt> <image_folder> [auto\|parallel\|hpc\|jupyter]` |
| Inference (Python) | `unified_inference(...)` — see below |

## Execution modes

| Mode | When |
|------|------|
| `auto` | Default — detects Jupyter vs HPC vs local |
| `parallel` | Local multi-core batch scoring |
| `hpc` | LSF/bsub multinode (set `num_nodes`) |
| `jupyter` | Interactive notebook session |

## Running it (script)

```bash
bash .cursor/skills/run-ad-inference/scripts/run_inference.sh \
  /path/to/model.ckpt \
  /path/to/images \
  auto
```

## Running it (Python)

```python
from be_vision_ad_tools.inference.unified_inference import unified_inference

result = unified_inference(
    model_path="/path/to/model.ckpt",
    test_folders="/path/to/images",       # folder, file, or list
    execution_mode="auto",
    batch_size=100,
    save_heatmaps=True,
    heatmap_style="cv2_side_by_side",
    output_dir="./inference_output",
)
```

`test_folders` accepts a single path, a list, or a text file with one image path per line.

## What "done" looks like (demonstration)

```
Inference complete:
- model: patchcore checkpoint (my_product)
- images: 1,240 scored from /data/lot_42/
- mode: parallel (8 workers)
- output: ./inference_output/ (scores + heatmaps)
- top anomaly: img_0042.png score=0.91
```

## What NOT to do

- Don't shell out to random Python one-liners outside `unified_inference` — it handles path resolution and batching.
- Don't assume single-image serial when the folder has thousands of images — use `auto` or `parallel`.
- For organizing scores into folders + posters, use the `organize-anomaly-scores` skill instead.

## pyskills twin

`pyskills-bridge/infer_ad/skill.py`
