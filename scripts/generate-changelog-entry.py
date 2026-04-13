#!/usr/bin/env python3
"""
Generate or update CHANGELOG.md entries from git diff analysis.

Uses *actual file diffs* (not just commit messages) to produce accurate,
specific changelog entries.  Analyses:
  - New / deleted files (→ Added / Removed)
  - File-path heuristics (agents, skills, workflows, MCP, docs, CI, scripts)
  - Content-pattern detection (new MCP servers, new agents, new skills, etc.)
  - Commit messages as supplementary context only

Two modes:
  release   (default) — version in apm.yml differs from latest tag →
                         insert a new ## [X.Y.Z] section below [Unreleased]
  unreleased          — version unchanged → merge new commits into
                         the ## [Unreleased] section

Usage:
  python scripts/generate-changelog-entry.py                          # auto-detect, preview
  python scripts/generate-changelog-entry.py --apply                  # write to CHANGELOG.md
  python scripts/generate-changelog-entry.py --apply --push           # CI: commit + push
  python scripts/generate-changelog-entry.py --mode unreleased        # force unreleased mode
  python scripts/generate-changelog-entry.py --mode release           # force release mode
  python scripts/generate-changelog-entry.py --base-ref origin/main   # explicit diff base

The --push flag is designed for CI auto-fix jobs that commit back to MR branches.
"""
import argparse
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
APM_YML = ROOT / "apm.yml"
CHANGELOG = ROOT / "CHANGELOG.md"

SECTION_ORDER = ("Added", "Changed", "Fixed", "Removed")
UNRELEASED_MARKER = "## [Unreleased]"

# Files to exclude from diff analysis (meta-files that always change)
EXCLUDED_FILES = {"CHANGELOG.md", "apm.yml"}
# Files whose diff content should not be scanned for modification patterns
# (e.g. this script's own source contains pattern strings that cause false positives)
CONTENT_SCAN_EXCLUDED = {"scripts/generate-changelog-entry.py"}


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------

def read_version() -> str:
    text = APM_YML.read_text(encoding="utf-8")
    m = re.search(r"^version:\s*(.+)", text, re.M)
    if not m:
        sys.exit("Could not read version from apm.yml")
    return m.group(1).strip().strip("'\"")


def find_latest_tag() -> str:
    """Return the most recent semver tag, or empty string."""
    result = _run_git("git", "tag", "--sort=-v:refname")
    for tag in result.splitlines():
        tag = tag.strip()
        if tag:
            return tag
    return ""


def version_has_tag(version: str) -> bool:
    result = _run_git("git", "tag", "-l", f"v{version}")
    return bool(result.strip())


def _run_git(*args: str) -> str:
    """Run a git command and return stdout, handling encoding."""
    result = subprocess.run(
        list(args), capture_output=True, cwd=ROOT,
        encoding="utf-8", errors="replace",
    )
    return result.stdout or ""


def get_diff_stat(base: str, until: str = "HEAD") -> list[dict]:
    """Get per-file diff stats: status (A/M/D/R), file path, insertions, deletions."""
    cmd = ["git", "diff", "--numstat", "--diff-filter=ADMR", "-M"]
    if base:
        cmd.append(f"{base}..{until}")
    else:
        cmd.append(until)
    result = _run_git(*cmd)
    files = []
    for line in result.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) >= 3:
            ins = int(parts[0]) if parts[0] != "-" else 0
            dels = int(parts[1]) if parts[1] != "-" else 0
            path = parts[2]
            if path in EXCLUDED_FILES:
                continue
            files.append({"path": path, "insertions": ins, "deletions": dels})
    return files


def get_diff_name_status(base: str, until: str = "HEAD") -> dict[str, str]:
    """Get file status: A=added, M=modified, D=deleted, R=renamed."""
    cmd = ["git", "diff", "--name-status", "--diff-filter=ADMR", "-M"]
    if base:
        cmd.append(f"{base}..{until}")
    else:
        cmd.append(until)
    result = _run_git(*cmd)
    status_map = {}
    for line in result.splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split("\t")
        if len(parts) >= 2:
            status = parts[0][0]  # first char: A/M/D/R
            path = parts[-1]  # last element (for renames, it's the new name)
            if path not in EXCLUDED_FILES:
                status_map[path] = status
    return status_map


