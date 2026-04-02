# Skill: Output Language

## Objective

This skill defines the multilingual output policy for all deliverables produced by the agentic system. It allows a single set of templates to serve teams working in different languages, without requiring per-language template duplicates.

---

## Declaring the target language

The target language is resolved using the following methods (in order of priority):

1. **`docs/project.yml`** — read the `lang` field if the file exists: `lang: de`. This is the persistent project-level configuration, set once at project initialisation via `/scaffold`. It takes precedence over everything else.
2. **Explicit session declaration** — `"Target language: German"` / `"Langue cible : français"` / `"Zielsprache: Deutsch"` / etc.
3. **`lang` field in an input deliverable's YAML front matter** — `lang: de`
4. **Default** — `en` (English) if no signal is found

The resolved language applies to all deliverables produced during the session. An explicit session declaration overrides `docs/project.yml` for the current session only.

---

## Translation rule

### Translate into the target language

- All prose content: descriptions, justifications, analyses, recommendations
- Section headings internal to the deliverable (e.g. "Context", "Decision", "Consequences", "Acceptance criteria")
- Acceptance criteria, business rules, user-facing messages, screen labels, and notification texts
- Comments and explanatory notes within the deliverable body
- The `Production confidence` section

### Do NOT translate (language-neutral elements)

| Element | Examples |
|---|---|
| Unique identifiers | `[US-001]`, `[ADR-xxx]`, `[RSK-NNN]`, `[PERF-RPT-001]` |
| File names | `adr-001-database-choice.md`, `1.1-product-vision.md` |
| YAML front matter **keys** | `status:`, `id:`, `template:`, `type:`, `lang:` |
| Code blocks, commands, queries | SQL, CLI, API paths, JSON/YAML snippets |
| Technical acronyms used as labels | ADR, API, CRUD, CI/CD, DAST, NFR, UAT, KPI, SLA, SLO, MVP |
| Cross-references to other deliverables | `see [GLO-001]`, `cf. [VIS-001]` |
| Template file names | `tpl-user-story.md`, `tpl-risk.md` |

---

## YAML front matter

Add the `lang` field to the front matter of every produced deliverable:

```yaml
lang: fr   # ISO 639-1 code — en | fr | de | es | pt | nl | it | pl | ...
```

---

## Multi-team projects

If the project spans multiple languages (e.g. client in French, technical team in English):

- Use the session's declared language as the default for all deliverables
- If the development team works exclusively in English, technical deliverables whose content is inseparable from code (e.g. `CLAUDE.md`, CI configuration files, inline code comments) may remain in English — this must be explicitly stated in the session prompt
- Business-facing deliverables (user stories, screen specs, notifications, risk records, steering reports) are **always** translated, regardless of this exception
