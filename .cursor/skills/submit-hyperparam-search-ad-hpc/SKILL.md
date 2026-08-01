---
name: submit-hyperparam-search-ad-hpc
description: Submit hyperparameter grid search + comparison poster to the office HPC cluster via LSF bsub (vad-hyperparam-search-submit). Use when model comparison must run on the cluster.
---

# Submit hyperparam search to HPC (bsub)

`vad-hyperparam-search-submit` wraps `vad-hyperparam-search` and submits it via `bsub`. Config: `hyperparam_search_submit.yaml`.

## Public API (use only these)

| Step | Command |
|------|---------|
| Submit (Hydra CLI) | `vad-hyperparam-search-submit data_root=<path> test_images=<path>` |
| Submit (script) | `bash .cursor/skills/submit-hyperparam-search-ad-hpc/scripts/submit_hyperparam_search.sh <data_root> <test> [class]` |
| Preview without bsub | add `hpc.dry_run=true` |

Do not invent other commands.

## pyskills twin

`pyskills-bridge/submit_hyperparam_search_ad_hpc/skill.py`