def get_diff_content(base: str, until: str = "HEAD") -> str:
    """Get the full unified diff for content-pattern analysis."""
    cmd = ["git", "diff", "-U3"]
    if base:
        cmd.append(f"{base}..{until}")
    else:
        cmd.append(until)
    # Exclude noisy files
    for f in EXCLUDED_FILES:
        cmd.append(f":(exclude){f}")
    return _run_git(*cmd)


def get_commits_between(since: str, until: str = "HEAD") -> list[str]:
    """Get commit subjects between two refs (used as supplementary context)."""
    cmd = ["git", "log", "--oneline", "--format=%s"]
    if since:
        cmd.append(f"{since}..{until}")
    else:
        cmd.append(until)
    result = _run_git(*cmd)
    return [line.strip() for line in result.splitlines() if line.strip()]


# ---------------------------------------------------------------------------
# Path classification
# ---------------------------------------------------------------------------

# Map file path patterns to human-readable area names
AREA_PATTERNS: list[tuple[str, str]] = [
    (r"^\.apm/agents/(.+)\.md$", "agent:{0}"),
    (r"^\.apm/skills/([^/]+)/", "skill:{0}"),
    (r"^\.apm/workflows/(.+)\.yml$", "workflow:{0}"),
    (r"^\.apm/contexts/mcp-registry\.yaml$", "mcp-registry"),
    (r"^\.apm/contexts/(.+)$", "context:{0}"),
    (r"^\.apm/hooks/engine/(.+)$", "hook-engine:{0}"),
    (r"^\.apm/prompts/(.+)$", "prompt:{0}"),
    (r"^\.apm/instructions/(.+)$", "instruction:{0}"),
    (r"^\.apm/templates/(.+)$", "template:{0}"),
    (r"^\.apm/knowledge/(.+)$", "knowledge:{0}"),
    (r"^providers/github-copilot/agents/(.+)$", "copilot-agent:{0}"),
    (r"^providers/github-copilot/prompts/(.+)$", "copilot-prompt:{0}"),
    (r"^providers/github-copilot/instructions/(.+)$", "copilot-instruction:{0}"),
    (r"^providers/claude-code/commands/(.+)$", "claude-command:{0}"),
    (r"^providers/cli/(.+)$", "cli:{0}"),
    (r"^\.github/instructions/(.+)$", "github-instruction:{0}"),
    (r"^\.github/(.+)$", "github:{0}"),
    (r"^ci-gates/(.+)$", "ci-gate:{0}"),
    (r"^scripts/(.+)$", "script:{0}"),
    (r"^docs/(.+)$", "docs:{0}"),
]


def classify_path(path: str) -> str:
    """Classify a file path into an area tag."""
    for pattern, tag_fmt in AREA_PATTERNS:
        m = re.match(pattern, path)
        if m:
            return tag_fmt.format(*m.groups()) if m.groups() else tag_fmt
    return f"other:{PurePosixPath(path).name}"


def area_group(path: str) -> str:
    """Return a coarse area group for summary grouping."""
    p = path.lower()
    if p.startswith(".apm/agents/"):
        return "agents"
    if p.startswith(".apm/skills/"):
        return "skills"
    if p.startswith(".apm/workflows/"):
        return "workflows"
    if p.startswith(".apm/contexts/mcp-registry"):
        return "mcp"
    if p.startswith(".apm/hooks/"):
        return "hooks"
    if p.startswith(".apm/prompts/"):
        return "prompts"
    if p.startswith(".apm/instructions/"):
        return "instructions"
    if p.startswith(".apm/knowledge/"):
        return "knowledge"
    if p.startswith("providers/github-copilot/"):
        return "copilot-provider"
    if p.startswith("providers/claude-code/"):
        return "claude-provider"
    if p.startswith("providers/cli/"):
        return "cli-provider"
    if p.startswith("ci-gates/"):
        return "ci-gates"
    if p.startswith("scripts/"):
        return "scripts"
    if p.startswith("docs/"):
        return "docs"
    if p.startswith(".github/instructions/"):
        return "copilot-instructions"
    if p.startswith(".github/"):
        return "copilot-runtime"
    return "other"


# ---------------------------------------------------------------------------
# Diff-based changelog generation
# ---------------------------------------------------------------------------

