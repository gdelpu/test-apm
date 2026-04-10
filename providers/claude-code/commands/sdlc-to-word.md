# /sdlc-to-word

Convert a Markdown deliverable to **Word** format using Pandoc.

$ARGUMENTS = path to the Markdown file to convert (e.g., "outputs/docs/1-prd/1-scoping/vis-001-product-vision.md")

## Steps

1. Load `.apm/skills/sdlc-confluence-sync/docs/sk-word-conversion.md` for conversion rules.
2. Load the corporate template from `.apm/skills/sdlc-confluence-sync/docs/template-corporate.docx`.
3. Execute the conversion using Pandoc with the corporate template.
4. Output the Word file to `output/word/`.
