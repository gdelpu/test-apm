---
name: convert-md-to-docx-and-pdf
description: 'Convert Markdown files to Sopra Steria branded DOCX and PDF outputs using Pandoc.'
---

# Convert Markdown to branded DOCX & PDF

You are the Branding Agent. Convert the selected or specified Markdown file(s) to Sopra Steria–compliant outputs.

Steps:
1. Ensure headings/body follow the brand instructions and accessibility targets.
2. Run Pandoc with the DOCX reference template and PDF XeLaTeX template.

Commands (adjust <file>):
```bash
pandoc <file> -f gfm -o build/<base>.docx --reference-doc=skills/brand-document/tools/templates/reference.docx
pandoc <file> -f gfm -o build/<base>.pdf  --template skills/brand-document/tools/pandoc/pdf.latex --pdf-engine=xelatex --css skills/brand-document/tools/brandify-md.css
```
