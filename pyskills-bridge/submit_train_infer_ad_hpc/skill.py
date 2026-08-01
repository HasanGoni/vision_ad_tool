"""Submit vad-train-infer to office HPC via LSF bsub.

Use when train + validation posters must run on the cluster.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pyskills.core import allow

from be_vision_ad_tools.tutorials.hpc_submit_cli import compose_submit_cfg, submit_hydra_job

__all__ = ['submit_train_infer']


def submit_train_infer(
    data_root: str | Path,
    validation_images: str | Path,
    model_name: str = 'patchcore',
    dry_run: bool = False,
    **kwargs: Any,
) -> dict[str, Any]:
    """Submit train-infer job to HPC. Returns bsub result dict."""
    overrides = [
        f'train.data_root={data_root}',
        f'train.model_name={model_name}',
        f'infer_after_training.validation_images={validation_images}',
        f'hpc.dry_run={str(dry_run).lower()}',
    ]
    for key, val in kwargs.items():
        overrides.append(f'{key}={val}')
    cfg = compose_submit_cfg('train_infer_submit', overrides)
    return submit_hydra_job(cfg)


allow(submit_train_infer)
