# AGENTS.md — vision_ad_tools

Persistent notes for AI agents working in this repository.

## HPC / office cluster

- The user runs heavy workloads on an **LSF HPC cluster** at the office via **`bsub`**.
- Every local Hydra CLI (`vad-train`, `vad-infer`, …) has a **companion submit CLI** (`vad-train-submit`, …) that wraps `bsub` and runs the local CLI on the cluster.
- HPC defaults: `be_vision_ad_tools/tutorials/conf/hpc/submit_defaults.yaml`. Per-workflow overlays: `*_submit.yaml`.
- Reuse `be_vision_ad_tools.inference.multinode_from_aiop_tool.HPC_Job` bsub defaults where possible.
- On machines without `bsub`, use `hpc.dry_run=true` to preview the submission command.

## New workflows convention

When adding a new Hydra CLI workflow:

1. Add local CLI in `nbs/*_hydra_cli.ipynb` (or extend `end2end_cli`).
2. Add companion `vad-*-submit` in `nbs/20_tutorials.hpc_submit_cli.ipynb` with `*_submit.yaml` config.
3. Register both in `pyproject.toml` `[project.scripts]`.
4. Create pyskills-pattern skill: `.cursor/skills/<name>/SKILL.md` + `scripts/*.sh`.
5. Create pyskills twin: `pyskills-bridge/<module>/skill.py` with `__all__`, `allow()`, discovery docstring.
6. Update `pyskills-bridge/REFERENCE.md`, `.github/copilot-instructions.md`, `docs/agent-skills-from-pyskills.md`.

## nbdev

- Notebooks under `nbs/` export to `be_vision_ad_tools/`. Run `uv run nbdev-export` after notebook edits.
- Config YAMLs live in `be_vision_ad_tools/tutorials/conf/` and are packaged via `pyproject.toml` package-data.

## Verification

Before claiming fixes work: `bash .cursor/skills/verify-ad-pipeline/scripts/verify_*.sh`

## Preprocessing contract

- p2/p98 percentile normalization
- No silent 16→8-bit conversion
- No elastic deformation
- `TilerConfigurationCallback` (not `TilingConfigurationCallback`)
