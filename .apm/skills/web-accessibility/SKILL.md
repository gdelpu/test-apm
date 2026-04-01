---
name: web-accessibility
description: 'Validate web applications against WCAG 2.1 AA covering contrast, keyboard navigation, ARIA, semantic HTML, and motion preferences. Generic skill — extend with client-specific brand color contrast tables.'
triggers: ['web accessibility', 'WCAG', 'contrast check', 'keyboard navigation', 'ARIA audit', 'a11y', 'accessibility validation']
version: '1.0.0'
---

# Skill: Web Accessibility

## Purpose

Validate web applications against WCAG 2.1 AA when applying or auditing branding. Brand compliance must never compromise accessibility. When brand rules and accessibility conflict, **accessibility wins**. This is the generic, client-agnostic skill. For Sopra Steria specifics, see `soprasteria-web-accessibility`.

## When to Activate

Use this skill whenever the target is a web application, website, portal, dashboard, or front-end codebase. Skip for documents, presentations, and print assets — those have simpler contrast/readability checks handled by the `audit-checklist` skill.

## WCAG 2.1 AA Core Principles

- **Perceivable** — content must be presentable in ways all users can perceive
- **Operable** — UI components and navigation must be operable by all users
- **Understandable** — information and UI operation must be understandable
- **Robust** — content must be robust enough for assistive technologies

## Priority Criteria for Branding Work

| WCAG Criterion | ID | Branding Relevance |
|---|---|---|
| Contrast (Minimum) | 1.4.3 | Direct — brand colors must meet 4.5:1 normal, 3:1 large |
| Non-text Contrast | 1.4.11 | Direct — UI components need 3:1 against adjacent colors |
| Use of Color | 1.4.1 | Direct — brand colors alone must not carry meaning |
| Focus Visible | 2.4.7 | Indirect — focus rings visible on brand backgrounds |
| Resize Text | 1.4.4 | Indirect — brand typography must support 200% zoom |
| Images of Text | 1.4.5 | Direct — use real text with brand fonts, not images |
| Info and Relationships | 1.3.1 | Indirect — heading hierarchy must use semantic HTML |
| Meaningful Sequence | 1.3.2 | Indirect — branded grid layouts preserve logical order |
| Keyboard | 2.1.1 | Indirect — all interactive elements keyboard accessible |
| Timing Adjustable | 2.2.1 | Indirect — branded animations must be pausable |
| Three Flashes | 2.3.1 | Indirect — no flashing more than 3 times/second |
| Name, Role, Value | 4.1.2 | Indirect — custom components expose correct ARIA |

## Color Contrast Validation

For every brand color used in the application:

1. Test all foreground/background pairings against WCAG thresholds
2. Check normal text (4.5:1), large text (3:1), and UI components (3:1)
3. On gradient backgrounds, verify contrast at the lightest point
4. Document which brand colors fail and recommended alternatives

## Keyboard Navigation Audit

- Tab order follows visual layout in logical sequence
- Focus indicators visible against all brand backgrounds
- No keyboard traps in modals, drawers, or popovers
- Skip-to-content link present and functional
- Dropdown menus, accordions, and tabs support arrow-key navigation

### Focus Ring Guidance

- Default focus ring on light backgrounds: `2px solid <primary-brand-color>`
- On dark backgrounds: `2px solid #FFFFFF` or bright accent
- Focus ring must have at least 3:1 contrast against adjacent background
- Never use `outline: none` without a visible replacement

## ARIA Usage Audit

- Icon-only buttons have `aria-label` or `aria-labelledby`
- Navigation landmarks use `<nav>`, `<main>`, `<header>`, `<footer>`
- Alert/status components use `role="alert"` or `aria-live`
- Tab panels use `role="tablist"`, `role="tab"`, `role="tabpanel"`
- Modals use `role="dialog"` with `aria-modal="true"` and focus management
- Expandable sections use `aria-expanded`
- Decorative brand icons use `aria-hidden="true"`

## Semantic HTML Audit

- Headings follow h1–h6 hierarchy without skipping levels
- Lists use `<ul>`, `<ol>`, `<dl>` — not styled `<div>` sequences
- Tables use `<table>`, `<th>`, `<caption>` — not CSS grid faking tabular data
- Forms use `<label>` elements properly associated via `for`/`id`
- Brand logo includes meaningful `alt` text; decorative imagery uses `alt=""`

## Motion and Animation Preferences

- Honor `prefers-reduced-motion: reduce`
- Branded carousels or rotating content must have pause/stop controls
- No auto-playing video or animation that cannot be paused
- Loading spinners acceptable but keep duration and motion minimal

## Stack-Specific Checks

### Vue.js (Vuetify, Quasar, custom)

- `v-btn` icon-only components have accessible labels
- `v-dialog` manages focus correctly on open/close
- `v-data-table` headers use proper scope attributes
- Router transitions respect `prefers-reduced-motion`

### React (MUI, Chakra, custom)

- `IconButton` components have `aria-label`
- `Dialog` / `Modal` manages focus trap
- `Tabs` use proper ARIA tab pattern
- `Snackbar` / `Alert` have live region behavior

### Angular (Angular Material, PrimeNG, custom)

- `mat-icon-button` has `aria-label`
- `mat-dialog` focus management works correctly
- `cdkTrapFocus` is used in branded overlays

### .NET (Blazor / Razor)

- Branded Blazor components render semantic HTML
- `EditForm` validation errors associate via `aria-describedby`
- Layouts include skip navigation and landmark roles

## Accessibility Report Format

| Category | Status | Issues |
|---|---|---|
| Color contrast | pass / partial / fail | count |
| Keyboard navigation | pass / partial / fail | count |
| ARIA usage | pass / partial / fail | count |
| Semantic HTML | pass / partial / fail | count |
| Motion preferences | pass / partial / fail | count |
| Focus management | pass / partial / fail | count |

### Non-negotiables

- Never approve a brand refactor that introduces contrast failures
- Never remove or hide focus indicators for a "cleaner" look
- Never use `outline: none` without a visible alternative
- Never rely solely on color to communicate state
- Always include the accessibility section in web application audit reports
