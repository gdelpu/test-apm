# Convert Markdown to Branded DOCX & PDF

Convert Markdown files to Sopra Steria–compliant DOCX and PDF outputs.

## Steps

1. Ensure headings and body text follow brand instructions and accessibility targets.
2. Generate DOCX via Pandoc with the official reference template.
3. Generate PDF via Pandoc with the XeLaTeX template and brand CSS.
4. Report any contrast or accessibility issues.

## Tool Commands

```bash
# DOCX generation
pandoc <file> -f gfm -o build/<base>.docx \
  --reference-doc=skills/brand-styler/tools/templates/reference.docx

# PDF generation
pandoc <file> -f gfm -o build/<base>.pdf \
  --template skills/brand-styler/tools/pandoc/pdf.latex \
  --pdf-engine=xelatex \
  --css skills/brand-styler/tools/brandify-md.css
```

## Prerequisites

- Pandoc installed
- XeLaTeX installed (for PDF)
- Brand Styler skill available
