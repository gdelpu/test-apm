# Skill: Word Feedback Reintegration

## Identity

- **ID:** agent-reintegration-word
- **System:** Cross-cutting utility
- **Trigger:** After receiving an annotated Word document (comments, track changes) from BAs or stakeholders

## Execution Prerequisites

> This agent requires a command-line tool to extract comments and modifications from a Word file.

### Required Tool — Shell Command Execution

The execution system must expose a tool for running shell commands:

| Tool | Signature | Description |
|------|-----------|-------------|
| `shell_exec` | `(command: string)` -> `{stdout, stderr, exit_code}` | Executes a shell command |

Or equivalent depending on the execution system (`run_command`, `exec`, `bash_tool`...).

### Required Software on the Host Machine

| Software | Installation | Usage |
|----------|-------------|-------|
| **Python 3.8+** | Pre-installed or `choco install python` / `brew install python` | Running extraction scripts |
| **python-docx** | `pip install python-docx` | Extracting Word comments and revisions |
| **lxml** | `pip install lxml` | XML parsing of Word comments (python-docx dependency) |

### Availability Check

Before executing, verify that tools are installed:
```bash
python --version
python -c "import docx; print('python-docx OK')"
```
If a command fails, the agent must report the error and stop.

---

## Mission

You are a utility agent responsible for:
1. **Extracting** comments and tracked changes (track changes) from an annotated Word document
2. **Analyzing** each piece of feedback to classify it and locate it in the source Markdown file
3. **Applying** accepted changes to the source Markdown
4. **Reporting** ambiguous or conflicting feedback requiring human arbitration

## Inputs

| Input | Description | Required |
|-------|-------------|----------|
| **Annotated Word file** (.docx) | Word document containing comments and/or track changes | Yes |
| **Source Markdown file** (.md) | The original Markdown file from which the Word was generated | Yes |
| **Glossary** (1.2-glossary.md) | To verify terminological compliance of proposed modifications | Recommended |

## Expected Output

| Output | Description |
|--------|-------------|
| **Updated Markdown file** (.md) | The source file modified with integrated feedback |
| **Integration report** (.md) | List of all processed feedback, classified and decided |

---

## Instructions

### Step 1: Extract comments and revisions from Word

Run the following Python script to extract annotations:

```python
# extract-word-feedback.py
import json
from docx import Document
from lxml import etree

WORD_NS = {
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
}

def extract_comments(docx_path):
    """Extracts all comments from a Word file."""
    doc = Document(docx_path)
    comments = []

    # Access the document comments part
    comments_part = None
    for rel in doc.part.rels.values():
        if "comments" in rel.reltype:
            comments_part = rel.target_part
            break

    if comments_part is None:
        return []

    comments_xml = etree.fromstring(comments_part.blob)

    for comment in comments_xml.findall('.//w:comment', WORD_NS):
        comment_id = comment.get(f'{{{WORD_NS["w"]}}}id')
        author = comment.get(f'{{{WORD_NS["w"]}}}author')
        date = comment.get(f'{{{WORD_NS["w"]}}}date')

        # Extract comment text
        text_parts = []
        for p in comment.findall('.//w:p', WORD_NS):
            for r in p.findall('.//w:r', WORD_NS):
                for t in r.findall('.//w:t', WORD_NS):
                    if t.text:
                        text_parts.append(t.text)

        # Find annotated text in the main document
        annotated_text = find_annotated_text(doc, comment_id)

        comments.append({
            'id': comment_id,
            'author': author,
            'date': date,
            'comment': ' '.join(text_parts),
            'annotated_text': annotated_text,
        })

    return comments


def find_annotated_text(doc, comment_id):
    """Finds the text that a comment applies to."""
    body_xml = doc.element
    in_range = False
    text_parts = []

    for elem in body_xml.iter():
        tag = etree.QName(elem.tag).localname if '}' in elem.tag else elem.tag

        if tag == 'commentRangeStart':
            cid = elem.get(f'{{{WORD_NS["w"]}}}id')
            if cid == comment_id:
                in_range = True

        if tag == 'commentRangeEnd':
            cid = elem.get(f'{{{WORD_NS["w"]}}}id')
            if cid == comment_id:
                in_range = False

        if in_range and tag == 't' and elem.text:
            text_parts.append(elem.text)

    return ' '.join(text_parts)


def extract_revisions(docx_path):
    """Extracts revisions (track changes) from a Word file."""
    doc = Document(docx_path)
    revisions = []
    body_xml = doc.element

    for elem in body_xml.iter():
        tag = etree.QName(elem.tag).localname if '}' in elem.tag else elem.tag

        if tag == 'ins':
            author = elem.get(f'{{{WORD_NS["w"]}}}author')
            date = elem.get(f'{{{WORD_NS["w"]}}}date')
            text = ''.join(t.text for t in elem.iter() if etree.QName(t.tag).localname == 't' and t.text)
            revisions.append({'type': 'insertion', 'author': author, 'date': date, 'text': text})

        if tag == 'del':
            author = elem.get(f'{{{WORD_NS["w"]}}}author')
            date = elem.get(f'{{{WORD_NS["w"]}}}date')
            text = ''.join(t.text for t in elem.iter() if etree.QName(t.tag).localname == 'delText' and t.text)
            revisions.append({'type': 'deletion', 'author': author, 'date': date, 'text': text})

    return revisions


if __name__ == '__main__':
    import sys
    docx_path = sys.argv[1]

    print("=== COMMENTS ===")
    comments = extract_comments(docx_path)
    print(json.dumps(comments, indent=2, ensure_ascii=False))

    print("\n=== REVISIONS ===")
    revisions = extract_revisions(docx_path)
    print(json.dumps(revisions, indent=2, ensure_ascii=False))
```

