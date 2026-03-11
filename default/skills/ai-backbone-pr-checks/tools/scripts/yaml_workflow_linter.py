#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required. Install with: pip install pyyaml") from exc

WORKFLOW_GLOBS = [
    ".github/workflows/*.yml",
    ".github/workflows/*.yaml",
    "default/.github/workflows/*.yml",
    "default/.github/workflows/*.yaml",
    "clients/*/.github/workflows/*.yml",
    "clients/*/.github/workflows/*.yaml",
]


# Collect: workflow files across root, shared default, and client scopes.
def find_workflows(root: Path) -> List[Path]:
    found = []
    for pattern in WORKFLOW_GLOBS:
        found.extend(root.glob(pattern))
    return sorted(set(path.resolve() for path in found if path.is_file()))


# Validate: one workflow for required structure and safety conventions.
def lint_workflow(path: Path, repo_root: Path) -> Tuple[List[str], List[str]]:
    blocking: List[str] = []
    warnings: List[str] = []
    rel = path.relative_to(repo_root).as_posix()

    # Parse: YAML first so malformed workflows fail deterministically.
    text = path.read_text(encoding="utf-8", errors="replace")
    try:
        data = yaml.safe_load(text) or {}
    except Exception as exc:
        return [f"{rel}: YAML parse error: {exc}"], []

    if not isinstance(data, dict):
        return [f"{rel}: root document must be an object"], []

    # Detect: YAML 1.1 parsers may coerce key 'on' into boolean True.
    has_on_key = ("on" in data) or (True in data)

    # Validate: mandatory top-level workflow fields.
    if "name" not in data:
        blocking.append(f"{rel}: missing top-level 'name'")
    if not has_on_key:
        blocking.append(f"{rel}: missing top-level 'on'")

    # Validate: jobs and steps shape to catch broken workflow definitions.
    jobs = data.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        blocking.append(f"{rel}: missing or invalid 'jobs'")
    else:
        for job_name, job in jobs.items():
            if not isinstance(job, dict):
                blocking.append(f"{rel}: job '{job_name}' must be an object")
                continue

            if "runs-on" not in job:
                blocking.append(f"{rel}: job '{job_name}' missing 'runs-on'")

            steps = job.get("steps")
            if not isinstance(steps, list) or not steps:
                warnings.append(f"{rel}: job '{job_name}' has no steps")
                continue

            for idx, step in enumerate(steps, start=1):
                if not isinstance(step, dict):
                    blocking.append(f"{rel}: job '{job_name}' step {idx} must be an object")
                    continue
                if "run" not in step and "uses" not in step:
                    blocking.append(f"{rel}: job '{job_name}' step {idx} missing 'run' or 'uses'")
                if "uses" in step and "@main" in str(step["uses"]):
                    warnings.append(f"{rel}: job '{job_name}' step {idx} uses @main")

    # Detect: least-privilege and unsafe trigger/permission combinations.
    if "permissions:" not in text:
        warnings.append(f"{rel}: missing explicit permissions block")

    if "pull_request_target" in text and "contents: write" in text:
        warnings.append(f"{rel}: pull_request_target with contents: write requires review")

    return blocking, warnings


# Run: entry point to aggregate findings, write JSON, and fail on blocking findings.
def main() -> None:
    parser = argparse.ArgumentParser(description="Lint GitHub workflow YAML files")
    parser.add_argument("--root", required=True, help="Repository root")
    parser.add_argument("--out", required=True, help="Path to JSON report")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    workflows = find_workflows(root)

    blocking: List[str] = []
    warnings: List[str] = []
    checked = [wf.relative_to(root).as_posix() for wf in workflows]

    # Validate: workflows file-by-file so reporting lists exact paths.
    for workflow in workflows:
        b, w = lint_workflow(workflow, root)
        blocking.extend(b)
        warnings.extend(w)

    status = "fail" if blocking else ("warn" if warnings else "pass")
    report: Dict[str, Any] = {
        "status": status,
        "summary": [
            f"Workflow files scanned: {len(workflows)}",
            f"Blocking issues: {len(blocking)}",
            f"Warnings: {len(warnings)}",
        ],
        "blocking_issues": blocking,
        "warnings": warnings,
        "metadata": {
            "workflow_count": len(workflows),
            "root": root.as_posix(),
        },
        "checked_files": checked,
    }

    # Report: output for workflow artifacts and PR summary comments.
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))

    if blocking:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