def detect_new_mcp_servers(diff_content: str) -> list[str]:
    """Find new MCP server IDs added to mcp-registry.yaml."""
    servers = []
    in_registry = False
    for line in diff_content.splitlines():
        if "mcp-registry.yaml" in line and line.startswith("diff --git"):
            in_registry = True
            continue
        if in_registry and line.startswith("diff --git"):
            in_registry = False
            continue
        if in_registry and line.startswith("+"):
            m = re.match(r"^\+\s+-\s+id:\s+(\S+)", line)
            if m:
                servers.append(m.group(1))
    return servers


def detect_new_agents(name_status: dict[str, str]) -> list[str]:
    """Find new agent files."""
    agents = []
    for path, status in name_status.items():
        if status == "A":
            m = re.match(r"^\.apm/agents/(.+)\.md$", path)
            if m:
                agents.append(m.group(1))
    return agents


def detect_new_skills(name_status: dict[str, str]) -> list[str]:
    """Find new skill directories (by detecting new SKILL.md files)."""
    skills = []
    for path, status in name_status.items():
        if status == "A":
            m = re.match(r"^\.apm/skills/([^/]+)/SKILL\.md$", path)
            if m:
                skills.append(m.group(1))
    return skills


def detect_new_docs(name_status: dict[str, str]) -> list[str]:
    """Find new documentation files."""
    docs = []
    for path, status in name_status.items():
        if status == "A" and path.startswith("docs/"):
            docs.append(path)
    return docs


def detect_deleted_files(name_status: dict[str, str]) -> list[str]:
    """Find deleted files."""
    return [p for p, s in name_status.items() if s == "D"]


def detect_new_scripts(name_status: dict[str, str]) -> list[str]:
    """Find new script files."""
    scripts = []
    for path, status in name_status.items():
        if status == "A" and path.startswith("scripts/"):
            scripts.append(path)
    return scripts


def detect_new_ci_gates(name_status: dict[str, str]) -> list[str]:
    """Find new CI gate files."""
    gates = []
    for path, status in name_status.items():
        if status == "A" and path.startswith("ci-gates/"):
            gates.append(path)
    return gates


def detect_new_provider_agents(name_status: dict[str, str]) -> list[str]:
    """Find new provider agent files."""
    agents = []
    for path, status in name_status.items():
        if status == "A":
            m = re.match(r"^providers/github-copilot/agents/(.+)\.agent\.md$", path)
            if m:
                agents.append(m.group(1))
    return agents


def detect_new_claude_commands(name_status: dict[str, str]) -> list[str]:
    """Find new Claude Code commands."""
    cmds = []
    for path, status in name_status.items():
        if status == "A":
            m = re.match(r"^providers/claude-code/commands/(.+)\.md$", path)
            if m:
                cmds.append(m.group(1))
    return cmds


def detect_new_instructions(name_status: dict[str, str]) -> list[str]:
    """Find new instruction files (canonical or provider)."""
    instr = []
    for path, status in name_status.items():
        if status == "A":
            if re.match(r"^\.apm/instructions/.+\.md$", path):
                instr.append(PurePosixPath(path).stem)
            elif re.match(r"^providers/github-copilot/instructions/.+\.md$", path):
                instr.append(PurePosixPath(path).stem)
    return list(set(instr))


def detect_significant_modifications(
    file_stats: list[dict],
    name_status: dict[str, str],
    exclude_files: set[str] | None = None,
) -> dict[str, list[str]]:
    """Detect significantly modified areas for the Changed section."""
    excluded = exclude_files or set()
    mods_by_area: dict[str, list[str]] = defaultdict(list)
    for f in file_stats:
        path = f["path"]
        if name_status.get(path) != "M":
            continue
        if path in excluded:
            continue
        # Only note files with meaningful changes (>1 line delta)
        delta = f["insertions"] + f["deletions"]
        if delta < 2:
            continue
        group = area_group(path)
        mods_by_area[group].append(path)
    return dict(mods_by_area)


# Content-aware modification patterns: (regex matching added lines, description)
MODIFICATION_PATTERNS: list[tuple[str, str]] = [
    (r"state.tracker|outputs/runs/|workflow-state\.schema|python -m engine --state", "Workflow state tracking standardised"),
    (r"allowedFilePaths|allowedFilePathsReadOnly", "Agent file path permissions updated"),
    (r"commandAllowlist", "Agent command allowlist updated"),
    (r"allowedNetworkDomains", "Agent network domain restrictions updated"),
    (r"edit/editFiles", "File-writing tool declarations updated"),
    (r"sonarqube|SonarQube", "SonarQube integration updated"),
    (r"Out of Scope|out.of.scope", "Agent scope constraints updated"),
    (r"file-output|File Creation Mandate", "File output mandate enforcement updated"),
    (r"PII|REDACTED|anonymis", "Data anonymisation handling updated"),
    (r"prompt.injection|injection.detect", "Prompt injection detection updated"),
    (r"mcp-registry|mcp.server|mcp.profile", "MCP configuration updated"),
    (r"brownfield|reverse.brief", "Brownfield detection updated"),
]


