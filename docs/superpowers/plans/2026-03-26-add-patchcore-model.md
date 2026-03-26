# Add PatchCore Model Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add PatchCore model with optimized defaults alongside PaDiM throughout all training, inference, export, and config notebooks.

**Architecture:** Add PatchCore-specific fields (`coreset_sampling_ratio`, `num_neighbors`) to `FlexibleTrainingConfig`, wire PatchCore params in `train_anomaly_model()`, add an exported `get_model_configs()` helper, then update all demo cells to loop over both models. Since this is an nbdev project, all code changes happen in notebooks (`.ipynb`), then `nbdev_export` regenerates `.py` files.

**Tech Stack:** anomalib (v1.x), nbdev, PyTorch Lightning

**Spec:** `docs/superpowers/specs/2026-03-26-add-patchcore-model-design.md`

---

### Task 1: Add PatchCore fields to FlexibleTrainingConfig and wire in train_anomaly_model()

**Files:**
- Modify: `nbs/04_training.flexible_anomaly_trainer.ipynb` (cells 20 and 33 — both `#| export`)

**This is the core task.** All other tasks depend on these exported changes.

- [ ] **Step 1: Add PatchCore fields to FlexibleTrainingConfig dataclass (cell 20)**

In the `FlexibleTrainingConfig` dataclass, add these fields after `n_features`:

```python
    # PatchCore-specific configuration
    coreset_sampling_ratio: float = 0.1  # PatchCore coreset sampling ratio (0-1)
    num_neighbors: int = 9  # PatchCore k-NN neighbors
```

- [ ] **Step 2: Add validation in `__post_init__` (cell 20)**

Add validation at the end of `__post_init__`:

```python
        # Validate PatchCore-specific parameters
        if not (0 < self.coreset_sampling_ratio <= 1):
            raise ValueError(f"coreset_sampling_ratio must be between 0 and 1, got {self.coreset_sampling_ratio}")
        if self.num_neighbors < 1:
            raise ValueError(f"num_neighbors must be a positive integer, got {self.num_neighbors}")
```

- [ ] **Step 3: Add PatchCore to layers conditional in train_anomaly_model() (cell 33)**

Change:
```python
        if config.model_name in [ModelType.PADIM, ModelType.STFPM]:
            model_config['layers'] = config.layers
```

To:
```python
        if config.model_name in [ModelType.PADIM, ModelType.STFPM, ModelType.PATCHCORE]:
            model_config['layers'] = config.layers
```

- [ ] **Step 4: Add PatchCore-specific params to model_config (cell 33)**

After the `n_features` conditional block, add:

```python
        if config.model_name == ModelType.PATCHCORE:
            model_config['coreset_sampling_ratio'] = config.coreset_sampling_ratio
            model_config['num_neighbors'] = config.num_neighbors
```

- [ ] **Step 5: Add PatchCore layer defaults to train_model_and_create_posters() in notebook 06**

In `nbs/06_inference.prediction_system.ipynb`, cell 136 (`#| export`), the `train_model_and_create_posters()` function has this block:

```python
        if model_name.lower() in ["padim", "stfpm"]:
            layers = ["layer1", "layer2", "layer3"]
        else:
            layers = ["layer3"]
```

Change to:

```python
        if model_name.lower() in ["padim", "stfpm"]:
            layers = ["layer1", "layer2", "layer3"]
        elif model_name.lower() == "patchcore":
            layers = ["layer2", "layer3"]
        else:
            layers = ["layer3"]
```

- [ ] **Step 6: Run nbdev_export and verify**

```bash
cd /home/hasan/workspace/projects/git_data/vision_ad_tool && nbdev_export
```

Verify the generated `.py` files contain PatchCore changes:
```bash
grep -n "coreset_sampling_ratio" be_vision_ad_tools/training/flexible_trainer.py
grep -n "PATCHCORE" be_vision_ad_tools/training/flexible_trainer.py
```

- [ ] **Step 7: Commit**

