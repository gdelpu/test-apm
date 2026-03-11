#!/usr/bin/env python3
import argparse
import json
import subprocess
from pathlib import Path
from typing import List, Dict, Any


# Run: shell commands and return stdout; raise on command failure.
def run(cmd: List[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "command failed")
    return proc.stdout


# Collect: changed files from git refs for local checks.
def changed_files_from_refs(base_ref: str, head_ref: str) -> List[str]:
    out = run(["git", "diff", "--name-only", f"{base_ref}..{head_ref}"])
    return [line.strip() for line in out.splitlines() if line.strip()]


# Collect: changed files from a PR via GitHub API through gh CLI.
def changed_files_from_pr(repo: str, pr: str) -> List[str]:
    out = run(["gh", "api", f"repos/{repo}/pulls/{pr}/files", "--paginate"])
    data = json.loads(out)
    return [item["filename"] for item in data if "filename" in item]


# Run: entry point to detect advisory process gaps from changed-file patterns.
def main() -> None:
    parser = argparse.ArgumentParser(description="Detect advisory test/documentation gaps")
    parser.add_argument("--repo", help="owner/repo for PR API mode")
    parser.add_argument("--pr", help="PR number for PR API mode")
    parser.add_argument("--base-ref", help="Base git ref for local diff mode")
    parser.add_argument("--head-ref", default="HEAD", help="Head git ref for local diff mode")
    parser.add_argument("--out", required=True, help="Path to JSON report")
    args = parser.parse_args()

    # Configure: CI mode reads PR changes; local mode reads git diff refs.
    if args.repo and args.pr:
        changed = changed_files_from_pr(args.repo, args.pr)
        mode = "pr"
    else:
        base_ref = args.base_ref or "HEAD~1"
        changed = changed_files_from_refs(base_ref, args.head_ref)
        mode = "local"

    warnings: List[str] = []

    # Detect: changed files by concern so heuristics stay explicit.
    changed_md = [f for f in changed if f.endswith(".md")]
    changed_workflows = [f for f in changed if "/.github/workflows/" in f and (f.endswith(".yml") or f.endswith(".yaml"))]
    changed_agents = [f for f in changed if f.endswith(".agent.md")]
    changed_prompts = [f for f in changed if f.endswith(".prompt.md")]
    changed_scripts = [
        f for f in changed
        if "/tools/scripts/" in f or f.startswith("scripts/agents/")
    ]

    # Detect: advisory-only heuristics for companion updates.
    if changed_scripts and not changed_md:
        warnings.append("Scripts changed without accompanying markdown docs/examples updates")

    if changed_workflows and not any(path.endswith("README.md") for path in changed_md):
        warnings.append("Workflow files changed without README/process documentation update")

    if changed_agents and not any("/skills/" in path for path in changed):
        warnings.append("Agent changed without skill/docs/tool updates")

    if changed_prompts and not any(path.endswith(".instructions.md") for path in changed):
        warnings.append("Prompt changed without instruction alignment update")

    status = "warn" if warnings else "pass"
    report: Dict[str, Any] = {
        "status": status,
        "summary": [
            f"Mode: {mode}",
            f"Changed files inspected: {len(changed)}",
            f"Warnings: {len(warnings)}",
        ],
        "blocking_issues": [],
        "warnings": warnings,
        "metadata": {
            "mode": mode,
            "changed_files_count": len(changed),
            "changed_workflows": len(changed_workflows),
            "changed_agents": len(changed_agents),
            "changed_prompts": len(changed_prompts),
            "changed_scripts": len(changed_scripts),
        },
        "checked_files": changed,
    }

    # Report: output for artifacts and PR comment aggregation.
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
