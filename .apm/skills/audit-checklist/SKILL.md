---
name: audit-checklist
description: 'Generic structured checklist for auditing applications, documents, presentations, and communication assets against brand guidelines and accessibility standards. Extend with client-specific brand skills for concrete rules.'
triggers: ['brand audit', 'branding checklist', 'compliance check', 'brand review', 'audit checklist', 'brand compliance']
version: '1.0.0'
---

# Skill: Audit Checklist

## Purpose

Provide a generic, reusable audit checklist for assessing brand and accessibility compliance of applications, slide decks, documents, and communication assets. This is the provider-agnostic skill; for Sopra Steria specifics, see `soprasteria-audit-checklist`.

## When to Use

- Auditing any deliverable for brand consistency
- Reviewing applications, presentations, or documents before delivery
- Pre-flight checks on visual assets

## Checklist Sections

### A. Logo

- Is an official logo file used (not a screenshot or recreation)?
- Is the correct logo version used for the background context?
- Is clear space / protection area respected?
- Is minimum size respected?
- Any unauthorized modifications (skewing, recoloring, effects)?
- Is the company name written correctly in body text?

### B. Colors

- Is the primary palette dominant?
- Are secondary colors used only as support / accents?
- Is white / negative space sufficiently present?
- Are brand gradients used appropriately (not excessively)?
- Are there unapproved colors dominating the composition?

### C. Typography

- Is the designated brand font used for headings?
- Is the designated body font used for running text?
- Is typographic hierarchy clear and consistent?
- Are alignments consistent with guideline intent?
- Are line lengths comfortable (~55–65 characters)?

### D. Icons and Illustrations

- Are approved icon styles used?
- Is icon weight and style consistent across the asset?
- Are color patches / accents within the approved style?

### E. Layout / Composition

- Does the cover follow the brand's layout logic?
- Are title zones proportionate?
- Is the grid coherent?
- Does the visual feel match the brand personality (light, clear, energising vs. cluttered)?

### F. Accessibility

- Is text/background contrast sufficient (4.5:1 normal, 3:1 large)?
- Is color the sole carrier of meaning anywhere?
- Are text overlays on gradients/images readable?
- Are charts, labels, and statuses accessible?

### F+. Web Accessibility (web applications only)

Activate this section when the audit target is a web application. Use the `web-accessibility` skill (or its client-specific variant) for detailed checks covering:

- Contrast validation
- Keyboard navigation
- ARIA and semantic HTML
- Motion preferences

### G. Templates and Official Assets

- Was an official template available but ignored?
- Was an official asset available but replaced by a manual imitation?
- Is the correct template family used for the artifact type?

## Output Format

Return findings in four buckets:

1. **Compliant** — meets requirements
2. **Needs correction** — mandatory fix
3. **Needs confirmation** — requires stakeholder input
4. **Not allowed** — violates brand rules

Then provide a prioritized remediation sequence:

1. Mandatory fixes
2. Recommended improvements
3. Optional polish
