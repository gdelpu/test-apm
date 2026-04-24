---
name: sdlc-ba-functional-design
description: 'Produce per-feature functional design deliverables: user stories, user journeys, screen specifications, notifications, test scenarios, test data, and the cross-feature E2E test plan.'
triggers: ['functional design', 'user stories', 'user journeys', 'screen specifications', 'test scenarios']
---

# Skill: sdlc-ba-functional-design

## Goal

Produce per-feature functional design deliverables: user stories, user journeys, screen specifications, notifications, test scenarios, test data, and the cross-feature E2E test plan.

## When to use

- After specification (S2) is complete with epics and features registered
- As System S3 in the `sdlc-ba` workflow
- Runs per-feature fan-out with conditional agents for screens, batches, and notifications

## Procedure

### Per-feature deliverables (fan-out on `features` collection):

#### Phase 1 — User Stories (agent 3.1)
1. Load the user story template from `resources/`
2. Read upstream: feature spec `[FT-xxx]`, business rules `[BRL-*]`, actors `[ACT-001]`
3. Produce atomic user stories with Given-When-Then acceptance criteria
4. Use the `edit/editFiles` tool to create `outputs/docs/1-prd/3-epics/{epic}/{feature}/us-{id}-{slug}.md` with identifier `[US-xxx]`

#### Phase 2 — User Journeys (agent 3.2) — depends on 3.1
1. Load the journey template from `resources/`
2. Chain user stories into end-to-end flows with Mermaid diagrams
3. Use the `edit/editFiles` tool to create `outputs/docs/1-prd/3-epics/{epic}/{feature}/uf-{id}-{slug}.md` with identifier `[UF-xxx]`

#### Phase 3 — Screen Specifications (agent 3.3) — conditional: `has_screens`
1. Load the screen spec template from `resources/`
2. Define components, fields, validation rules, and actions per screen
3. Use the `edit/editFiles` tool to create `outputs/docs/1-prd/3-epics/{epic}/{feature}/scr-{id}-{slug}.md` with identifier `[SCR-xxx]`

#### Phase 4 — Figma Prototypes (agent 3.3b) — conditional: `has_screens`, depends on 3.3
1. Scan ADR files (`outputs/docs/2-tech/1-architecture/adr/`) for design-system decisions; if an ADR mandates a specific design system, adopt its tokens and component conventions
2. Generate interactive HTML prototypes from screen specifications
3. Optional Figma MCP integration for design system sync

#### Phase 5 — Batch Specifications (agent 3.3c) — conditional: `has_batches`
1. Define batch process specifications: input/output formats, volumes, scheduling
2. Write batch specs with identifier `[BAT-xxx]`

#### Phase 6 — Notifications (agent 3.4) — conditional: `has_notifications`
1. Define notification definitions: channels, recipients, triggers, content templates
2. Write notification specs with identifier `[NTF-xxx]`

#### Phase 7 — Test Scenarios (agent 3.5) — depends on 3.2, 3.3, 3.3c, 3.4
1. Load the test scenario template from `resources/`
2. Produce Gherkin-format functional test scenarios with coverage matrices
3. Use the `edit/editFiles` tool to create `outputs/docs/1-prd/3-epics/{epic}/{feature}/sce-{id}-{slug}.md` with identifier `[SCE-xxx]`

#### Phase 8 — Test Data (agent 3.6) — depends on 3.5
1. Build structured test dataset catalogue with pre-conditions for each scenario
2. Use the `edit/editFiles` tool to create `outputs/docs/1-prd/4-tests/dat-test-001-seeds.md` with identifier `[DAT-TEST-001]`

### Project-scope consolidation (fan-in):

#### Phase 9 — E2E Test Plan (agent 3.6b) — depends on all 3.5 instances
1. Consolidate cross-US, cross-feature E2E test journeys
2. Prepare Xray campaign structure
3. Use the `edit/editFiles` tool to create `outputs/docs/1-prd/4-tests/e2e-plan-001.md` with identifier `[E2E-PLAN-001]`

## Output

Per feature: `[US-xxx]`, `[UF-xxx]`, `[SCR-xxx]`, `[BAT-xxx]`, `[NTF-xxx]`, `[SCE-xxx]`, `[DAT-TEST-001]`
Project scope: `[E2E-PLAN-001]`

## Rules

- Phase 1 (stories) is the entry point for each feature — no dependencies except the feature spec
- Conditional agents (screens, batches, notifications) only run when the feature has the corresponding flag
- Phase 7 (test scenarios) waits for all preceding per-feature phases
- Phase 9 (E2E plan) is project-scope fan-in — waits for ALL features' test scenarios
- Sprint scope filtering applies: only features in the current sprint scope are processed

## Resources

| Resource | Purpose |
|----------|---------|
| `docs/tpl-user-story.md` | User story with GWT criteria template |
| `docs/tpl-user-journey.md` | User journey flow template |
| `docs/tpl-screen-spec.md` | Screen specification template |
| `docs/tpl-notification.md` | Notification definition template |
| `docs/tpl-test-scenario.md` | Gherkin test scenario template |
| `docs/tpl-test-data.md` | Seeds catalogue template |
