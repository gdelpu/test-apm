---
name: assets-and-templates
description: 'Guidance for discovering, classifying, and using official brand logos, templates, and supporting assets. Generic skill — extend with client-specific asset inventories.'
triggers: ['brand assets', 'official templates', 'logo usage', 'asset inventory', 'brand resources', 'template discovery']
version: '1.0.0'
---

# Skill: Assets and Templates

## Purpose

Guide agents in working with official brand logos, templates, and supporting assets. This is the generic, client-agnostic skill. For Sopra Steria specifics, see `soprasteria-assets-and-templates`.

## Rules

- Prefer official template usage over manual rebuilding.
- Prefer official logos over screenshots or reconstructed copies.
- If multiple official assets exist, pick the one matching context (dark background, white background, social media, document template, etc.).
- Keep a visible inventory of which asset was used and why.

## Required Behavior

When assets are provided, the agent should:

1. List all available assets
2. Classify them by type (logo, template, icon, example)
3. Map them to usage scenarios
4. Highlight missing dependencies or gaps

## Asset Categories

- Logos (color, monochrome, reversed)
- Presentation templates (PowerPoint, Google Slides)
- Document templates (Word, PDF, LaTeX)
- Icon libraries
- Signature / lockup assets
- Example documents / decks
- Theme token files for applications (optional)

## Inventory Structure

For each asset, record:

| Field | Description |
|-------|-------------|
| Display name | Human-readable name |
| Filename | Exact file name |
| Type | Logo / template / icon / example |
| Intended use | Where and when to use it |
| Preferred contexts | Light background, dark background, print, digital |
| Constraints | Minimum size, clear space, do-not-modify rules |

## If the User Asks for Repository-Ready Output

Create:

- One asset inventory markdown file
- Reusable skill files referencing the inventory
- Optional implementation notes and starter tokens
