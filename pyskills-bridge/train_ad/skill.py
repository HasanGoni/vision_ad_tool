"""Train an Anomalib-based anomaly detection model using be_vision_ad_tools flexible_trainer.

Use when the user needs a new AD checkpoint for X-ray/AOI defect detection.

## Public API

- `train(data_root, model_name='patchcore', class_name='anomaly_detection', **kwargs)`
- `train_from_yaml(yaml_path)`

## Dataset layout

data_root/good/ (normal) and data_root/bad/ (abnormal) by default.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pyskills.core import allow

__all__ = ['train', 'train_from_yaml']


def train(
    data_root: str | Path,
    model_name: str = 'patchcore',
    class_name: str = 'anomaly_detection',
    backbone: str = 'resnet18',
    max_epochs: int = 100,
    **kwargs: Any,
) -> dict[str, Any]:
    """Train an anomaly model. Returns training result dict."""
    from be_vision_ad_tools.training.flexible_trainer import FlexibleTrainingConfig, train_anomaly_model

    config = FlexibleTrainingConfig(
        data_root=Path(data_root),
        class_name=class_name,
        model_name=model_name,
        backbone=backbone,
        max_epochs=max_epochs,
        **kwargs,
    )
    return train_anomaly_model(config)


def train_from_yaml(yaml_path: str | Path) -> dict[str, Any]:
    """Train from a YAML config file."""
    from be_vision_ad_tools.training.flexible_trainer import train_anomaly_model
    return train_anomaly_model(yaml_path)


allow(train, train_from_yaml)
