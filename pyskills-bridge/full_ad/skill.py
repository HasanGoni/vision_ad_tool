"""Full pipeline: train then unified inference with threshold organization."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from omegaconf import OmegaConf
from pyskills.core import allow

from be_vision_ad_tools.tutorials.end2end_cli import run_full

__all__ = ['full_pipeline']


def full_pipeline(
    data_root: str | Path,
    test_folders: str | Path | list[str | Path],
    model_name: str = 'patchcore',
    **kwargs: Any,
) -> dict[str, Any]:
    """Train, then run infer-organize on test folders."""
    cfg = OmegaConf.create({
        'train': {'data_root': str(data_root), 'model_name': model_name, **kwargs.get('train', {})},
        'infer_organize': {'test_folders': test_folders, **kwargs.get('infer_organize', {})},
    })
    return run_full(cfg)


allow(full_pipeline)
