# Post-Hook: Deliverable Quality Control — Universal Checklist

> **Type:** post | **Scope:** agent + station | **Domain:** universal | **Severity:** blocker

## Objective

Executed **after the agent has produced its deliverable**, before returning to the coordinator. The agent MUST run this complete checklist and correct any non-conforming items before considering the deliverable complete.

For **domain-specific** validation checklists (BA deliverable types, Tech deliverable types, Steer/Test specifics), see the `sdlc-deliverable-validation` skill and its docs (`sk-validate-BA-Agents.md`, `sk-validate-Tech-Agents.md`, `sk-validate-Steer-Agents.md`).

---

## Doc Depth Awareness

This hook adapts its checks based on the `doc_depth` setting in `docs/project.yml` (`essential` or `full`). If absent, default to `full`.

**Depth-specific relaxations:**
- **essential**: Traceability section is optional. Glossary cross-reference check is skipped (no glossary produced). Definition of Ready checklists are not required. Inline user stories and business rules in feature files are accepted (no separate files required).
- **full**: All checks apply without relaxation.

---

## Universal Checklist (all deliverables)

### Form
- [ ] The YAML front matter is present and complete
- [ ] The status is set to `draft`
- [ ] The heading structure follows the hierarchy (H1 > H2 > H3 > H4)
- [ ] All traceable elements have a unique identifier with the correct prefix
- [ ] Cross-references point to existing identifiers
- [ ] The traceability section is present at the end of the document — **skip if `doc_depth` is `essential`**
- [ ] The file naming follows the convention

### Content
- [ ] All business terms used are defined in the glossary — **skip if `doc_depth` is `essential`** (no glossary produced)
- [ ] No ambiguity: each sentence has only one possible interpretation
- [ ] No technical assumptions (no mention of databases, APIs, or frameworks) — **brownfield exception: constraints from the existing system referenced by `[ASIS-xxx]` are allowed**
- [ ] Example data uses realistic and concrete values
- [ ] The deliverable is self-contained: a reader can understand it with only the listed dependencies

### Structural Conformance to the Template
- [ ] All H2 sections from the corresponding template (`tpl-*.md`) are present in the produced deliverable. **Important:** when a `template_variant` is used (e.g., `tpl-feature-essential.md`), validate against that variant, not the full template.
- [ ] No residual placeholders (`<!-- ... -->`, `YYYY-MM-DD`, `[Project Name]`, `xxx` values, `TermName`, text between angle brackets `<...>`)
- [ ] All front matter fields are filled in (no empty or generic values)
- [ ] Minimum counts by deliverable type are respected (adjusted by depth — see Minimum Counts section below)

---

## Minimum Counts by Depth

### `full` depth (default)
- Glossary: >= 5 defined terms
- Actors & Roles: >= 2 actors, rights matrix present
- Functional requirements: >= 3 requirements with `EX-xxx` identifiers
- Domain model: >= 3 entities with attributes, Mermaid diagram present
- Epics & Features: >= 1 epic with >= 2 features
- Business rules: >= 3 rules with IF/THEN structure
- User Stories: >= 2 Given/When/Then acceptance criteria per story
- Test scenarios: at least 1 nominal scenario + 1 error scenario per covered business rule

### `essential` depth
- Epics & Features: >= 1 epic with >= 2 features
- Features: >= 1 inline user story with >= 1 acceptance criterion per story
- Features: >= 1 feature-level acceptance criterion (FAC-xxx)

---

## Next Reader Test

For each major section of the deliverable, evaluate whether the next consuming agent can act on it without ambiguity:

- **CONFIDENT**: complete, actionable content, no ambiguity detected — no marking required
- **PARTIAL**: content present but incomplete — document the gap in `## Attention Points`
- **INSUFFICIENT**: content too vague to be used — correct before delivering (do not deliver as-is)

> If >= 1 section is **INSUFFICIENT**, the agent MUST correct it before delivering. A PARTIAL section is acceptable if the gap is documented.

---

## Self-Verification Process

After generating the deliverable, execute these steps:

1. Re-read the complete deliverable
2. Run the universal checklist (Form + Content + Structural conformance)
3. Run the next reader test section by section
4. **Invoke the domain-specific checklist** from `sdlc-deliverable-validation` skill for the deliverable type
5. For each non-conforming item: correct immediately
6. If an item cannot be corrected (missing information): add a warning in `## Attention Points`
7. Add the `## Production confidence` section at the very end:

```markdown
## Production confidence

| Dimension | Level | Identified gaps |
|-----------|-------|-----------------|
| Sufficient inputs | CONFIDENT / PARTIAL / INSUFFICIENT | [list of gaps, "None" if CONFIDENT] |
| Scope coverage | CONFIDENT / PARTIAL / INSUFFICIENT | [sections or concepts not covered] |
| Usability by [next agent] | CONFIDENT / PARTIAL / INSUFFICIENT | [what the next agent will need to compensate] |

**Global score:** X/3 CONFIDENT — [1-2 sentence comment justifying the score.]
```

## Attention Points Format

```markdown
## Attention Points

> [PA-001] The term "framework contract" is used but not defined in the current glossary. To be clarified at the next workshop.
> [PA-002] The discount calculation rule requires business validation (assumption: discount applied to the pre-tax amount).
```

---

## Decision

| Result | Condition |
|--------|-----------|
| **GO** | All checklist items pass; no INSUFFICIENT sections |
| **WARN** | All mandatory items pass; >= 1 PARTIAL section documented in Attention Points |
| **STOP** | >= 1 mandatory checklist item fails; or >= 1 INSUFFICIENT section not corrected |
