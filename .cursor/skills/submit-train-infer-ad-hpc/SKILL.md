---
name: submit-train-infer-ad-hpc
description: Submit train + validation posters to the office HPC cluster via LSF bsub (vad-train-infer-submit). Use when train-infer must run on the cluster instead of locally.
---

# Submit train-infer to HPC (bsub)

`vad-train-infer-submit` wraps `vad-train-infer` and submits it via `bsub`. Config: `train_infer_submit.yaml`.

## Public API (use only these)

| Step | Command |
|------|---------|
| Submit (Hydra CLI) | `vad-train-infer-submit train.data_root=<path> infer_after_training.validation_images=<val>` |
| Submit (script) | `bash .cursor/skills/submit-train-infer-ad-hpc/scripts/submit_train_infer.sh <data_root> <val_images> [model]` |
| Preview without bsub | add `hpc.dry_run=true` |

Do not invent other commands.

## pyskills twin

`pyskills-bridge/submit_train_infer_ad_hpc/skill.py`
