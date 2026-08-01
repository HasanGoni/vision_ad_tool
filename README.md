# vision_ad_tool

Anomaly detection toolbox for semiconductor X-ray/AOI imagery. Wraps [Anomalib](https://github.com/openvinotoolkit/anomalib) with training, unified inference (serial / parallel / HPC), and score-based image triage.

Package: `be_vision_ad_tools` · nbdev + uv

---

## Agent skills (Cursor & GitHub Copilot)

This repo ships **agent skills** built using ideas from [AnswerDotAI/pyskills](https://github.com/AnswerDotAI/pyskills) (Apache-2.0). You do **not** need `pip install pyskills` for Cursor or Copilot — steal the **architecture**, not the package.

### What we stole from pyskills

| pyskills idea | How it appears here |
|---------------|---------------------|
| First docstring paragraph → discovery | `description:` in each `SKILL.md` |
| `__all__` → curated API | **Public API** table in each skill |
| `doc(module)` → load on demand | Agent reads `SKILL.md` when task matches |
| `allow()` → security boundary | "Do not invent other commands" |
| Demonstrations over rules (THEORY.md) | **What "done" looks like** example in each skill |
| Functions as transactions | Executable `scripts/*.sh` per skill |

**Full guide:** [docs/agent-skills-from-pyskills.md](docs/agent-skills-from-pyskills.md)

### Arrange for Cursor

Open this repo in Cursor. Skills live at:

```
.cursor/skills/
├── verify-ad-pipeline/      # run before commit
├── train-anomaly-model/     # vad-train — train Padim/Patchcore/etc.
├── run-ad-inference/        # vad-infer — batch score images
├── organize-anomaly-scores/ # vad-organize — triage by score (image list)
├── infer-organize-ad/       # vad-infer-organize — infer + score buckets + posters
├── train-infer-ad/          # vad-train-infer — train + validation posters
├── full-ad-pipeline/        # vad-full — train + infer-organize end-to-end
└── hyperparameter-search-ad/ # vad-hyperparam-search — grid search + poster
├── submit-train-ad-hpc/       # vad-train-submit — queue training via bsub
├── submit-infer-ad-hpc/       # vad-infer-submit
├── submit-organize-ad-hpc/    # vad-organize-submit
├── submit-infer-organize-ad-hpc/
├── submit-train-infer-ad-hpc/
├── submit-full-ad-hpc/
└── submit-hyperparam-search-ad-hpc/
```

| Skill | Hydra CLI | Primary trigger |
|-------|-----------|-----------------|
| `verify-ad-pipeline` | — | After editing `be_vision_ad_tools/` or `nbs/` |
| `train-anomaly-model` | `vad-train` | Train/fit/build an AD checkpoint |
| `run-ad-inference` | `vad-infer` | Batch-score images or folders |
| `organize-anomaly-scores` | `vad-organize` | Triage from an image list file |
| `infer-organize-ad` | `vad-infer-organize` | Score folder + bucket + posters |
| `train-infer-ad` | `vad-train-infer` | Train + validation posters in one step |
| `full-ad-pipeline` | `vad-full` | End-to-end train + test triage |
| `hyperparameter-search-ad` | `vad-hyperparam-search` | Grid search + comparison poster |
| `submit-train-ad-hpc` | `vad-train-submit` | Queue training on office HPC (bsub) |
| `submit-infer-ad-hpc` | `vad-infer-submit` | Queue inference on HPC |
| `submit-organize-ad-hpc` | `vad-organize-submit` | Queue score triage on HPC |
| `submit-infer-organize-ad-hpc` | `vad-infer-organize-submit` | Queue infer-organize on HPC |
| `submit-train-infer-ad-hpc` | `vad-train-infer-submit` | Queue train-infer on HPC |
| `submit-full-ad-hpc` | `vad-full-submit` | Queue full pipeline on HPC |
| `submit-hyperparam-search-ad-hpc` | `vad-hyperparam-search-submit` | Queue hyperparam search on HPC |

Each folder has `SKILL.md` + `scripts/`. Cursor matches skills from the YAML `description:` when your task fits.

**Example:** after editing the trainer, ask: *"verify the AD pipeline before we commit."*

### Arrange for GitHub Copilot

Copilot reads repo-wide instructions from:

```
.github/copilot-instructions.md
```

That file points to the same scripts and verification workflow. Per-workflow detail stays in `.cursor/skills/*/SKILL.md` (shared content — one source of truth).

Optional: copy skill bodies into `.github/instructions/*.instructions.md` if your org uses Copilot custom instruction files.

### Optional: pyskills bridge (Solveit / Python-kernel agents)

For Python-kernel harnesses (Solveit, clikernel), importable twins live in `pyskills-bridge/`:

```bash
cd pyskills-bridge && uv sync
```

See [pyskills-bridge/REFERENCE.md](pyskills-bridge/REFERENCE.md).

### Quick reference

```
DISCOVER    → short description (when to load)
CURATE      → public API table
DEMONSTRATE → show what "done" looks like
EXECUTE     → scripts/, not ad-hoc bash
VERIFY      → locate → read → report concretely
BOUND       → do not invent other commands
```

---

## End-to-end Hydra CLIs

Hydra CLIs are **nbdev-exported** from `nbs/18_tutorials.end2end_hydra_cli.ipynb` and `nbs/19_training.hyperparameter_hydra_cli.ipynb` into `be_vision_ad_tools/tutorials/` and `be_vision_ad_tools/training/`. Configs are packaged at `be_vision_ad_tools/tutorials/conf/*.yaml`.

| Command | Workflow |
|---------|----------|
| `vad-train` | `train_anomaly_model` |
| `vad-infer` | `unified_inference` |
| `vad-organize` | `predict_and_organize_by_score` |
| `vad-infer-organize` | `unified_inference_with_threshold_posters` |
| `vad-train-infer` | train + `run_inference_after_training` |
| `vad-full` | train + infer-organize pipeline |
| `vad-hyperparam-search` | `diff_parameter_and_save_poster` |

```bash
uv sync
vad-train data_root=/path/to/data model_name=patchcore
vad-infer model_path=/path/model.ckpt test_folders=/path/images
vad-full train.data_root=/path/data infer_organize.test_folders=/path/test
vad-hyperparam-search data_root=/path/data test_images=/path/test
```

Configs: `be_vision_ad_tools/tutorials/conf/*.yaml` — override any field on the CLI.

### HPC submit CLIs (office cluster via bsub)

Each local CLI has a companion `vad-*-submit` that submits the same workflow to LSF via `bsub`. Same Hydra overrides plus `hpc.*` (`queue`, `cores`, `memory_mb`, `walltime_minutes`, `job_name`, `log_dir`). Use `hpc.dry_run=true` to preview without a cluster.

| Submit command | Runs on cluster |
|----------------|-----------------|
| `vad-train-submit` | `vad-train` |
| `vad-infer-submit` | `vad-infer` |
| `vad-organize-submit` | `vad-organize` |
| `vad-infer-organize-submit` | `vad-infer-organize` |
| `vad-train-infer-submit` | `vad-train-infer` |
| `vad-full-submit` | `vad-full` |
| `vad-hyperparam-search-submit` | `vad-hyperparam-search` |

```bash
vad-train-submit data_root=/path/to/data model_name=patchcore hpc.queue=batch hpc.cores=8
vad-train-submit data_root=/path/to/data hpc.dry_run=true   # preview bsub command locally
```

HPC configs: `be_vision_ad_tools/tutorials/conf/hpc/submit_defaults.yaml`, `*_submit.yaml`. nbdev: `nbs/20_tutorials.hpc_submit_cli.ipynb`.

Legacy shim: `tutorials/end2end_tutorial/` re-exports from `be_vision_ad_tools.tutorials.end2end_cli`.

### nbdev3 + pyproject.toml

Project metadata, dependencies, console scripts, and nbdev settings live in **`pyproject.toml`** (`[tool.nbdev]`). `settings.ini` is kept for reference; pyproject is the source of truth. Requires **nbdev ≥ 3**.

```bash
uv sync
uv run nbdev-export    # notebooks → be_vision_ad_tools/
uv run nbdev-test      # CI tests
```

---

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

This file will become your README and also the index of your
documentation.

## Developer Guide

If you are new to using `nbdev` here are some useful pointers to get you
started.

### Install vision_ad_tool in Development mode

``` sh
# make sure vision_ad_tool package is installed in development mode
$ pip install -e .

# make changes under nbs/ directory
# ...

# compile to have changes apply to vision_ad_tool
$ uv run nbdev-prepare
```

## Usage

### Installation

Install latest from the GitHub
[repository](https://github.com/HasanGoni/vision_ad_tool):

``` sh
$ pip install git+https://github.com/HasanGoni/vision_ad_tool.git
```

or from [conda](https://anaconda.org/HasanGoni/vision_ad_tool)

``` sh
$ conda install -c HasanGoni vision_ad_tool
```

or from [pypi](https://pypi.org/project/vision_ad_tool/)

``` sh
$ pip install vision_ad_tool
```

### Documentation

Documentation can be found hosted on this GitHub
[repository](https://github.com/HasanGoni/vision_ad_tool)'s
[pages](https://HasanGoni.github.io/vision_ad_tool/). Additionally you
can find package manager specific guidelines on
[conda](https://anaconda.org/HasanGoni/vision_ad_tool) and
[pypi](https://pypi.org/project/vision_ad_tool/) respectively.

## How to use

Fill me in please! Don't forget code examples:

``` python
1+1
```

    2
