"""Wrappers around be_vision_ad_tools end-to-end workflow functions."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from omegaconf import DictConfig, OmegaConf

from be_vision_ad_tools.inference.anomaly_score_organizer import predict_and_organize_by_score
from be_vision_ad_tools.inference.unified_inference import unified_inference
from be_vision_ad_tools.inference.unified_with_threshold_posters import unified_inference_with_threshold_posters
from be_vision_ad_tools.training.flexible_trainer import FlexibleTrainingConfig, train_anomaly_model, run_inference_after_training


def cfg_to_dict(cfg: DictConfig) -> dict[str, Any]:
    """Convert a Hydra DictConfig to a plain dict with variables resolved."""
    return OmegaConf.to_container(cfg, resolve=True, throw_on_missing=True)  # type: ignore[return-value]


def run_train(cfg: DictConfig) -> dict[str, Any]:
    """Train an anomaly-detection model."""
    params = cfg_to_dict(cfg)
    config = FlexibleTrainingConfig(**params)
    return train_anomaly_model(config)


def run_infer(cfg: DictConfig) -> dict[str, Any]:
    """Run unified inference on image folder(s) or list file."""
    params = cfg_to_dict(cfg)
    return unified_inference(**params)


def run_organize(cfg: DictConfig) -> dict[str, Any]:
    """Predict anomaly scores and organize images into threshold folders."""
    params = cfg_to_dict(cfg)
    return predict_and_organize_by_score(**params)


def run_infer_organize(cfg: DictConfig) -> dict[str, Any]:
    """Unified inference + threshold folders + optional posters."""
    params = cfg_to_dict(cfg)
    return unified_inference_with_threshold_posters(**params)


def run_train_infer(cfg: DictConfig) -> dict[str, Any]:
    """Train a model, then run inference/posters from training results."""
    root = cfg_to_dict(cfg)
    train_params = root.get('train', root)
    infer_params = root.get('infer_after_training', {})

    training_results = run_train(OmegaConf.create(train_params))
    return run_inference_after_training(training_results, **infer_params)


def run_full(cfg: DictConfig) -> dict[str, Any]:
    """Train, then run unified inference with threshold organization."""
    root = cfg_to_dict(cfg)
    train_params = root['train']
    infer_params = root['infer_organize']

    training_results = run_train(OmegaConf.create(train_params))
    if not training_results.get('success', False):
        raise RuntimeError('Training failed; aborting full pipeline')

    export_paths = training_results.get('export_paths', {})
    model_path = export_paths.get('torch') or training_results.get('best_model_path')
    if model_path is None:
        raise RuntimeError('No model path in training results')

    infer_params = dict(infer_params)
    infer_params['model_path'] = str(model_path)
    return run_infer_organize(OmegaConf.create(infer_params))
