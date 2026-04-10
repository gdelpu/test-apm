#!/usr/bin/env python3
"""
Generate or update CHANGELOG.md entries from git commit history.

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
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APM_YML = ROOT / "apm.yml"
CHANGELOG = ROOT / "CHANGELOG.md"

# Conventional-commit prefix → changelog section mapping
SECTION_MAP = {
    "feat": "Added",
    "add": "Added",
    "fix": "Fixed",
    "bugfix": "Fixed",
    "hotfix": "Fixed",
    "refactor": "Changed",
    "chore": "Changed",
    "perf": "Changed",
    "docs": "Changed",
    "style": "Changed",
    "ci": "Changed",
    "build": "Changed",
    "revert": "Removed",
    "remove": "Removed",
}
DEFAULT_SECTION = "Changed"
SECTION_ORDER = ("Added", "Changed", "Fixed", "Removed")

UNRELEASED_MARKER = "## [Unreleased]"


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
    result = subprocess.run(
        ["git", "tag", "--sort=-v:refname"],
        capture_output=True, text=True, cwd=ROOT,
    )
    for tag in result.stdout.splitlines():
        tag = tag.strip()
        if tag:
            return tag
    return ""


def get_commits_between(since: str, until: str = "HEAD") -> list[str]:
    """Get commit subjects between two refs."""
    cmd = ["git", "log", "--oneline", "--format=%s"]
    if since:
        cmd.append(f"{since}..{until}")
    else:
        cmd.append(until)
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def version_has_tag(version: str) -> bool:
    """Check whether v{version} tag already exists."""
    result = subprocess.run(
        ["git", "tag", "-l", f"v{version}"],
        capture_output=True, text=True, cwd=ROOT,
    )
    return bool(result.stdout.strip())


# ---------------------------------------------------------------------------
# Commit classification
# ---------------------------------------------------------------------------

def classify_commit(subject: str) -> tuple[str, str]:
    """Return (section, cleaned message) from a commit subject."""
    if subject.startswith("Merge "):
        return "", ""
    # Skip auto-generated changelog commits to avoid recursion
    if subject.startswith("chore: auto-generate changelog") or \
       subject.startswith("chore: update unreleased changelog"):
        return "", ""

    m = re.match(r"^(\w+)(?:\([^)]*\))?:\s*(.+)", subject)
    if m:
        prefix = m.group(1).lower()
        message = m.group(2).strip()
        section = SECTION_MAP.get(prefix, DEFAULT_SECTION)
        return section, message[0].upper() + message[1:] if message else ""

    return DEFAULT_SECTION, subject[0].upper() + subject[1:] if subject else ""


def classify_commits(commits: list[str]) -> dict[str, list[str]]:
    """Classify a list of commit subjects into changelog sections."""
    sections: dict[str, list[str]] = {}
    seen: set[str] = set()
    for subject in commits:
        section, message = classify_commit(subject)
        if not section or not message:
            continue
        key = message.lower()
        if key in seen:
            continue
        seen.add(key)
        sections.setdefault(section, []).append(message)
    return sections


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


def build_release_entry(version: str, commits: list[str],
                        unreleased_body: str) -> str:
    """Build a ## [X.Y.Z] entry, merging unreleased content + new commits."""
    # Start with existing unreleased sections
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

    # Classify new commits
    new_sections = classify_commits(commits)

    # Merge: existing items first, then new (deduplicated)
    merged: dict[str, list[str]] = {}
    seen: set[str] = set()
    for heading in SECTION_ORDER:
        for item in existing_sections.get(heading, []):
            key = item.lower()
            if key not in seen:
                seen.add(key)
                merged.setdefault(heading, []).append(item)
        for item in new_sections.get(heading, []):
            key = item.lower()
            if key not in seen:
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
    # Find the unreleased section boundaries
    marker_idx = text.find(UNRELEASED_MARKER)
    if marker_idx < 0:
        sys.exit("CHANGELOG.md has no ## [Unreleased] section")

    after_marker = marker_idx + len(UNRELEASED_MARKER)
    # Find next ## [ heading
    next_heading = re.search(r"\n## \[", text[after_marker:])
    if next_heading:
        body_end = after_marker + next_heading.start()
    else:
        body_end = len(text)

    # Replace: clear unreleased body, insert versioned entry
    new_text = (
        text[:after_marker] + "\n\n"
        + entry + "\n"
        + text[body_end:]
    )
    return new_text


def update_unreleased(text: str, commits: list[str]) -> str:
    """Merge new commit entries into the [Unreleased] section."""
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

    # Classify new commits, skip duplicates
    new_sections = classify_commits(commits)
    added_count = 0
    for heading in SECTION_ORDER:
        for item in new_sections.get(heading, []):
            if item.lower() not in existing_items:
                existing_sections.setdefault(heading, []).append(item)
                existing_items.add(item.lower())
                added_count += 1

    if added_count == 0:
        return text  # Nothing new to add

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
        description="Generate or update CHANGELOG.md entries from git history")
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

    print(f"Version: {version}  |  Latest tag: {latest_tag or '(none)'}  |  Mode: {mode}")

    # Determine commit range
    base = args.base_ref or latest_tag
    commits = get_commits_between(base)
    print(f"Commits since {base or 'beginning'}: {len(commits)}")

    text = read_changelog()

    if mode == "release":
        if has_versioned_entry(version):
            print(f"CHANGELOG.md already has a versioned entry for {version} — nothing to do")
            return
        unreleased_body = parse_unreleased_body(text)
        entry = build_release_entry(version, commits, unreleased_body)

        if not args.apply:
            print("\n--- Draft release entry (use --apply to write) ---\n")
            print(entry)
            return

        new_text = insert_release_entry(text, entry)
        CHANGELOG.write_text(new_text, encoding="utf-8")
        print(f"Inserted release entry for {version} (unreleased items promoted)")

        if args.push:
            git_commit_and_push(f"chore: auto-generate changelog entry for {version}")

    else:  # unreleased
        new_text = update_unreleased(text, commits)
        if new_text == text:
            print("No new items to add to [Unreleased]")
            return

        if not args.apply:
            # Show what would be added
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