```bash
git add nbs/04_training.flexible_anomaly_trainer.ipynb nbs/06_inference.prediction_system.ipynb be_vision_ad_tools/
git commit -m "feat: Add PatchCore config fields and wire in train_anomaly_model()"
```

---

### Task 2: Add get_model_configs() exported helper

**Files:**
- Modify: `nbs/04_training.flexible_anomaly_trainer.ipynb` (add new `#| export` cell after cell 23)

- [ ] **Step 1: Add get_model_configs() export cell**

Add a new `#| export` cell after the `from_dict()` cell (cell 23) with:

```python
#| export
def get_model_configs(
    data_root: Union[str, Path] = None,
    **shared_kwargs
) -> list:
    """Return optimized configs for PaDiM and PatchCore.

    Args:
        data_root: Path to data root (passed to both configs)
        **shared_kwargs: Any shared FlexibleTrainingConfig kwargs applied to both

    Returns:
        List of [padim_config, patchcore_config]
    """
    base_kwargs = {}
    if data_root is not None:
        base_kwargs['data_root'] = data_root
    base_kwargs.update(shared_kwargs)

    padim_config = FlexibleTrainingConfig(
        model_name=ModelType.PADIM,
        backbone=BackboneType.RESNET18,
        layers=["layer1", "layer2", "layer3"],
        **base_kwargs,
    )
    patchcore_config = FlexibleTrainingConfig(
        model_name=ModelType.PATCHCORE,
        backbone=BackboneType.WIDE_RESNET50,
        layers=["layer2", "layer3"],
        coreset_sampling_ratio=0.1,
        num_neighbors=9,
        **base_kwargs,
    )
    return [padim_config, patchcore_config]
```

- [ ] **Step 2: Run nbdev_export and verify**

```bash
cd /home/hasan/workspace/projects/git_data/vision_ad_tool && nbdev_export
grep -n "get_model_configs" be_vision_ad_tools/training/flexible_trainer.py
```

- [ ] **Step 3: Commit**

```bash
git add nbs/04_training.flexible_anomaly_trainer.ipynb be_vision_ad_tools/
git commit -m "feat: Add get_model_configs() helper for PaDiM + PatchCore"
```

---

### Task 3: Update training demo cells in notebook 04

**Files:**
- Modify: `nbs/04_training.flexible_anomaly_trainer.ipynb` (demo cells 35, 74)

- [ ] **Step 1: Update cell 35 — basic training example**

Replace the single PaDiM config with a loop:

```python
#| eval: false
from be_vision_ad_tools.training.flexible_trainer import get_model_configs

root = Path(r'/home/ai_dsx.work/data/projects/AD_tool_test/images')
configs = get_model_configs(
    data_root=root,
    normal_dir="good",
    abnormal_dir="bad",
    class_name="test_manual",
    max_epochs=1,
)

results = {}
for config in configs:
    model_name = config.model_name.value if hasattr(config.model_name, 'value') else config.model_name
    print(f"\n{'='*60}\nTraining {model_name}\n{'='*60}")
    results[model_name] = train_anomaly_model(config)
```

- [ ] **Step 2: Commit**

```bash
git add nbs/04_training.flexible_anomaly_trainer.ipynb
git commit -m "feat: Update training demo cells to loop over PaDiM + PatchCore"
```

---

### Task 4: Update hyperparameter search notebook 07

**Files:**
- Modify: `nbs/07_training.hyperparameter_search.ipynb` (demo cells 15, 19, 73)

- [ ] **Step 1: Update cell 15 — grid setup example**

Change:
```python
model_names = ['padim']
```
To:
```python
model_names = ['padim', 'patchcore']
```

- [ ] **Step 2: Update cell 19 — function call example**

Change:
```python
    model_names=['padim'],           # Just 1 model for quick test
```
To:
```python
    model_names=['padim', 'patchcore'],
```

- [ ] **Step 3: Update cell 73 — comprehensive example**

Change:
```python
    model_names=['padim'],
```
To:
```python
    model_names=['padim', 'patchcore'],
```