def parse_diff_added_lines_per_file(diff_content: str) -> dict[str, list[str]]:
    """Extract added lines (starting with +) per file from unified diff."""
    result: dict[str, list[str]] = {}
    current_file = ""
    for line in diff_content.splitlines():
        m = re.match(r"^diff --git a/(.+?) b/(.+)$", line)
        if m:
            current_file = m.group(2)
            continue
        if current_file and line.startswith("+") and not line.startswith("+++"):
            result.setdefault(current_file, []).append(line[1:])
    return result


def detect_modification_categories(
    diff_content: str,
    name_status: dict[str, str],
) -> tuple[list[str], set[str]]:
    """Detect content-aware modification categories from diff added lines.

    Returns (changelog_entries, set_of_files_covered_by_patterns).
    """
    added_per_file = parse_diff_added_lines_per_file(diff_content)
    modified_files = {p for p, s in name_status.items()
                      if s == "M" and p not in EXCLUDED_FILES and p not in CONTENT_SCAN_EXCLUDED}

    # pattern_desc -> list of matching files
    pattern_hits: dict[str, list[str]] = defaultdict(list)
    covered_files: set[str] = set()

    for filepath in modified_files:
        added_lines = added_per_file.get(filepath, [])
        if not added_lines:
            continue
        joined = "\n".join(added_lines)
        # First-match-wins: attribute each file to the first matching pattern only
        for regex, desc in MODIFICATION_PATTERNS:
            if re.search(regex, joined, re.I):
                pattern_hits[desc].append(filepath)
                covered_files.add(filepath)
                break  # stop checking further patterns for this file

    entries: list[str] = []
    for desc, files in sorted(pattern_hits.items()):
        parts: list[str] = []
        groups: dict[str, list[str]] = defaultdict(list)
        for f in files:
            groups[area_group(f)].append(f)
        for group_name in sorted(groups):
            group_files = groups[group_name]
            if group_name == "copilot-provider":
                prompts = [f for f in group_files if "prompts/" in f]
                agents = [f for f in group_files if "agents/" in f]
                instrs = [f for f in group_files if "instructions/" in f]
                if prompts:
                    parts.append(f"{len(prompts)} Copilot prompt(s)")
                if agents:
                    parts.append(f"{len(agents)} Copilot agent(s)")
                if instrs:
                    parts.append(f"{len(instrs)} Copilot instruction(s)")
            elif group_name == "claude-provider":
                cmds = [f for f in group_files if "commands/" in f]
                if cmds:
                    parts.append(f"{len(cmds)} Claude Code command(s)")
                else:
                    parts.append(f"{len(group_files)} Claude Code file(s)")
            elif group_name == "agents":
                names = ", ".join(f"`{PurePosixPath(f).stem}`" for f in sorted(group_files))
                parts.append(f"agent(s) {names}")
            elif group_name == "skills":
                skill_names = list({PurePosixPath(f).parts[2]
                                   for f in group_files if len(PurePosixPath(f).parts) > 2})
                names = ", ".join(f"`{s}`" for s in sorted(skill_names))
                parts.append(f"skill(s) {names}")
            else:
                human = group_name.replace("-", " ")
                parts.append(f"{len(group_files)} {human} file(s)")

        if parts:
            entries.append(f"{desc}: {', '.join(parts)}")
        else:
            entries.append(desc)

    return entries, covered_files


def _agent_display_name(filename: str) -> str:
    """Convert kebab-case filename to title case display name."""
    return filename.replace("-", " ").replace(".", " ").title().strip()


