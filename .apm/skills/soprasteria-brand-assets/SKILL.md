---
name: soprasteria-brand-assets
description: 'Locate and use official Sopra Steria branding resources (logos, templates, icons, guidelines) when auditing or refactoring applications, documents, or presentations.'
triggers: ['brand resources', 'logo files', 'brand inventory', 'asset discovery', 'official branding']
---

# Skill: Sopra Steria Brand Assets

## Purpose

This skill enables an agent to locate and use official Sopra Steria branding resources when auditing or refactoring applications, documents, or presentations.

The agent must always rely on **official assets** provided in the repository.

---

# Brand Resource Location

All official branding resources are located in:

knowledge/brand/soprasteria/

Asset inventory:

knowledge/brand/soprasteria/asset-inventory.md

The agent must read the inventory before applying branding changes.

---

# Asset Categories

The following asset types are available.

Brand guidelines

knowledge/brand/soprasteria/guidelines/

Logos

knowledge/brand/soprasteria/logos/

Templates

knowledge/brand/soprasteria/templates/

Icons

knowledge/brand/soprasteria/icons/

---

# Agent Responsibilities

When performing branding tasks the agent must:

1. Load the asset inventory
2. Identify the appropriate branding resources
3. Apply branding rules to the target artifact
4. Ensure compliance with Sopra Steria identity

---

# Branding Tasks Supported

The skill supports the following tasks.

Application theming

- update colors
- apply typography
- integrate logos
- adapt UI components

Document refactoring

- migrate documents to official templates
- align typography and layout
- ensure proper logo placement

Presentation styling

- migrate slides into official PowerPoint template
- apply icon library
- align color system

Brand compliance audit

- detect incorrect logos
- detect incorrect colors
- detect layout violations
- detect missing branding elements

---

# Logo Usage Rules

The agent must always choose the correct logo variant.

Color logo

Default usage.

Black logo

Use on light backgrounds.

White logo

Use on dark backgrounds.

The agent must never:

- recolor the logo
- stretch the logo
- modify proportions
- apply filters or shadows

---

# Template Usage Rules

If official templates exist the agent must:

- reuse the template
- migrate existing content into the template
- preserve template styles

The agent must **never recreate template layouts manually**.

---

# Icon Usage Rules

Icons must be taken from:

knowledge/brand/soprasteria/icons/

The agent should:

- reuse icons from the library
- maintain consistent icon style
- avoid external icon packs unless explicitly allowed

---

# Compliance Validation

Before finalizing branding changes the agent must verify:

- logo correctness
- color compliance
- typography alignment
- template usage
- layout consistency

If branding cannot be verified, the agent should request clarification.

---

# Reusability

This skill is reusable across repositories and can be invoked by any agent responsible for:

- UI theming
- document generation
- presentation creation
- brand compliance auditing