"""Submit vad-organize to office HPC via LSF bsub.

Use when score triage from an image list must run on the cluster.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pyskills.core import allow

from be_vision_ad_tools.tutorials.hpc_submit_cli import compose_submit_cfg, submit_hydra_job

__all__ = ['submit_organize']


def submit_organize(
    model_path: str | Path,
    image_list_file: str | Path,
    output_dir: str | Path = './score_review',
    dry_run: bool = False,
    **kwargs: Any,
) -> dict[str, Any]:
    """Submit organize job to HPC. Returns bsub result dict."""
    overrides = [
        f'model_path={model_path}',
        f'image_list_file={image_list_file}',
        f'output_dir={output_dir}',
        f'hpc.dry_run={str(dry_run).lower()}',
    ]
    for key, val in kwargs.items():
        overrides.append(f'{key}={val}')
    cfg = compose_submit_cfg('organize_submit', overrides)
    return submit_hydra_job(cfg)


allow(submit_organize)
