# Hook: DEP Post-Quality Control

## Objective

This hook runs **after** every DEP Agent finishes producing its deliverable. It performs a self-verification pass and fills the `## Production confidence` section of the output template.

---

## Phase 1 — Template conformance check

Verify that the produced file:
1. Has valid YAML front matter with all required fields (`id`, `title`, `type`, `status`, `author`).
2. Follows the structure of the declared template exactly (all sections present, no missing headers).
3. Contains no unfilled placeholders (`—`, `YYYY-MM-DD`, `[PROVIDER]`, etc.) in non-optional fields.
4. All code blocks (YAML, HCL, bash) are syntactically consistent (no obvious errors in structure).

---

## Phase 2 — Configuration quality check

Run asset-specific checks depending on the deliverable type:

### dep-ci deliverables
- [ ] `include:` block references `dep/library/ci-library` with `ref: production`
- [ ] At least `gitleaks` and `branch-lint` jobs are included
- [ ] `sonarqube` job is included (mandatory quality gate)
- [ ] Every included job has a justification in the "Selected jobs" table
- [ ] Branch strategy diagram is coherent with the configured `*_BRANCH_REGEX` variables
- [ ] `.gitlab-ci.yml` YAML structure is valid (proper indentation, no duplicate keys)

### dep-mw deliverables
- [ ] `git` module is always present
- [ ] Every module has a justification in the module inventory table
- [ ] Module versions are consistent with stack conventions (`[STK-001]`) when available
- [ ] `mw-config.yml` YAML is valid (modules list, name/version/configuration keys)
- [ ] Role-based guide covers all team roles identified in inputs

### dep-iac deliverables
- [ ] One launchpad per environment (dev / staging / prod) is defined
- [ ] Cloud provider is consistent with `[CTX-001]` environment constraints
- [ ] No hardcoded credentials or secrets in any generated file
- [ ] CI Library `iac` job integration is documented
- [ ] `main.tf` backend is configured for GitLab-managed Terraform state

---

## Phase 3 — Points of attention completeness

Verify:
- Every assumption made during generation is listed in `## ⚠ Points of attention`
- Every WARN from pre-input-validation hook is reflected as a point of attention
- No row has empty `Description` or `Action required` fields

---

## Phase 4 — Confidence score computation

Score one point per passing criterion group:

| # | Group | Pass condition |
|---|-------|----------------|
| 1 | Template conformance | All Phase 1 checks pass |
| 2 | Asset-specific quality | All Phase 2 checks for the deliverable type pass |
| 3 | Tech traceability | At least one upstream Tech-Agent deliverable referenced |
| 4 | Points of attention | All assumptions documented, no empty rows |
| 5 | Configuration usability | Generated config file (YAML/HCL) is copy-paste ready |

**Confidence score: N/5**

---

## Phase 5 — Fill Production confidence section

Replace the `## Production confidence` section in the deliverable with:

```markdown
## Production confidence

| Criterion | Status | Notes |
|-----------|--------|-------|
| Template conformance | ✅ / ⚠ / ❌ | [detail] |
| Asset-specific quality | ✅ / ⚠ / ❌ | [detail] |
| Tech traceability | ✅ / ⚠ / ❌ | [detail] |
| Points of attention | ✅ / ⚠ / ❌ | [detail] |
| Configuration usability | ✅ / ⚠ / ❌ | [detail] |

**Confidence score: N/5**
```

Legend: ✅ Pass | ⚠ Partial / Warning | ❌ Fail
