---
name: brand-accessibility
description: 'Validate web applications against WCAG 2.1 AA when applying or auditing branding. Covers contrast, keyboard navigation, ARIA, semantic HTML, and motion preferences. Default brand: Sopra Steria.'
triggers: ['web accessibility', 'WCAG', 'contrast check', 'keyboard navigation', 'ARIA audit', 'a11y']
version: '2.0.0'
---

# Skill: Brand Accessibility

## Purpose

Validate web applications against WCAG 2.1 AA when applying or auditing branding.
Brand compliance must never compromise accessibility. When brand rules and accessibility conflict, accessibility wins.

Default contrast values are for Sopra Steria. To override for a different client, provide brand-specific contrast pairs in `.apm/knowledge/brand/<client>/`.

---

## When to Activate

Use this skill whenever the branding target is a web application, website, portal, dashboard, or front-end codebase.
Skip this skill for documents, presentations, and print assets — those have simpler contrast/readability checks handled by the `brand-audit` skill.

---

## WCAG 2.1 AA Compliance Audit

Validate all UI surfaces against WCAG 2.1 Level AA success criteria.

Key principles:
- **Perceivable** — content must be presentable in ways all users can perceive
- **Operable** — UI components and navigation must be operable by all users
- **Understandable** — information and UI operation must be understandable
- **Robust** — content must be robust enough for assistive technologies

Priority criteria for branding work:

| WCAG Criterion | ID | Branding relevance |
|---|---|---|
| Contrast (Minimum) | 1.4.3 | Direct — brand colors must meet 4.5:1 for normal text, 3:1 for large text |
| Non-text Contrast | 1.4.11 | Direct — UI components and graphical objects need 3:1 against adjacent colors |
| Use of Color | 1.4.1 | Direct — brand colors alone must not carry meaning |
| Focus Visible | 2.4.7 | Indirect — focus rings must be visible on brand-colored backgrounds |
| Resize Text | 1.4.4 | Indirect — brand typography must support 200% zoom without loss |
| Images of Text | 1.4.5 | Direct — avoid using brand text as images; use real text with brand fonts |
| Info and Relationships | 1.3.1 | Indirect — heading hierarchy in branded layouts must use semantic HTML |
| Meaningful Sequence | 1.3.2 | Indirect — branded grid layouts must preserve logical reading order |
| Keyboard | 2.1.1 | Indirect — all branded interactive elements must be keyboard accessible |
| Timing Adjustable | 2.2.1 | Indirect — branded animations/carousels must be pausable |
| Three Flashes | 2.3.1 | Indirect — branded animations must not flash more than 3 times/second |
| Page Titled | 2.4.2 | Indirect — branded page titles must be descriptive |
| Link Purpose | 2.4.4 | Indirect — branded link styles must pair with meaningful text |
| Language of Page | 3.1.1 | Indirect — branded pages must declare language |
| Name, Role, Value | 4.1.2 | Indirect — custom branded components must expose correct ARIA |

---

## Color Contrast Validation

Verify that all brand color/text pairings meet WCAG 2.1 AA contrast ratios.

Rules:
- On gradient backgrounds, verify contrast at the lightest point of the gradient, not the darkest.
- Deep purple and red are generally safe as primary interactive/text colors on white.

### Default Brand Contrast Matrix: Sopra Steria

| Foreground | Background | Ratio | Pass AA normal? | Pass AA large? |
|---|---|---|---|---|
| `#FFFFFF` white text | `#4D1D82` deep purple | 10.3:1 | YES | YES |
| `#FFFFFF` white text | `#8B1D82` purple | 6.2:1 | YES | YES |
| `#FFFFFF` white text | `#CF022B` red | 5.6:1 | YES | YES |
| `#FFFFFF` white text | `#EF7D00` orange | 2.9:1 | NO | YES (large only) |
| `#1D1D1B` off-black text | `#FFFFFF` white | 18.6:1 | YES | YES |
| `#1D1D1B` off-black text | `#EDEDED` light grey | 12.5:1 | YES | YES |
| `#4D1D82` deep purple text | `#FFFFFF` white | 10.3:1 | YES | YES |
| `#A8A8A7` mid grey text | `#FFFFFF` white | 2.7:1 | NO | NO |

- **Orange `#EF7D00` fails AA for normal white text.** Use it only for large text, icons, or decorative accents.
- **Mid grey `#A8A8A7` fails AA on white.** Do not use for body text or labels. Acceptable for decorative borders only.

---

## Keyboard Navigation Audit

Verify that all brand-themed interactive elements work via keyboard:

