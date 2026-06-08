# SkillOpt Improve Skill

Improves existing Claude/Codex skills with a SkillOpt-style optimization loop: define evals, run rollouts, reflect on failures, apply bounded edits, and gate candidate changes against validation results.

## Use Cases

- Improve a skill toward a measurable goal.
- Build evaluation cases for a skill before revising it.
- Run a lightweight local SkillOpt-style loop when a full benchmark adapter is not available.
- Prepare official Microsoft SkillOpt experiments when a dataset, split, and scorer exist.

## Files

- `SKILL.md` - Main Claude Agent Skill entrypoint.
- `references/eval-design.md` - Guidance for designing skill improvement evals.
- `references/skillopt-method.md` - Microsoft SkillOpt methodology and configuration notes.
- `scripts/skillopt_workspace.py` - Workspace, patch, result-summary, and validation-gate helper.

## Dependencies

The bundled helper uses only Python standard-library modules. Official SkillOpt runs are optional and require installing/configuring Microsoft SkillOpt separately.

## Example

```text
Use the SkillOpt Improve Skill to improve my PDF processing skill so it handles scanned forms more reliably.
```

The skill should create an optimization workspace, design or load eval cases, compare baseline and candidate results, and only apply changes that pass validation.
