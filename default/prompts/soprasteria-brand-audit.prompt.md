# Sopra Steria brand audit

Assess the provided application, document, slide deck, page, mockup, or codebase against Sopra Steria branding.

## Objectives
- Determine the current level of Sopra Steria brand compliance.
- Identify gaps in logo use, colors, typography, layout, imagery, iconography, and accessibility.
- Recommend the smallest viable set of changes to reach strong brand alignment.

## What to inspect
1. Logo usage and placement
2. Color palette and gradient usage
3. Typography choices and hierarchy
4. Layout grid, spacing, and white-space behavior
5. Images and iconography
6. Office-template compliance for Word/PPT if relevant
7. Accessibility and contrast
8. Naming/casing consistency for Sopra Steria
9. **Web accessibility (WCAG 2.1 AA)** — when the target is a web application, use the soprasteria-web-accessibility skill to validate:
   - color contrast for all brand pairings
   - keyboard navigation and focus visibility
   - ARIA usage on branded custom components
   - semantic HTML structure
   - motion/animation preferences
   - stack-specific checks (Vue, React, Angular, Blazor)

## Output format
### 1. Executive summary
- medium
- overall compliance score /100
- key strengths
- key issues

### 2. Detailed findings
Use a table with:
- category
- status: compliant / partial / non-compliant
- evidence
- impact
- recommended fix

### 3. Prioritized remediation plan
Group fixes into:
- quick wins
- structural fixes
- asset dependencies

### 4. Accessibility section (web applications only)
Include when auditing web apps, websites, or dashboards:

| Category | Status | Issues |
|---|---|---|
| Color contrast | pass / partial / fail | count |
| Keyboard navigation | pass / partial / fail | count |
| ARIA usage | pass / partial / fail | count |
| Semantic HTML | pass / partial / fail | count |
| Motion preferences | pass / partial / fail | count |
| Focus management | pass / partial / fail | count |

List critical a11y issues, warnings, and brand-specific accessibility tensions.

### 5. If code is present
Identify:
- theme/token files to create or change
- components to refactor
- CSS/SCSS/Tailwind areas to update
- accessibility fixes required
- screenshots or states that still need manual review
