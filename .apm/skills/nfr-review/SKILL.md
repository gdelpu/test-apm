---
name: nfr-review
description: 'Review and define non-functional requirements (NFRs) covering security, performance, resilience, observability, and accessibility with measurable targets.'
triggers: ['NFR review', 'non-functional requirements', 'quality attributes', 'NFR definition', 'cross-cutting concerns']
---

# Skill: nfr-review

## Goal

Review and define non-functional requirements ensuring that security, performance, resilience, observability, and accessibility concerns are explicitly addressed with measurable targets.

## When to use

- In idea-to-spec workflows after the feature spec is drafted
- In spec-kit and feature-implementation workflows during specification review
- In release-readiness checks to verify NFR coverage
- In modernization workflows to establish target-state quality attributes
- When the spec-orchestrator needs to enrich a spec with cross-cutting concerns

## Procedure

1. Load the feature specification and any existing clarifications.
2. Load the constitution for baseline quality expectations.
3. Review each NFR category against the spec:
   - **Security**: authentication, authorization, data protection, input validation
   - **Performance**: response time, throughput, scalability targets
   - **Resilience**: failure modes, recovery time, graceful degradation
   - **Observability**: logging, metrics, tracing, alerting
   - **Accessibility**: WCAG compliance level, keyboard navigation, screen reader support
   - **Compatibility**: browser/device/API version support
4. For each NFR, define a measurable target (e.g., "p95 response time < 200ms").
5. Identify gaps — NFR categories with no coverage in the spec.
6. Propose additions for missing NFRs based on constitution defaults.
7. Write the NFR review document.

## Output

`specs/features/<feature>/nfr-review.md`

## Gate criteria

- **Pass**: All categories reviewed, each NFR has a measurable target, no gaps in security or performance
- **Fail**: Missing security or performance NFRs, or NFRs without measurable targets
- **Conditional**: Minor gaps in non-critical categories (e.g., accessibility for internal tools)

## Rules

- Every NFR must have a measurable, testable target — avoid vague statements like "should be fast".
- Security and performance NFRs are mandatory; others depend on project context.
- NFRs must be traceable to test strategy items.
- When the constitution defines baseline expectations, NFRs must meet or exceed them.
