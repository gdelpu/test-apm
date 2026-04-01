---
name: soprasteria-audit-checklist
description: 'Structured checklist for auditing apps, slide decks, documents, and communication assets against Sopra Steria brand and accessibility standards.'
triggers: ['brand audit', 'branding checklist', 'compliance check', 'brand review', 'audit checklist']
---

# Skill: Sopra Steria Audit Checklist

Use this checklist whenever auditing an app, slide deck, document, or communication asset.

## A. Logo
- Is an official logo file used?
- Is the correct logo version used for the background?
- Is clear space respected?
- Is minimum size respected?
- Any skewing, recoloring, effects, or swirl manipulation?
- Is “Sopra Steria” written correctly in body text?

## B. Colors
- Is the primary palette dominant?
- Are secondary colors used only as support?
- Is white sufficiently present?
- Is the brand gradient used appropriately rather than excessively?
- Are there non-approved colors that dominate the composition?

## C. Typography
- Is Hurme Geometric Sans used where appropriate?
- Is Tahoma used for office body text when relevant?
- Is hierarchy clear?
- Are alignments consistent with guideline intent?
- Are lines too long, too dense, or too tight?

## D. Icons and illustrations
- Are approved icon styles used?
- Are icons outline-based and simple?
- Are color patches in the approved style?
- Is icon weight consistent across the asset?

## E. Layout / composition
- Does the cover follow vertical or horizontal layout logic?
- Are title zones proportionate?
- Is the grid coherent?
- Is the visual feel light, clear, and energising rather than cluttered?
- Are the five key ingredients present where relevant?

## F. Accessibility (all targets)
- Is text/background contrast sufficient (4.5:1 normal, 3:1 large)?
- Is color the only carrier of meaning anywhere?
- Are text overlays on gradients/images readable?
- Are charts, labels, and statuses accessible?

## F+ . Web Accessibility (web applications only)
Activate this section when the audit target is a web application, website, portal, or dashboard.
Use the **soprasteria-web-accessibility** skill for detailed checks.

### Contrast
- Do all brand color/text pairings meet WCAG 2.1 AA contrast ratios?
- Is orange `#EF7D00` used only for large text, icons, or decoration — never as normal text on white?
- Is mid grey `#A8A8A7` excluded from body text and labels?
- On branded gradients, is contrast verified at the lightest gradient point?

### Keyboard
- Can all interactive elements be reached and operated via keyboard?
- Are focus indicators visible on every brand background (light and dark)?
- Is there a skip-to-content link?
- Do branded modals and drawers trap and restore focus correctly?
- Are there any keyboard traps?

### ARIA and semantics
- Do icon-only branded buttons have `aria-label`?
- Do branded navigation, header, main, and footer areas use landmark elements?
- Do branded alerts and notifications use `aria-live` regions?
- Does the heading hierarchy follow h1–h6 without skipping levels?
- Do branded form fields associate labels correctly?
- Does the brand logo image have appropriate `alt` text?

### Motion
- Do branded animations respect `prefers-reduced-motion`?
- Can carousels and auto-playing content be paused?

### Component-level
- Do branded tabs, accordions, modals, and tooltips follow ARIA authoring patterns?
- Do branded data tables use proper `<th>`, scope, and caption?

## G. Templates and official assets
- Was an official template available but ignored?
- Was an official asset available but replaced by a manual imitation?
- Is the correct template family used for the artifact type?

## Output format
Return findings in four buckets:
- Compliant
- Needs correction
- Needs confirmation
- Not allowed

Then provide a prioritized remediation sequence:
1. mandatory fixes
2. recommended improvements
3. optional polish
