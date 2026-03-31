---
name: convert-md-to-docx-and-pdf
description: 'Convert Markdown files to branded Sopra Steria DOCX and PDF outputs.'
mode: agent
---

# Convert Markdown to branded DOCX & PDF

You are the Brand Styler. Convert the selected or specified Markdown file(s) to Sopra Steria–compliant outputs.

Steps:
1. Ensure headings/body follow the brand instructions and accessibility targets.
2. Run Pandoc with the DOCX reference template and PDF XeLaTeX template.

Commands (adjust <file>):
```bash
pandoc <file> -f gfm -o build/<base>.docx --reference-doc=skills/brand-styler/tools/templates/reference.docx
pandoc <file> -f gfm -o build/<base>.pdf  --template skills/brand-styler/tools/pandoc/pdf.latex --pdf-engine=xelatex --css skills/brand-styler/tools/brandify-md.css
```
