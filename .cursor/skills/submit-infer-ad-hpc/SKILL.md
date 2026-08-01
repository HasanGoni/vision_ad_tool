---
name: submit-infer-ad-hpc
description: Submit batch AD inference to the office HPC cluster via LSF bsub (vad-infer-submit). Use when the user wants to queue inference on the cluster, submit vad-infer to HPC, or score images via bsub instead of locally.
---

# Submit inference to HPC (bsub)

`vad-infer-submit` wraps `vad-infer` and submits it via `bsub`. Config: `infer_submit.yaml` + `hpc/submit_defaults.yaml`.

## Public API (use only these)

| Step | Command |
|------|---------|
| Submit infer (Hydra CLI) | `vad-infer-submit model_path=<ckpt> test_folders=<path>` |
| Submit infer (script) | `bash .cursor/skills/submit-infer-ad-hpc/scripts/submit_infer.sh <model> <folder>` |
| Preview without bsub | `vad-infer-submit model_path=<ckpt> test_folders=<path> hpc.dry_run=true` |

Do not invent other commands.

## What "done" looks like

```text
Submitted vad-infer to HPC:
- lsf_job_id: 12345679
- logs: ./hpc_logs/vad-infer_*.out
```

## pyskills twin

`pyskills-bridge/submit_infer_ad_hpc/skill.py`