def analyze_diff(base: str, until: str = "HEAD") -> dict[str, list[str]]:
    """Main analysis: produce changelog sections from git diff."""
    name_status = get_diff_name_status(base, until)
    file_stats = get_diff_stat(base, until)
    diff_content = get_diff_content(base, until)
    commits = get_commits_between(base, until)

    sections: dict[str, list[str]] = defaultdict(list)
    seen: set[str] = set()  # dedup tracker

    def add(section: str, msg: str) -> None:
        key = msg.lower()
        if key not in seen:
            seen.add(key)
            sections[section].append(msg)

    # --- ADDED ---
    new_agents = detect_new_agents(name_status)
    if new_agents:
        names = ", ".join(f"`{a}`" for a in sorted(new_agents))
        add("Added", f"New canonical agent(s): {names}")

    new_skills = detect_new_skills(name_status)
    if new_skills:
        names = ", ".join(f"`{s}`" for s in sorted(new_skills))
        add("Added", f"New skill(s): {names}")

    new_mcp = detect_new_mcp_servers(diff_content)
    if new_mcp:
        for srv in new_mcp:
            add("Added", f"MCP server `{srv}` added to registry and profiles")

    new_provider_agents = detect_new_provider_agents(name_status)
    if new_provider_agents:
        names = ", ".join(_agent_display_name(a) for a in sorted(new_provider_agents))
        add("Added", f"GitHub Copilot provider agent(s): {names}")

    new_claude = detect_new_claude_commands(name_status)
    if new_claude:
        names = ", ".join(f"`{c}`" for c in sorted(new_claude))
        add("Added", f"Claude Code command(s): {names}")

    new_instructions = detect_new_instructions(name_status)
    if new_instructions:
        names = ", ".join(f"`{i}`" for i in sorted(new_instructions))
        add("Added", f"New instruction(s): {names}")

    new_docs = detect_new_docs(name_status)
    if new_docs:
        for doc in sorted(new_docs):
            add("Added", f"`{doc}`")

    new_scripts = detect_new_scripts(name_status)
    if new_scripts:
        for s in sorted(new_scripts):
            add("Added", f"`{s}`")

    new_ci = detect_new_ci_gates(name_status)
    if new_ci:
        names = ", ".join(f"`{PurePosixPath(c).name}`" for c in sorted(new_ci))
        add("Added", f"CI gate file(s): {names}")

    # Catch remaining new files not yet covered
    covered_new = (
        {f".apm/agents/{a}.md" for a in new_agents}
        | {f"providers/github-copilot/agents/{a}.agent.md" for a in new_provider_agents}
        | set(new_docs)
        | set(new_scripts)
        | set(new_ci)
    )
    for path, status in name_status.items():
        if status == "A" and path not in covered_new:
            # New hook engine files
            if path.startswith(".apm/hooks/engine/"):
                add("Added", f"`{path}`")
            # New knowledge files
            elif path.startswith(".apm/knowledge/"):
                add("Added", f"`{path}`")

    # --- CHANGED ---
    # Phase 1: Content-aware pattern detection (covers small but meaningful changes)
    content_entries, content_covered = detect_modification_categories(diff_content, name_status)
    for entry in content_entries:
        add("Changed", entry)

    # Phase 2: Area-based fallback for files not covered by content patterns
    mods = detect_significant_modifications(file_stats, name_status, exclude_files=content_covered)

    if "agents" in mods:
        agent_names = [PurePosixPath(p).stem for p in mods["agents"]]
        names = ", ".join(f"`{a}`" for a in sorted(agent_names))
        add("Changed", f"Agent updates: {names}")

    if "skills" in mods:
        skill_names = list({PurePosixPath(p).parts[2] for p in mods["skills"]
                          if len(PurePosixPath(p).parts) > 2})
        names = ", ".join(f"`{s}`" for s in sorted(skill_names))
        add("Changed", f"Skill updates: {names}")

    if "hooks" in mods:
        hook_files = [PurePosixPath(p).name for p in mods["hooks"]]
        names = ", ".join(f"`{h}`" for h in sorted(hook_files))
        add("Changed", f"Hook engine updates: {names}")

    if "mcp" in mods and not new_mcp:
        add("Changed", "MCP registry configuration updated")

    if "copilot-provider" in mods:
        mod_agents = [PurePosixPath(p).stem for p in mods["copilot-provider"]
                     if "agents/" in p]
        mod_prompts = [PurePosixPath(p).stem for p in mods["copilot-provider"]
                      if "prompts/" in p]
        mod_instrs = [PurePosixPath(p).stem for p in mods["copilot-provider"]
                     if "instructions/" in p]
        if mod_agents:
            names = ", ".join(f"`{a}`" for a in sorted(mod_agents))
            add("Changed", f"Copilot provider agent updates: {names}")
        if mod_prompts:
            count = len(mod_prompts)
            add("Changed", f"{count} Copilot prompt(s) updated")
        if mod_instrs:
            names = ", ".join(f"`{i}`" for i in sorted(mod_instrs))
            add("Changed", f"Copilot instruction updates: {names}")

    if "copilot-instructions" in mods:
        instr_names = [PurePosixPath(p).stem for p in mods["copilot-instructions"]]
        names = ", ".join(f"`{i}`" for i in sorted(instr_names))
        add("Changed", f"Copilot instruction updates: {names}")

    if "claude-provider" in mods:
        mod_cmds = [PurePosixPath(p).stem for p in mods["claude-provider"]
                   if "commands/" in p]
        if mod_cmds:
            count = len(mod_cmds)
            add("Changed", f"{count} Claude Code command(s) updated")

    if "docs" in mods:
        doc_names = [PurePosixPath(p).name for p in mods["docs"]]
        names = ", ".join(f"`{d}`" for d in sorted(doc_names))
        add("Changed", f"Documentation updates: {names}")

    if "scripts" in mods:
        script_names = [PurePosixPath(p).name for p in mods["scripts"]]
        names = ", ".join(f"`{s}`" for s in sorted(script_names))
        add("Changed", f"Script updates: {names}")

    if "ci-gates" in mods:
        gate_names = [PurePosixPath(p).name for p in mods["ci-gates"]]
        names = ", ".join(f"`{g}`" for g in sorted(gate_names))
        add("Changed", f"CI gate updates: {names}")

    if "workflows" in mods:
        wf_names = [PurePosixPath(p).stem for p in mods["workflows"]]
        names = ", ".join(f"`{w}`" for w in sorted(wf_names))
        add("Changed", f"Workflow updates: {names}")

    # --- FIXED ---
    # Extract fix-related info from commit messages as supplementary data.
    # Skip noise: version bumps, changelog chores, messages that duplicate
    # diff-detected content.
    SKIP_FIX_PATTERNS = [
        r"^update version",
        r"^bump version",
        r"changelog",
        r"^merge",
        r"^auto-generate",
    ]
    # Collect lowercased content-entry keywords to detect overlap
    content_keywords = " ".join(e.lower() for e in content_entries)
    for subject in commits:
        if subject.startswith("Merge "):
            continue
        if subject.startswith("chore: auto-generate changelog"):
            continue
        m_fix = re.match(r"^fix(?:\([^)]*\))?:\s*(.+)", subject, re.I)
        if m_fix:
            msg = m_fix.group(1).strip()
            if not msg:
                continue
            msg_clean = msg[0].upper() + msg[1:]
            # Skip noise patterns
            if any(re.search(pat, msg, re.I) for pat in SKIP_FIX_PATTERNS):
                continue
            # Skip if the message largely overlaps with a content-detected entry
            msg_words = set(re.findall(r"\w{4,}", msg.lower()))
            if msg_words and len(msg_words & set(re.findall(r"\w{4,}", content_keywords))) > len(msg_words) * 0.5:
                continue
            add("Fixed", msg_clean)

    # --- REMOVED ---
    deleted = detect_deleted_files(name_status)
    if deleted:
        # Group deletions
        del_agents = [p for p in deleted if p.startswith(".apm/agents/")]
        del_skills = [p for p in deleted if p.startswith(".apm/skills/")]
        del_other = [p for p in deleted
                    if p not in del_agents and p not in del_skills]
        if del_agents:
            names = ", ".join(f"`{PurePosixPath(p).stem}`" for p in sorted(del_agents))
            add("Removed", f"Agent(s): {names}")
        if del_skills:
            skill_names = list({PurePosixPath(p).parts[2] for p in del_skills
                              if len(PurePosixPath(p).parts) > 2})
            names = ", ".join(f"`{s}`" for s in sorted(skill_names))
            add("Removed", f"Skill(s): {names}")
        if del_other:
            for p in sorted(del_other):
                add("Removed", f"`{p}`")

    return dict(sections)


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def format_sections(sections: dict[str, list[str]]) -> str:
    """Format classified sections as markdown (### Added, ### Changed, etc.)."""
    lines: list[str] = []
    for heading in SECTION_ORDER:
        if heading in sections:
            lines.append(f"### {heading}")
            for item in sections[heading]:
                lines.append(f"- {item}")
            lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Changelog reading / writing