**Note:** PatchCore does not use `n_features` — it uses `coreset_sampling_ratio` instead. The existing `simple_hyperparameter_search()` function passes `n_features` to `FlexibleTrainingConfig` for all models, but `n_features` is only applied to PaDiM in `train_anomaly_model()`. So adding PatchCore to the model_names list works correctly — PatchCore simply ignores `n_features` and uses its own defaults for `coreset_sampling_ratio`.

- [ ] **Step 4: Commit**

```bash
git add nbs/07_training.hyperparameter_search.ipynb
git commit -m "feat: Add PatchCore to hyperparameter search examples"
```

---

### Task 5: Update multi-node training notebook 08

**Files:**
- Modify: `nbs/08_training.multi_node.ipynb` (export cell 11, demo cell 26)

- [ ] **Step 1: Update generate_training_tasks() default (cell 11, export)**

Change the default from:
```python
    if model_names is None:
        model_names = ['padim']
```
To:
```python
    if model_names is None:
        model_names = ['padim', 'patchcore']
```

- [ ] **Step 2: Update demo cell 26**

Change:
```python
model_names = ['padim']
```
To:
```python
model_names = ['padim', 'patchcore']
```

- [ ] **Step 3: Run nbdev_export**

```bash
cd /home/hasan/workspace/projects/git_data/vision_ad_tool && nbdev_export
```

- [ ] **Step 4: Commit**

```bash
git add nbs/08_training.multi_node.ipynb be_vision_ad_tools/
git commit -m "feat: Add PatchCore to multi-node training defaults"
```

---

### Task 6: Update inference demo cells in notebook 06

**Files:**
- Modify: `nbs/06_inference.prediction_system.ipynb` (demo cell 138)

- [ ] **Step 1: Update cell 138 — train_model_and_create_posters demo**

Replace the single call with a loop:

```python
#| eval: false
for model_name in ['padim', 'patchcore']:
    print(f"\n{'='*60}\nTraining and creating posters for {model_name}\n{'='*60}")
    train_model_and_create_posters(
        data_root=DATA_ROOT,
        normal_dir="good",
        abnormal_dir="bad",
        class_name="normal",
        model_name=model_name,
        output_folder=f"{output_folder}_{model_name}",
    )
```

- [ ] **Step 2: Commit**

```bash
git add nbs/06_inference.prediction_system.ipynb
git commit -m "feat: Add PatchCore to inference demo cells"
```

---

### Task 7: Update postprocessing demo cells in notebook 09

**Files:**
- Modify: `nbs/09_postprocessing.model_metadata.ipynb` (demo cells 11, 50)

- [ ] **Step 1: Update cell 11 — add PatchCore model path example**

After the existing PaDiM path, add:

```python
# PatchCore model path example
model_path_patchcore = Path(r'/home/ai_dsx.work/data/projects/AD_tool_test/models/exports/TEST_MULITNODE_task_001_patchcore_wide_resnet50_2_layer2-layer3/weights/torch/model.pt')
print(f'patchcore model exists: {model_path_patchcore.exists()}')
```

- [ ] **Step 2: Update cell 50 — add PatchCore metadata modification example**

After the existing PaDiM example, add:

```python
# PatchCore model metadata modification
model_path_pc = Path(r'/home/ai_dsx.work/data/projects/AD_tool_test/models/exports/TEST_MULITNODE_task_000_patchcore_wide_resnet50_2_layer2-layer3/weights/torch/model.pt')
if model_path_pc.exists():
    modify_model_metadata_cli(
        model_path=model_path_pc,
        image_threshold=10,
        pixel_threshold=10,
        pred_score_max=10.0,
        anomaly_map_min=0,
        anomaly_map_max=12.0,
        create_poster=True,
        test_images_folder=test_images,
        poster_rows=1,
        poster_cols=2
    )
```

- [ ] **Step 3: Commit**

```bash
git add nbs/09_postprocessing.model_metadata.ipynb
git commit -m "feat: Add PatchCore examples to model metadata notebook"
```

---

### Task 8: Update remaining inference demo notebooks (10, 12, 13, 14)

