# Add PatchCore Model Alongside PaDiM

**Date**: 2026-03-26
**Status**: Approved

## Summary

Add PatchCore model support alongside PaDiM throughout the entire vision_ad_tool pipeline. PatchCore is already defined in the `ModelType` enum but not actively used in notebooks. This spec adds PatchCore with optimized defaults to all training, inference, export, and config notebooks using a parameterized/loop approach.

## PatchCore-Optimized Defaults

| Parameter | PaDiM | PatchCore |
|-----------|-------|-----------|
| Backbone | `resnet18` | `wide_resnet50_2` |
| Layers | `["layer1", "layer2", "layer3"]` | `["layer2", "layer3"]` |
| coreset_sampling_ratio | N/A | `0.1` |
| num_neighbors | N/A | `9` |
| Image size | `(256, 256)` | `(256, 256)` |

## Architecture

A `get_model_configs()` helper function returns a list of `FlexibleTrainingConfig` instances for both PaDiM and PatchCore with their respective optimized defaults. All notebook demo cells loop over this list.

```python
def get_model_configs() -> list:
    """Return optimized configs for PaDiM and PatchCore."""
    padim_config = FlexibleTrainingConfig(
        model_name=ModelType.PADIM,
        backbone=BackboneType.RESNET18,
        layers=["layer1", "layer2", "layer3"],
    )
    patchcore_config = FlexibleTrainingConfig(
        model_name=ModelType.PATCHCORE,
        backbone="wide_resnet50_2",
        layers=["layer2", "layer3"],
        coreset_sampling_ratio=0.1,
        num_neighbors=9,
    )
    return [padim_config, patchcore_config]
```

Usage pattern in notebooks:

```python
for config in get_model_configs():
    train_anomaly_model(config)
```

## Notebooks to Modify

### Training
- **04_training.flexible_anomaly_trainer.ipynb**: Add `get_model_configs()` helper; update training demo cells to loop over both models
- **07_training.hyperparameter_search.ipynb**: Include PatchCore in hyperparameter search grid
- **08_training.multi_node.ipynb**: Add PatchCore to distributed task generation

### Inference
- **06_inference.prediction_system.ipynb**: Update inference demos to load/run both model types
- **10_inference.multinode_infer.ipynb**: Handle both models in multinode inference
- **11_inference.multinode_from_aiop_tool.ipynb**: Include PatchCore in HPC inference
- **12_inference.multinode_inference.ipynb**: Add PatchCore to smart batching
- **13_inference.unified_inference.ipynb**: Run unified inference for both models
- **14_inference.anomaly_score_organizer.ipynb**: Loop over both models for score organization
- **15_inference.unified_with_threshold_posters.ipynb**: Generate posters for both models

### Postprocessing
- **09_postprocessing.model_metadata.ipynb**: Show metadata modification for both model types

## Notebooks NOT Modified

- **00_core.ipynb**: Core module stub, no model-specific code
- **01_data.transfer.ipynb**: Data transfer, no model-specific code
- **16_tiling_fix_and_implementation.ipynb**: Bug documentation, tiling is model-agnostic
- **17_fixing_padim_tiling_current_version.ipynb**: Bug documentation
- **index.ipynb**: Project index/README

## FlexibleTrainingConfig Changes

Add PatchCore-specific fields to the dataclass:

- `coreset_sampling_ratio: float = 0.1` - PatchCore coreset sampling ratio
- `num_neighbors: int = 9` - PatchCore k-NN neighbors

These fields are only used when `model_name == ModelType.PATCHCORE` and are ignored for other models.

## train_anomaly_model() Changes

Update the model instantiation logic to pass PatchCore-specific parameters when `model_name == ModelType.PATCHCORE`:

```python
if model_name == ModelType.PATCHCORE:
    from anomalib.models import Patchcore
    model = Patchcore(
        backbone=backbone,
        layers=layers,
        coreset_sampling_ratio=config.coreset_sampling_ratio,
        num_neighbors=config.num_neighbors,
    )
```

## Inference System

No changes needed to inference code. The existing `_detect_model_class_from_filename()` already detects "patchcore" in filenames. The `TorchInferencer` and `OpenVINOInferencer` are model-agnostic.

## Export

Model export uses the same `ExportType.TORCH` / `ExportType.ONNX` paths. No changes needed to export logic — PatchCore exports the same way as PaDiM.

## Testing

Verify by running notebooks end-to-end:
1. Training produces both PaDiM and PatchCore model files
2. Inference loads and runs both model types
3. Score organization works for both
4. Poster generation includes both models
5. Model metadata can be modified for both

## Risks

- PatchCore with `wide_resnet50_2` uses more memory than PaDiM with `resnet18` — users on limited GPU may need to reduce image size or switch backbone
- Coreset sampling adds training time compared to PaDiM
