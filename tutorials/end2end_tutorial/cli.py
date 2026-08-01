"""Hydra CLIs for end-to-end anomaly-detection workflows."""

from __future__ import annotations

from pathlib import Path

import hydra
from omegaconf import DictConfig

from .workflow import (
    run_full,
    run_infer,
    run_infer_organize,
    run_organize,
    run_train,
    run_train_infer,
)

_CONF = str(Path(__file__).resolve().parent / 'conf')


@hydra.main(version_base=None, config_path=_CONF, config_name='train')
def train_cli(cfg: DictConfig) -> None:
    """Train an anomaly-detection model."""
    result = run_train(cfg)
    print(result)


@hydra.main(version_base=None, config_path=_CONF, config_name='infer')
def infer_cli(cfg: DictConfig) -> None:
    """Score images with unified inference."""
    result = run_infer(cfg)
    print(result)


@hydra.main(version_base=None, config_path=_CONF, config_name='organize')
def organize_cli(cfg: DictConfig) -> None:
    """Organize images by anomaly score."""
    result = run_organize(cfg)
    print(result)


@hydra.main(version_base=None, config_path=_CONF, config_name='infer_organize')
def infer_organize_cli(cfg: DictConfig) -> None:
    """Inference + threshold folders + posters."""
    result = run_infer_organize(cfg)
    print(result)


@hydra.main(version_base=None, config_path=_CONF, config_name='train_infer')
def train_infer_cli(cfg: DictConfig) -> None:
    """Train, then inference/posters from training results."""
    result = run_train_infer(cfg)
    print(result)


@hydra.main(version_base=None, config_path=_CONF, config_name='full')
def full_cli(cfg: DictConfig) -> None:
    """Train, then unified inference with threshold organization."""
    result = run_full(cfg)
    print(result)
