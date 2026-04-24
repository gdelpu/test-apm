#!/usr/bin/env python3
"""Generate marketplace.json from apm.yml and filesystem asset counts.

Usage:
    python scripts/generate-marketplace.py [--output marketplace.json]

Reads the canonical apm.yml and counts assets in .apm/ to produce a
marketplace.json with:
  - Internal catalog metadata (displayName, assets, registry, …)
  - APM-compatible `plugins` array with `git-subdir` sources pointing at
    the GitLab monorepo, so a GitHub-hosted marketplace can reference
    individual primitives hosted on a different Git provider.

Run this script as the single source of truth for marketplace.json.
Run generate-plugins.py separately to (re)create individual plugin.json files.
"""

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
APM_YML = REPO_ROOT / "apm.yml"
APM_DIR = REPO_ROOT / ".apm"

REPO_URL = "https://github.com/gdelpu/test-apm"

# GitLab monorepo URL — plugins live here, marketplace may be on GitHub
GITLAB_REPO_URL = (
    "https://github.com/gdelpu/test-apm.git"
)
GITLAB_REPO_SLUG = "gdelpu/test-apm"
GITLAB_REPO_REF = "feature/marketplace"


def count_files(directory: Path, pattern: str = "*.md") -> int:
    """Count files matching pattern in a directory (non-recursive)."""
    if not directory.is_dir():
        return 0
    return len(list(directory.glob(pattern)))


def count_dirs(directory: Path) -> int:
    """Count immediate subdirectories."""
    if not directory.is_dir():
        return 0
    return len([d for d in directory.iterdir() if d.is_dir()])


def count_recursive_files(directory: Path, pattern: str = "*") -> int:
    """Count files matching pattern recursively."""
    if not directory.is_dir():
        return 0
    return len([f for f in directory.rglob(pattern) if f.is_file()])


def count_assets() -> dict:
    """Count all asset types from the .apm/ directory."""
    return {
        "agents": count_files(APM_DIR / "agents"),
        "skills": count_dirs(APM_DIR / "skills"),
        "workflows": count_files(APM_DIR / "workflows", "*.yml"),
        "prompts": count_files(APM_DIR / "prompts"),
        "instructions": count_files(APM_DIR / "instructions"),
        "templates": count_files(APM_DIR / "templates", "*"),
        "contexts": count_files(APM_DIR / "contexts", "*"),
        "hooks": count_recursive_files(APM_DIR / "hooks", "*.md"),
        "knowledgeFiles": count_recursive_files(APM_DIR / "knowledge"),
    }


def list_agents() -> list[str]:
    """List canonical agent names (without extension)."""
    agents_dir = APM_DIR / "agents"
    if not agents_dir.is_dir():
        return []
    return sorted(p.stem for p in agents_dir.glob("*.md"))


def list_workflows() -> list[str]:
    """List canonical workflow names (without extension)."""
    workflows_dir = APM_DIR / "workflows"
    if not workflows_dir.is_dir():
        return []
    return sorted(p.stem for p in workflows_dir.glob("*.yml"))


# ---------------------------------------------------------------------------
# APM plugins array helpers
# ---------------------------------------------------------------------------

def _parse_frontmatter(path: Path) -> dict:
    """Return YAML frontmatter as dict (or {} if absent/unparseable)."""
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


def _git_subdir(subdir: str) -> dict:
    """APM git-subdir source object pointing at the GitLab monorepo."""
    return {"type": "git-subdir", "repo": GITLAB_REPO_SLUG, "ref": GITLAB_REPO_REF, "subdir": subdir}


def _plugin_entry(name: str, description: str, tags: list, subdir: str) -> dict:
    return {"name": name, "description": description, "tags": tags,
            "source": _git_subdir(subdir)}


