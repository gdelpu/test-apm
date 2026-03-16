---
name: soprasteria-app-branding
description: 'Adapt applications, websites, portals, design systems, and front-end codebases to Sopra Steria branding while preserving usability and accessibility.'
triggers: ['app branding', 'application theming', 'UI branding', 'design tokens', 'theme refactor', 'CSS branding']
---

# Skill: Sopra Steria App Branding

## Purpose
Use this skill to adapt applications, websites, portals, design systems, and front-end codebases to Sopra Steria branding while preserving usability and accessibility.

## Main principle
Branding an application is not the same as turning it into a brochure.
The result should feel unmistakably Sopra Steria, but still usable, maintainable, and accessible.

## Refactor order

### 1) Inventory the existing theme
Capture:
- current color tokens
- typography stack
- icon library
- logo placement
- header / footer patterns
- button styles
- chart colors
- empty states / alerts / badges
- dark mode behavior if any

### 2) Replace with Sopra Steria-compatible structure

#### Theme tokens to introduce
At minimum define tokens for:
- `brand-primary-900: #4D1D82`
- `brand-primary-700: #8B1D82`
- `brand-accent-red: #CF022B`
- `brand-accent-orange: #EF7D00`
- `brand-neutral-900: #1D1D1B`
- `brand-neutral-600: #A8A8A7`
- `brand-neutral-200: #EDEDED`
- `brand-neutral-0: #FFFFFF`
- optional secondary highlights from approved secondary palette

#### Typography mapping
- Preferred brand font: Hurme Geometric Sans 3
- Headings: Hurme Geometric Sans 4 when feasible
- Practical fallback for enterprise apps when official font is unavailable: Tahoma or system sans-serif
- Never claim full brand compliance if Hurme is not actually available in the runtime environment

#### Visual system rules
- Use white generously as the base canvas.
- Keep the interface clean and uncluttered.
- Use purple as the structural brand anchor.
- Use red/orange as selective emphasis, not as permanent visual noise.
- Use gradients deliberately in hero zones, banners, title areas, splash states, or branded intro screens — not everywhere.

### 3) Component adaptation guidance

#### Header / top navigation
- Use restrained white or dark-purple base.
- Place official logo with proper clear space.
- Avoid oversized gradients behind navigation unless it is a branded landing area.

#### Buttons
- Primary buttons: dark purple base with accessible contrast.
- Secondary buttons: outline or light variants using neutral system.
- Danger / destructive states can use red if semantically appropriate.
- Avoid using orange or pink as generic primary actions.

#### Cards / panels
- White cards on light backgrounds.
- Use subtle neutral borders or spacing rather than heavy decoration.
- Reserve gradient treatment for featured cards or branded highlight panels.

#### Forms
- Prioritize readability and focus states.
- Keep labels and helper text neutral and high-contrast.
- Use brand color in focus rings and active elements while preserving WCAG compliance.

#### Tables
- Keep tables mostly neutral.
- Use brand color for selected rows, headers, or accents only where it improves comprehension.

#### Alerts / status
- Do not force brand colors onto semantic status colors when that harms usability.
- Brand should frame the experience, not erase product semantics.

#### Charts
- Prefer primary palette first.
- Secondary colors may extend chart differentiation.
- Maintain enough contrast between series.
- Add labels or patterns when color alone would be ambiguous.

### 4) Logo handling inside apps
- Use official PNG/SVG logo assets only.
- Default placement: header, sign-in page, branded splash, about page, exported reports.
- Never stretch or recolor the logo.
- Respect minimum sizes and whitespace.

### 5) Accessibility validation (WCAG 2.1 AA)

Accessibility must be verified after every branding change. Use the **soprasteria-web-accessibility** skill for the full checklist.

#### Contrast
- Verify all brand color pairings meet WCAG 2.1 AA (4.5:1 normal text, 3:1 large text, 3:1 UI components).
- Orange `#EF7D00` on white fails AA for normal text — restrict to large text, icons, or decorative use.
- Mid grey `#A8A8A7` on white fails AA — do not use for body text or labels.
- On gradient backgrounds, measure contrast at the lightest point.

#### Keyboard and focus
- Ensure all interactive elements are reachable via Tab/Shift+Tab and operable via Enter/Space.
- Focus rings must be visible on all brand backgrounds:
  - Light backgrounds: `2px solid #4D1D82`
  - Dark backgrounds: `2px solid #FFFFFF` or `2px solid #EF7D00`
- Focus ring must have at least 3:1 contrast against adjacent background.
- Never use `outline: none` without a visible replacement.
- Skip-to-content link must be present.
- Branded modals must trap focus and restore it on close.

#### ARIA and semantics
- Icon-only buttons need `aria-label`.
- Navigation, header, main, footer must use landmark elements.
- Branded alerts use `role="alert"` or `aria-live`.
- Heading hierarchy must follow h1–h6 without skipping.
- Brand logo must have `alt="Sopra Steria"` (or `alt="Sopra Steria - Home"` when linked).
- Decorative brand imagery must use `alt=""`.

#### Motion
- Respect `prefers-reduced-motion: reduce`.
- Branded carousels and auto-play content must be pausable.

#### Semantic color usage
- Never rely on brand color alone to communicate state (error, success, selected, disabled).
- Pair color with text labels, icons, or patterns.

## Deliverable format for app requests
When responding, provide:
1. audit summary
2. token map
3. component refactor plan
4. sample CSS / design token object / theme config
5. risk notes (e.g. missing brand font, no official logo asset in runtime)
