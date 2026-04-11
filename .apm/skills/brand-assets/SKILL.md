---
name: brand-assets
description: 'Locate and use official branding resources (logos, templates, icons, guidelines) when auditing or refactoring applications, documents, or presentations. Default brand: Sopra Steria. Extensible for other client brands via knowledge/brand/<client>/.'
triggers: ['brand resources', 'logo files', 'brand inventory', 'asset discovery', 'official branding', 'brand materials', 'official templates', 'logo usage']
version: '2.0.0'
---

# Skill: Brand Assets

## Purpose

Enable agents to locate and use official branding resources when auditing or refactoring applications, documents, or presentations.

The agent must always rely on **official assets** provided in the repository or by the client. Prefer official template usage over manual rebuilding. Prefer official logos over screenshots or reconstructed vector copies.

## Asset Location

Brand resources are located at a well-known path within the repository:

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
2. Classify assets by type (logo, template, icon, guideline)
3. Map assets to usage scenarios (see Usage Mapping below)
4. Identify the appropriate branding resources for the task
5. Apply branding rules to the target artifact
6. Highlight missing dependencies
7. Ensure compliance with the brand identity

## Suggested Inventory Structure

For each asset, record:

- Display name
- Filename
- Type
- Intended use
- Preferred contexts
- Constraints

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

## Icon Usage Rules

Icons must be taken from the official icon library. The agent should:

- Reuse icons from the library
- Maintain consistent icon style
- Avoid external icon packs unless explicitly allowed

## Compliance Validation

Before finalizing branding changes, verify:

- Logo correctness (variant, placement, clear space)
- Color compliance
- Typography alignment
- Template usage
- Layout consistency

If branding cannot be verified, request clarification.

---

## Default Brand: Sopra Steria

All official Sopra Steria branding resources are located in:

```
knowledge/brand/soprasteria/
```

Asset inventory: `knowledge/brand/soprasteria/asset-inventory.md`

The agent must read the inventory before applying branding changes.

### Asset Paths

| Category | Path |
|----------|------|
| Brand guidelines | `knowledge/brand/soprasteria/guidelines/` |
| Logos | `knowledge/brand/soprasteria/logos/` |
| Templates | `knowledge/brand/soprasteria/templates/` |
| Icons | `knowledge/brand/soprasteria/icons/` |

### Available Assets

| Asset | Type | Intended Use |
|-------|------|-------------|
| `BrandGuideline_SopraSteria.pdf` | Guideline | Authoritative brand rules |
| `SOPRASTERIA_logo_RVB_exe.png` | Logo (color) | Default on light/white backgrounds |
| `SOPRASTERIA_logo_RVB_noir_exe.png` | Logo (black) | When color printing is unavailable |
| `SOPRASTERIA_logo_RVB_blanc_exe.png` | Logo (white) | On dark backgrounds |
| `sopra-steria-dossier-template.dotx` | Word template | Dossiers, letters, memos |
| `sopra-steria-presentation-template.potx` | PowerPoint template | 16:9 presentations |
| `ICON_LIBRARY.pptx` | Icon library | PowerPoint visuals, approved icons |

### Usage Mapping

- Full-color logo on white or light uncluttered backgrounds
- White logo on dark backgrounds
- Monochrome black logo when color printing is unavailable
- PowerPoint template for 16:9 presentations
- Word template for dossiers / letters / memos
- Official icon library for PowerPoint visuals and icon usage

### Compliance Priority Order

1. Official templates
2. Official logos
3. Official icon library
4. Brand guideline rules
