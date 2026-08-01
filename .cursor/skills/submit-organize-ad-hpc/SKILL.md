---
name: submit-organize-ad-hpc
description: Submit anomaly score triage (image list) to the office HPC cluster via LSF bsub (vad-organize-submit). Use when organizing images by score must run on the cluster via bsub.
---

# Submit organize to HPC (bsub)

`vad-organize-submit` wraps `vad-organize` and submits it via `bsub`. Config: `organize_submit.yaml`.

## Public API (use only these)

| Step | Command |
|------|---------|
| Submit organize (Hydra CLI) | `vad-organize-submit model_path=<ckpt> image_list_file=<list.txt> output_dir=./review` |
| Submit organize (script) | `bash .cursor/skills/submit-organize-ad-hpc/scripts/submit_organize.sh <model> <list.txt> [out]` |
| Preview without bsub | add `hpc.dry_run=true` |

Do not invent other commands.

## pyskills twin

`pyskills-bridge/submit_organize_ad_hpc/skill.py`
