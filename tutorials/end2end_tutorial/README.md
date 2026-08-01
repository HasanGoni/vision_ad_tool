# End-to-end tutorial CLIs

Hydra-driven command-line entry points for the main `be_vision_ad_tools` workflows.

## Commands

| CLI | Config | Library function |
|-----|--------|------------------|
| `vad-train` | `conf/train.yaml` | `train_anomaly_model` |
| `vad-infer` | `conf/infer.yaml` | `unified_inference` |
| `vad-organize` | `conf/organize.yaml` | `predict_and_organize_by_score` |
| `vad-infer-organize` | `conf/infer_organize.yaml` | `unified_inference_with_threshold_posters` |
| `vad-train-infer` | `conf/train_infer.yaml` | `train_anomaly_model` + `run_inference_after_training` |
| `vad-full` | `conf/full.yaml` | train + `unified_inference_with_threshold_posters` |

Install the package (`uv sync` or `pip install -e .`), then run:

```bash
vad-train data_root=/path/to/data class_name=my_product
vad-infer model_path=/path/model.ckpt test_folders=/path/images
vad-organize model_path=/path/model.ckpt image_list_file=/path/list.txt output_dir=./review
vad-infer-organize model_path=/path/model.ckpt test_folders=/path/images
vad-train-infer train.data_root=/path/to/data infer_after_training.validation_images=/path/val
vad-full train.data_root=/path/to/data infer_organize.test_folders=/path/test
```

Override any config field on the command line (Hydra syntax). Edit defaults in `conf/*.yaml`.

Configs live in `tutorials/end2end_tutorial/conf/` (bundled with the package).
