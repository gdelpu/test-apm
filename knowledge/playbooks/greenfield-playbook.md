# Greenfield Playbook

Step-by-step guide for new feature or project delivery.

## Prerequisites

- Feature idea or requirement documented.
- Stakeholders identified.

## Steps

### 1. Establish constitution

Define quality, security, testing, and performance standards.
Reference `knowledge/constitution/enterprise-defaults.md` for baseline.

### 2. Write specification

- Scope: what is included and excluded.
- Acceptance criteria: testable, measurable.
- Non-functional requirements: performance, security, accessibility.

### 3. Clarify ambiguities

- List unknowns and assumptions.
- Get stakeholder confirmation on blocking items.
- Update spec with resolutions.

### 4. Architecture review

- Review against `knowledge/governance/architecture-principles.md`.
- Check security posture against `knowledge/governance/secure-by-default.md`.
- Verify testing approach against `knowledge/governance/testing-policy.md`.

### 5. Implementation plan

- Break into phases with clear milestones.
- Identify risks and define rollback strategies.
- Define rollout approach (feature flags, canary, blue-green).

### 6. Task breakdown

- One task per unit of testable work.
- Trace each task to spec acceptance criteria.
- Include testing tasks as first-class items.

### 7. Implement

- Follow test-first: write test → implement → verify.
- Self-review before PR/MR.
- Run quality validation workflow before marking complete.

### 8. Quality gate

- Run `quality-validation` workflow.
- Verify all acceptance criteria pass.
- Get peer review approval.

## Workflow shortcut

Run the full sequence: `./providers/cli/run-workflow.sh feature-implementation <feature>`
