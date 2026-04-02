# Post-Hook: Deliverable Quality Control

## Objective

This hook is executed **after the agent has produced its deliverable**, before returning to the coordinator. The agent MUST run this complete checklist and correct any non-conforming items before considering the deliverable complete.

---

## Doc depth awareness

This hook adapts its checks based on the `doc_depth` setting in `docs/project.yml` (`essential`, `standard`, or `full`). If absent, default to `full`.

**Depth-specific relaxations:**
- **essential**: Traceability section is optional. Glossary cross-reference check is skipped (no glossary produced). Definition of Ready checklists are not required. Inline user stories and business rules in feature files are accepted (no separate files required).
- **standard**: Traceability section is optional. Definition of Ready checklists are not required.
- **full**: All checks apply without relaxation.

---

## Universal checklist (all deliverables)

### Form
- [ ] The YAML front matter is present and complete
- [ ] The status is set to `draft`
- [ ] The heading structure follows the hierarchy (H1 > H2 > H3 > H4)
- [ ] All traceable elements have a unique identifier with the correct prefix
- [ ] Cross-references point to existing identifiers
- [ ] The traceability section is present at the end of the document — **skip if `doc_depth` is `essential` or `standard`**
- [ ] The file naming follows the convention

### Content
- [ ] All business terms used are defined in the glossary — **skip if `doc_depth` is `essential`** (no glossary produced)
- [ ] No ambiguity: each sentence has only one possible interpretation
- [ ] No technical assumptions (no mention of databases, APIs, or frameworks) — **brownfield exception: constraints from the existing system referenced by `[ASIS-xxx]` are allowed**
- [ ] Example data uses realistic and concrete values
- [ ] The deliverable is self-contained: a reader can understand it with only the listed dependencies

### Structural conformance to the template
- [ ] All H2 sections from the corresponding template (`tpl-*.md`) are present in the produced deliverable. **Important:** when a `template_variant` is used (e.g., `tpl-feature-essential.md`), validate against that variant, not the full template.
- [ ] No residual placeholders (`<!-- ... -->`, `YYYY-MM-DD`, `[Project Name]`, `xxx` values, `TermName`, text between angle brackets `<...>`)
- [ ] All front matter fields are filled in (no empty or generic values)
- [ ] Minimum counts by deliverable type are respected (adjusted by depth):

#### Minimum counts — `full` depth (default)
  - Glossary: >= 5 defined terms
  - Actors & Roles: >= 2 actors, rights matrix present
  - Functional requirements: >= 3 requirements with `EX-xxx` identifiers
  - Domain model: >= 3 entities with attributes, Mermaid diagram present
  - Epics & Features: >= 1 epic with >= 2 features
  - Business rules: >= 3 rules with IF/THEN structure
  - User Stories: >= 2 Given/When/Then acceptance criteria per story
  - Test scenarios: at least 1 nominal scenario + 1 error scenario per covered business rule

#### Minimum counts — `standard` depth
  - Glossary: >= 5 defined terms
  - Actors & Roles: >= 2 actors, rights matrix present
  - Functional requirements: >= 3 requirements with `EX-xxx` identifiers
  - Domain model: >= 3 entities with attributes, Mermaid diagram present
  - Epics & Features: >= 1 epic with >= 2 features
  - User Stories: >= 2 Given/When/Then acceptance criteria per story

#### Minimum counts — `essential` depth
  - Epics & Features: >= 1 epic with >= 2 features
  - Features: >= 1 inline user story with >= 1 acceptance criterion per story
  - Features: >= 1 feature-level acceptance criterion (FAC-xxx)

---

## Next reader test

For each major section of the deliverable, evaluate whether the next consuming agent can act on it without ambiguity:

- **CONFIDENT**: complete, actionable content, no ambiguity detected — no marking required
- **PARTIAL**: content present but incomplete — document the gap in `## Attention Points`
- **INSUFFICIENT**: content too vague to be used — correct before delivering (do not deliver as-is)

> If >= 1 section is **INSUFFICIENT**, the agent MUST correct it before delivering. A PARTIAL section is acceptable if the gap is documented.

---

## Deliverable-type-specific checklists

### Vision & Scope
- [ ] The problem to be solved is clearly stated
- [ ] Objectives are measurable (not "improve the process")
- [ ] Excluded scope is explicitly listed
- [ ] Business constraints are identified

