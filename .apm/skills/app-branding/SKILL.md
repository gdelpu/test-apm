---
name: app-branding
description: 'Adapt applications, websites, portals, design systems, and front-end codebases to a target brand identity while preserving usability and accessibility. Generic skill — extend with client-specific brand rules.'
triggers: ['app branding', 'application theming', 'UI branding', 'design tokens', 'theme refactor', 'CSS branding', 'application styling']
version: '1.0.0'
---

# Skill: App Branding

## Purpose

Adapt applications, websites, portals, design systems, and front-end codebases to a target brand identity while preserving usability and accessibility. This is the generic, client-agnostic skill. For Sopra Steria specifics, see `soprasteria-app-branding`.

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

- **Header / navigation** — restrained base, proper logo placement
- **Buttons** — primary, secondary, danger variants with accessible contrast
- **Cards / panels** — white cards, subtle borders, reserve gradients for featured cards
- **Forms** — readable labels, branded focus rings with WCAG compliance
- **Tables** — mostly neutral; brand color for accents where it improves comprehension
- **Alerts / status** — do not force brand colors onto semantic status colors when it harms usability
- **Charts** — primary palette first, secondary to extend differentiation, always maintain contrast

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

Use the `web-accessibility` skill (or client-specific variant) for the full checklist.

## Deliverable Format

When responding to app branding requests, provide:

1. Audit summary of current state
2. Token map (old → new)
3. Component refactor plan
4. Sample CSS / design token object / theme config
5. Risk notes (e.g., missing brand font, no official logo asset at runtime)
