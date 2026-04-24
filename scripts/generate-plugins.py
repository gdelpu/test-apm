#!/usr/bin/env python3
"""Generate individual plugin.json files for every APM primitive in .apm/.

Creates plugin.json files for:
  - .apm/agents/<name>/          (one per agent .md)
  - .apm/skills/<name>/          (one per skill directory)
  - .apm/workflows/<name>/       (one per workflow .yml, with dependencies)
  - .apm/prompts/<name>/         (one per prompt file pair)
  - .apm/instructions/<name>/    (one per instruction file with frontmatter)
  - .apm/hooks/<scope>/<name>/   (one per hook .md)

Does NOT write marketplace.json — run generate-marketplace.py for that.

Usage:
    python scripts/generate-plugins.py [--dry-run]
"""

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
APM_DIR = REPO_ROOT / ".apm"

GITLAB_REPO_URL = (
    "https://github.com/gdelpu/test-apm.git"
)
GITLAB_REPO_SLUG = "gdelpu/test-apm"
GITLAB_REPO_REF = "feature/marketplace"

COMMON_FIELDS = {
    "version": "0.0.34",
    "author": "Sopra Steria Group",
    "license": "UNLICENSED",
    "repository": GITLAB_REPO_URL,
    "homepage": "https://steria.sharepoint.com/sites/aibackbone/SitePages/Home.aspx",
}


def git_subdir_source(subdir: str) -> dict:
    """Build a git-subdir marketplace source pointing at the GitLab monorepo."""
    return {"type": "git-subdir", "repo": GITLAB_REPO_SLUG, "ref": GITLAB_REPO_REF, "subdir": subdir}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_frontmatter(path: Path) -> dict:
    """Return dict of YAML frontmatter fields (or {} if none)."""
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return {}
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return {}
    try:
        return yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError:
        return {}


def truncate(s: str, max_len: int = 250) -> str:
    if len(s) > max_len:
        return s[:max_len - 3] + "..."
    return s


def tags_from_name(name: str) -> list[str]:
    """Derive baseline tags from a kebab-case name."""
    parts = name.replace("-", " ").split()
    known_domains = {
        "sdlc", "spec", "api", "brand", "security", "quality", "test",
        "frontend", "dotnet", "react", "workflow", "agent", "skill",
        "brownfield", "modernization", "refactor", "governance",
    }
    tags = []
    for p in parts:
        if p in known_domains:
            tags.append(p)
    return tags


