#!/usr/bin/env python3
"""Generate marketplace.json from apm.yml and filesystem asset counts.

Usage:
    python scripts/generate-marketplace.py [--output marketplace.json]

Reads the canonical apm.yml and counts assets in .apm/ to produce a
marketplace.json suitable for registry discovery and catalog UIs.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
APM_YML = REPO_ROOT / "apm.yml"
APM_DIR = REPO_ROOT / ".apm"


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
            "url": "https://innersource.soprasteria.com/ai-backbone/ai-sdlc-foundation",
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
