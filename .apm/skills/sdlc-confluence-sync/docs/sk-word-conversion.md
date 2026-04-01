# Skill: Markdown -> Word Conversion

## Identity

- **ID:** agent-conversion-word
- **System:** Cross-cutting utility
- **Trigger:** On demand, after producing one or more deliverables

## Execution Prerequisites

> This agent requires a command-line tool (`pandoc`) accessible from the agent execution system.

### Required Tool — Shell Command Execution

The execution system must expose a tool for running shell commands:

| Tool | Signature | Description |
|------|-----------|-------------|
| `shell_exec` | `(command: string)` -> `{stdout, stderr, exit_code}` | Executes a shell command |

Or equivalent depending on the execution system (`run_command`, `exec`, `bash_tool`...).

### Required Software on the Host Machine

| Software | Installation | Usage |
|----------|-------------|-------|
| **Pandoc** | `choco install pandoc` (Windows) / `brew install pandoc` (Mac) | MD -> DOCX conversion |
| **mermaid-cli (mmdc)** | `npm install -g @mermaid-js/mermaid-cli` | Rendering Mermaid diagrams to PNG |
| **python-docx** (optional) | `pip install python-docx` | Extracting Word review comments |

### Availability Check

Before executing, verify that pandoc is installed:
```bash
pandoc --version
```
If the command fails, the agent must report the error and stop.

---

## Mission

You are a utility agent responsible for converting Markdown deliverables into professional Word documents, ready for review by Business Analysts and stakeholders.

## Inputs

- **Markdown files**: one or more deliverables produced by BA agents
- **Corporate Word template**: `shared/templates/template-corporate.docx` (if available)

## Expected Output

One or more `.docx` files corresponding to the input Markdown files, with:
- Professional formatting (styles, headers, footers)
- Automatic table of contents
- Properly formatted tables
- Mermaid diagrams converted to images

## Instructions

### Conversion with Pandoc

The basic command to convert a Markdown file to Word:

```bash
pandoc input.md -o output.docx --from markdown --to docx
```

With corporate template:

```bash
pandoc input.md -o output.docx --from markdown --to docx --reference-doc=shared/templates/template-corporate.docx
```

### Consolidated conversion (all deliverables in a phase)

To produce a single document consolidating all deliverables from a phase:

```bash
pandoc 1.1-product-vision.md 1.2-glossary.md 1.3-actors-roles.md \
  -o "Phase1-Scoping.docx" \
  --from markdown \
  --to docx \
  --reference-doc=shared/templates/template-corporate.docx \
  --toc \
  --toc-depth=3
```

### Handling Mermaid Diagrams

Mermaid diagrams are not natively supported by Pandoc. Two options:

**Option A: Pre-conversion with mermaid-cli**
```bash
# Install mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# Convert diagrams to PNG before Pandoc conversion
mmdc -i diagram.mmd -o diagram.png

# Then replace ```mermaid``` blocks with images ![](diagram.png) in the MD
```

**Option B: Pandoc mermaid-filter**
```bash
npm install -g mermaid-filter
pandoc input.md -o output.docx --filter mermaid-filter
```

### Handling YAML Front Matter

YAML front matter can be used by Pandoc for Word document metadata:
- `title` -> Document title
- `author` -> Author
- `date` -> Date

Pandoc automatically ignores YAML fields it does not recognize (id, phase, type, status, etc.), which is the desired behavior.

### Batch Conversion Script

To automatically convert all deliverables of a project:

```bash
#!/bin/bash
# convert-all.sh

TEMPLATE="shared/templates/template-corporate.docx"
OUTPUT_DIR="output/word"

mkdir -p "$OUTPUT_DIR"

# Individual conversion of each MD file
for md_file in output/markdown/*.md; do
  filename=$(basename "$md_file" .md)
  pandoc "$md_file" -o "$OUTPUT_DIR/$filename.docx" \
    --from markdown --to docx \
    --reference-doc="$TEMPLATE" \
    --toc --toc-depth=3
done

# Consolidated document by phase
pandoc output/markdown/1.*.md -o "$OUTPUT_DIR/Phase1-Scoping-Complete.docx" \
  --from markdown --to docx --reference-doc="$TEMPLATE" --toc --toc-depth=3

pandoc output/markdown/2.*.md -o "$OUTPUT_DIR/Phase2-Specification-Complete.docx" \
  --from markdown --to docx --reference-doc="$TEMPLATE" --toc --toc-depth=3

pandoc output/markdown/3.*.md -o "$OUTPUT_DIR/Phase3-Design-Complete.docx" \
  --from markdown --to docx --reference-doc="$TEMPLATE" --toc --toc-depth=3
```

### Word Comment Reintegration

When a BA annotates the Word document (comments, track changes), the feedback must be reintegrated into the source Markdown.

**Approach with python-docx:**

```python
# extract-comments.py
from docx import Document

def extract_comments(docx_path):
    """Extracts comments from an annotated Word file."""
    doc = Document(docx_path)
    # Word comments are stored in doc.part.comments
    # Extract and format as Markdown for reintegration
    pass
```

The feedback integration agent (not implemented here) would read these comments and update the source Markdown files.

## Technical Prerequisites

| Tool | Installation | Usage |
|------|-------------|-------|
| Pandoc | `choco install pandoc` (Windows) / `brew install pandoc` (Mac) | MD -> DOCX conversion |
| mermaid-cli | `npm install -g @mermaid-js/mermaid-cli` | Mermaid diagram -> PNG conversion |
| python-docx | `pip install python-docx` | Word comment extraction |
