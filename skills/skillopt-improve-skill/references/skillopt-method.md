# SkillOpt Method Reference

Use this when the task calls for Microsoft SkillOpt itself or when a local optimization loop should mirror its structure.

Source checked from `https://github.com/microsoft/SkillOpt` main commit `b5328e8b220bffef60dd280a4ab77c075d456098` on 2026-06-08.

## Contents

- Core Loop
- When To Use Official SkillOpt
- Official Setup
- Official Training Shape
- Key Config Knobs
- Adding A New Benchmark
- Local Loop Equivalence

## Core Loop

SkillOpt treats a Markdown skill document as the trainable state of a frozen target agent. Each training step follows:

1. Rollout: run the target model or agent on tasks using the current skill. Save scored trajectories.
2. Reflect: have an optimizer model analyze failures and successes, producing structured edit patches.
3. Aggregate: merge semantically similar edits and remove duplicates.
4. Select: rank edits and clip to the current textual learning-rate budget.
5. Update: apply selected add, insert, replace, or delete edits to create a candidate skill.
6. Gate: evaluate the candidate on a validation split and accept only if it improves.

At epoch boundaries, SkillOpt adds:

- Slow update: compare previous and current skills on shared samples to identify improved, regressed, persistent-failure, and stable-success patterns.
- Meta skill: keep compact cross-epoch optimizer memory so later reflections reuse learned strategy.

## When To Use Official SkillOpt

Use the official package when all are true:

- A repeatable dataset or benchmark exists.
- There is a scoring function that returns task-level `hard` and/or `soft` scores.
- A built-in SkillOpt environment fits, or there is time to implement an `EnvAdapter`.
- Running multiple model calls is acceptable.

Prefer the local Codex loop when the user gives an ordinary Codex skill plus an improvement goal but no dataset, benchmark adapter, or automated scorer.

## Official Setup

Install from PyPI:

```bash
pip install skillopt
```

Or install from source:

```bash
git clone https://github.com/microsoft/SkillOpt.git
cd SkillOpt
pip install -e .
```

Configure credentials for the chosen backend. The repository supports OpenAI-compatible, Azure OpenAI, Claude, Qwen/vLLM, and MiniMax style backends. Verify exact env vars and CLI flags with the checked-out README and `python scripts/train.py --help`.

## Official Training Shape

Typical source checkout command:

```bash
python scripts/train.py \
  --config configs/searchqa/default.yaml \
  --split_dir /path/to/split \
  --optimizer_model gpt-5.5 \
  --target_model gpt-5.5 \
  --num_epochs 4 \
  --batch_size 40 \
  --out_root outputs/my_run
```

Use `env.skill_init` or the relevant CLI override to seed training with the user's existing skill document.

Evaluate a resulting skill with the repo's eval script:

```bash
python scripts/eval_only.py \
  --config configs/searchqa/default.yaml \
  --skill outputs/my_run/best_skill.md \
  --split valid_unseen
```

Confirm split names against the installed version because docs and examples can differ by release.

## Key Config Knobs

- `train.num_epochs`: number of optimization epochs.
- `train.batch_size`: rollout tasks per step.
- `gradient.minibatch_size`: reflection batch size.
- `gradient.failure_only`: whether to reflect only on failures.
- `optimizer.learning_rate`: maximum selected edits per step.
- `optimizer.lr_scheduler`: `constant`, `linear`, `cosine`, or autonomous schedules when supported.
- `optimizer.use_slow_update`: enable epoch-boundary longitudinal guidance.
- `optimizer.use_meta_skill`: enable cross-epoch strategy memory.
- `evaluation.use_gate`: accept candidates only through validation gating.
- `env.skill_init`: initial skill Markdown path.

## Adding A New Benchmark

To optimize a custom task with official SkillOpt, implement:

1. A `SplitDataLoader` that loads train, validation, and test items.
2. A rollout helper that runs the target model with the skill content and scores each item.
3. An `EnvAdapter` that wires loading, rollout, reflection, and task types into SkillOpt.
4. A YAML config referencing the environment and training knobs.
5. Registration in the training script or environment registry used by the installed version.

Rollout results should include at least `id`, `hard`, and `soft`; include prompts, predictions, task type, and failure reason when useful for reflection.

## Local Loop Equivalence

When running without official SkillOpt, preserve these invariants:

- Separate target execution from optimizer reflection.
- Make edits evidence-backed and bounded by a learning-rate budget.
- Apply structured patches rather than free-form rewrites when possible.
- Gate every candidate against validation cases.
- Keep rejected-edit memory.
- Track slow-update and meta-skill notes across epochs.
