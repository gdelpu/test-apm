---
name: soprasteria-brand-refactor
description: 'Refactor an application, document, presentation, or template into Sopra Steria brand style with audit, strategy, implementation, and validation.'
---

# Sopra Steria brand refactor

Refactor the provided application, document, presentation, or template into Sopra Steria brand style.

## Required behavior
1. Audit the current state briefly.
2. Propose the refactor strategy.
3. Implement the changes.
4. End with a validation checklist.

## Refactor priorities
- Use official assets and templates when available.
- Create or update reusable brand tokens first.
- Prioritize primary palette and accessibility.
- Preserve readability and clean hierarchy.
- Keep gradients controlled and premium.
- Preserve content meaning while upgrading presentation.

## Deliverable expectations by medium
### If the input is an application
- create/update a reusable theme system
- refactor shared components first
- normalize headers, navigation, cards, forms, buttons, tables, charts, dialogs, and empty states
- validate WCAG 2.1 AA compliance using the soprasteria-web-accessibility skill
- verify color contrast for all brand pairings (especially orange and grey on white)
- ensure focus indicators are visible on all brand backgrounds
- verify keyboard navigation, ARIA usage, semantic HTML, and motion preferences
- document logo/background rules and accessibility constraints

### If the input is a PowerPoint
- align slides to official cover/title/content logic
- simplify layouts
- replace non-brand colors/icons/images
- standardize title, subtitle, section divider, and closing slides

### If the input is a Word document
- reapply proper styles
- clean cover page
- improve headings, spacing, tables, callouts, and image placement
- ensure Office-friendly fonts where needed

### If the input is mixed assets
- produce a reusable style guide section first
- then apply it consistently across artifacts

## Mandatory output format
### Refactor summary
### Files changed
### Key branding decisions
### Accessibility compliance (web applications)
For web targets, include:
- contrast validation results for brand color pairings
- keyboard and focus audit results
- ARIA and semantic HTML findings
- motion preference compliance
- critical issues vs warnings
- brand-specific accessibility tensions and resolutions
### Accessibility checks (all targets)
### Remaining manual review items
