"""Train a model, then run_inference_after_training."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from omegaconf import OmegaConf
from pyskills.core import allow

from be_vision_ad_tools.tutorials.end2end_cli import run_train_infer

__all__ = ['train_infer']


def train_infer(
    data_root: str | Path,
    validation_images: str | Path | list[str | Path],
    model_name: str = 'padim',
    test_images: str | Path | list[str | Path] | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Train, then run inference/posters from training results."""
    cfg = OmegaConf.create({
        'train': {'data_root': str(data_root), 'model_name': model_name, **kwargs.get('train', {})},
        'infer_after_training': {
            'validation_images': validation_images,
            'test_images': test_images,
            **kwargs.get('infer_after_training', {}),
        },
    })
    return run_train_infer(cfg)


allow(train_infer)
