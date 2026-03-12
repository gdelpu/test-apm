---
name: 'A6 – GitHub Update'
description: 'Post a structured PR comment summarising all station findings and apply labels based on the gate decision.'
---

# Station A6 — GitHub Update

## Goal

Apply the gate decision to the PR: post a formatted comment, apply labels, and optionally
request a review from the designated human approver team.

## Inputs

- `station_out/gate_decision.json`
- `station_out/work_order.json`
- All station reports: `policy_report.json`, `security_report.json`, `promptsec_report.json`, `sim_report.json`
- GitHub PR number (from `work_order.json`)

## Actions

### 1 — Apply labels

Using `gh pr edit --add-label`:

- Apply every label listed in `gate_decision.json` → `"labels"`.
- If a previous run added `agent-factory:approved` or `agent-factory:blocked`, remove the
  stale label before adding the new one (a PR should carry exactly one outcome label at a time).

### 2 — Request review (REVIEW decision only)

If `gate_decision.json` → `"decision" == "REVIEW"`, request a review from the
`@<org>/agent-security-approvers` team:

```bash
gh pr edit {PR_NUMBER} --add-reviewer <org>/agent-security-approvers
```

### 3 — Post PR comment

Delete any existing `<!-- agent-factory-report -->` comment from a prior run, then post a new one.

#### Comment template

```markdown
<!-- agent-factory-report -->
## 🏭 Agent Factory Report

**Decision**: {DECISION_BADGE}
**Scanned**: {TIMESTAMP}
**PR**: {PR_TITLE} by @{AUTHOR}

---

### Station Summary

| Station | Status | Findings |
|---------|--------|----------|
| A0 Intake | ✅ pass | — |
| A1 Policy & Structure | {A1_STATUS_BADGE} | {A1_SUMMARY} |
| A2 Security Static | {A2_STATUS_BADGE} | {A2_SUMMARY} |
| A3 Prompt Injection | {A3_STATUS_BADGE} | {A3_SUMMARY} |
| A4 Sandbox Simulation | {A4_STATUS_BADGE} | {A4_SUMMARY} |

---

### {BLOCK_OR_REVIEW_SECTION}

{BLOCKING_FINDINGS_TABLE_OR_NONE}

---

### Warnings & Informational

{WARNINGS_TABLE_OR_NONE}

---

<details>
<summary>Full report artifacts</summary>

- `station_out/work_order.json`
- `station_out/policy_report.json`
- `station_out/security_report.json`
- `station_out/promptsec_report.json`
- `station_out/sim_report.json`
- `station_out/gate_decision.json`

</details>
```

#### Decision badges

| Decision | Badge markdown |
|----------|---------------|
| APPROVE | `✅ **APPROVED** — safe to merge` |
| BLOCK | `❌ **BLOCKED** — critical issues must be resolved` |
| REVIEW | `⚠️ **NEEDS REVIEW** — human approval required before merge` |

#### Status badges

| Status | Badge |
|--------|-------|
| `pass` | `✅ pass` |
| `fail` | `❌ fail` |
| `skipped` | `⏭ skipped` |

#### Blocking findings table

If `blocking_findings` is non-empty, render:

```markdown
### ❌ Blocking Findings

| Station | Check | Severity | File | Message |
|---------|-------|----------|------|---------|
| A3 | PI-01 | 🔴 critical | `default/agents/example.agent.md` | Instruction-override phrase detected |
```

If empty, render: `_No blocking findings._`

#### Warnings table

Render only `medium` and `low` findings from all station reports:

```markdown
| Station | Check | Severity | Message |
|---------|-------|----------|---------|
| A1 | P-05 | 🔵 low | Description is 12 characters — consider expanding |
```

## Notes

- Always include `<!-- agent-factory-report -->` as the first line of the comment so
  subsequent runs can find and replace it.
- Keep the comment under 65,000 characters (GitHub limit); truncate `sim_report` details if needed.
- Do not expose raw secret values from `security_report.json` in the PR comment —
  refer to them as `"[REDACTED]"` and note the line number only.
