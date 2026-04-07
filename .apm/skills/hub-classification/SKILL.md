---
name: hub-classification
description: 'Classify user intent against available workflows and agents, then recommend the best match for dispatch.'
triggers:
  - start
  - help
  - what workflow
  - which agent
  - how do I
  - where do I begin
---

# Hub Classification Skill

Classify user intent and recommend the appropriate workflow or agent from the
ai-sdlc-foundation catalog.

## Inputs

- **User message**: the raw request or question from the user.
- **Hub catalog**: `.apm/contexts/hub-catalog.yaml` — the cached index of all
  workflows (name, description, type, stations, when_to_use) and agents
  (name, description, tools).
- **In-progress state** (optional): any `specs/features/*/workflow-state.md`
  files indicating workflows that can be resumed.

## Classification Protocol

### Step 1 — Load catalog

Read `.apm/contexts/hub-catalog.yaml`. If the file is missing, fall back to
dynamic introspection: read `.apm/workflows/*.yml` (name, description, type)
and `.apm/agents/*.md` (frontmatter: name, description).

### Step 2 — Check for in-progress work

Scan `specs/features/*/workflow-state.md` for existing workflow executions.
If any exist, include in the response: "You have in-progress work on [feature].
Would you like to resume?"

### Step 3 — Fast path (keyword match)

Match the user message against catalog entries:

| Signal pattern | Recommended target | Type |
|---|---|---|
| "new feature", "implement", "build", "create", "add functionality" | `feature-implementation` workflow | delivery |
| "bug", "fix", "broken", "regression", "defect" | `bug-fixing` workflow | delivery |
| "modernize", "upgrade", "migrate", "refactor framework" | `modernization` workflow | modernization |
| "production down", "incident", "outage", "P1" | `incident-resolution` workflow | delivery |
| "spec", "specification", "requirements", "define" | `spec-kit` or `idea-to-spec` workflow | specification |
| "quality", "lint", "test coverage", "security scan" | `quality-validation` workflow | validation |
| "PR", "merge request", "code review" | `pr-validation` workflow | validation |
| "compliance", "GDPR", "PII", "AI Act" | `compliance-check` workflow | validation |
| "release", "go-live", "deploy readiness" | `release-readiness` workflow | validation |
| "maturity", "assessment", "health check" | `maturity-assessment` workflow | assessment |
| "retrospective", "retro", "improvement" | `delivery-retrospective` workflow | assessment |
| "full project", "full SDLC", "entire lifecycle" | `sdlc-full` workflow | SDLC harness |
| "business analysis", "BA", "PRD", "user stories" | `sdlc-ba` workflow | SDLC harness |
| "architecture", "ADR", "tech design" | `sdlc-tech` workflow | SDLC harness |
| "sprint", "governance", "COPIL", "steering" | `sdlc-steer` workflow | SDLC harness |
| "analyze repo", "codebase overview", "understand code" | `repository-analyzer` agent | analysis |
| "backlog from code", "reverse engineer" | `reverse-backlog-generator` agent | analysis |
| "brand", "Sopra Steria style", "branding" | `brand-styler` or `ssg-branding-agent` agent | branding |
| "security review", "prompt injection", "LLM security" | `security-reviewer` agent | security |
| "BMAD", "hypothesis", "measure" | `bmad` workflow | delivery |
| "tasks from spec", "plan to tasks" | `spec-to-execution` workflow | specification |
| "list workflows", "what's available", "show catalog" | Display full catalog | catalog |
| "compare", "difference between", "X vs Y" | Compare two entries side-by-side | catalog |

If a fast-path match is found with high confidence (user message clearly aligns
with one entry), skip the interview and go directly to Step 5.

### Step 4 — Interview path (when ambiguous)

Ask structured questions to narrow the recommendation. Stop as soon as
a confident match is found — do not ask unnecessary questions.

**Q1 — Goal category**
> What are you trying to achieve?
> - Build a new feature
> - Fix a bug or defect
> - Modernize / upgrade / migrate
> - Assess quality or compliance
> - Run a full project lifecycle (BA + Tech + Test + Governance)
> - Respond to a production incident
> - Brand or style documents
> - Analyze or understand a codebase
> - Something else

**Q2 — Context** (if Q1 narrows to delivery/specification)
> - Is this a greenfield (new) or brownfield (existing) system?
> - Do you have an existing specification, or do we need to create one first?

**Q3 — Scope** (if multiple workflows still match)
> - Single feature or multi-feature / full program?
> - Sprint-scoped or full project?

**Q4 — Governance** (if SDLC harness is a candidate)
> - Do you need formal gates with human review?
> - Do you need Confluence publishing and traceability chains?

After each answer, re-evaluate the candidate list. When only one strong
candidate remains, proceed to Step 5.

### Step 5 — Propose and confirm

Present the recommendation with enough context for an informed decision:

```
I recommend: **[Workflow/Agent Name]**
- Type: [delivery | validation | assessment | modernization | SDLC harness]
- Stations: [N] (for workflows)
- Purpose: [one-line description]
- When to use: [matching bullet from catalog]

Shall I start execution?
```

If two candidates are close, present both and let the user choose.

### Step 6 — Dispatch

On user confirmation, signal the hub-orchestrator to dispatch:

- **Workflow dispatch**: provide workflow name + feature path to `workflow-orchestrator`
- **SDLC harness dispatch**: provide workflow name to `sdlc-coordinator`
- **Agent dispatch**: invoke the agent directly
- **Pass-through flags**: forward any `--scope`, `--resume`, `--station`,
  `--skip-gate`, `--dry-run` flags from the user message

## Outputs

- **Recommendation**: workflow or agent name, with justification
- **Dispatch signal**: target orchestrator + parameters for execution
- **Catalog view** (if requested): full list grouped by type

## Fallback

If no confident match is found after the interview:

1. Show the full catalog grouped by type (delivery, validation, assessment,
   modernization, SDLC harness).
2. For each entry, show name + one-line description.
3. Ask the user to pick or refine their request.