# ---------------------------------------------------------------------------

def read_changelog() -> str:
    if not CHANGELOG.exists():
        sys.exit("CHANGELOG.md not found")
    return CHANGELOG.read_text(encoding="utf-8")


def has_versioned_entry(version: str) -> bool:
    if not CHANGELOG.exists():
        return False
    text = CHANGELOG.read_text(encoding="utf-8")
    return bool(re.search(r"^## \[" + re.escape(version) + r"\]", text, re.M))


def parse_unreleased_body(text: str) -> str:
    """Extract the body text under ## [Unreleased] (before the next ## [)."""
    m = re.search(
        r"## \[Unreleased\]\s*\n(.*?)(?=\n## \[|\Z)",
        text, re.S,
    )
    return m.group(1).strip() if m else ""


def parse_existing_unreleased_items(body: str) -> set[str]:
    """Extract lowercase bullet items already present under [Unreleased]."""
    items: set[str] = set()
    for line in body.splitlines():
        m = re.match(r"^-\s+(.+)", line)
        if m:
            items.add(m.group(1).strip().lower())
    return items


def collect_all_versioned_items(text: str) -> set[str]:
    """Collect all lowercase bullet items from existing versioned sections."""
    items: set[str] = set()
    in_versioned = False
    for line in text.splitlines():
        if re.match(r"^## \[\d+\.\d+\.\d+", line):
            in_versioned = True
            continue
        if re.match(r"^## \[", line):
            in_versioned = False
            continue
        if in_versioned:
            bm = re.match(r"^-\s+(.+)", line)
            if bm:
                items.add(bm.group(1).strip().lower())
    return items


