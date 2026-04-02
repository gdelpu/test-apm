# Skill: Document Anonymization (Word / PowerPoint)

## Identity

- **ID:** agent-anonymisation-document
- **System:** Cross-cutting utility
- **Trigger:** On demand, before sharing any document containing personal data (clients, prospects, demos, training, RFPs...)

## Execution Prerequisites

> This agent requires Python and the `presidio`, `python-docx`, and `python-pptx` libraries installed on the host machine.

### Required Tool — Shell Command Execution

| Tool | Signature | Description |
|------|-----------|-------------|
| `shell_exec` | `(command: string)` -> `{stdout, stderr, exit_code}` | Executes a shell command |

Or equivalent depending on the execution system (`run_command`, `exec`, `bash_tool`...).

### Required Software on the Host Machine

| Software | Installation | Usage |
|----------|-------------|-------|
| **Python 3.9+** | Pre-installed or `choco install python` / `brew install python` | Script execution |
| **presidio-analyzer** | `pip install presidio-analyzer` | Personal entity detection (NER) |
| **presidio-anonymizer** | `pip install presidio-anonymizer` | Entity substitution / pseudonymization |
| **spacy + FR model** | `pip install spacy && python -m spacy download fr_core_news_lg` | French NLP (required by Presidio) |
| **python-docx** | `pip install python-docx` | Read / write Word files (.docx) |
| **python-pptx** | `pip install python-pptx` | Read / write PowerPoint files (.pptx) |

### Availability Check

```bash
python -c "from presidio_analyzer import AnalyzerEngine; from presidio_anonymizer import AnonymizerEngine; from docx import Document; from pptx import Presentation; print('OK')"
```

If the command fails, the agent must report the error and stop.

---

## Mission

You are a utility agent responsible for anonymizing Office documents (Word `.docx` or PowerPoint `.pptx`) by automatically detecting personally identifiable information (PII) and replacing them with consistent pseudonyms throughout the document.

Anonymization is **consistent**: the same entity detected multiple times in the document always receives the same pseudonym (e.g., "Jean Dupont" -> "PERSON_01" everywhere), preserving the document's readability.

---

## Inputs

| Input | Description | Required |
|-------|-------------|----------|
| **Source file** (.docx or .pptx) | Document to anonymize | Yes |
| **Language** | Document language code (`fr`, `en`...). Default: `fr` | Recommended |
| **Additional entities** | List of business terms to anonymize in addition to automatically detected entities (client company names, projects...) | Optional |
| **[RGPD-001]** | If available, the DCP entity catalog identified during the PIA can feed detection rules | Optional |

---

## Expected Output

| Output | Description |
|--------|-------------|
| **Anonymized file** (`[original-name]-anonymized.docx` or `.pptx`) | Document with all PII replaced by pseudonyms |
| **Anonymization report** (`[ANON-001]-report.md`) | Original -> pseudonym correspondence table + statistics (number of entities detected per type) |

---

## Detailed Instructions

### Step 1: Extract text according to document format

**For a Word file (.docx):**

```python
# extract-docx-text.py
from docx import Document

def extract_paragraphs_docx(path):
    """Returns a list of (paragraph_object, text)."""
    doc = Document(path)
    result = []
    for para in doc.paragraphs:
        if para.text.strip():
            result.append(('paragraph', para, para.text))
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    if para.text.strip():
                        result.append(('cell', para, para.text))
    return doc, result
```

**For a PowerPoint file (.pptx):**

```python
# extract-pptx-text.py
from pptx import Presentation

def extract_paragraphs_pptx(path):
    """Returns a list of (run_object, text) for each text run."""
    prs = Presentation(path)
    result = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                for para in shape.text_frame.paragraphs:
                    for run in para.runs:
                        if run.text.strip():
                            result.append(('run', run, run.text))
    return prs, result
```

---

### Step 2: Detect personal entities with Presidio

```python
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider

# Configure the NLP engine for French
provider = NlpEngineProvider(nlp_configuration={
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "fr", "model_name": "fr_core_news_lg"}]
})
nlp_engine = provider.create_engine()

analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["fr", "en"])

# Target entity types
ENTITY_TYPES = [
    "PERSON",           # Person names
    "EMAIL_ADDRESS",    # Emails
    "PHONE_NUMBER",     # Phone numbers
    "LOCATION",         # Cities, addresses
    "ORGANIZATION",     # Organization names
    "IBAN_CODE",        # IBAN
    "CREDIT_CARD",      # Card numbers
    "DATE_TIME",        # Dates (optional, enable if needed)
    "NRP",              # Nationality, religion, politics
    "IP_ADDRESS",       # IP addresses
]

def detect_entities(text, language="fr"):
    results = analyzer.analyze(text=text, language=language, entities=ENTITY_TYPES)
    return results
```

---

