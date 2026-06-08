# Evaluation Design For Skill Improvement

Use this when a user gives a skill and an improvement goal but no ready-made benchmark.

## Turn Goals Into Scores

Map the goal to one primary score before editing:

- Reliability goal: pass rate across representative tasks.
- Tool-use goal: correct tool choice, valid arguments, and successful execution.
- Output-quality goal: rubric score from 0 to 1 with concrete criteria.
- Triggering goal: whether the skill activates for intended prompts and stays inactive for unrelated prompts.
- Safety or guardrail goal: count violations as hard failures.
- Efficiency goal: fewer unnecessary steps, smaller context load, or shorter successful traces.

Prefer simple deterministic scoring when possible. Use model or human judgment only when criteria are subjective, and record the rubric.

## Build Eval Cases

Create cases as JSONL records with this shape:

```json
{"id":"case-001","prompt":"User request to test","criteria":"What must be true for a pass","split":"valid","tags":["triggering"]}
```

Include:

- Happy paths the skill should handle.
- Edge cases related to the improvement goal.
- Negative-trigger cases if the goal includes better activation.
- Regression cases that protect existing important behavior.

Use separate splits when there are enough cases:

- `train`: cases used for reflection and patch proposals.
- `valid`: cases used for gate decisions.
- `test`: final held-out check.

With fewer than 8 cases, use leave-one-out style thinking: do not bake exact validation answers into the skill.

## Rollout Result Shape

Write rollout results as JSONL:

```json
{"id":"case-001","score":1.0,"passed":true,"failure_reason":"","notes":"brief evidence"}
```

Accepted score fields are `score`, `soft`, `hard`, or `passed`. Keep the same `id` values across baseline and candidate runs so gate comparisons can detect regressions.

## Reflection Rules

Reflect on patterns across cases:

- Look for repeated ambiguity, missing preconditions, wrong tool selection, invalid file handling, brittle validation, or bloated context.
- Preserve success patterns that explain why passing cases passed.
- Avoid adding exact answers, benchmark-specific constants, or generated case IDs to the skill.
- Prefer edits that teach a decision rule, workflow step, resource lookup, or validation habit.

## Gate Decision

Accept a candidate only when:

- Candidate average score is strictly higher than baseline or current best.
- Regression count is within the threshold set for the task, normally zero.
- The skill still validates structurally.
- The diff is scoped to evidence from the rollout.

Reject and record why when improvements are noisy, the patch duplicates existing guidance, the candidate overfits generated cases, or the validation score is flat.