- Tab order follows the visual brand layout in logical sequence
- Focus indicators are visible against brand backgrounds (deep purple focus ring on white, white focus ring on dark backgrounds)
- No keyboard traps in branded modals, drawers, or popovers
- Skip-to-content link is present and functional on branded layouts
- Branded dropdown menus, accordions, and tabs support arrow-key navigation
- Escape closes branded modals and overlays

Focus ring guidance:
- Default focus ring: `2px solid #4D1D82` on light backgrounds
- On dark/purple backgrounds: `2px solid #FFFFFF` or `2px solid #EF7D00`
- Focus ring must have at least 3:1 contrast against the adjacent background

---

## ARIA Usage Audit

Check that branded custom components expose proper semantics:

- Branded icon-only buttons have `aria-label` or `aria-labelledby`
- Branded navigation landmarks use `<nav>`, `<main>`, `<header>`, `<footer>`
- Branded alert/status components use `role="alert"` or `role="status"` with `aria-live`
- Branded tab panels use `role="tablist"`, `role="tab"`, `role="tabpanel"`
- Branded modals use `role="dialog"` with `aria-modal="true"` and proper focus management
- Branded tooltips use `role="tooltip"` with `aria-describedby`
- Branded expandable sections use `aria-expanded`
- Decorative brand icons use `aria-hidden="true"`

---

## Semantic HTML Audit

Branding must not break semantic structure:

- Branded headings follow h1–h6 hierarchy without skipping levels
- Branded lists use `<ul>`, `<ol>`, `<dl>` — not styled `<div>` sequences
- Branded tables use `<table>`, `<th>`, `<caption>` — not CSS grid faking tabular data
- Branded forms use `<label>` elements properly associated via `for`/`id`
- Branded images have meaningful `alt` text (decorative brand imagery uses `alt=""`)
- Main brand logo image includes appropriate `alt` text (e.g., `alt="Sopra Steria"` or `alt="Sopra Steria - Home"` when it links to home)

---

## Motion and Animation Preferences

Branded animations must respect user preferences:

- Honor `prefers-reduced-motion: reduce` — disable or simplify branded transitions, gradient animations, hero animations, scroll effects
- Branded carousels or rotating content must have pause/stop controls
- No auto-playing branded video or animation that cannot be paused
- Branded loading spinners are acceptable but keep duration and motion minimal

---

## Stack-Specific Checks

### Vue.js (Vuetify, Quasar, custom)

- Verify `v-btn` components have accessible labels when icon-only
- Check that `v-dialog` manages focus correctly on open/close
- Ensure `v-data-table` headers use proper scope attributes
- Verify `v-navigation-drawer` is keyboard-navigable
- Check that `v-snackbar` / `v-alert` use proper ARIA live regions
- Ensure branded router transitions respect `prefers-reduced-motion`

### React (MUI, Chakra, custom)

- Verify `IconButton` components have `aria-label`
- Check that `Dialog` / `Modal` manages focus trap
- Ensure `Tabs` use proper ARIA tab pattern
- Verify custom branded hooks don't bypass keyboard handlers
- Check `Snackbar` / `Alert` live region behavior

### Angular (Angular Material, PrimeNG, custom)

- Verify `mat-icon-button` has `aria-label`
- Check `mat-dialog` focus management
- Verify `mat-tab-group` keyboard support
- Ensure `cdkTrapFocus` is used in branded overlays

### .NET (Blazor / Razor)

- Verify branded Blazor components render semantic HTML
- Check that `EditForm` validation errors associate with fields via `aria-describedby`
- Ensure branded Razor layouts include skip navigation and landmark roles

---

## Accessibility Report Format

When auditing a web application, include this accessibility section in the brand audit report:

### Accessibility compliance summary

| Category | Status | Issues |
|---|---|---|
| Color contrast | pass / partial / fail | count |
| Keyboard navigation | pass / partial / fail | count |
| ARIA usage | pass / partial / fail | count |
| Semantic HTML | pass / partial / fail | count |
| Motion preferences | pass / partial / fail | count |
| Focus management | pass / partial / fail | count |

### Critical accessibility issues
List items that block WCAG 2.1 AA compliance.

### Accessibility warnings
List items that are non-blocking but should be addressed.

### Brand-specific accessibility notes
List cases where brand choices create accessibility tension and the recommended resolution.

---

## Non-negotiables

- Never approve a brand refactor that introduces contrast failures.
- Never use brand orange `#EF7D00` for normal-sized text on white.
- Never use mid grey `#A8A8A7` for readable text on white.
- Never remove or hide focus indicators to achieve a "cleaner" branded look.
- Never use `outline: none` without a visible alternative focus style.
- Never rely solely on brand color to communicate state (error, success, selected, disabled).
- Always include the accessibility section in web application audit reports.
