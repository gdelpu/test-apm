---
name: 'A7 – GitLab Update'
description: 'Post a structured MR note summarising all station findings and apply labels based on the gate decision via the GitLab REST API.'
---

# Station A7 — GitLab Update

## Goal

Apply the gate decision to the merge request: post a formatted note, apply labels, and optionally
request a review from the designated human approver group.

## Inputs

- `station_out/gate_decision.json`
- `station_out/work_order.json`
- All station reports: `policy_report.json`, `security_report.json`, `promptsec_report.json`, `sim_report.json`
- GitLab MR IID (from `CI_MERGE_REQUEST_IID` or `work_order.json`)

## Environment Variables Required

| Variable | Source | Purpose |
|----------|--------|---------|
| `CI_API_V4_URL` | GitLab CI predefined | Base URL for REST API calls |
| `CI_PROJECT_ID` | GitLab CI predefined | Numeric project ID |
| `CI_MERGE_REQUEST_IID` | GitLab CI predefined | Merge request internal ID |
| `GITLAB_TOKEN` | CI/CD secret variable | PAT or project token with `api` scope |

## Actions

### 1 — Apply labels

Using the GitLab Labels API (`PUT /projects/:id/merge_requests/:iid`):

- Read the current MR labels via `GET /projects/${CI_PROJECT_ID}/merge_requests/${CI_MERGE_REQUEST_IID}`.
- Remove any stale outcome label (`agent-factory:approved`, `agent-factory:blocked`, `agent-factory:needs-review`) from the existing set.
- Merge in every label listed in `gate_decision.json` → `"labels"`.
- `PUT` the updated label list back to the MR.

A merge request should carry exactly one outcome label at a time.

### 2 — Request review (REVIEW decision only)

If `gate_decision.json` → `"decision" == "REVIEW"`, add the
`agent-security-approvers` group as a reviewer via the Merge Request Approvals API:

```bash
curl --fail-with-body -s \
  -X POST "${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/merge_requests/${CI_MERGE_REQUEST_IID}/approvals" \
  -H "PRIVATE-TOKEN: ${GITLAB_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"group_ids": [<AGENT_SECURITY_APPROVERS_GROUP_ID>]}'
```

### 3 — Post MR note

Delete any existing note whose body starts with `<!-- agent-factory-report -->` from a prior run
(list notes via `GET .../merge_requests/:iid/notes`, find the matching one, `DELETE` it),
then `POST` a new note.

#### Note template

```markdown
<!-- agent-factory-report -->
## 🏭 Agent Factory Report

**Decision**: {DECISION_BADGE}
**Scanned**: {TIMESTAMP}
**MR**: !{MR_IID} — {MR_TITLE} by @{AUTHOR}

---

### Station Summary

| Station | Status | Findings |
|---------|--------|----------|
| A0 Intake | ✅ pass | — |
| A1 Policy & Structure | {A1_STATUS_BADGE} | {A1_SUMMARY} |
| A2 Security Static | {A2_STATUS_BADGE} | {A2_SUMMARY} |
| A3 Prompt Injection | {A3_STATUS_BADGE} | {A3_SUMMARY} |
| A4 Red Team | {A4_STATUS_BADGE} | {A4_SUMMARY} |
| A5 Sandbox Simulation | {A5_STATUS_BADGE} | {A5_SUMMARY} |

---

### {BLOCK_OR_REVIEW_SECTION}

{BLOCKING_FINDINGS_TABLE_OR_NONE}

---

### Warnings & Informational

{WARNINGS_TABLE_OR_NONE}

---

<details>
<summary>Full report artifacts</summary>

Download from the pipeline's job artifacts:
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

## API Reference

All calls use `${CI_API_V4_URL}` as the base and authenticate with `PRIVATE-TOKEN: ${GITLAB_TOKEN}`.

| Action | Method | Endpoint |
|--------|--------|----------|
| Get MR details | `GET` | `/projects/:id/merge_requests/:iid` |
| Update MR labels | `PUT` | `/projects/:id/merge_requests/:iid` |
| List MR notes | `GET` | `/projects/:id/merge_requests/:iid/notes` |
| Delete a note | `DELETE` | `/projects/:id/merge_requests/:iid/notes/:note_id` |
| Create a note | `POST` | `/projects/:id/merge_requests/:iid/notes` |
| Set approvers | `POST` | `/projects/:id/merge_requests/:iid/approvals` |

## Notes

- Always include `<!-- agent-factory-report -->` as the first line of the note body so
  subsequent pipeline runs can find and replace it.
- Keep the note under 1,000,000 characters (GitLab note body limit); truncate `sim_report` details if needed.
- Do not expose raw secret values from `security_report.json` in the MR note —
  refer to them as `"[REDACTED]"` and note the line number only.
- If `GITLAB_TOKEN` is not set, skip all API calls and log a warning instead of failing the pipeline.