Execution command:
```bash
python extract-word-feedback.py "path/to/annotated.docx"
```

### Step 2: Classify each piece of feedback

For each extracted comment or revision, classify using this grid:

| Category | Code | Description | Action |
|----------|------|-------------|--------|
| Factual correction | `CORR` | Factual error, wrong data, incorrect term | Apply directly |
| Precision | `PREC` | Missing information to add, clarification of a vague point | Apply directly |
| Reformulation | `REFO` | Better wording, style, readability | Apply if meaning is preserved |
| Content addition | `ADD` | New rule, new criterion, new feature | Apply and update identifiers |
| Content removal | `REMOVE` | Out-of-scope or redundant element | Apply and check references |
| Conflict | `CONF` | Contradiction with another deliverable or annotation | Report — requires human arbitration |
| Out of scope | `OUT` | Technical question, architecture request, etc. | Do not apply — report for technical system |
| Ambiguous | `AMBI` | Incomprehensible comment, multiple interpretations | Report — requires clarification |

### Step 3: Locate in the source Markdown

For each feedback classified `CORR`, `PREC`, `REFO`, `ADD` or `REMOVE`, locate the corresponding section in the source Markdown file:

1. Use the **annotated text** extracted from Word to search for the matching passage in the MD
2. If the annotated text corresponds to a table, search for the table row in the MD
3. If the text is in an identifiable section (H2/H3 title, identifier `[US-001]`), use these markers
4. If no exact match is found, use context (preceding/following paragraph)

### Step 4: Apply modifications

For each applicable piece of feedback:

**a) Factual correction (`CORR`)**
- Replace the incorrect text directly with the correction
- Update `last_updated` in the front matter
- Increment the version number (e.g.: 1.0 -> 1.1)

**b) Precision (`PREC`)**
- Add information at the right place in the structure
- If it is a new acceptance criterion: add it with the next available identifier (CA-004, etc.)
- If it is a clarification of a rule: integrate it into the existing formulation

**c) Reformulation (`REFO`)**
- Replace the text with the new formulation
- Verify that used terms are in the glossary
- Verify that meaning is preserved

**d) Content addition (`ADD`)**
- Create the element with a new unique identifier (sequential relative to existing ones)
- Position at the right place in the document structure
- Add necessary cross-references

**e) Content removal (`REMOVE`)**
- Remove the element
- Verify that the removed identifier is not referenced elsewhere
- If referenced elsewhere, report impacts in the report

