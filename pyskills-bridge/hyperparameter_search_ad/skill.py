"""Hyperparameter grid search + comparison poster (diff_parameter_and_save_poster)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from omegaconf import OmegaConf
from pyskills.core import allow

from be_vision_ad_tools.training.hyperparameter_hydra_cli import run_hyperparam_search

__all__ = ['hyperparam_search']


def hyperparam_search(
    data_root: str | Path,
    test_images: str | Path | list[str | Path],
    class_name: str = 'hyperparam_search',
    model_names: list[str] | None = None,
    backbones: list[str] | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Run hyperparameter grid search and save a comparison poster."""
    cfg = OmegaConf.create({
        'data_root': str(data_root),
        'test_images': test_images,
        'class_name': class_name,
        'model_names': model_names or ['padim', 'patchcore'],
        'backbones': backbones or ['wide_resnet50'],
        **kwargs,
    })
    return run_hyperparam_search(cfg)


allow(hyperparam_search)
