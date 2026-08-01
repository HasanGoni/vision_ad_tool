# Stealing ideas from pyskills for Cursor & GitHub Copilot

A practical guide for building agent skills without adopting the full pyskills stack.

**Source:** [AnswerDotAI/pyskills](https://github.com/AnswerDotAI/pyskills) (Apache-2.0)  
**Applies to:** Cursor Agent Skills, GitHub Copilot custom instructions / instruction files

---

## The one-sentence alignment

**pyskills teaches Python-kernel agents via importable modules; Cursor and Copilot teach via markdown + scripts — but both should use progressive disclosure, a curated public API, and demonstrations over rules.**

You do not need `pip install pyskills` to benefit. Steal the *architecture*, not the package.

---

## pyskills vs your harness

| Concept | pyskills | Cursor | GitHub Copilot |
|---------|----------|--------|----------------|
| Discovery blurb | First paragraph of module docstring → `list_pyskills()` | YAML `description:` in `SKILL.md` frontmatter | `.github/copilot-instructions.md` or skill/instruction file summary |
| Full instructions | Rest of docstring → `doc(module)` | `SKILL.md` body (loaded when matched) | Instruction file body or referenced docs |
| Public API | `__all__` | "Public API" table + `scripts/` | "Use only these commands" section |
| Executable surface | Python functions with `allow()` | Shell/Python scripts in `scripts/` | Same — scripts or documented CLI entry points |
| Security boundary | `allow(func)` whitelist for sandbox | "Do not invent other commands" | Same explicit boundary |
| Install location | `pyproject.toml` entry point or `~/.local/share/pyskills/` | `.cursor/skills/` or `~/.cursor/skills/` | `.github/` or repo-root instruction files |
| Show > tell | Completed example in docstring (THEORY.md) | "What done looks like" block in skill | Same demonstration block |

---

## The 6 ideas worth stealing

### 1. Progressive disclosure

Don't dump everything upfront. Split into two layers:

1. **Discovery** — one sentence: *when* should the agent load this skill?
2. **Depth** — full procedure, loaded only after the agent picks the skill

**pyskills:**
```python
"""Run tests before committing.   ← discovery (list_pyskills)

Full steps:                        ← depth (doc())
1. run_tests()
2. generate_batch()
...
"""
```

**Cursor / Copilot:**
```yaml
---
description: Run tests and sanity checks before committing changes to this library.
---
# Full procedure below...
```

### 2. Curate the public API (`__all__` equivalent)

Agents freestyle when the surface is open-ended. List exactly what they may use.

```markdown
## Public API (use only these)

| Step | Command |
|------|---------|
| Tests | `bash .cursor/skills/verify-pipeline/scripts/verify_tests.sh` |
| Batch | `bash .cursor/skills/verify-pipeline/scripts/verify_batch.sh <name>` |

Do not invent other commands.
```

This is the markdown equivalent of pyskills `__all__` and `allow()`.

### 3. Demonstrations over instructions

From pyskills THEORY.md: *models imitate what context shows, not what it tells.*

Always include a **completed example** of what "done" looks like:

```text
Verified pipeline:
- pytest: 15/15 passed
- batch: 10 images generated, 2 inspected visually
- annotations: 30 boxes, all in bounds
- cleaned scratch output
```

Not: "make sure everything works."

### 4. Scripts are transactions, markdown is the contract

- **Scripts** = do one thing, return output, exit (pyskills functions are transactions)
- **SKILL.md** = when to run, what order, what to report

Put bash/Python in `scripts/` — not only inline code blocks. Scripts are repeatable; inline blocks get mangled.

### 5. One vocabulary across tools

pyskills THEORY.md enforces consistent parameter names (`modality`, `out_dir`, `context=`, `nums=`). Do the same in your skills:

- Pick one term per concept and use it everywhere
- Same flag names in scripts, Python API, and skill prose
- Same output directory names (`output_verify`, not `tmp`, `test`, `out2`)

### 6. Summaries locate, views read, diffs confirm

When verifying work, the agent should:

1. **Locate** — run a summary command (counts, file list)
2. **Read** — actually inspect outputs (Read tool, open images)
3. **Confirm** — report concrete numbers, not vibes

Encode this in the skill: "Read at least one image — don't just check the file exists."

---

## Where to put skills

### Cursor

```
your-repo/
└── .cursor/skills/
    └── my-skill/
        ├── SKILL.md
        └── scripts/
            ├── step_one.sh
            └── step_two.sh
```

Personal (all projects): `~/.cursor/skills/my-skill/`

Cursor matches skills from the `description:` field when the user's task fits.

### GitHub Copilot

Copilot uses instruction files rather than the Cursor skill format. Closest equivalents:

| Cursor | GitHub Copilot |
|--------|----------------|
| `.cursor/skills/foo/SKILL.md` | `.github/copilot-instructions.md` (repo-wide) |
| Skill `description:` | First paragraph of instruction file |
| `scripts/` folder | Documented commands in instructions + repo scripts |
| Per-workflow skill | `.github/instructions/*.instructions.md` (Copilot custom instructions, preview) |

**Repo-wide Copilot instructions** (`.github/copilot-instructions.md`):

```markdown
# Project instructions

## When editing library code
Before claiming a fix works, run:
1. `bash .cursor/skills/verify-pipeline/scripts/verify_tests.sh`
2. `bash .cursor/skills/verify-pipeline/scripts/verify_batch.sh <modality>`

Report results like:
- pytest: N/N passed
- batch: N images, M inspected

## Public API
Do not invent verification commands. Use only scripts in `.cursor/skills/*/scripts/`.
```

**Per-task instructions** (if your Copilot setup supports `.github/instructions/`):

```
.github/instructions/
├── verify-before-commit.instructions.md
├── train-model.instructions.md
└── run-inference.instructions.md
```

Same content as Cursor `SKILL.md` bodies — adjust frontmatter to Copilot's format if required by your org.

---

## SKILL.md template (Cursor)

Copy this skeleton for each workflow:

```markdown
---
name: my-workflow
description: One sentence — when should the agent load this? Be specific about triggers.
---

# My Workflow Title

One paragraph: what this does and why it matters.

## Public API (use only these)

| Step | Command |
|------|---------|
| ... | `bash .cursor/skills/my-workflow/scripts/....sh` |

Do not invent other commands.

## What "done" looks like

\`\`\`text
Concrete report example with real numbers and file paths.
\`\`\`

## Step 1 — ...

\`\`\`bash
bash .cursor/skills/my-workflow/scripts/step_one.sh
\`\`\`

Why this step matters. What to check in the output.

## Step 2 — ...

Actually inspect outputs — don't just check exit codes.

## What NOT to do

- Don't ...
- Don't ...

## Only after all of this

Tell the user what you verified in concrete terms.
```

---

## Copilot instruction template

For `.github/copilot-instructions.md` or a focused instruction file:

```markdown
# [Workflow name]

## When to apply
Use these instructions when [specific trigger — e.g. editing files under `src/`, before committing, user asks to train a model].

## Commands (use only these)
- Verify: `bash scripts/verify.sh`
- Train: `bash scripts/train.sh <data_root>`

Do not invent other commands or bypass these scripts.

## Expected completion report
\`\`\`
Verified:
- tests: N/N passed
- output: [concrete details]
\`\`\`

## Steps
1. Run verify script
2. Inspect at least one output artifact
3. Report using the format above

## Do not
- Claim "it works" without running verify
- Hand-edit generated artifacts instead of fixing the source
```

---

## Mapping: pyskills module → Cursor skill

If you ever build both (e.g. Solveit + Cursor on the same repo):

| pyskills | Cursor skill |
|----------|--------------|
| Module docstring para 1 | `description:` |
| Module docstring body | `SKILL.md` body |
| `__all__ = ['foo', 'bar']` | Public API table |
| `def foo(): ...` | `scripts/foo.sh` or `scripts/foo.py` |
| `allow(foo, bar)` | "Do not invent other commands" |
| `doc(module)` | Agent reads `SKILL.md` on match |
| `register_pyskill()` | Copy skill dir to `.cursor/skills/` |

Keep procedure in one place. Mirror names across both; don't maintain two divergent workflows.

---

## Real examples from our work

### computer_use — `verify-synthetic-pipeline`

- **Discovery:** "Run tests and sanity checks before committing changes to synthetic image generator"
- **Public API:** 3 scripts (`verify_tests.sh`, `verify_batch.sh`, `verify_stub.sh`)
- **Demonstration:** concrete pytest count + images inspected + annotations valid
- **pyskills twin:** `pyskills-bridge/verify_synthetic/skill.py` (optional, for Python-kernel agents)

### vision_ad_tool — eight skills

| Skill | Trigger | Hydra CLI | Key script |
|-------|---------|-----------|------------|
| `verify-ad-pipeline` | After editing `be_vision_ad_tools/` | — | `verify_imports.sh`, `verify_nbdev.sh` |
| `train-anomaly-model` | User wants new AD checkpoint | `vad-train` | `train_model.sh` |
| `run-ad-inference` | Batch-score images | `vad-infer` | `run_inference.sh` |
| `organize-anomaly-scores` | Triage by anomaly score (image list) | `vad-organize` | `organize_scores.sh` |
| `infer-organize-ad` | Infer + score buckets + posters | `vad-infer-organize` | `infer_organize.sh` |
| `train-infer-ad` | Train + validation posters | `vad-train-infer` | `train_infer.sh` |
| `full-ad-pipeline` | End-to-end train + test triage | `vad-full` | `full_pipeline.sh` |
| `hyperparameter-search-ad` | Compare models / grid search | `vad-hyperparam-search` | `hyperparam_search.sh` |

---

## Checklist: is your skill "pyskills-aligned"?

- [ ] `description:` is one sentence, says *when* to load
- [ ] Public API table lists every allowed command
- [ ] "Do not invent other commands" (or equivalent boundary)
- [ ] "What done looks like" has a filled-in example report
- [ ] Scripts live in `scripts/`, not only inline bash blocks
- [ ] Verification requires *reading* outputs, not just exit codes
- [ ] Vocabulary is consistent across skill, scripts, and code
- [ ] "What NOT to do" section prevents common agent mistakes

---

## What NOT to steal

| Skip | Why |
|------|-----|
| `pip install pyskills` in Cursor-only workflow | Cursor doesn't call `list_pyskills()` or `doc()` |
| Entry points in `pyproject.toml` | Copilot/Cursor don't discover via setuptools |
| `allow()` / `safepyrun` sandbox | Unless you run a Python-kernel agent (Solveit, clikernel) |
| nbdev coupling | Independent of skill design |

Steal the **patterns**. Skip the **infrastructure** unless your harness needs it.

---

## Quick reference card

```
DISCOVER  →  short description (when to load)
CURATE    →  public API table (__all__ equivalent)
DEMONSTRATE → show what "done" looks like
EXECUTE   →  scripts/, not vibes
VERIFY    →  locate → read → report concretely
BOUND     →  "do not invent other commands"
```

---

## Further reading

- [pyskills README](https://github.com/AnswerDotAI/pyskills)
- [pyskills THEORY.md](https://github.com/AnswerDotAI/pyskills/blob/main/THEORY.md) — grammar, demonstrations, interpreter doctrine
- [Agent Skills specification](https://agentskills.io) — filesystem convention pyskills parallels
- Cursor: `.cursor/skills/<name>/SKILL.md`
- Copilot: [GitHub Copilot custom instructions](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot)