def write_plugin(path: Path, data: dict, dry_run: bool) -> None:
    if dry_run:
        print(f"  [DRY] would write {path.relative_to(REPO_ROOT)}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"  {path.relative_to(REPO_ROOT)}")


# ---------------------------------------------------------------------------
# Agents
# ---------------------------------------------------------------------------

def process_agents(dry_run: bool) -> list[dict]:
    """Create .apm/agents/<stem>/plugin.json for each agent .md file."""
    agents_dir = APM_DIR / "agents"
    plugins = []
    for md in sorted(agents_dir.glob("*.md")):
        fm = parse_frontmatter(md)
        name = fm.get("name") or md.stem
        description = truncate(fm.get("description") or f"Agent: {name}")
        tags = sorted({"agents", "sdlc"} | set(tags_from_name(md.stem)))

        plugin = {
            "name": name,
            "description": description,
            **COMMON_FIELDS,
            "tags": tags,
            "agents": [f"../{md.name}"],
        }
        plugin_dir = agents_dir / md.stem
        write_plugin(plugin_dir / "plugin.json", plugin, dry_run)
        plugins.append({"stem": md.stem, "name": name, "description": description})
    return plugins


# ---------------------------------------------------------------------------
# Skills
# ---------------------------------------------------------------------------

def process_skills(dry_run: bool) -> list[dict]:
    """Create .apm/skills/<name>/plugin.json for each skill directory."""
    skills_dir = APM_DIR / "skills"
    plugins = []
    for skill_dir in sorted(d for d in skills_dir.iterdir() if d.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        fm = parse_frontmatter(skill_md)
        name = skill_dir.name
        description = truncate(fm.get("description") or f"Skill: {name}")

        # Build tags from triggers + domain detection
        raw_triggers = fm.get("triggers") or []
        if isinstance(raw_triggers, str):
            raw_triggers = [raw_triggers]
        # Use first 5 meaningful trigger words as tags
        trigger_tags = []
        for t in raw_triggers[:5]:
            slug = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
            if slug and len(slug) <= 30:
                trigger_tags.append(slug)

        tags = sorted({"skills", "sdlc"} | set(tags_from_name(name)) | set(trigger_tags[:4]))

        plugin = {
            "name": name,
            "description": description,
            **COMMON_FIELDS,
            "tags": tags,
            "skills": "./",
        }
        write_plugin(skill_dir / "plugin.json", plugin, dry_run)
        plugins.append({"stem": name, "name": name, "description": description})
    return plugins


# ---------------------------------------------------------------------------
# Workflows
# ---------------------------------------------------------------------------

def process_workflows(dry_run: bool) -> list[dict]:
    """Create .apm/workflows/<name>/plugin.json for each workflow .yml."""
    workflows_dir = APM_DIR / "workflows"
    plugins = []
    type_tag_map = {
        "delivery": "delivery-workflow",
        "validation": "validation-workflow",
        "assessment": "assessment-workflow",
        "modernization": "modernization-workflow",
    }

    for yml_file in sorted(workflows_dir.glob("*.yml")):
        if yml_file.stem == "_schema":
            continue
        try:
            data = yaml.safe_load(yml_file.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue

        name = data.get("name") or yml_file.stem
        description = truncate(data.get("description") or f"Workflow: {name}")
        wf_type = data.get("type", "delivery")

        stations = data.get("stations") or []
        agent_deps = sorted({s.get("agent") for s in stations if s.get("agent")})
        skill_deps = sorted({sk for s in stations for sk in (s.get("skills") or [])})
        num_stations = len(stations)

        # Build companion .md description if exists
        md_companion = workflows_dir / f"{yml_file.stem}.md"
        if md_companion.exists():
            md_text = md_companion.read_text(encoding="utf-8")
            # Extract the first paragraph after the title
            lines = [l for l in md_text.splitlines() if l.strip() and not l.startswith("#")]
            if lines:
                description = truncate(lines[0])

        # Tags
        base_tags = {"workflows", "sdlc", type_tag_map.get(wf_type, wf_type)}
        base_tags |= set(tags_from_name(name))
        tags = sorted(base_tags)

        # Dependencies: use `git` field format expected by APM CLI
        def _git_dep(subdir: str) -> dict:
            return {"git": f"https://github.com/{GITLAB_REPO_SLUG}",
                    "ref": GITLAB_REPO_REF, "subdir": subdir}

        dependencies = (
            [_git_dep(f".apm/agents/{a}") for a in agent_deps] +
            [_git_dep(f".apm/skills/{s}") for s in skill_deps]
        )

        plugin = {
            "name": name,
            "description": description,
            **COMMON_FIELDS,
            "tags": tags,
            "type": wf_type,
            "stations": num_stations,
            "dependencies": dependencies,
        }
        # Remove empty lists
        plugin = {k: v for k, v in plugin.items() if v != []}

        plugin_dir = workflows_dir / yml_file.stem
        write_plugin(plugin_dir / "plugin.json", plugin, dry_run)
        plugins.append({"stem": yml_file.stem, "name": name, "description": description,
                         "agents": agent_deps, "skills": skill_deps})
    return plugins


# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

def process_prompts(dry_run: bool) -> list[dict]:
    """Create .apm/prompts/<stem>/plugin.json for each .prompt.md file."""
    prompts_dir = APM_DIR / "prompts"
    plugins = []
    seen: set[str] = set()

    for prompt_file in sorted(prompts_dir.glob("*.prompt.md")):
        fm = parse_frontmatter(prompt_file)
        name = fm.get("name") or prompt_file.stem.replace(".prompt", "")
        if name in seen:
            continue
        seen.add(name)
        description = truncate(fm.get("description") or f"Prompt: {name}")
        mode = fm.get("mode", "ask")

        tags = sorted({"prompts", "sdlc"} | set(tags_from_name(name)))
        if mode == "agent":
            tags = sorted(set(tags) | {"agent-mode"})

        # Reference the companion .md if present (display file)
        companion = prompts_dir / f"{prompt_file.stem.replace('.prompt', '')}.md"
        commands = [f"../{prompt_file.name}"]
        if companion.exists():
            commands.append(f"../{companion.name}")

        plugin = {
            "name": name,
            "description": description,
            **COMMON_FIELDS,
            "tags": tags,
            "commands": commands,
        }
        plugin_dir = prompts_dir / name
        write_plugin(plugin_dir / "plugin.json", plugin, dry_run)
        plugins.append({"stem": name, "name": name, "description": description})
    return plugins


# ---------------------------------------------------------------------------
# Instructions
# ---------------------------------------------------------------------------

def process_instructions(dry_run: bool) -> list[dict]:
    """Create .apm/instructions/<stem>/plugin.json for instruction files with frontmatter."""
    instructions_dir = APM_DIR / "instructions"
    plugins = []

    for md in sorted(instructions_dir.glob("*.md")):
        fm = parse_frontmatter(md)
        # Skip files without structured frontmatter (pure narrative files)
        if not fm.get("description") and not fm.get("name"):
            continue
        name = fm.get("name") or md.stem
        description = truncate(fm.get("description") or f"Instruction: {name}")
        apply_to = fm.get("applyTo", "**")

        tags = sorted({"instructions", "sdlc"} | set(tags_from_name(md.stem)))

        plugin = {
            "name": name,
            "description": description,
            **COMMON_FIELDS,
            "tags": tags,
            "applyTo": apply_to,
            "instructions": [f"../{md.name}"],
        }
        plugin_dir = instructions_dir / md.stem
        write_plugin(plugin_dir / "plugin.json", plugin, dry_run)
        plugins.append({"stem": md.stem, "name": name, "description": description})
    return plugins


# ---------------------------------------------------------------------------
# Hooks
# ---------------------------------------------------------------------------

def process_hooks(dry_run: bool) -> list[dict]:
    """Create plugin.json for hook .md files in pre/ and post/ subdirs."""
    hooks_dir = APM_DIR / "hooks"
    plugins = []

    for scope in ("pre", "post"):
        scope_dir = hooks_dir / scope
        if not scope_dir.exists():
            continue
        for md in sorted(scope_dir.rglob("*.md")):
            text = md.read_text(encoding="utf-8")
            # Extract title from first heading
            title_m = re.search(r"^#+\s+(.*)", text, re.MULTILINE)
            title = title_m.group(1).strip() if title_m else md.stem

            # Extract description: first real paragraph (not blockquote/badge/heading)
            para_lines = [
                l.strip() for l in text.splitlines()
                if l.strip()
                and not l.startswith("#")
                and not l.startswith(">")
                and not l.startswith("|")
                and not l.startswith("---")
            ]
            description = truncate(para_lines[0]) if para_lines else truncate(title)

            # Determine hook type
            hook_type = "pre-hook" if scope == "pre" else "post-hook"
            # Get severity from file text
            sev_m = re.search(r"\*\*Severity:\*\*\s*(\w+)", text)
            severity = sev_m.group(1).lower() if sev_m else "warning"

            tags = sorted({"hooks", "sdlc", hook_type} | set(tags_from_name(md.stem)))

            # Unique plugin name: scope/subdir/stem
            rel = md.relative_to(hooks_dir)
            plugin_name = "-".join(rel.with_suffix("").parts)

            plugin = {
                "name": plugin_name,
                "description": description,
                **COMMON_FIELDS,
                "tags": tags,
                "hookType": scope,
                "severity": severity,
                "hooks": str(md.relative_to(APM_DIR.parent)),
            }
            plugin_dir = md.parent / md.stem
            write_plugin(plugin_dir / "plugin.json", plugin, dry_run)
            plugins.append({"stem": plugin_name, "name": plugin_name, "description": description})
    return plugins


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description="Generate plugin.json files for all .apm primitives")
    parser.add_argument("--dry-run", action="store_true", help="List actions without writing files")
    args = parser.parse_args()

    dry = args.dry_run

    print("=== Agents ===")
    agents = process_agents(dry)

    print("\n=== Skills ===")
    skills = process_skills(dry)

    print("\n=== Workflows ===")
    workflows = process_workflows(dry)

    print("\n=== Prompts ===")
    prompts = process_prompts(dry)

    print("\n=== Instructions ===")
    instructions = process_instructions(dry)

    print("\n=== Hooks ===")
    hooks = process_hooks(dry)

    total = len(agents) + len(skills) + len(workflows) + len(prompts) + len(instructions) + len(hooks)
    print(
        f"\nSummary: {total} plugin.json files"
        f" ({len(agents)} agents, {len(skills)} skills, {len(workflows)} workflows,"
        f" {len(prompts)} prompts, {len(instructions)} instructions, {len(hooks)} hooks)"
    )
    print("Run generate-marketplace.py to regenerate marketplace.json.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
