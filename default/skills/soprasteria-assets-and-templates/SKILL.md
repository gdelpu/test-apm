---
name: soprasteria-assets-and-templates
description: 'Guidance for working with official Sopra Steria logos, templates, and supporting brand assets. Covers asset discovery, classification, and usage mapping.'
triggers: ['brand assets', 'official templates', 'logo usage', 'asset inventory', 'brand resources']
---

# Skill: Sopra Steria Assets and Templates

## Purpose
This skill tells the agent how to work with official logos, templates, and supporting brand assets.

## Rules
- Prefer official template usage over manual rebuilding.
- Prefer official logos over screenshots or reconstructed vector copies.
- If multiple official assets exist, pick the one matching context: dark background, white background, social media, document template, etc.
- Keep a visible inventory of which asset was used and why.

## Required behavior
When assets are provided, the agent should:
1. list them
2. classify them by type
3. map them to usage scenarios
4. highlight missing dependencies

## Asset categories to maintain
- Logos
- PowerPoint templates
- Word templates
- Icon libraries
- Signature assets
- Example documents / decks
- Optional theme token files for apps

## Suggested inventory structure
For each asset, record:
- display name
- filename
- type
- intended use
- preferred contexts
- constraints

## Example usage mapping
- full-color logo on white or light uncluttered backgrounds
- white logo on dark backgrounds
- monochrome black logo when color printing is unavailable
- PowerPoint template for 16:9 presentations
- Word template for dossiers / letters / memos
- official icon library for PowerPoint visuals

## If the user asks for repository-ready output
Create:
- one agent file
- reusable skill files
- one asset inventory markdown
- optional implementation notes and starter tokens
