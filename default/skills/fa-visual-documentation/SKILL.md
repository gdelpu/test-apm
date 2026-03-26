---
name: fa-visual-documentation
description: 'Tri-format diagram generation (Mermaid source, Markdown with embedded diagrams, SVG exports), interactive HTML presentations with branding, and automated screenshot tours via Playwright for functional analysis visual deliverables.'
triggers: ['create diagram', 'tri-format', 'mermaid diagram', 'SVG export', 'HTML presentation', 'screenshot tour', 'visual documentation', 'stakeholder map', 'process flow', 'context diagram', 'generate SVG']
version: '1.0.0'
author: 'soprasteria'
---

# Skill: FA Visual Documentation

## Purpose

Produces all visual deliverables for functional analysis projects: tri-format diagrams (Mermaid, Markdown, SVG), interactive HTML presentations for meetings and reviews, and automated screenshot tours for current state analysis.

## When to Apply

Use this skill when:
- Creating any diagram (process flow, stakeholder map, context diagram, etc.)
- Generating SVG exports from Mermaid sources
- Building interactive HTML presentations for meetings
- Capturing screenshot tours of existing systems
- Producing visual assets for stakeholder communication

---

## Tri-Format Diagram Standard

Every diagram MUST be created in THREE formats. No exceptions.

### Format 1: Mermaid Source (`.mmd`)

Location: `Projects/[project]/diagrams/mermaid-source/[name].mmd`
Purpose: Version control, editing, source of truth.
Content: Pure Mermaid syntax only.

### Format 2: Markdown with Embedded Mermaid (`.md`)

Location: `Projects/[project]/diagrams/[name].md`
Purpose: Viewing in editors (VS Code, Cursor, GitHub).
Content: Title, description, Mermaid code fence, legend/key.

### Format 3: SVG Export (`.svg`)

Location: `Projects/[project]/diagrams/svg-exports/[name].svg`
Purpose: Presentations, Word/PDF documents, stakeholder-ready output.
Generation: `bash diagrams/generate-svg.sh` or `npx mmdc -i source.mmd -o output.svg`

### Why Tri-Format

- `.mmd` — Easy to edit and version-control
- `.md` — View directly in editors without conversion
- `.svg` — Professional, scalable, embeddable in any document

### Common Diagram Types

| Type | Mermaid Syntax | Use Case |
|------|---------------|----------|
| Context Diagram | `graph TD` | System boundaries and external actors |
| Stakeholder Map | `graph TD` | Stakeholder relationships and influence |
| Process Flow | `flowchart LR` or `graph LR` | Current/future state processes |
| State Diagram | `stateDiagram-v2` | Entity lifecycle states |
| Use Case | `graph TD` | Actor-system interactions |
| Data Model | `erDiagram` | Entity relationships |
| Journey Map | `journey` | User experience across touchpoints |
| Sequence | `sequenceDiagram` | Interaction sequences |
| Ecosystem Map | `graph TD` | System landscape |
| Gantt | `gantt` | Timeline and milestones |

### Example: Creating a Stakeholder Map

1. Create: `diagrams/mermaid-source/stakeholder-map.mmd`
2. Create: `diagrams/stakeholder-map.md` (with embedded mermaid code fence)
3. Generate: `diagrams/svg-exports/stakeholder-map.svg`

### Diagram Quality Checklist

- Source file (.mmd) exists
- Markdown with embedded Mermaid exists
- SVG export generated
- Legend or key included
- Stakeholder-friendly labels (no technical jargon)
- Consistent styling across project diagrams

### Batch SVG Generation

```bash
cd Projects/[project]/diagrams/
bash generate-svg.sh
```

This converts all `.mmd` files in `mermaid-source/` to `.svg` in `svg-exports/`.

---

## HTML Presentations

### When to Use

- Requirements review meetings (interactive card review with comments)
- Status meetings (visual dashboards and progress)
- Stakeholder presentations (professional branded output)
- Workshop facilitation (interactive exercises)

### Generation Workflow

1. User requests: "Create HTML presentation for [meeting type] about [topic]"
2. Identify source markdown files (requirements, stories, discovery notes)
3. Select template based on meeting type
4. Extract and structure content (IDs, titles, priorities, AC)
5. Generate self-contained HTML file
6. Output to: `Projects/[project]/deliverables/.../FA/communication/[name].html`

### Presentation Types

| Meeting Type | Key Features | Source Files |
|-------------|-------------|-------------|
| Requirements Review | Cards with modals, comment capture, review checkboxes | Requirements markdown |
| Status Meeting | Dashboard cards, progress indicators, metrics | Project overview |
| Stakeholder Presentation | Branded slides, key findings, executive view | Executive summary |
| Workshop | Interactive exercises, voting, collaborative input | Discovery notes |

### Required HTML Components

1. **Header** — Logo, project name, title, date, version
2. **Statistics Dashboard** — Key metrics, visual cards, progress indicators
3. **Content Sections** — Organised by category, interactive cards, expandable details
4. **Interactive Features** — Modals for detail views, comment/note capture, review checkboxes
5. **Export/Reset** — Export meeting notes as text, reset review data
6. **Footer** — Branding, version information

### Interactive Features

- **Modal windows** for detailed item views
- **Local storage** for review notes and comments (persists across sessions)
- **Export functionality** to download meeting notes as plain text
- **Priority badges** for visual categorisation
- **Filters** for sorting and filtering content

### Branding

For branded HTML presentations, use the colour palette and typography from the existing `soprasteria-brand-*` skills. Key CSS variables:

```
--ss-primary, --ss-purple, --ss-red, --ss-orange, --ss-black
Font: Segoe UI, system-ui, sans-serif
```

### Naming Convention

- `requirements-overview-presentation.html`
- `status-meeting-[dd-mm-YYYY].html`
- `stakeholder-presentation-v[X.Y.Z].html`

---

## Screenshot Tours

### Purpose

Automated visual documentation of existing systems for current state analysis, stakeholder review, testing baselines, and visual guides.

### Prerequisites

```bash
npm install playwright @playwright/test sharp canvas fs-extra
npx playwright install chromium
```

### Capture Types

| Type | Use Case | Output |
|------|----------|--------|
| Full Page | Complete page documentation | PNG (high-res) |
| Viewport | Above-the-fold content | PNG (1920x1080) |
| Element | Specific component focus | PNG (cropped) |
| Sequence | Multi-step user flow | Numbered PNGs |
| Comparative | Before/after changes | Side-by-side PNG |

### Tour Configuration

Define steps with URL, title, description, optional wait selectors, and annotations (arrow, circle, rectangle, text, highlight).

### Output Structure

```
Projects/[project]/
+-- visual-assets/
    +-- screenshots/
    |   +-- v1.0.0/              (versioned snapshots)
    |   +-- current/             (latest captures)
    |   +-- comparisons/         (before/after views)
    +-- annotations/             (annotation source JSON)
    +-- reports/
        +-- site-tour-v1.0.0.md  (generated tour report)
        +-- visual-index.html    (interactive gallery)
```

### Usage Patterns

- "Take screenshots of [site] focusing on [functionality]"
- "Document the current admin interface"
- "Create a visual tour of the registration flow"
- "Screenshot the checkout process step by step"

### Tour Report

After capture, generate a markdown report linking each screenshot with its description, annotations, and any observations relevant to the FA process.