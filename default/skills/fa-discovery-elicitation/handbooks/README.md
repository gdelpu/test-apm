# AI/HANDBOOKS – Methodology reference (BABOK + IREB)

This folder holds all handbook material for the FA Copilot: **BABOK** and **IREB (CPRE)** in one place.

**Purpose:** Use alongside each other as methodology input for FA work (business analysis, requirements engineering, elicitation, modeling, management).

---

## Structure

| Location | Contents |
|----------|----------|
| **This folder** (`.md` files) | Markdown handbooks used by the copilot (BABOK-Guide.md + IREB English .md) |
| **PDF/** | Same content as PDFs for humans (reading, printing, sharing). BABOK + IREB English. |

---

## Regenerating IREB markdown from PDFs

From repo root:
```bash
.venv/bin/python AI/scripts/ireb_pdf_to_md.py
```
- Reads: `AI/HANDBOOKS/PDF/*.pdf`
- Writes: `AI/HANDBOOKS/*.md` (IREB only; BABOK-Guide-File-en.pdf is skipped; canonical BABOK text is `BABOK-Guide.md`)

Requires `.venv` with `pymupdf` (see `AI/scripts/requirements-conversion.txt`).

---

## Key markdown files (examples)

- `BABOK-Guide.md` – BABOK V3 (primary business analysis reference)
- `cpre_foundationlevel_handbook_en_v1.2.md` – IREB Foundation Level handbook
- `ireb_cpre_glossary_en_2.2.md` – IREB glossary
- `advanced_level_elicitation_handbook_en_v2.2.0.md` – IREB Elicitation (advanced)
- `ireb-cpre-handbook-for-requirements-management-en-v2.1.md` – IREB Requirements management
- Syllabi and factsheets for FL, elicitation, modeling, RE@Agile
