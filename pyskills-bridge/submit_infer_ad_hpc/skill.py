"""Submit vad-infer to office HPC via LSF bsub.

Use when batch inference must run on the cluster instead of locally.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pyskills.core import allow

from be_vision_ad_tools.tutorials.hpc_submit_cli import compose_submit_cfg, submit_hydra_job

__all__ = ['submit_infer']


def submit_infer(
    model_path: str | Path,
    test_folders: str | Path,
    dry_run: bool = False,
    **kwargs: Any,
) -> dict[str, Any]:
    """Submit inference job to HPC. Returns bsub result dict."""
    overrides = [
        f'model_path={model_path}',
        f'test_folders={test_folders}',
        f'hpc.dry_run={str(dry_run).lower()}',
    ]
    for key, val in kwargs.items():
        overrides.append(f'{key}={val}')
    cfg = compose_submit_cfg('infer_submit', overrides)
    return submit_hydra_job(cfg)


allow(submit_infer)
