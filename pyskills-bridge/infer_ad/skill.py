"""Score images for anomalies using unified_inference — auto serial/parallel/HPC.

Use when batch-scoring production X-ray/AOI images from a trained checkpoint.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pyskills.core import allow

__all__ = ['infer']


def infer(
    model_path: str | Path,
    test_folders: str | Path | list[str | Path],
    execution_mode: str = 'auto',
    batch_size: int = 100,
    output_dir: str | Path | None = None,
    save_heatmaps: bool = True,
    **kwargs: Any,
) -> dict[str, Any]:
    """Run unified inference. Returns result dict with scores and paths."""
    from be_vision_ad_tools.inference.unified_inference import unified_inference

    return unified_inference(
        model_path=model_path,
        test_folders=test_folders,
        execution_mode=execution_mode,
        batch_size=batch_size,
        output_dir=output_dir,
        save_heatmaps=save_heatmaps,
        **kwargs,
    )


allow(infer)