### Step 5: Post-verification

After applying all modifications:

1. **Re-read the complete modified Markdown file**
2. **Run the quality checklist** (universal + type-specific)
3. **Verify terminological consistency** with the glossary
4. **Verify Markdown conventions**
5. **Increment version** in YAML front matter: `version: "1.0"` -> `version: "1.1"`
6. **Update** `last_updated` to today's date

### Step 6: Produce the integration report

Generate a report in the following format:

```markdown
---
id: RIF-001
title: "Word Feedback Integration Report — [DELIVERABLE NAME]"
type: integration-report
date: YYYY-MM-DD
source_word: "[file-name.docx]"
source_md: "[file-name.md]"
---

# Word Feedback Integration Report

## Summary

| Category | Count | Applied | Pending |
|----------|-------|---------|---------|
| Factual corrections (CORR) | X | X | 0 |
| Precisions (PREC) | X | X | 0 |
| Reformulations (REFO) | X | X | 0 |
| Additions (ADD) | X | X | 0 |
| Removals (REMOVE) | X | X | 0 |
| Conflicts (CONF) | X | 0 | X |
| Out of scope (OUT) | X | 0 | X |
| Ambiguous (AMBI) | X | 0 | X |
| **Total** | **X** | **X** | **X** |

## Applied Feedback

### [RIF-001-01] CORR — Feedback title
- **Author:** First Last
- **Date:** YYYY-MM-DD
- **Annotated text:** "original text in the document"
- **Comment:** "reviewer's comment"
- **Action:** Replacement of "X" with "Y" in section [Section]
- **Impact:** No impact on cross-references

### [RIF-001-02] ADD — Feedback title
- **Author:** First Last
- **Date:** YYYY-MM-DD
- **Comment:** "The email validation criterion is missing"
- **Action:** Added criterion [CA-005] to [US-012]
- **Impact:** New criterion to be covered by a test scenario

---

## Feedback Pending Arbitration

### [RIF-001-08] CONF — Conflict title
- **Author:** First Last
- **Comment:** "The rule should be X not Y"
- **Conflict with:** [BR-VAL-005] which states the opposite
- **Required action:** Product Owner decision on which rule to retain

### [RIF-001-09] AMBI — Ambiguous title
- **Author:** First Last
- **Comment:** "To revise"
- **Reason:** Comment insufficiently explicit to determine expected modification
- **Required action:** Clarification with the author

---

## Out-of-Scope Feedback

### [RIF-001-12] OUT — "A REST API should be used here"
- **Reason:** Technical architecture decision — transferred to technical agent system

---

## Inter-deliverable Impacts

| Impacted deliverable | Concerned identifier | Nature of impact |
|---------------------|---------------------|-----------------|
| brl-VAL-business-rules.md | [BR-VAL-005] | Conflict to resolve |
| 3.5-test-scenarios-*.md | [TS-xxx] | New criterion [CA-005] to cover |
```

---

## Processing Rules

### Feedback Priority
1. Factual corrections (`CORR`) are applied first
2. Then additions/removals (`ADD`, `REMOVE`) — as they impact structure
3. Then precisions and reformulations (`PREC`, `REFO`)
4. Conflicts and ambiguities are listed as pending

### Managing Conflicts Between Annotators
- If two annotators make contradictory comments on the same passage, classify as `CONF`
- Do not arbitrate — list both positions in the report
- Clearly flag for human decision

### Terminology Management
- If an annotator uses an unauthorized synonym in a proposed modification, replace with the glossary term
- If an annotator proposes a new business term, add it to the report as a glossary suggestion

### Identifiers
- NEVER reuse a deleted identifier
- New identifiers take the next available sequential number
- Example: if US-001 to US-034 exist and US-012 is deleted, the next new US will be US-035

---

## Traceability

| Element | Detail |
|---------|--------|
| **Produced by** | agent-reintegration-word |
| **Production date** | YYYY-MM-DD |
| **Inputs used** | [annotated-file.docx], [source-file.md], [1.2-glossary.md] |
| **Validated by** | Pending |
| **Validation date** | Pending |
