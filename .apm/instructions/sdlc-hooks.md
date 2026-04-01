# SDLC Lifecycle Hooks

These hooks apply to all SDLC domain agents (BA, Tech, Steer, Test).
They run at defined points in every skill execution cycle.

## Execution Order

```
pre-input-validation → pre-amendment-mode → [SKILL EXECUTION] → post-quality-control → post-confluence-push
```

---

## 1. Pre-Hook: Input Validation (Phase 0)

Runs **before any production**. Validates that all declared inputs are present, valid, and semantically sufficient.

### Phase 0a — Presence & Status Check

**Mandatory inputs:**
- File is available at declared path
- YAML front matter contains `id` matching expected identifier
- `status` field is `validated` (not `draft` or absent)
- Declared `dependencies` are themselves satisfied (1-level cascade)

If any mandatory input fails → STOP → produce blocking report instead of deliverable.

**Recommended inputs (optional):**
- If absent: note gap in `Production confidence` section, continue
- If present with `status: draft`: treat as degraded confidence → WARN

**Brownfield audit agents (S0):** operate in adaptive mode (A/B/C). Selected mode replaces status verification.

### Phase 0b — Sufficiency Criteria Evaluation

For each available input, evaluate its `**Sufficiency criteria**` block:
- **BLOCK**: cannot reason correctly → stop + blocking report
- **WARN**: production possible with uncertainty zones documented
- **GO**: all critical criteria satisfied

### Phase 0c — Global Decision

| Score | Condition | Action |
|-------|-----------|--------|
| **GO** | All mandatory present + validated + GO threshold | Continue normally |
| **WARN** | Mandatory OK, ≥ 1 WARN on sufficiency | Continue with flag in `Production confidence` |
| **STOP** | ≥ 1 mandatory absent / not validated / BLOCK | Stop → blocking report |

### Blocking Report Format

```markdown
# Blocking Report — [Agent ID] — [date]

## Blocking inputs
| Input | Problem | Impact |
|-------|---------|--------|

## Warning inputs
| Input | Problem | Estimated impact |
|-------|---------|-----------------|

## Required actions
1. [Action to resolve blocker]

## Next step
Re-run agent with corrected inputs.
```

---

## 2. Pre-Hook: Amendment Mode

**Activation:** If no `[IMPACT-xxx]` is provided → skip hook → creation mode.

When an existing deliverable and targeted modifications (delta items from IMPACT file) are provided:

### Rules
1. Apply ONLY the listed delta items — nothing else
2. Do not reformulate, reorganize, or improve content outside scope
3. **Addition**: insert at correct location, assign next sequential ID
4. **Suppression**: remove element AND clean all cross-references
5. **Quasi-code** (SQL, OpenAPI, k6, Mermaid): edit only targeted lines
6. **YAML front matter**: set `status: draft`, add `amended_by: IMPACT-xxx` and `amendment_date`
7. **Amendment log**: append at end of deliverable:

```markdown
## Amendment log
| Date | IMPACT | Element | Type | Summary |
|------|--------|---------|------|---------|
```

---

## 3. Post-Hook: Deliverable Quality Control

Runs **after production**, before returning to coordinator. Correct any non-conforming items.

### Universal Checklist

**Form:**
- YAML front matter present and complete
- Status set to `draft`
- Heading hierarchy correct (H1 > H2 > H3 > H4)
- All traceable elements have unique identifier with correct prefix
- Cross-references point to existing identifiers
- Traceability section present at end
- File naming follows convention

**Content:**
- All business terms defined in glossary
- No ambiguity: each sentence has one interpretation
- No technical assumptions (brownfield exception: `[ASIS-xxx]` constraints allowed)
- Example data uses realistic values
- Deliverable is self-contained

**Template Conformance:**
- All H2 sections from corresponding `tpl-*.md` present
- No residual placeholders
- All front matter fields filled
- Minimum counts respected per deliverable type

### Next Reader Test

For each major section:
- **CONFIDENT**: complete, actionable — no marking
- **PARTIAL**: incomplete — document gap in `## Attention Points`
- **INSUFFICIENT**: too vague — correct before delivering

If ≥ 1 INSUFFICIENT → agent MUST correct before delivering.

---

## 4. Post-Hook: Confluence Push

Runs **after quality control** as last step. Pushes deliverable to Confluence.

### Prerequisites (checked by reading files on disk)
1. `docs/project.yml` → `confluence_enabled` field (`false` = skip, `true`/absent = proceed)
2. `.env` → `CONFLUENCE_INSTANCE_URL`, `CONFLUENCE_USER_EMAIL`, `CONFLUENCE_API_TOKEN`, `CONFLUENCE_SPACE_KEY`
3. `tools/confluence-config.yaml` → `instance_url` and `space_key`
4. Pandoc installed
5. `mmdc` (mermaid-cli) — optional

### Execution
If prerequisites met → run `node tools/confluence-publish.js <file>`.
If missing → skip with warning and continue. Never block delivery on Confluence failure.