### Step 3: Build the consistent pseudonymization dictionary

To ensure the same entity always receives the same pseudonym, build a global dictionary before substitution:

```python
def build_pseudonym_map(all_texts, language="fr"):
    """
    Iterates over all document texts, detects entities,
    and builds a dictionary {original_value: pseudonym}.
    """
    counters = {}  # {entity_type: count}
    pseudonym_map = {}  # {original_value: pseudonym}

    for text in all_texts:
        results = detect_entities(text, language)
        for result in results:
            original = text[result.start:result.end]
            if original not in pseudonym_map:
                entity_type = result.entity_type
                counters[entity_type] = counters.get(entity_type, 0) + 1
                pseudonym_map[original] = f"{entity_type}_{counters[entity_type]:02d}"

    return pseudonym_map
```

---

### Step 4: Substitute entities in the document

Substitution must operate **run by run** (Word) or **run by run** (PowerPoint) to preserve formatting:

```python
def anonymize_text(text, pseudonym_map):
    """Replaces all known occurrences in a text."""
    result = text
    # Sort by decreasing length to avoid partial substitutions
    for original in sorted(pseudonym_map.keys(), key=len, reverse=True):
        result = result.replace(original, pseudonym_map[original])
    return result

def anonymize_docx(doc, paragraphs_list, pseudonym_map, output_path):
    for (kind, obj, _text) in paragraphs_list:
        new_text = anonymize_text(obj.text, pseudonym_map)
        if new_text != obj.text:
            # Rewrite text in the first run, clear the others
            if obj.runs:
                obj.runs[0].text = new_text
                for run in obj.runs[1:]:
                    run.text = ""
            else:
                obj.text = new_text
    doc.save(output_path)

def anonymize_pptx(prs, runs_list, pseudonym_map, output_path):
    for (kind, run, _text) in runs_list:
        run.text = anonymize_text(run.text, pseudonym_map)
    prs.save(output_path)
```

---

### Step 5: Produce the anonymization report `[ANON-001]`

Generate a Markdown file summarizing all substitutions made:

```markdown
---
id: ANON-001
title: Anonymization Report — [source file name]
date: [date]
status: validated
---

# Anonymization Report

## Processed File
- **Source:** `[source-file-name.docx]`
- **Output:** `[source-file-name-anonymized.docx]`
- **Detected language:** fr
- **Date:** [date]

## Statistics

| Entity Type | Detected Occurrences |
|------------|----------------------|
| PERSON | X |
| ORGANIZATION | X |
| EMAIL_ADDRESS | X |
| PHONE_NUMBER | X |
| LOCATION | X |
| ... | ... |

## Correspondence Table

| Original Value | Pseudonym | Type |
|----------------|-----------|------|
| Jean Dupont | PERSON_01 | PERSON |
| Sopra Steria | ORGANIZATION_01 | ORGANIZATION |
| jean.dupont@email.com | EMAIL_ADDRESS_01 | EMAIL_ADDRESS |
| ... | ... | ... |

## Points of Attention

List here any potentially missed entities or those requiring manual verification (e.g., ambiguous business terms, abbreviated proper nouns not detected by the NLP model).
```

---

### Step 6: Quality checklist before delivery

Before delivering the anonymized file, verify:

- [ ] The anonymized file opens without error in Word / PowerPoint
- [ ] Formatting (fonts, tables, images) is preserved
- [ ] Pseudonyms are consistent (e.g., no two different pseudonyms for the same person)
- [ ] The `[ANON-001]` report is complete and readable
- [ ] No obvious proper nouns remain in the text (quick review)
- [ ] Manually provided additional entities have been substituted

---

## Special Cases

### Manual additional entities

If the requester provides a list of terms to anonymize in addition to automatic detection (e.g., internal project names, client codes), add them directly to the `pseudonym_map` with dedicated prefixes:

```python
custom_entities = ["ProjectAlpha", "Client XYZ", "Central Bank"]
for i, term in enumerate(custom_entities, start=1):
    pseudonym_map[term] = f"CUSTOM_{i:02d}"
```

### Partial anonymization (specific sections only)

If only certain sections need to be anonymized (e.g., only client presentation slides, not technical slides), the user can specify slide numbers (PPTX) or section titles (DOCX) to process.

### Text in images

> **Known limitation:** Text embedded in images (screenshots, logos with text, photos) cannot be detected or modified by this agent. Manual verification of these elements is recommended and must be mentioned in the report.

---

## Execution Command Examples

**Anonymizing a Word document:**
```bash
python anonymize.py --input "client-presentation.docx" --lang fr --output "client-presentation-anonymized.docx"
```

**Anonymizing a PowerPoint with additional entities:**
```bash
python anonymize.py --input "demo-deck.pptx" --lang fr --custom "ProjectAlpha,Client XYZ" --output "demo-deck-anonymized.pptx"
```
