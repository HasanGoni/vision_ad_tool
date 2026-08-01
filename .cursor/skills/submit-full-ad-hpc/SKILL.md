---
name: submit-full-ad-hpc
description: Submit end-to-end train + infer-organize pipeline to the office HPC cluster via LSF bsub (vad-full-submit). Use when the full AD pipeline must run on the cluster.
---

# Submit full pipeline to HPC (bsub)

`vad-full-submit` wraps `vad-full` and submits it via `bsub`. Config: `full_submit.yaml` (default walltime 480 min).

## Public API (use only these)

| Step | Command |
|------|---------|
| Submit (Hydra CLI) | `vad-full-submit train.data_root=<path> infer_organize.test_folders=<test>` |
| Submit (script) | `bash .cursor/skills/submit-full-ad-hpc/scripts/submit_full.sh <data_root> <test> [model]` |
| Preview without bsub | add `hpc.dry_run=true` |

Do not invent other commands.

## pyskills twin

`pyskills-bridge/submit_full_ad_hpc/skill.py`
