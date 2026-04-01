---
name: brand-assets
description: 'Locate and use official branding resources (logos, templates, icons, guidelines) when auditing or refactoring applications, documents, or presentations. Generic skill — extend with client-specific asset locations.'
triggers: ['brand resources', 'logo files', 'brand inventory', 'asset discovery', 'official branding', 'brand materials']
version: '1.0.0'
---

# Skill: Brand Assets

## Purpose

Enable agents to locate and use official branding resources when auditing or refactoring applications, documents, or presentations. This is the generic, client-agnostic skill. For Sopra Steria specifics, see `soprasteria-brand-assets`.

The agent must always rely on **official assets** provided in the repository or by the client.

## Asset Location

Brand resources should be located in a well-known path within the repository:

```
knowledge/brand/<client>/
```

The agent must check for an asset inventory file before applying branding changes.

## Asset Categories

| Category | Typical Path | Contents |
|----------|-------------|----------|
| Brand guidelines | `guidelines/` | PDF or markdown rules documents |
| Logos | `logos/` | SVG, PNG in various variants (color, mono, reversed) |
| Templates | `templates/` | POTX, DOTX, PDF templates |
| Icons | `icons/` | SVG or PNG icon libraries |

## Agent Responsibilities

When performing branding tasks, the agent must:

1. Load the asset inventory for the target brand
2. Identify the appropriate branding resources for the task
3. Apply branding rules to the target artifact
4. Ensure compliance with the brand identity

## Branding Tasks Supported

- **Application theming** — update colors, apply typography, integrate logos, adapt UI components
- **Document refactoring** — migrate to official templates, align typography and layout
- **Presentation styling** — migrate slides to official templates, apply icon library
- **Brand compliance audit** — detect incorrect logos, colors, layout violations

## Logo Usage Rules

The agent must choose the correct logo variant:

- **Color logo** — default usage on light/white backgrounds
- **Monochrome / black logo** — when color printing is unavailable
- **White / reversed logo** — on dark backgrounds

The agent must never: recolor, stretch, modify proportions, or apply filters to logos.

## Template Usage Rules

If official templates exist, the agent must:

- Reuse the template (never recreate layouts manually)
- Migrate existing content into the template
- Preserve template styles

## Compliance Validation

Before finalizing branding changes, verify:

- Logo correctness (variant, placement, clear space)
- Color compliance
- Typography alignment
- Template usage
- Layout consistency

If branding cannot be verified, request clarification.
