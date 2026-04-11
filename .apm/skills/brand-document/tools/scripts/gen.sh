#!/usr/bin/env bash
set -euo pipefail
mkdir -p build
for f in skills/brand-document/docs/*.md; do
  base=$(basename "$f" .md)
  pandoc "$f" -f gfm -o "build/${base}.docx" \
    --reference-doc=skills/brand-document/tools/templates/reference.docx
  pandoc "$f" -f gfm -o "build/${base}.pdf" \
    --template skills/brand-document/tools/pandoc/pdf.latex \
    --pdf-engine=xelatex \
    --css skills/brand-document/tools/brandify-md.css
  echo "Built build/${base}.{docx,pdf}"
done
