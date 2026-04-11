---
name: brand-document
description: 'Adapt PowerPoint, Word, PDF, proposal, dossier, memo, brochure, and similar assets to a target brand identity. Converts Markdown to branded DOCX and PDF via Pandoc. Default brand: Sopra Steria.'
triggers: ['document branding', 'PowerPoint branding', 'Word branding', 'presentation styling', 'slide branding', 'document template', 'dossier branding', 'document conversion', 'DOCX generation', 'PDF generation', 'branded document', 'Pandoc', 'brand styling']
version: '2.0.0'
---

# Skill: Brand Document

## Purpose

Adapt PowerPoint, Word, PDF, proposal, dossier, memo, brochure, and similar assets to a target brand identity. Also generates branded DOCX and PDF outputs from Markdown via Pandoc. Default brand values are for Sopra Steria. To override for a different client, provide assets in `knowledge/brand/<client>/`.

## Priority Order

1. Use official template if available
2. Use official logo and icon assets
3. Correct typography and hierarchy
4. Align layout to the composition system
5. Verify accessibility and consistency

## PowerPoint Guidance

- Prefer the official corporate or sector-specific templates
- Use official layouts instead of manually reproducing master slides
- Keep covers aligned with the brand's layout system
- Use brand icons from the official icon library
- Do not overload slides with gradients — keep the look structured and airy
- Favor visual hierarchy with white space, strong headings, and restrained accent color

## Word / Document Guidance

- Prefer official Word/document templates
- Body text should use the designated office font
- Main headings follow the brand heading approach while preserving office practicality
- Keep standard paper size as the reference format

## Cover / Title Page Rules

Follow the brand's cover layout logic:

- Logo sizing proportional to document dimensions
- Title margins follow the brand's spacing formula
- Consistent treatment across vertical and horizontal formats

## Typography Rules

- Brand heading font for titles and section headers
- Brand body font or office alternative for running text
- Keep line lengths comfortable (~55–65 characters)
- Prefer left alignment except for justified running text or centered quotes

## Icon Usage

- Use the approved icon library where possible
- Maintain consistent icon style throughout the document
- Follow brand color rules for icon tints

## Co-branding in Documents / Slides

- Place a visual separator between partner logos
- Position logos according to who initiated the communication
- Balance logo sizes visually

## Email / Campaign Note

Mass email campaigns should use dedicated tools and approved templates rather than ad hoc hand-crafted layouts.

---

## Markdown → DOCX / PDF Conversion

This skill includes bundled Pandoc templates and scripts to convert Markdown files to branded DOCX and PDF outputs conforming to brand specification and WCAG 2.1 AA contrast requirements.

### Bundled Assets

- `tools/brandify-md.css` — CSS variables and styles for web/HTML output
- `tools/pandoc/metadata.yaml` — Pandoc YAML metadata defaults (paper size, margins)
- `tools/pandoc/pdf.latex` — XeLaTeX template applying brand fonts and colors
- `tools/templates/reference.docx` — Word reference template with brand styles
- `tools/scripts/brandify-docx.py` — Python script to regenerate the DOCX reference template
- `tools/scripts/check-contrast.mjs` — Node.js script for WCAG contrast checking
- `tools/scripts/gen.sh` — Shell script to batch-build all docs to DOCX and PDF
- `docs/sample.md` — Sample branded document for testing and demonstration

### Usage

#### Batch build all docs
```bash
bash skills/brand-document/tools/scripts/gen.sh
```

#### Convert a single file
```bash
pandoc <file> -f gfm -o build/<base>.docx \
  --reference-doc=skills/brand-document/tools/templates/reference.docx

pandoc <file> -f gfm -o build/<base>.pdf \
  --template skills/brand-document/tools/pandoc/pdf.latex \
  --pdf-engine=xelatex \
  --css skills/brand-document/tools/brandify-md.css
```

#### Regenerate the DOCX reference template
```bash
python skills/brand-document/tools/scripts/brandify-docx.py
```

#### Contrast check
```bash
node skills/brand-document/tools/scripts/check-contrast.mjs
```

---

## Default Brand: Sopra Steria

### PowerPoint

- Supported formats: 16:9 and A4 corporate templates
- Use official layouts; do not manually reproduce master slides
- Keep covers aligned with the horizontal layout system

### Word

- Available template families: memo, letter, file, and CV templates
- Keep A4 as the reference format
- Body text in office documents: **Tahoma**
- Main headings can follow the brand heading approach while preserving office practicality

### Cover Rules

**Vertical covers:** logo width ≈ 1/4 of document width; title margins = 3X left and right.

**Horizontal covers:** logo width ≈ 1/3 of document height; title margins = 2X left and right.

Where `X` is derived from the width of the logo swirls.

### Typography

- Brand font: **Hurme Geometric Sans 3**
- Main heading font: **Hurme Geometric Sans 4**
- Office body text: **Tahoma**

### Icons

- Outline-based and dark purple
- Color patches: keep them smaller than the icon, limited to approved style

### Co-branding

- Place a gradient separator line between logos
- Position Sopra Steria left if Sopra Steria initiated the communication, otherwise right

### Brand Palette (Document Tokens)

| Token | Hex | Use |
|---|---|---|
| `--ss-purple` | `#4D1D82` | Headings, links, icons |
| `--ss-red` | `#CF022B` | Accent links, highlights |
| `--ss-orange` | `#EF7D00` | Warnings, secondary accents |
| `--ss-black` | `#1D1D1B` | Body text |

### Fonts

- **Headings**: Hurme Geometric Sans 4 → fallback Tahoma
- **Body**: Hurme Geometric Sans 3 → fallback Tahoma / Segoe UI / Arial

---

## Deliverable Format

When responding to document branding requests, provide:

1. Asset type and template recommendation
2. Slide/page-level issues identified
3. Concrete corrections with references to brand rules
4. Optional rewritten layout structure
5. Asset dependencies still needed
