---
name: figma-design-sync
description: 'Interact with Figma via MCP — read designs, extract component specs, validate against design system tokens. Formalises the existing optional Figma integration.'
triggers:
  - figma design
  - figma sync
  - design system
  - figma components
  - design tokens
---

# Skill: figma-design-sync

## Goal

Interact with Figma via the Figma MCP server for bidirectional design synchronisation — pull component specs and design tokens from Figma, push HTML prototype feedback. This skill formalises the existing optional Figma integration in `sdlc-ba-functional-design` (ba-3.3b).

## MCP Server

- **Registry ID**: `figma-mcp`
- **Repository**: https://github.com/figma/mcp-server-guide
- **Auth**: Personal Access Token
- **Env**: `FIGMA_ACCESS_TOKEN`

## When to use

- Pulling component specifications from Figma for functional design
- Extracting design tokens (colors, typography, spacing) for brand compliance
- Validating HTML prototypes against Figma design system
- Importing Figma frames as references for UI specifications
- Checking brand compliance against Figma design library

## When NOT to use

- When no Figma designs exist for the project
- For pure backend/API projects with no UI
- When design work is done in other tools (Sketch, Adobe XD)

## Procedure

### Step 1 — Check MCP availability

Attempt to invoke the `figma-mcp` tool. If unavailable, skip to **Fallback**.

### Step 2 — Execute operation

Based on the user's request:
- **Read designs**: Pull frame/component data from a Figma file
- **Extract tokens**: Retrieve design tokens (colors, typography, spacing, shadows)
- **Component specs**: Get dimensions, properties, and variants for specific components
- **Prototype sync**: Compare HTML prototypes against Figma designs for drift
- **Brand validation**: Check designs against brand guidelines in `.apm/knowledge/brand/`

### Step 3 — Format results

Write design references and token extracts to output files.

### Fallback (without MCP)

If `figma-mcp` is unavailable:
1. Generate standalone HTML/CSS prototypes as the primary deliverable (already the default in ba-3.3b)
2. Use design tokens from `.apm/knowledge/brand/` if available locally
3. Warn that Figma sync is unavailable — prototypes are based on spec text only
4. The goal is functional validation, not pixel-perfect final. Stay sober and functional.

## Output

Use `edit/editFiles` to write:
- Design tokens: `outputs/specs/features/<feature>/design-tokens.json`
- Component specs: `outputs/specs/features/<feature>/component-specs.md`
- Prototype validation: integrated into existing prototype output files

## Security

- Never expose Figma access tokens in output files
- Figma file URLs may contain sensitive project names — use `[REDACTED:url]` in public outputs
- Design data is treated as **internal** sensitivity classification
