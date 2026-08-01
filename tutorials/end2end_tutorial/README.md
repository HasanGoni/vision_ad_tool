# End-to-end tutorial CLIs (compatibility shim)

Hydra CLIs are now **nbdev-exported** from `nbs/18_tutorials.end2end_hydra_cli.ipynb` into `be_vision_ad_tools/tutorials/end2end_cli.py`.

Configs are packaged at `be_vision_ad_tools/tutorials/conf/*.yaml`.

This directory keeps thin re-exports for backward compatibility (`tutorials.end2end_tutorial.workflow` / `.cli`).

## Commands

| CLI | Config | Library function |
|-----|--------|------------------|
| `vad-train` | `conf/train.yaml` | `train_anomaly_model` |
| `vad-infer` | `conf/infer.yaml` | `unified_inference` |
| `vad-organize` | `conf/organize.yaml` | `predict_and_organize_by_score` |
| `vad-infer-organize` | `conf/infer_organize.yaml` | `unified_inference_with_threshold_posters` |
| `vad-train-infer` | `conf/train_infer.yaml` | train + `run_inference_after_training` |
| `vad-full` | `conf/full.yaml` | train + infer-organize pipeline |
| `vad-hyperparam-search` | `conf/hyperparam_search.yaml` | `diff_parameter_and_save_poster` |

```bash
uv sync
vad-train data_root=/path/to/data class_name=my_product
vad-hyperparam-search data_root=/path/to/data test_images=/path/to/test
```

Override any config field on the command line (Hydra syntax).
