---
name: submit-train-ad-hpc
description: Submit anomaly model training to the office HPC cluster via LSF bsub (vad-train-submit). Use when the user wants to queue training on the cluster, submit vad-train to HPC, or run Padim/Patchcore training via bsub instead of locally.
---

# Submit training to HPC (bsub)

`vad-train-submit` wraps `vad-train` and submits it as an LSF batch job via `bsub`. HPC defaults live in `be_vision_ad_tools/tutorials/conf/hpc/submit_defaults.yaml` and `train_submit.yaml`.

## Public API (use only these)

| Step | Command |
|------|---------|
| Submit train (Hydra CLI) | `vad-train-submit data_root=<path> [model_name=patchcore] hpc.queue=batch` |
| Submit train (script) | `bash .cursor/skills/submit-train-ad-hpc/scripts/submit_train.sh <data_root> [model] [class]` |
| Preview without bsub | `vad-train-submit data_root=<path> hpc.dry_run=true` |

Do not invent other commands.

## HPC overrides

Override any `hpc.*` field: `hpc.cores`, `hpc.memory_mb`, `hpc.walltime_minutes`, `hpc.queue`, `hpc.job_name`, `hpc.log_dir`, `hpc.use_gpu=true`.

## What "done" looks like

```text
Submitted vad-train to HPC:
- lsf_job_id: 12345678
- logs: ./hpc_logs/vad-train_20260801_102100.out
- remote: cd /path/to/vision_ad_tools && uv run vad-train data_root=/data/my_product ...
```

## pyskills twin

`pyskills-bridge/submit_train_ad_hpc/skill.py`
