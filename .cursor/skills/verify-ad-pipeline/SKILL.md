---
name: verify-ad-pipeline
description: Run dependency sync, import smoke tests, and nbdev CI for the be_vision_ad_tools (vision_ad_tool) anomaly-detection library before trusting or committing changes. Use after editing anything under be_vision_ad_tools/ or nbs/, before telling the user a change works, and before committing — don't claim a fix works without running this.
---

# Verify the AD toolbox pipeline

`be_vision_ad_tools` wraps Anomalib for semiconductor X-ray/AOI anomaly detection. A silently broken trainer or inference path is worse than an obvious crash — it produces wrong scores that look plausible.

## Public API (use only these)

| Step | Command |
|------|---------|
| Sync deps | `bash .cursor/skills/verify-ad-pipeline/scripts/verify_sync.sh` |
| Import smoke | `bash .cursor/skills/verify-ad-pipeline/scripts/verify_imports.sh` |
| nbdev CI | `bash .cursor/skills/verify-ad-pipeline/scripts/verify_nbdev.sh` |

Do not invent other verification commands.

## What "done" looks like (demonstration)

```
Verified AD toolbox:
- uv sync: OK
- imports: flexible_trainer, unified_inference, anomaly_score_organizer
- nbdev_test: passed
- no uncommitted scratch in output_verify/
```

Report verification in these concrete terms — not a bare "it works."

## 1. Sync dependencies

```bash
bash .cursor/skills/verify-ad-pipeline/scripts/verify_sync.sh
```

Uses `uv sync` if available, else `pip install -e .`. Run this after any `pyproject.toml` change.

## 2. Import smoke test

```bash
bash .cursor/skills/verify-ad-pipeline/scripts/verify_imports.sh
```

Confirms the three main entry surfaces import without error. No GPU training here — if this fails, fix imports before running anything heavier.

## 3. nbdev CI

```bash
bash .cursor/skills/verify-ad-pipeline/scripts/verify_nbdev.sh
```

Same as `.github/workflows/test.yaml` (fastai/nbdev-ci). If you edited notebooks under `nbs/`, run `nbdev_prepare` first so `be_vision_ad_tools/` is in sync.

## Preprocessing contract (group policy)

When verifying changes that touch data loading or transforms, confirm these rules still hold:

- **p2/p98 percentile normalization** — no ad-hoc min/max scaling
- **No silent PIL 16→8-bit conversion** — preserve bit depth intentionally
- **No elastic deformation** — alters void/defect geometry
- **Patch/stitch rules** — use `TilerConfigurationCallback` (not `TilingConfigurationCallback`)

## Only after all of this

Tell the user what you verified concretely. Don't commit library changes without having actually run verification.

## pyskills twin

See `pyskills-bridge/verify_ad/skill.py` and `pyskills-bridge/REFERENCE.md`.
