# Modernization Playbook

Staged migration guide for legacy system modernization.

## Prerequisites

- Existing system accessible for analysis.
- Business case for modernization defined.
- Stakeholder alignment on scope and timeline.

## Phases

### Phase 1: Baseline

- Run `repository-analyzer` agent for architecture discovery.
- Document current technology stack, dependencies, and pain points.
- Map existing test coverage and quality metrics.
- Capture current performance baselines.

### Phase 2: Target definition

- Define target architecture and technology choices.
- Decision records for each significant choice (ADR format).
- Coexistence strategy: how old and new systems interact during migration.

### Phase 3: Architecture review

- Review target against `knowledge/governance/architecture-principles.md`.
- Verify migration path maintains security posture.
- Confirm observability is preserved or improved.

### Phase 4: Migration plan

- Break migration into phases with independent value delivery.
- Each phase must be rollback-safe.
- Data migration plan with integrity verification.
- Load testing targets for each phase.

### Phase 5: Risk assessment

- Identify migration blockers and dependencies.
- Map data integrity risks.
- Define failure scenarios and recovery procedures.

### Phase 6: Task breakdown

- One phase at a time — avoid big-bang migrations.
- Include parity verification tasks (old vs. new behavior).
- Include performance comparison tasks.

### Phase 7: Execute

- Implement phase by phase.
- Verify parity after each phase.
- Run quality validation workflow.
- Monitor production metrics during and after cutover.

## Key principles

- **Coexistence over cutover**: old and new must run side by side.
- **Rollback at every phase**: never burn bridges.
- **Parity verification**: prove the new system behaves like the old one.
- **Incremental value**: each phase delivers independently usable improvements.

## Workflow shortcut

Run: `./providers/cli/run-workflow.sh modernization <feature>`