def build_release_entry(version: str, diff_sections: dict[str, list[str]],
                        unreleased_body: str,
                        existing_versioned_items: set[str] | None = None) -> str:
    """Build a ## [X.Y.Z] entry from diff analysis + unreleased content."""
    already_released: set[str] = existing_versioned_items or set()

    # Parse existing unreleased sections
    existing_sections: dict[str, list[str]] = {}
    current_heading = ""
    for line in unreleased_body.splitlines():
        hm = re.match(r"^###\s+(\w+)", line)
        if hm:
            current_heading = hm.group(1)
            continue
        bm = re.match(r"^-\s+(.+)", line)
        if bm and current_heading:
            existing_sections.setdefault(current_heading, []).append(bm.group(1).strip())

    # Merge: diff analysis first, then unreleased items (deduplicated)
    merged: dict[str, list[str]] = {}
    seen: set[str] = set()
    for heading in SECTION_ORDER:
        # Diff-derived entries take priority
        for item in diff_sections.get(heading, []):
            key = item.lower()
            if key not in seen and key not in already_released:
                seen.add(key)
                merged.setdefault(heading, []).append(item)
        # Then any manually curated unreleased items
        for item in existing_sections.get(heading, []):
            key = item.lower()
            if key not in seen and key not in already_released:
                seen.add(key)
                merged.setdefault(heading, []).append(item)

    if not merged:
        merged["Changed"] = ["Version bump (fill in details)"]

    today = date.today().isoformat()
    lines = [f"## [{version}] — {today}", ""]
    lines.append(format_sections(merged))
    return "\n".join(lines)


def insert_release_entry(text: str, entry: str) -> str:
    """Replace [Unreleased] body with empty and insert versioned entry below."""
    marker_idx = text.find(UNRELEASED_MARKER)
    if marker_idx < 0:
        sys.exit("CHANGELOG.md has no ## [Unreleased] section")

    after_marker = marker_idx + len(UNRELEASED_MARKER)
    next_heading = re.search(r"\n## \[", text[after_marker:])
    if next_heading:
        body_end = after_marker + next_heading.start()
    else:
        body_end = len(text)

    new_text = (
        text[:after_marker] + "\n\n"
        + entry + "\n"
        + text[body_end:]
    )
    return new_text


