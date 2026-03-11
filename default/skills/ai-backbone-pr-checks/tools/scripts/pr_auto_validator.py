#!/usr/bin/env python3
import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import List, Dict, Any

try:
    import yaml
except ImportError as exc:
    raise SystemExit("PyYAML is required. Install with: pip install pyyaml") from exc

FRONTMATTER_SUFFIXES = (".agent.md", ".prompt.md", ".instructions.md")
WORKFLOW_DIR_MARKERS = ("/.github/workflows/",)


# Run: execute shell commands and fail fast with captured error output.
def run(cmd: List[str]) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or proc.stdout.strip() or "command failed")
    return proc.stdout


# Collect: changed files from git refs for local execution mode.
def changed_files_from_refs(base_ref: str, head_ref: str) -> List[str]:
    out = run(["git", "diff", "--name-only", f"{base_ref}..{head_ref}"])
    return [line.strip() for line in out.splitlines() if line.strip()]


# Collect: changed files from a PR via GitHub CLI API in CI mode.
def changed_files_from_pr(repo: str, pr: str) -> List[str]:
    out = run(["gh", "api", f"repos/{repo}/pulls/{pr}/files", "--paginate"])
    data = json.loads(out)
    return [item["filename"] for item in data if "filename" in item]


# Parse: top-of-file YAML frontmatter into a dictionary.
def extract_frontmatter(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}
    fm_text = text[4:end]
    loaded = yaml.safe_load(fm_text) or {}
    return loaded if isinstance(loaded, dict) else {}


# Validate: lowercase-kebab naming policy for resource files.
def is_kebab_case(stem: str) -> bool:
    return bool(re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", stem))


# Extract: markdown links and keep only non-URL targets for local path checks.
def collect_markdown_links(path: Path) -> List[str]:
    text = path.read_text(encoding="utf-8", errors="replace")
    links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
    return [link for link in links if not re.match(r"^[a-zA-Z]+://", link)]


# Validate: repository PR rules on one changed file.
def validate_file(path_str: str, blocking: List[str], warnings: List[str]) -> None:
    path = Path(path_str)
    if not path.exists() or path.is_dir():
        return

    name = path.name

    # Validate: frontmatter and naming for agent/prompt/instruction resources.
    if name.endswith(FRONTMATTER_SUFFIXES):
        fm = extract_frontmatter(path)
        if not fm:
            blocking.append(f"{path_str}: missing or malformed YAML frontmatter")
        else:
            if "name" not in fm:
                blocking.append(f"{path_str}: frontmatter missing 'name'")
            if "description" not in fm:
                blocking.append(f"{path_str}: frontmatter missing 'description'")
            if isinstance(fm.get("description"), str):
                desc = fm["description"].strip()
                if not (desc.startswith("'") and desc.endswith("'")):
                    warnings.append(f"{path_str}: description should be wrapped in single quotes")

        stem = name.replace(".agent.md", "").replace(".prompt.md", "").replace(".instructions.md", "")
        if not is_kebab_case(stem):
            blocking.append(f"{path_str}: filename must use lowercase kebab-case")

    # Validate: SKILL manifest frontmatter requirements.
    if name == "SKILL.md":
        fm = extract_frontmatter(path)
        if not fm:
            blocking.append(f"{path_str}: missing or malformed YAML frontmatter")
        else:
            if "name" not in fm or "description" not in fm:
                blocking.append(f"{path_str}: frontmatter must include 'name' and 'description'")

    # Detect: lightweight workflow hardening gaps.
    normalized_path = f"/{path_str.replace(chr(92), '/')}/"
    if path.suffix in (".yml", ".yaml") and any(marker in normalized_path for marker in WORKFLOW_DIR_MARKERS):
        text = path.read_text(encoding="utf-8", errors="replace")
        if "permissions:" not in text:
            warnings.append(f"{path_str}: missing explicit workflow permissions")
        if "@main" in text:
            warnings.append(f"{path_str}: action reference uses @main")

    # Validate: local markdown links resolve inside the repository.
    if path.suffix == ".md":
        for link in collect_markdown_links(path):
            target = link.split("#", 1)[0]
            if not target or target.startswith("mailto:"):
                continue
            if target.startswith("/"):
                continue
            normalized = target.replace("%20", " ")
            candidate = (path.parent / normalized).resolve()
            repo_root = Path.cwd().resolve()
            try:
                candidate.relative_to(repo_root)
            except ValueError:
                continue
            if not candidate.exists():
                warnings.append(f"{path_str}: broken relative link target '{target}'")


# Run: entry point to choose changed-file source, execute checks, and emit JSON.
def main() -> None:
    parser = argparse.ArgumentParser(description="Validate changed files for PR policy checks")
    parser.add_argument("--repo", help="owner/repo for PR API mode")
    parser.add_argument("--pr", help="PR number for PR API mode")
    parser.add_argument("--base-ref", help="Base git ref for local diff mode")
    parser.add_argument("--head-ref", default="HEAD", help="Head git ref for local diff mode")
    parser.add_argument("--out", required=True, help="Path to JSON report")
    args = parser.parse_args()

    # Configure: CI mode uses PR metadata, local mode uses git diff refs.
    if args.repo and args.pr:
        changed = changed_files_from_pr(args.repo, args.pr)
        mode = "pr"
    else:
        base_ref = args.base_ref or "HEAD~1"
        changed = changed_files_from_refs(base_ref, args.head_ref)
        mode = "local"

    blocking: List[str] = []
    warnings: List[str] = []

    # Validate: only changed files to keep PR checks fast.
    for changed_file in changed:
        validate_file(changed_file, blocking, warnings)

    status = "fail" if blocking else ("warn" if warnings else "pass")
    report = {
        "status": status,
        "summary": [
            f"Mode: {mode}",
            f"Changed files inspected: {len(changed)}",
            f"Blocking issues: {len(blocking)}",
            f"Warnings: {len(warnings)}",
        ],
        "blocking_issues": blocking,
        "warnings": warnings,
        "metadata": {
            "mode": mode,
            "changed_files_count": len(changed),
        },
        "checked_files": changed,
    }

    # Report: machine-readable output for PR comments and artifacts.
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))

    if blocking:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
