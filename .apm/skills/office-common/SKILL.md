---
name: office-common
description: 'Shared OOXML utilities for packing, unpacking, validating, and converting Office documents (.docx, .pptx, .xlsx). Provides LibreOffice integration, XML schema validation, tracked-change helpers, and redlining support used by the docx, pptx, and xlsx skills.'
version: 1.0.0
triggers:
  - 'ooxml'
  - 'pack office'
  - 'unpack office'
  - 'validate office document'
  - 'office xml'
  - 'repack docx'
  - 'repack pptx'
  - 'repack xlsx'
---

# Office Common Utilities

Shared OOXML pack/unpack/validate/convert utilities used by the `docx`, `pptx`, and `xlsx` skills.

## Overview

Office documents (.docx, .pptx, .xlsx) are ZIP archives containing XML files following the OOXML standard. This skill provides the common tooling for working with them at the XML level.

## Available Scripts

| Script | Purpose |
|--------|---------|
| `pack.py` | Repack an unpacked directory back into a valid Office file (.docx/.pptx/.xlsx) with optional tracked-change generation |
| `unpack.py` | Unpack an Office file into its constituent XML files for editing |
| `validate.py` | Validate an Office file against OOXML schemas |
| `soffice.py` | LibreOffice wrapper — format conversion, PDF export, accepting tracked changes. Auto-configures for sandboxed environments |

## Helpers

| Module | Purpose |
|--------|---------|
| `helpers/merge_runs.py` | Merge adjacent `<w:r>` runs with identical formatting in WordprocessingML |
| `helpers/simplify_redlines.py` | Simplify tracked-change markup (merge adjacent ins/del blocks) |

## Validators

| Module | Purpose |
|--------|---------|
| `validators/base.py` | Base schema validator for OOXML ZIP/XML validation |
| `validators/docx.py` | DOCX-specific element and namespace validation |
| `validators/pptx.py` | PPTX-specific namespace handling |
| `validators/redlining.py` | Validate tracked changes (insertions, deletions, author attribution) |

## Schemas

Contains 39 XSD schema files for OOXML validation:
- ECMA Fourth Edition schemas
- ISO/IEC 29500-4:2016 schemas
- MCE (Markup Compatibility and Extensibility)
- Microsoft extension schemas (2010–2020)

## Typical Workflow

```bash
# 1. Unpack
python skills/office-common/unpack.py document.docx unpacked/

# 2. Edit XML files in unpacked/ directory

# 3. Repack with tracked changes
python skills/office-common/pack.py unpacked/ output.docx --original document.docx

# 4. Validate
python skills/office-common/validate.py output.docx
```

## Dependencies

- Python 3.10+
- `lxml` — XML parsing and schema validation
- LibreOffice (`soffice`) — optional, for format conversion and PDF export
