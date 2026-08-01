"""Inference + threshold organization + posters (unified_inference_with_threshold_posters)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from omegaconf import OmegaConf
from pyskills.core import allow

from tutorials.end2end_tutorial.workflow import run_infer_organize

__all__ = ['infer_organize']


def infer_organize(
    model_path: str | Path,
    test_folders: str | Path | list[str | Path],
    output_dir: str | Path | None = None,
    execution_mode: str = 'auto',
    **kwargs: Any,
) -> dict[str, Any]:
    """Run unified inference with threshold folders and optional posters."""
    cfg = OmegaConf.create({
        'model_path': str(model_path),
        'test_folders': test_folders,
        'output_dir': output_dir,
        'execution_mode': execution_mode,
        **kwargs,
    })
    return run_infer_organize(cfg)


allow(infer_organize)