def build_plugins_list() -> list[dict]:
    """Build the APM-compatible plugins list from filesystem primitives."""
    plugins: list[dict] = []

    # Full package — entire repo, root plugin.json
    plugins.append({
        "name": "ssg-ai-backbone",
        "description": (
            "Complete AI SDLC Foundation — all agents, skills, workflows, prompts, "
            "instructions and foundational knowledge for specification-driven delivery, "
            "quality validation, security governance, and full-lifecycle SDLC support."
        ),
        "version": "0.0.34",
        "tags": ["ai-agents", "sdlc", "copilot", "claude-code", "full-stack",
                 "workflows", "specification-driven", "security-governance"],
        "source": {"type": "url", "url": GITLAB_REPO_URL},
    })

    # Agents
    agents_dir = APM_DIR / "agents"
    for md in sorted(agents_dir.glob("*.md")):
        fm = _parse_frontmatter(md)
        desc = str(fm.get("description") or f"Agent: {md.stem}")[:250]
        plugins.append(_plugin_entry(md.stem, desc, ["agents", "sdlc"],
                                     f".apm/agents/{md.stem}"))

    # Skills
    skills_dir = APM_DIR / "skills"
    for skill_dir in sorted(d for d in skills_dir.iterdir() if d.is_dir()):
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        fm = _parse_frontmatter(skill_md)
        desc = str(fm.get("description") or f"Skill: {skill_dir.name}")[:250]
        plugins.append(_plugin_entry(skill_dir.name, desc, ["skills", "sdlc"],
                                     f".apm/skills/{skill_dir.name}"))

    # Workflows
    workflows_dir = APM_DIR / "workflows"
    type_tag = {"delivery": "delivery-workflow", "validation": "validation-workflow",
                "assessment": "assessment-workflow", "modernization": "modernization-workflow"}
    for yml in sorted(workflows_dir.glob("*.yml")):
        if yml.stem == "_schema":
            continue
        try:
            data = yaml.safe_load(yml.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        desc = str(data.get("description") or f"Workflow: {yml.stem}")[:250]
        wtype = data.get("type", "delivery")
        tags = ["workflows", "sdlc", type_tag.get(wtype, wtype)]
        plugins.append(_plugin_entry(yml.stem, desc, tags,
                                     f".apm/workflows/{yml.stem}"))

    # Prompts
    prompts_dir = APM_DIR / "prompts"
    seen: set[str] = set()
    for pf in sorted(prompts_dir.glob("*.prompt.md")):
        stem = pf.stem.replace(".prompt", "")
        if stem in seen:
            continue
        seen.add(stem)
        fm = _parse_frontmatter(pf)
        desc = str(fm.get("description") or f"Prompt: {stem}")[:250]
        plugins.append(_plugin_entry(stem, desc, ["prompts", "sdlc"],
                                     f".apm/prompts/{stem}"))

    # Instructions (only those with structured frontmatter)
    instructions_dir = APM_DIR / "instructions"
    for md in sorted(instructions_dir.glob("*.md")):
        fm = _parse_frontmatter(md)
        if not fm.get("description") and not fm.get("name"):
            continue
        desc = str(fm.get("description") or f"Instruction: {md.stem}")[:250]
        plugins.append(_plugin_entry(md.stem, desc, ["instructions", "sdlc"],
                                     f".apm/instructions/{md.stem}"))

    # Hooks (pre/ and post/)
    hooks_dir = APM_DIR / "hooks"
    for scope in ("pre", "post"):
        scope_dir = hooks_dir / scope
        if not scope_dir.exists():
            continue
        for md in sorted(scope_dir.rglob("*.md")):
            text = md.read_text(encoding="utf-8")
            para = [l.strip() for l in text.splitlines()
                    if l.strip() and not l.startswith(("#", ">", "|", "---"))]
            desc = (para[0] if para else md.stem)[:250]
            rel = md.relative_to(hooks_dir)
            plugin_name = "-".join(rel.with_suffix("").parts)
            hook_tag = "pre-hook" if scope == "pre" else "post-hook"
            plugins.append(_plugin_entry(plugin_name, desc, ["hooks", "sdlc", hook_tag],
                                         f".apm/hooks/{'/'.join(rel.with_suffix('').parts)}"))

    return plugins


def generate_marketplace(apm: dict) -> dict:
    """Build marketplace.json structure from apm.yml data and filesystem."""
    assets = count_assets()

    return {
        # Identity (from apm.yml)
        "name": apm["name"],
        "version": apm["version"],
        "displayName": "AI SDLC Foundation",
        "description": apm.get("description", "").strip(),
        "publisher": "sopra-steria-group",
        # Classification
        "categories": [
            "SDLC",
            "AI Agents",
            "Workflows",
            "Quality & Governance",
            "Security",
            "Specification",
        ],
        "tags": [
            "ai-agents",
            "sdlc",
            "copilot",
            "claude-code",
            "specification-driven",
            "quality-validation",
            "security-governance",
            "brand-compliance",
            "mcp",
            "workflows",
            "architecture",
            "testing",
            "modernization",
            "code-review",
        ],
        # Targets & install modes (from apm.yml)
        "targets": apm.get("targets", []),
        "installModes": list(apm.get("install-modes", {}).keys()),
        # Asset counts (live from filesystem)
        "assets": assets,
        # Exports (from apm.yml)
        "exports": apm.get("exports", {}),
        # Catalogs
        "agents": list_agents(),
        "workflows": list_workflows(),
        # Distribution
        "repository": {
            "type": "git",
            "url": REPO_URL,
        },
        "registry": {
            "type": "gitlab-generic",
            "packageName": apm["name"],
            "bundles": [
                f"{apm['name']}-copilot.tar.gz",
                f"{apm['name']}-claude.tar.gz",
                f"{apm['name']}-cli.tar.gz",
                f"{apm['name']}-all.tar.gz",
            ],
        },
        # Branding
        "icon": "docs/assets/ai-backbone.png",
        "license": "UNLICENSED",
        "homepage": "https://steria.sharepoint.com/sites/aibackbone/SitePages/Home.aspx",
        # Documentation links
        "links": {
            "quickStart": "docs/consumer/quick-start.md",
            "consumerGuide": "docs/consumer/apm-consumer-guide.md",
            "contributing": "docs/contributor/contributing.md",
            "architecture": "docs/contributor/architecture.md",
            "changelog": "CHANGELOG.md",
        },
        # Schemas (from apm.yml)
        "schemas": apm.get("schemas", {}),
        # CI gates
        "ciGates": {
            "path": apm.get("ci-gates", "ci-gates"),
            "stations": [
                "A0-intake",
                "A1-policy",
                "A2-security-static",
                "A3-prompt-injection",
                "A4-red-team",
                "A5-sandbox-simulation",
                "A6-policy-gate",
                "A7-gitlab-update",
            ],
        },
        # Dependencies (from apm.yml)
        "dependencies": apm.get("dependencies", []),
        # Metadata
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        # APM-compatible plugins index (git-subdir sources for cross-host GitLab monorepo)
        "plugins": build_plugins_list(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate marketplace.json from apm.yml")
    parser.add_argument(
        "-o",
        "--output",
        default=str(REPO_ROOT / "marketplace.json"),
        help="Output path (default: marketplace.json in repo root)",
    )
    args = parser.parse_args()

    if not APM_YML.is_file():
        print(f"Error: {APM_YML} not found", file=sys.stderr)
        return 1

    with open(APM_YML, encoding="utf-8") as f:
        apm = yaml.safe_load(f)

    marketplace = generate_marketplace(apm)
    output_path = Path(args.output)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(marketplace, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Generated {output_path} (v{apm['version']})")
    print(f"  agents={marketplace['assets']['agents']}"
          f"  skills={marketplace['assets']['skills']}"
          f"  workflows={marketplace['assets']['workflows']}"
          f"  prompts={marketplace['assets']['prompts']}")
    print(f"  plugins (APM registry)={len(marketplace['plugins'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
