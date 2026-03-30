# Brownfield Playbook

Step-by-step guide for changes to existing systems.

## Prerequisites

- Access to the existing codebase and documentation.
- Understanding of the change scope.

## Steps

### 1. Reverse brief

- Document the current state: architecture, dependencies, data flows.
- Map existing tests and coverage.
- Identify affected modules and stakeholders.
- Use the `repository-analyzer` agent for automated discovery.

### 2. Define target state

- What changes are needed and why.
- Backward compatibility requirements.
- Coexistence strategy (old + new running together).

### 3. Architecture review

- Minimal blast radius: change only what's necessary.
- Check dependency impacts.
- Verify against architecture principles.

### 4. Migration plan

- Phased approach with rollback at each phase.
- Data migration strategy if applicable.
- Feature flag / toggle strategy.

### 5. Risk assessment

- Identify breaking changes.
- Map regression risk per module.
- Define monitoring targets for the transition period.

### 6. Task breakdown

- Traceable to spec and reverse brief.
- Include regression test tasks.
- Include rollback verification tasks.

### 7. Implement

- Test-first: extend existing test suite first.
- Verify coexistence at each step.
- Run quality validation workflow.

## Workflow shortcut

Run the full sequence: `./providers/cli/run-workflow.sh modernization <feature>`
