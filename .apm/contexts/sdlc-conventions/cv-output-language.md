# Convention: Output Language Policy

## Objective

This convention defines the language policy for deliverable content produced by all agents.

---

## Rules

### 1. Deliverable content language

All deliverable content (prose, descriptions, business rules, acceptance criteria, etc.) is produced in the **project's working language**.

The working language is determined by the following priority order:

1. **`docs/project.yml`** — `lang:` field (set once at project initialisation via `/scaffold`)
2. **Explicit session instruction** — e.g. "Target language: English"
3. **Language of source documents** — inferred from client-provided inputs
4. **Language of existing deliverables** — `lang:` field in YAML front matter
5. **Default** — `en` (English)

### 2. Technical identifiers remain in English

Regardless of the working language, the following elements are always in English:
- YAML front matter keys (`id`, `status`, `phase`, `type`, etc.)
- Identifier prefixes (`VIS-`, `EP-`, `US-`, `BR-`, etc.)
- Mermaid diagram keywords (`stateDiagram-v2`, `erDiagram`, etc.)
- File names and folder names
- Git-related content (commit messages, branch names)

### 3. Glossary terms are in the business language

Glossary terms follow the language actually used by the business stakeholders. If the business uses French terms, the glossary is in French. Mixed-language glossaries are acceptable when the business naturally mixes languages (e.g., "Channel Manager" in a French hotel context).
