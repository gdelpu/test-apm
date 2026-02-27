#!/usr/bin/env bash
set -euo pipefail
mkdir -p build
for f in skills/brand-styler/docs/*.md; do
  base=$(basename "$f" .md)
  pandoc "$f" -f gfm -o "build/${base}.docx" \
    --reference-doc=skills/brand-styler/tools/templates/reference.docx
  pandoc "$f" -f gfm -o "build/${base}.pdf" \
    --template skills/brand-styler/tools/pandoc/pdf.latex \
    --pdf-engine=xelatex \
    --css skills/brand-styler/tools/brandify-md.css
  echo "Built build/${base}.{docx,pdf}"
done
