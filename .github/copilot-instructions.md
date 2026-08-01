# vision_ad_tool — Copilot instructions

This repo includes agent skills inspired by [AnswerDotAI/pyskills](https://github.com/AnswerDotAI/pyskills). Steal the **patterns** (progressive disclosure, curated API, demonstrations), not the Python package.

Full guide: [docs/agent-skills-from-pyskills.md](../docs/agent-skills-from-pyskills.md)

## When editing `be_vision_ad_tools/` or `nbs/`

Before claiming a fix works or committing:

1. `bash .cursor/skills/verify-ad-pipeline/scripts/verify_sync.sh`
2. `bash .cursor/skills/verify-ad-pipeline/scripts/verify_imports.sh`
3. `bash .cursor/skills/verify-ad-pipeline/scripts/verify_nbdev.sh`

Report concretely, e.g.:

```text
Verified AD toolbox:
- sync: OK
- imports: flexible_trainer, unified_inference, anomaly_score_organizer
- nbdev-test: passed
```

## Public API — use only these commands

### Hydra CLIs (primary)

Install with `uv sync` or `pip install -e .`. Configs: `be_vision_ad_tools/tutorials/conf/*.yaml`.

| CLI | Workflow | Example |
|-----|----------|---------|
| `vad-train` | Train model | `vad-train data_root=/path/to/data model_name=patchcore` |
| `vad-infer` | Batch score images | `vad-infer model_path=/path/model.ckpt test_folders=/path/images` |
| `vad-organize` | Triage by score (image list) | `vad-organize model_path=/path/model.ckpt image_list_file=/path/list.txt output_dir=./review` |
| `vad-infer-organize` | Infer + score buckets + posters | `vad-infer-organize model_path=/path/model.ckpt test_folders=/path/images` |
| `vad-train-infer` | Train + validation posters | `vad-train-infer train.data_root=/path/data infer_after_training.validation_images=/path/val` |
| `vad-full` | Train + infer-organize pipeline | `vad-full train.data_root=/path/data infer_organize.test_folders=/path/test` |
| `vad-hyperparam-search` | Grid search + comparison poster | `vad-hyperparam-search data_root=/path/data test_images=/path/test` |

### HPC submit CLIs (bsub at office)

Pair each local CLI with `vad-*-submit`. Same Hydra overrides plus `hpc.*` (queue, cores, memory, walltime, logs). Preview without cluster: `hpc.dry_run=true`.

| Submit CLI | Runs on cluster |
|------------|-----------------|
| `vad-train-submit` | `vad-train` |
| `vad-infer-submit` | `vad-infer` |
| `vad-organize-submit` | `vad-organize` |
| `vad-infer-organize-submit` | `vad-infer-organize` |
| `vad-train-infer-submit` | `vad-train-infer` |
| `vad-full-submit` | `vad-full` |
| `vad-hyperparam-search-submit` | `vad-hyperparam-search` |

Configs: `be_vision_ad_tools/tutorials/conf/hpc/submit_defaults.yaml`, `*_submit.yaml`.

### Skill scripts (wrappers around vad-*)

| Skill | Script |
|-------|--------|
| Verify | `.cursor/skills/verify-ad-pipeline/scripts/verify_*.sh` |
| Train | `.cursor/skills/train-anomaly-model/scripts/train_model.sh <data_root> [model]` |
| Inference | `.cursor/skills/run-ad-inference/scripts/run_inference.sh <model> <folder>` |
| Score triage (list) | `.cursor/skills/organize-anomaly-scores/scripts/organize_scores.sh <model> <list.txt> <out>` |
| Infer + organize | `.cursor/skills/infer-organize-ad/scripts/infer_organize.sh <model> <folder> [out]` |
| Train + infer | `.cursor/skills/train-infer-ad/scripts/train_infer.sh <data_root> <val_images> [model]` |
| Full pipeline | `.cursor/skills/full-ad-pipeline/scripts/full_pipeline.sh <data_root> <test> [model]` |
| Hyperparam search | `.cursor/skills/hyperparameter-search-ad/scripts/hyperparam_search.sh <data_root> <test> [class]` |
| Submit train HPC | `.cursor/skills/submit-train-ad-hpc/scripts/submit_train.sh <data_root> [model]` |
| Submit infer HPC | `.cursor/skills/submit-infer-ad-hpc/scripts/submit_infer.sh <model> <folder>` |
| Submit organize HPC | `.cursor/skills/submit-organize-ad-hpc/scripts/submit_organize.sh <model> <list.txt> <out>` |
| Submit infer-organize HPC | `.cursor/skills/submit-infer-organize-ad-hpc/scripts/submit_infer_organize.sh <model> <folder>` |
| Submit train-infer HPC | `.cursor/skills/submit-train-infer-ad-hpc/scripts/submit_train_infer.sh <data_root> <val> [model]` |
| Submit full HPC | `.cursor/skills/submit-full-ad-hpc/scripts/submit_full.sh <data_root> <test> [model]` |
| Submit hyperparam HPC | `.cursor/skills/submit-hyperparam-search-ad-hpc/scripts/submit_hyperparam_search.sh <data_root> <test>` |

Do not invent other commands. Do not bypass these with ad-hoc one-liners.

## Preprocessing contract (group policy)

- p2/p98 percentile normalization
- No silent PIL 16→8-bit conversion
- No elastic deformation (alters defect geometry)
- Use `TilerConfigurationCallback` for tiling (not `TilingConfigurationCallback`)

## Per-workflow details

See `.cursor/skills/*/SKILL.md` for full procedures and "what done looks like" examples.