**Files:**
- Modify: `nbs/10_inference.multinode_infer.ipynb` (demo cells 69-71)
- Modify: `nbs/12_inference.multinode_inference.ipynb` (demo cells 11, 116-117)
- Modify: `nbs/13_inference.unified_inference.ipynb` (demo cell 14 — has PaDiM-specific model path)
- Modify: `nbs/14_inference.anomaly_score_organizer.ipynb` (demo cell 36)

- [ ] **Step 1: Update notebook 10 demo comments (cells 69-71)**

Change PaDiM-only comments to mention both models. For example, change:
```python
# Your trained PaDiM model
```
To:
```python
# Your trained model (PaDiM or PatchCore)
```

- [ ] **Step 2: Update notebook 12 demo cell 11 — add PatchCore path**

After the existing PaDiM path:
```python
# PatchCore model path
MODEL_PATH_PC = Path(MODEL_ROOT, 'exports', 'TEST_MULITNODE_task_000_patchcore_wide_resnet50_2_layer2-layer3', 'weights', 'torch', 'model.pt')
```

- [ ] **Step 3: Update notebook 13 demo cell 14 — add PatchCore model path**

After the existing PaDiM model path variable, add a PatchCore equivalent:
```python
# PatchCore model
MODEL_PATH_PC = Path(MODEL_ROOT, 'exports', 'TEST_MULITNODE_task_000_patchcore_wide_resnet50_2_layer2-layer3', 'weights', 'torch', 'model.pt')
```

- [ ] **Step 4: Update notebook 14 demo cell 36 — add PatchCore metadata**

Change:
```python
metadata={...,"model": "padim"}
```
To:
```python
metadata={...,"model": "padim"}  # Also works with "patchcore"
```

- [ ] **Step 5: Commit**

```bash
git add nbs/10_inference.multinode_infer.ipynb nbs/12_inference.multinode_inference.ipynb nbs/13_inference.unified_inference.ipynb nbs/14_inference.anomaly_score_organizer.ipynb
git commit -m "feat: Add PatchCore references to inference demo notebooks"
```

---

### Task 9: Run nbdev_export and final verification

**Files:**
- All notebooks
- All generated `be_vision_ad_tools/**/*.py`

- [ ] **Step 1: Run nbdev_export**

```bash
cd /home/hasan/workspace/projects/git_data/vision_ad_tool && nbdev_export
```

- [ ] **Step 2: Verify PatchCore in generated files**

```bash
grep -rn "coreset_sampling_ratio" be_vision_ad_tools/
grep -rn "num_neighbors" be_vision_ad_tools/
grep -rn "PATCHCORE" be_vision_ad_tools/training/flexible_trainer.py
grep -rn "get_model_configs" be_vision_ad_tools/training/flexible_trainer.py
grep -rn "patchcore" be_vision_ad_tools/inference/prediction_system.py
```

- [ ] **Step 3: Verify imports work**

```bash
cd /home/hasan/workspace/projects/git_data/vision_ad_tool && python -c "
from be_vision_ad_tools.training.flexible_trainer import (
    FlexibleTrainingConfig, ModelType, BackboneType, get_model_configs
)
configs = get_model_configs()
for c in configs:
    print(f'{c.model_name.value}: backbone={c.backbone}, layers={c.layers}')
print('All imports and configs OK')
"
```

- [ ] **Step 4: Final commit if any remaining changes**

```bash
git add -A && git status
# Only commit if there are changes
git commit -m "chore: Regenerate Python modules with PatchCore support"
```

---

## Notebooks NOT Modified (confirmed no changes needed)

- `00_core.ipynb` — stub
- `01_data.transfer.ipynb` — data transfer, no model logic
- `11_inference.multinode_from_aiop_tool.ipynb` — HPC infrastructure only
- `15_inference.unified_with_threshold_posters.ipynb` — all functions model-agnostic
- `16_tiling_fix_and_implementation.ipynb` — bug docs
- `17_fixing_padim_tiling_current_version.ipynb` — bug docs
- `index.ipynb` — project README
