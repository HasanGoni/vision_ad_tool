"""Submit vad-train to office HPC via LSF bsub.

Use when training must run on the cluster instead of locally.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pyskills.core import allow

from be_vision_ad_tools.tutorials.hpc_submit_cli import compose_submit_cfg, submit_hydra_job

__all__ = ['submit_train']


def submit_train(
    data_root: str | Path,
    model_name: str = 'patchcore',
    class_name: str = 'anomaly_detection',
    dry_run: bool = False,
    **kwargs: Any,
) -> dict[str, Any]:
    """Submit training job to HPC. Returns bsub result dict."""
    overrides = [
        f'data_root={data_root}',
        f'model_name={model_name}',
        f'class_name={class_name}',
        f'hpc.dry_run={str(dry_run).lower()}',
    ]
    for key, val in kwargs.items():
        overrides.append(f'{key}={val}')
    cfg = compose_submit_cfg('train_submit', overrides)
    return submit_hydra_job(cfg)


allow(submit_train)