def update_unreleased(text: str, diff_sections: dict[str, list[str]]) -> str:
    """Merge new diff-derived entries into the [Unreleased] section."""
    marker_idx = text.find(UNRELEASED_MARKER)
    if marker_idx < 0:
        sys.exit("CHANGELOG.md has no ## [Unreleased] section")

    after_marker = marker_idx + len(UNRELEASED_MARKER)
    next_heading = re.search(r"\n## \[", text[after_marker:])
    if next_heading:
        body_end = after_marker + next_heading.start()
    else:
        body_end = len(text)

    existing_body = text[after_marker:body_end].strip()
    existing_items = parse_existing_unreleased_items(existing_body)

    # Parse existing sections
    existing_sections: dict[str, list[str]] = {}
    current_heading = ""
    for line in existing_body.splitlines():
        hm = re.match(r"^###\s+(\w+)", line)
        if hm:
            current_heading = hm.group(1)
            continue
        bm = re.match(r"^-\s+(.+)", line)
        if bm and current_heading:
            existing_sections.setdefault(current_heading, []).append(bm.group(1).strip())

    added_count = 0
    for heading in SECTION_ORDER:
        for item in diff_sections.get(heading, []):
            if item.lower() not in existing_items:
                existing_sections.setdefault(heading, []).append(item)
                existing_items.add(item.lower())
                added_count += 1

    if added_count == 0:
        return text

    new_body = format_sections(existing_sections)
    new_text = text[:after_marker] + "\n\n" + new_body + "\n" + text[body_end:]
    return new_text


# ---------------------------------------------------------------------------
# Git push helper
# ---------------------------------------------------------------------------

def git_commit_and_push(commit_msg: str) -> None:
    """Stage CHANGELOG.md, commit, and push to the MR source branch."""
    subprocess.run(["git", "add", "CHANGELOG.md"], cwd=ROOT, check=True)
    subprocess.run(
        ["git", "commit", "-m", commit_msg],
        cwd=ROOT, check=True,
    )
    branch = os.environ.get("CI_COMMIT_REF_NAME", "")
    if branch:
        subprocess.run(
            ["git", "push", "origin", f"HEAD:{branch}"],
            cwd=ROOT, check=True,
        )
        print(f"Pushed changelog commit to {branch}")
    else:
        print("No CI_COMMIT_REF_NAME — skipping push (run manually)")


# ---------------------------------------------------------------------------
# Detect mode
# ---------------------------------------------------------------------------

def detect_mode(current_version: str) -> str:
    """Auto-detect: 'release' if version doesn't have a tag yet, else 'unreleased'."""
    if version_has_tag(current_version):
        return "unreleased"
    return "release"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate or update CHANGELOG.md from git diff analysis")
    parser.add_argument("--apply", action="store_true",
                        help="Write changes to CHANGELOG.md")
    parser.add_argument("--push", action="store_true",
                        help="CI mode: git add + commit + push after applying")
    parser.add_argument("--mode", choices=["release", "unreleased"],
                        help="Force mode (default: auto-detect from tags)")
    parser.add_argument("--base-ref", default="",
                        help="Explicit git ref to diff against (e.g. origin/main)")
    args = parser.parse_args()

    version = read_version()
    latest_tag = find_latest_tag()
    mode = args.mode or detect_mode(version)

    # Determine diff base
    base = args.base_ref or latest_tag
    print(f"Version: {version}  |  Latest tag: {latest_tag or '(none)'}  |  Mode: {mode}")
    print(f"Diff base: {base or '(none — full history)'}")

    # Analyze actual diff
    diff_sections = analyze_diff(base)
    total_items = sum(len(v) for v in diff_sections.values())
    print(f"Detected {total_items} changelog item(s) from diff analysis")

    text = read_changelog()

    if mode == "release":
        if has_versioned_entry(version):
            print(f"CHANGELOG.md already has {version} — nothing to do")
            return
        unreleased_body = parse_unreleased_body(text)
        already_released = collect_all_versioned_items(text)
        entry = build_release_entry(version, diff_sections,
                                    unreleased_body, already_released)

        if not args.apply:
            print("\n--- Draft release entry (use --apply to write) ---\n")
            print(entry)
            return

        new_text = insert_release_entry(text, entry)
        CHANGELOG.write_text(new_text, encoding="utf-8")
        print(f"Inserted release entry for {version}")

        if args.push:
            git_commit_and_push(
                f"chore: auto-generate changelog entry for {version}")

    else:  # unreleased
        new_text = update_unreleased(text, diff_sections)
        if new_text == text:
            print("No new items to add to [Unreleased]")
            return

        if not args.apply:
            new_body = parse_unreleased_body(new_text)
            print("\n--- Updated [Unreleased] section (use --apply to write) ---\n")
            print(new_body)
            return

        CHANGELOG.write_text(new_text, encoding="utf-8")
        print("Updated [Unreleased] section with new items")

        if args.push:
            git_commit_and_push("chore: update unreleased changelog entries")


if __name__ == "__main__":
    main()
