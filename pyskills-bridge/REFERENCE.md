# pyskills ↔ Cursor skills for vision_ad_tools

Four workflows, two media. Use Cursor skills in the IDE; use pyskills modules in Solveit/clikernel.

## Skills map

| Workflow | Cursor skill | pyskills module | Main function |
|----------|--------------|-----------------|---------------|
| Verify before commit | `verify-ad-pipeline` | `verify_ad.skill` | `verify_all()` |
| Train model | `train-anomaly-model` | `train_ad.skill` | `train()` |
| Batch inference | `run-ad-inference` | `infer_ad.skill` | `infer()` |
| Score triage | `organize-anomaly-scores` | `organize_ad.skill` | `organize()` |

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
import verify_ad.skill as v
import train_ad.skill as t
import infer_ad.skill as i
import organize_ad.skill as o

print(doc(v))
v.verify_all()
t.train('/data/my_product', model_name='patchcore')
i.infer('/path/model.ckpt', '/path/images')
o.organize('/path/model.ckpt', 'images.txt', './review')
```

## Preprocessing contract (group policy)

Shared across all skills:

- p2/p98 percentile normalization
- No silent PIL 16→8-bit conversion
- No elastic deformation
- `TilerConfigurationCallback` for tiling (not `TilingConfigurationCallback`)

## Repo source

Clone `https://github.com/HasanGoni/vision_ad_tool` into this directory. Package: `be_vision_ad_tools`.