### Glossary
- [ ] Each term has a definition that does not contain the term itself
- [ ] Forbidden synonyms are listed
- [ ] No duplicates (one concept = one term)
- [ ] Terms are sorted alphabetically

### Actors & Roles
- [ ] Each actor has at least one role
- [ ] The rights matrix covers all entities x all roles
- [ ] "System" actors (external systems) are included

### Domain model
- [ ] Each entity has at least one attribute
- [ ] All cardinalities are specified (1-1, 1-N, N-N)
- [ ] Entities with a lifecycle have a state diagram
- [ ] Enums/value lists are exhaustively defined

### Epics
- [ ] Each epic has at least one feature
- [ ] Dependencies between features are identified
- [ ] Priority is indicated (MoSCoW or numeric)
- [ ] At least 3 acceptance criteria (EAC-xxx) in Given/When/Then format with concrete values
- [ ] EAC criteria test business outcomes spanning multiple features (not single-feature behaviour)
- [ ] Definition of Ready checklist is present (from template)

### Features
- [ ] Each feature is linked to an epic
- [ ] At least 2 acceptance criteria (FAC-xxx) in Given/When/Then format with concrete values — **`essential`: at least 1 FAC**
- [ ] FAC criteria test integrated capability (not individual story behaviour)
- [ ] Definition of Ready checklist is present (from template) — **skip if `doc_depth` is `essential` or `standard`**
- [ ] Functional boundaries (in scope / out of scope) are explicit
- [ ] **`essential` only:** Inline user stories are present with As/I want/So that format and at least 1 acceptance criterion each
- [ ] **`essential` only:** Inline business rules are present as concise bullet points

### Business rules
- [ ] Each rule has a condition (IF) and a consequence (THEN)
- [ ] Calculation rules include numerical examples
- [ ] Validation rules specify the error message
- [ ] Each rule references the concerned entities

### User Stories
- [ ] Format "As a [actor], I want [action] so that [benefit]"
- [ ] At least 2 acceptance criteria per story (CA-xxx)
- [ ] Criteria are in Given/When/Then format with concrete values
- [ ] The story is linked to a feature
- [ ] Applicable business rules are referenced — **skip if `doc_depth` is `standard`** (no separate BR files)
- [ ] Definition of Ready checklist is present (from template) — **skip if `doc_depth` is `standard`**

### User journeys
- [ ] The nominal flow (happy path) is complete end-to-end
- [ ] At least one alternative flow is documented
- [ ] At least one error flow is documented
- [ ] Each step references the associated screen or action

### Screen specifications
- [ ] Each input field has its type, constraints, and mandatory/optional status
- [ ] Conditional behaviours are described (show/hide, enable/disable)
- [ ] User messages are specified (success, error, confirmation)
- [ ] Actions (buttons) are listed with their behaviour

### Notifications
- [ ] The triggering event is identified
- [ ] Recipient(s) according to context are defined
- [ ] The channel is specified (email, in-app, SMS...)
- [ ] The message content is drafted with dynamic variables identified

### Test scenarios
- [ ] Each business rule has at least one test scenario
- [ ] There are nominal, boundary and error scenarios
- [ ] Test data is concrete (not "a valid value")
- [ ] The expected result is verifiable (not "the system works correctly")

### Existing system audit [ASIS-001]
- [ ] All identifiers use the `ASIS-` prefix
- [ ] Each assumed element is marked with "To validate"
- [ ] The Documentary Quality section honestly lists the gaps
- [ ] Sources are indicated for each documented element

### Delta analysis [DELTA-001]
- [ ] All elements from `[ASIS-001]` are covered in the delta matrix
- [ ] Each element has an explicit status: NOUVEAU, MODIFIE, PRESERVE or DEPRECIE
- [ ] MODIFIE elements have a description of the change (before vs after)
- [ ] Presumed PRESERVE statuses are flagged in Attention Points
- [ ] DELTA-xxx identifiers are correctly prefixed

---

## Self-verification process

After generating the deliverable, execute these steps:

1. Re-read the complete deliverable
2. Run the universal checklist (Form + Content + Structural conformance)
3. Run the next reader test section by section
4. Run the checklist specific to the deliverable type
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

## Attention Points format

```markdown
## Attention Points

> [PA-001] The term "framework contract" is used but not defined in the current glossary. To be clarified at the next workshop.
> [PA-002] The discount calculation rule requires business validation (assumption: discount applied to the pre-tax amount).
```
