---
name: submit-infer-organize-ad-hpc
description: Submit infer + score buckets + posters to the office HPC cluster via LSF bsub (vad-infer-organize-submit). Use when folder triage with posters must run on the cluster.
---

# Submit infer-organize to HPC (bsub)

`vad-infer-organize-submit` wraps `vad-infer-organize` and submits it via `bsub`. Config: `infer_organize_submit.yaml`.

## Public API (use only these)

| Step | Command |
|------|---------|
| Submit (Hydra CLI) | `vad-infer-organize-submit model_path=<ckpt> test_folders=<path>` |
| Submit (script) | `bash .cursor/skills/submit-infer-organize-ad-hpc/scripts/submit_infer_organize.sh <model> <folder> [out]` |
| Preview without bsub | add `hpc.dry_run=true` |

Do not invent other commands.

## pyskills twin

`pyskills-bridge/submit_infer_organize_ad_hpc/skill.py`
