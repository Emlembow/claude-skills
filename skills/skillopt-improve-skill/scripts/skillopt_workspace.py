#!/usr/bin/env python3
"""Small utilities for SkillOpt-style Codex skill optimization."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import sys
from pathlib import Path
from typing import Any


SLOW_UPDATE_START = "<!-- SLOW_UPDATE_START -->"
SLOW_UPDATE_END = "<!-- SLOW_UPDATE_END -->"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _json_dumps(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2) + "\n"


def _load_json_or_jsonl(path: Path) -> list[dict[str, Any]]:
    text = _read_text(path).strip()
    if not text:
        return []
    if text[0] == "[":
        data = json.loads(text)
        if not isinstance(data, list):
            raise ValueError(f"{path} must contain a JSON list or JSONL records")
        return [dict(item) for item in data]
    records: list[dict[str, Any]] = []
    for line_no, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        item = json.loads(line)
        if not isinstance(item, dict):
            raise ValueError(f"{path}:{line_no} is not a JSON object")
        records.append(item)
    return records


def _write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    lines = [json.dumps(record, ensure_ascii=False, sort_keys=True) for record in records]
    _write_text(path, "\n".join(lines) + ("\n" if lines else ""))


def _parse_case(raw: str, index: int) -> dict[str, Any]:
    parts = raw.split("|", 2)
    if len(parts) == 3:
        case_id, prompt, criteria = parts
    elif len(parts) == 2:
        case_id, prompt = parts
        criteria = ""
    else:
        case_id = f"case-{index:03d}"
        prompt = raw
        criteria = ""
    return {
        "id": case_id.strip() or f"case-{index:03d}",
        "prompt": prompt.strip(),
        "criteria": criteria.strip(),
        "split": "valid",
        "tags": [],
        "source": "cli",
    }


def cmd_init(args: argparse.Namespace) -> int:
    skill = Path(args.skill).expanduser().resolve()
    if not skill.exists():
        raise FileNotFoundError(f"Skill file not found: {skill}")
    if skill.is_dir():
        skill = skill / "SKILL.md"
    if skill.name != "SKILL.md":
        print(f"[WARN] Expected SKILL.md, using {skill}", file=sys.stderr)

    goal = args.goal or ""
    if args.goal_file:
        goal = _read_text(Path(args.goal_file).expanduser().resolve()).strip()
    if not goal.strip():
        raise ValueError("Provide --goal or --goal-file")

    timestamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    default_out = Path.cwd() / f"skillopt-run-{skill.parent.name}-{timestamp}"
    out_dir = Path(args.out_dir).expanduser().resolve() if args.out_dir else default_out.resolve()

    for dirname in (
        "candidates",
        "patches",
        "rejected",
        "reports",
        "results",
        "rollouts",
        "notes",
        "prompts",
    ):
        (out_dir / dirname).mkdir(parents=True, exist_ok=True)

    seed_skill = out_dir / "seed_skill.md"
    current_skill = out_dir / "candidates" / "current_skill.md"
    shutil.copyfile(skill, seed_skill)
    shutil.copyfile(skill, current_skill)

    cases: list[dict[str, Any]] = []
    if args.cases_jsonl:
        cases.extend(_load_json_or_jsonl(Path(args.cases_jsonl).expanduser().resolve()))
    for idx, raw_case in enumerate(args.case or [], len(cases) + 1):
        cases.append(_parse_case(raw_case, idx))

    _write_text(out_dir / "goal.md", goal.strip() + "\n")
    _write_jsonl(out_dir / "eval_cases.jsonl", cases)
    _write_text(
        out_dir / "prompts" / "reflection_prompt.md",
        "Analyze rollout results against the goal. Produce a SkillOpt-style JSON patch "
        "with general, evidence-backed edits. Do not hardcode eval answers.\n",
    )
    manifest = {
        "created_at_utc": timestamp,
        "source_skill": str(skill),
        "seed_skill": str(seed_skill),
        "current_skill": str(current_skill),
        "goal_file": str(out_dir / "goal.md"),
        "eval_cases": str(out_dir / "eval_cases.jsonl"),
        "case_count": len(cases),
        "method": "SkillOpt-style local Codex loop",
        "skillopt_source": "https://github.com/microsoft/SkillOpt",
    }
    state = {
        "epoch": 0,
        "step": 0,
        "best_score": None,
        "accepted_patches": [],
        "rejected_patches": [],
        "slow_update_notes": [],
        "meta_skill_notes": [],
    }
    _write_text(out_dir / "manifest.json", _json_dumps(manifest))
    _write_text(out_dir / "optimizer_state.json", _json_dumps(state))
    print(_json_dumps(manifest), end="")
    return 0


def _is_protected_target(skill: str, target: str) -> bool:
    if not target:
        return False
    start = skill.find(SLOW_UPDATE_START)
    end = skill.find(SLOW_UPDATE_END)
    target_pos = skill.find(target)
    if start == -1 or end == -1 or target_pos == -1:
        return False
    return start <= target_pos < end + len(SLOW_UPDATE_END)


def _strip_markers(text: str) -> str:
    return text.replace(SLOW_UPDATE_START, "").replace(SLOW_UPDATE_END, "")


def _append_before_slow_update(skill: str, content: str) -> str:
    start = skill.find(SLOW_UPDATE_START)
    if start == -1:
        return skill.rstrip() + "\n\n" + content.rstrip() + "\n"
    before = skill[:start].rstrip()
    after = skill[start:]
    return before + "\n\n" + content.rstrip() + "\n\n" + after


def _apply_edit(skill: str, edit: dict[str, Any], index: int) -> tuple[str, dict[str, Any]]:
    op = str(edit.get("op", "")).strip()
    target = str(edit.get("target", ""))
    content = _strip_markers(str(edit.get("content", ""))).strip()
    report = {
        "index": index,
        "op": op,
        "target_preview": target[:160],
        "content_preview": content[:160],
        "status": "unknown",
    }

    if target and _is_protected_target(skill, target):
        report["status"] = "skipped_protected_slow_update_region"
        return skill, report

    if op == "append":
        report["status"] = "applied_append"
        return _append_before_slow_update(skill, content), report

    if op == "insert_after":
        if not target or target not in skill:
            report["status"] = "applied_insert_after_fallback_append"
            return _append_before_slow_update(skill, content), report
        insert_at = skill.index(target) + len(target)
        newline = skill.find("\n", insert_at)
        insert_at = newline + 1 if newline != -1 else len(skill)
        report["status"] = "applied_insert_after"
        return skill[:insert_at] + "\n" + content.rstrip() + "\n" + skill[insert_at:], report

    if op == "replace":
        if not target:
            report["status"] = "skipped_replace_missing_target"
            return skill, report
        if target not in skill:
            report["status"] = "skipped_replace_target_not_found"
            return skill, report
        report["status"] = "applied_replace"
        return skill.replace(target, content, 1), report

    if op == "delete":
        if not target:
            report["status"] = "skipped_delete_missing_target"
            return skill, report
        if target not in skill:
            report["status"] = "skipped_delete_target_not_found"
            return skill, report
        report["status"] = "applied_delete"
        return skill.replace(target, "", 1), report

    report["status"] = "skipped_unknown_op"
    return skill, report


def _load_patch(path: Path) -> dict[str, Any]:
    data = json.loads(_read_text(path))
    if isinstance(data, list):
        return {"reasoning": "", "edits": data}
    if not isinstance(data, dict):
        raise ValueError("Patch must be a JSON object or list of edits")
    if "patch" in data and "edits" not in data and isinstance(data["patch"], dict):
        data = data["patch"]
    data.setdefault("edits", [])
    if not isinstance(data["edits"], list):
        raise ValueError("Patch 'edits' must be a list")
    return data


def cmd_apply_patch(args: argparse.Namespace) -> int:
    skill_path = Path(args.skill).expanduser().resolve()
    patch_path = Path(args.patch).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    patch = _load_patch(patch_path)
    skill = _read_text(skill_path)
    reports = []
    for index, edit in enumerate(patch.get("edits", []), 1):
        if not isinstance(edit, dict):
            reports.append({"index": index, "status": "skipped_non_object_edit"})
            continue
        skill, report = _apply_edit(skill, edit, index)
        reports.append(report)
    _write_text(out_path, skill)
    result = {
        "patch": str(patch_path),
        "input_skill": str(skill_path),
        "output_skill": str(out_path),
        "reasoning": patch.get("reasoning", ""),
        "reports": reports,
    }
    if args.report:
        _write_text(Path(args.report).expanduser().resolve(), _json_dumps(result))
    print(_json_dumps(result), end="")
    return 0


def _score_from_record(record: dict[str, Any]) -> float:
    for key in ("score", "soft", "hard", "passed"):
        if key in record:
            value = record[key]
            if isinstance(value, bool):
                return 1.0 if value else 0.0
            try:
                return float(value)
            except (TypeError, ValueError):
                continue
    raise ValueError(f"Record has no numeric score field: {record}")


def _summarize_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    scores = [_score_from_record(record) for record in records]
    avg = sum(scores) / len(scores) if scores else 0.0
    return {
        "count": len(scores),
        "average": avg,
        "passed_count": sum(1 for score in scores if score >= 1.0),
        "min": min(scores) if scores else None,
        "max": max(scores) if scores else None,
    }


def cmd_summarize_results(args: argparse.Namespace) -> int:
    records = _load_json_or_jsonl(Path(args.results).expanduser().resolve())
    summary = _summarize_records(records)
    if args.report:
        _write_text(Path(args.report).expanduser().resolve(), _json_dumps(summary))
    print(_json_dumps(summary), end="")
    return 0


def _records_by_id(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_id: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records, 1):
        record_id = str(record.get("id") or f"row-{index:04d}")
        by_id[record_id] = record
    return by_id


def cmd_compare(args: argparse.Namespace) -> int:
    baseline = _load_json_or_jsonl(Path(args.baseline).expanduser().resolve())
    candidate = _load_json_or_jsonl(Path(args.candidate).expanduser().resolve())
    baseline_summary = _summarize_records(baseline)
    candidate_summary = _summarize_records(candidate)
    baseline_by_id = _records_by_id(baseline)
    candidate_by_id = _records_by_id(candidate)
    common_ids = sorted(set(baseline_by_id) & set(candidate_by_id))
    regressions = []
    improvements = []
    for record_id in common_ids:
        base_score = _score_from_record(baseline_by_id[record_id])
        cand_score = _score_from_record(candidate_by_id[record_id])
        delta = cand_score - base_score
        if delta < -args.regression_tolerance:
            regressions.append({"id": record_id, "baseline": base_score, "candidate": cand_score, "delta": delta})
        elif delta > args.regression_tolerance:
            improvements.append({"id": record_id, "baseline": base_score, "candidate": cand_score, "delta": delta})
    delta_avg = candidate_summary["average"] - baseline_summary["average"]
    accepted = delta_avg > args.min_delta and len(regressions) <= args.max_regressions
    result = {
        "accepted": accepted,
        "delta_average": delta_avg,
        "baseline": baseline_summary,
        "candidate": candidate_summary,
        "common_count": len(common_ids),
        "improvement_count": len(improvements),
        "regression_count": len(regressions),
        "regressions": regressions,
        "criteria": {
            "min_delta": args.min_delta,
            "max_regressions": args.max_regressions,
            "regression_tolerance": args.regression_tolerance,
        },
    }
    if args.report:
        _write_text(Path(args.report).expanduser().resolve(), _json_dumps(result))
    print(_json_dumps(result), end="")
    return 0 if accepted else 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init = subparsers.add_parser("init", help="Create a SkillOpt-style optimization workspace")
    init.add_argument("--skill", required=True, help="Path to a SKILL.md file or skill folder")
    init.add_argument("--goal", help="Improvement goal text")
    init.add_argument("--goal-file", help="Path to a file containing the improvement goal")
    init.add_argument("--out-dir", help="Workspace directory to create")
    init.add_argument("--cases-jsonl", help="Existing eval cases as JSON or JSONL")
    init.add_argument("--case", action="append", help="Inline case: id|prompt|criteria")
    init.set_defaults(func=cmd_init)

    apply = subparsers.add_parser("apply-patch", help="Apply a SkillOpt-style JSON patch")
    apply.add_argument("--skill", required=True, help="Input skill markdown")
    apply.add_argument("--patch", required=True, help="Patch JSON file")
    apply.add_argument("--out", required=True, help="Output candidate skill markdown")
    apply.add_argument("--report", help="Optional JSON report path")
    apply.set_defaults(func=cmd_apply_patch)

    summarize = subparsers.add_parser("summarize-results", help="Summarize rollout result JSONL")
    summarize.add_argument("--results", required=True, help="Result JSON or JSONL file")
    summarize.add_argument("--report", help="Optional JSON report path")
    summarize.set_defaults(func=cmd_summarize_results)

    compare = subparsers.add_parser("compare", help="Compare baseline and candidate rollout results")
    compare.add_argument("--baseline", required=True, help="Baseline result JSON or JSONL")
    compare.add_argument("--candidate", required=True, help="Candidate result JSON or JSONL")
    compare.add_argument("--min-delta", type=float, default=0.0, help="Required average improvement")
    compare.add_argument("--max-regressions", type=int, default=0, help="Allowed case-level regressions")
    compare.add_argument("--regression-tolerance", type=float, default=0.0, help="Ignore tiny per-case deltas")
    compare.add_argument("--report", help="Optional JSON report path")
    compare.set_defaults(func=cmd_compare)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:  # noqa: BLE001
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
