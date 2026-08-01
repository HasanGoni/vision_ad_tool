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
- nbdev_test: passed
```

## Public API — use only these scripts

| Workflow | Script |
|----------|--------|
| Verify | `.cursor/skills/verify-ad-pipeline/scripts/verify_*.sh` |
| Train | `.cursor/skills/train-anomaly-model/scripts/train_model.sh <data_root> [model]` |
| Inference | `.cursor/skills/run-ad-inference/scripts/run_inference.sh <model> <folder>` |
| Score triage | `.cursor/skills/organize-anomaly-scores/scripts/organize_scores.sh <model> <list.txt> <out>` |

Do not invent other commands. Do not bypass these scripts with ad-hoc one-liners.

## Preprocessing contract (group policy)

- p2/p98 percentile normalization
- No silent PIL 16→8-bit conversion
- No elastic deformation (alters defect geometry)
- Use `TilerConfigurationCallback` for tiling (not `TilingConfigurationCallback`)

## Per-workflow details

See `.cursor/skills/*/SKILL.md` for full procedures and "what done looks like" examples.
