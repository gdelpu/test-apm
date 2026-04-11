---
name: brand-app
description: 'Adapt applications, websites, portals, design systems, and front-end codebases to a target brand identity while preserving usability and accessibility. Default brand: Sopra Steria. Extensible for other client brands via knowledge/brand/<client>/.'
triggers: ['app branding', 'application theming', 'UI branding', 'design tokens', 'theme refactor', 'CSS branding', 'application styling']
version: '2.0.0'
---

# Skill: App Branding

## Purpose

Adapt applications, websites, portals, design systems, and front-end codebases to a target brand identity while preserving usability and accessibility. Default brand values are for Sopra Steria. To override for a different client, provide assets in `knowledge/brand/<client>/` and define client-specific tokens.

## Main Principle

Branding an application is not the same as turning it into a brochure. The result should feel unmistakably branded, but still usable, maintainable, and accessible.

## Refactor Order

### 1. Inventory the Existing Theme

Capture the current state:

- Color tokens / CSS custom properties
- Typography stack (fonts, sizes, weights)
- Icon library
- Logo placement
- Header / footer patterns
- Button styles and variants
- Chart / data visualization colors
- Empty states, alerts, badges
- Dark mode behavior (if any)

### 2. Replace with Brand-Compatible Structure

#### Theme Tokens

Define tokens for at minimum:

- Primary brand colors (2–4 colours)
- Accent / highlight colors
- Neutral scale (black, greys, white)
- Semantic colors (error, warning, success, info)

#### Typography Mapping

- Brand heading font
- Brand body font
- Practical fallback for environments where brand fonts are unavailable
- Never claim full brand compliance if the official font is not available at runtime

#### Visual System Rules

- Use white / negative space generously as the base canvas
- Keep the interface clean and uncluttered
- Use the primary brand color as the structural anchor
- Use accent colors for selective emphasis, not permanent visual noise
- Use gradients deliberately in hero zones, not everywhere

### 3. Component Adaptation

Apply brand tokens to common UI components:

- **Header / navigation** — restrained base, proper logo placement. Avoid oversized gradients behind navigation unless it is a branded landing area.
- **Buttons** — primary, secondary, danger variants with accessible contrast. Avoid using accent colors as generic primary actions.
- **Cards / panels** — white cards, subtle borders, reserve gradients for featured cards.
- **Forms** — readable labels, branded focus rings with WCAG compliance. Keep labels and helper text neutral and high-contrast.
- **Tables** — mostly neutral; brand color for accents where it improves comprehension.
- **Alerts / status** — do not force brand colors onto semantic status colors when it harms usability. Brand should frame the experience, not erase product semantics.
- **Charts** — primary palette first, secondary to extend differentiation. Add labels or patterns when color alone would be ambiguous.

### 4. Logo Handling

- Use official logo assets only (PNG/SVG)
- Default placements: header, sign-in page, about page, exported reports
- Never stretch, recolor, or apply filters to the logo
- Respect minimum sizes and whitespace

### 5. Accessibility Validation (WCAG 2.1 AA)

Accessibility must be verified after every branding change:

- All color pairings meet 4.5:1 (normal text) and 3:1 (large text, UI components)
- Focus indicators visible on all brand backgrounds
- Skip-to-content link present
- No reliance on color alone to communicate state
- All interactive elements keyboard-accessible

Use the `brand-accessibility` skill for the full checklist.

---

## Default Brand: Sopra Steria

### Theme Tokens

| Token | Hex |
|-------|-----|
| `brand-primary-900` | `#4D1D82` |
| `brand-primary-700` | `#8B1D82` |
| `brand-accent-red` | `#CF022B` |
| `brand-accent-orange` | `#EF7D00` |
| `brand-neutral-900` | `#1D1D1B` |
| `brand-neutral-600` | `#A8A8A7` |
| `brand-neutral-200` | `#EDEDED` |
| `brand-neutral-0` | `#FFFFFF` |

Optional secondary highlights from approved secondary palette (see `brand-core`).

### Typography

- Preferred brand font: **Hurme Geometric Sans 3**
- Headings: **Hurme Geometric Sans 4** when feasible
- Practical fallback for enterprise apps: **Tahoma** or system sans-serif
- Never claim full brand compliance if Hurme is not actually available in the runtime environment

### Visual System

- Use white generously as the base canvas
- Use purple as the structural brand anchor
- Use red/orange as selective emphasis, not as permanent visual noise
- Use gradients deliberately in hero zones, banners, title areas, splash states, or branded intro screens — not everywhere

### Component Guidance

#### Header / top navigation
- Use restrained white or dark-purple base
- Place official logo with proper clear space

#### Buttons
- Primary buttons: dark purple base with accessible contrast
- Secondary buttons: outline or light variants using neutral system
- Danger / destructive states can use red if semantically appropriate

#### Cards / panels
- White cards on light backgrounds
- Use subtle neutral borders or spacing rather than heavy decoration

#### Forms
- Use brand color in focus rings and active elements while preserving WCAG compliance

#### Tables
- Use brand color for selected rows, headers, or accents only where it improves comprehension

#### Charts
- Prefer primary palette first; secondary colors may extend chart differentiation
- Maintain enough contrast between series

### Critical Accessibility Notes

- **Orange `#EF7D00` on white fails AA for normal text** — restrict to large text, icons, or decorative use
- **Mid grey `#A8A8A7` on white fails AA** — do not use for body text or labels
- On gradient backgrounds, measure contrast at the lightest point
- Focus rings:
  - Light backgrounds: `2px solid #4D1D82`
  - Dark backgrounds: `2px solid #FFFFFF` or `2px solid #EF7D00`
  - Focus ring must have at least 3:1 contrast against adjacent background
- Never use `outline: none` without a visible replacement
- Skip-to-content link must be present
- Branded modals must trap focus and restore it on close
- Icon-only buttons need `aria-label`
- Brand logo must have `alt="Sopra Steria"` (or `alt="Sopra Steria - Home"` when linked)
- Decorative brand imagery must use `alt=""`
- Respect `prefers-reduced-motion: reduce`

---

## Deliverable Format

When responding to app branding requests, provide:

1. Audit summary of current state
2. Token map (old → new)
3. Component refactor plan
4. Sample CSS / design token object / theme config
5. Risk notes (e.g., missing brand font, no official logo asset at runtime)
