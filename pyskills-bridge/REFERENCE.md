# pyskills ↔ Cursor skills for vision_ad_tools

Fifteen workflows, two media. Use Cursor skills in the IDE; use pyskills modules in Solveit/clikernel.

## Skills map

| Workflow | Cursor skill | Local CLI | HPC submit CLI | pyskills module | Main function |
|----------|--------------|-----------|----------------|-----------------|---------------|
| Verify before commit | `verify-ad-pipeline` | — | — | `verify_ad.skill` | `verify_all()` |
| Train model | `train-anomaly-model` | `vad-train` | `vad-train-submit` | `train_ad.skill` | `train()` |
| Batch inference | `run-ad-inference` | `vad-infer` | `vad-infer-submit` | `infer_ad.skill` | `infer()` |
| Score triage | `organize-anomaly-scores` | `vad-organize` | `vad-organize-submit` | `organize_ad.skill` | `organize()` |
| Infer + organize | `infer-organize-ad` | `vad-infer-organize` | `vad-infer-organize-submit` | `infer_organize_ad.skill` | `infer_organize()` |
| Train + infer | `train-infer-ad` | `vad-train-infer` | `vad-train-infer-submit` | `train_infer_ad.skill` | `train_infer()` |
| Full pipeline | `full-ad-pipeline` | `vad-full` | `vad-full-submit` | `full_ad.skill` | `full_pipeline()` |
| Hyperparam search | `hyperparameter-search-ad` | `vad-hyperparam-search` | `vad-hyperparam-search-submit` | `hyperparameter_search_ad.skill` | `hyperparam_search()` |
| Submit train HPC | `submit-train-ad-hpc` | — | `vad-train-submit` | `submit_train_ad_hpc.skill` | `submit_train()` |
| Submit infer HPC | `submit-infer-ad-hpc` | — | `vad-infer-submit` | `submit_infer_ad_hpc.skill` | `submit_infer()` |
| Submit organize HPC | `submit-organize-ad-hpc` | — | `vad-organize-submit` | `submit_organize_ad_hpc.skill` | `submit_organize()` |
| Submit infer-organize HPC | `submit-infer-organize-ad-hpc` | — | `vad-infer-organize-submit` | `submit_infer_organize_ad_hpc.skill` | `submit_infer_organize()` |
| Submit train-infer HPC | `submit-train-infer-ad-hpc` | — | `vad-train-infer-submit` | `submit_train_infer_ad_hpc.skill` | `submit_train_infer()` |
| Submit full HPC | `submit-full-ad-hpc` | — | `vad-full-submit` | `submit_full_ad_hpc.skill` | `submit_full()` |
| Submit hyperparam HPC | `submit-hyperparam-search-ad-hpc` | — | `vad-hyperparam-search-submit` | `submit_hyperparam_search_ad_hpc.skill` | `submit_hyperparam_search()` |

## HPC submit configs

Shared defaults: `be_vision_ad_tools/tutorials/conf/hpc/submit_defaults.yaml`

Per-workflow submit overlays: `be_vision_ad_tools/tutorials/conf/*_submit.yaml`

nbdev source: `nbs/20_tutorials.hpc_submit_cli.ipynb` → `be_vision_ad_tools/tutorials/hpc_submit_cli.py`

## Concept map (same as computer_use bridge)

| pyskills | Cursor |
|----------|--------|
| First docstring paragraph | YAML `description:` |
| `__all__` | Public API table |
| `doc(module)` | SKILL.md body |
| `allow(func)` | "use only these scripts" |
| Demonstration block | "What done looks like" section |

## Install pyskills bridge

```bash
cd pyskills-bridge
uv sync
uv run python -c "from pyskills import list_pyskills; print([k for k in list_pyskills() if k.endswith('.skill')])"
```

## Python-kernel usage

```python
from pyskills import doc
import submit_train_ad_hpc.skill as st

print(doc(st))
st.submit_train('/data/my_product', dry_run=True)
```

## Preprocessing contract (group policy)

Shared across all skills:

- p2/p98 percentile normalization
- No silent PIL 16→8-bit conversion
- No elastic deformation
- `TilerConfigurationCallback` for tiling (not `TilingConfigurationCallback`)

## Repo source

Clone `https://github.com/HasanGoni/vision_ad_tool` into this directory. Package: `be_vision_ad_tools`.

Hydra CLIs are nbdev-exported from `nbs/18_tutorials.end2end_hydra_cli.ipynb`, `nbs/19_training.hyperparameter_hydra_cli.ipynb`, and `nbs/20_tutorials.hpc_submit_cli.ipynb`. Configs: `be_vision_ad_tools/tutorials/conf/*.yaml`.
