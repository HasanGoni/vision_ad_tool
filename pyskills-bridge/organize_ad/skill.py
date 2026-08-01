"""Score images, bucket by anomaly threshold, and create review posters.

Use for false-alarm triage and active-learning queue building.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pyskills.core import allow

__all__ = ['organize']


def organize(
    model_path: str | Path,
    image_list_file: str | Path,
    output_dir: str | Path,
    score_thresholds: list[float] | None = None,
    create_posters: bool = True,
    **kwargs: Any,
) -> dict[str, Any]:
    """Predict, organize by score, optionally create posters."""
    from be_vision_ad_tools.inference.anomaly_score_organizer import predict_and_organize_by_score

    if score_thresholds is None:
        score_thresholds = [0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    return predict_and_organize_by_score(
        model_path=model_path,
        image_list_file=image_list_file,
        output_dir=output_dir,
        score_thresholds=score_thresholds,
        create_posters=create_posters,
        save_metadata=True,
        **kwargs,
    )


allow(organize)
