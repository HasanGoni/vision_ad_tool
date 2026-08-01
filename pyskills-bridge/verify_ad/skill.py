"""Run dependency sync, import smoke tests, and nbdev CI for be_vision_ad_tools before trusting or committing changes.

Use after editing `be_vision_ad_tools/` or `nbs/`, before telling the user a change works.

## Verification steps

1. `sync_deps()` — `uv sync` or `pip install -e .`
2. `smoke_imports()` — import flexible_trainer, unified_inference, anomaly_score_organizer
3. `run_nbdev_test()` — same as GitHub Actions nbdev-ci

## Completed example

```
Verified AD toolbox:
- sync: OK
- imports: flexible_trainer, unified_inference, anomaly_score_organizer
- nbdev_test: passed
```
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from pyskills.core import allow

__all__ = ['REPO_ROOT', 'sync_deps', 'smoke_imports', 'run_nbdev_test', 'verify_all']

REPO_ROOT = Path(__file__).resolve().parents[2]


def _run(cmd: list[str], *, cwd: Path | None = None) -> str:
    result = subprocess.run(cmd, cwd=cwd or REPO_ROOT, capture_output=True, text=True, check=False)
    out = (result.stdout or '') + (result.stderr or '')
    if result.returncode != 0:
        raise RuntimeError(f"Command failed ({result.returncode}): {' '.join(cmd)}\n{out}")
    return out


def sync_deps() -> str:
    """Sync project dependencies. Returns command output."""
    if _which('uv'):
        return _run(['uv', 'sync'])
    return _run([sys.executable, '-m', 'pip', 'install', '-e', '.'])


def smoke_imports() -> str:
    """Import core modules without running GPU training."""
    from be_vision_ad_tools.training.flexible_trainer import train_anomaly_model, FlexibleTrainingConfig
    from be_vision_ad_tools.inference.unified_inference import unified_inference
    from be_vision_ad_tools.inference.anomaly_score_organizer import predict_and_organize_by_score
    _ = train_anomaly_model, FlexibleTrainingConfig, unified_inference, predict_and_organize_by_score
    return 'OK: core imports succeeded'


def run_nbdev_test() -> str:
    """Run nbdev_test (CI equivalent)."""
    cmd = ['uv', 'run', 'nbdev_test'] if _which('uv') else ['nbdev_test']
    return _run(cmd)


def verify_all() -> dict[str, str]:
    """Run full verification pipeline. Returns step outputs."""
    return {
        'sync': sync_deps(),
        'imports': smoke_imports(),
        'nbdev': run_nbdev_test(),
    }


def _which(name: str) -> str | None:
    from shutil import which
    return which(name)


allow(sync_deps, smoke_imports, run_nbdev_test, verify_all)
