---
name: brand-styler
description: 'Generates and converts documents to Sopra Steria brand specification with AA accessibility. Produces branded DOCX and PDF outputs via Pandoc using custom font, color, and layout templates.'
---

# Brand Styler

Generates Markdown documents, DOCX, and PDFs conforming to the Sopra Steria brand specification and WCAG 2.1 AA contrast requirements.

## Bundled Assets

- `tools/brandify-md.css` — CSS variables and styles for web/HTML output
- `tools/pandoc/metadata.yaml` — Pandoc YAML metadata defaults (paper size, margins)
- `tools/pandoc/pdf.latex` — XeLaTeX template applying brand fonts and colors
- `tools/templates/reference.docx` — Word reference template with brand styles
- `tools/scripts/brandify-docx.py` — Python script to regenerate the DOCX reference template
- `tools/scripts/check-contrast.mjs` — Node.js script for WCAG contrast checking
- `tools/scripts/gen.sh` — Shell script to batch-build all docs to DOCX and PDF
- `docs/sample.md` — Sample branded document for testing and demonstration

## Usage

### Batch build all docs
```bash
bash skills/brand-styler/tools/scripts/gen.sh
```

### Convert a single file
```bash
pandoc <file> -f gfm -o build/<base>.docx \
  --reference-doc=skills/brand-styler/tools/templates/reference.docx

pandoc <file> -f gfm -o build/<base>.pdf \
  --template skills/brand-styler/tools/pandoc/pdf.latex \
  --pdf-engine=xelatex \
  --css skills/brand-styler/tools/brandify-md.css
```

### Regenerate the DOCX reference template
```bash
python skills/brand-styler/tools/scripts/brandify-docx.py
```

### Contrast check
```bash
node skills/brand-styler/tools/scripts/check-contrast.mjs
```

## Brand Palette

| Token | Hex | Use |
|---|---|---|
| `--ss-purple` | `#4D1D82` | Headings, links, icons |
| `--ss-red` | `#CF022B` | Accent links, highlights |
| `--ss-orange` | `#EF7D00` | Warnings, secondary accents |
| `--ss-black` | `#1D1D1B` | Body text |

## Fonts

- **Headings**: Hurme Geometric Sans 4 → fallback Tahoma
- **Body**: Hurme Geometric Sans 3 → fallback Tahoma / Segoe UI / Arial