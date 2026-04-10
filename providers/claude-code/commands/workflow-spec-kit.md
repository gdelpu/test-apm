# /workflow-spec-kit

Run the Spec Kit workflow to produce a complete specification without implementation.

## Pre-flight: detect project context

Before executing any station, determine whether this is a **brownfield** (existing system) or **greenfield** (new project). Ask the user if not already clear.

## Steps

1. Read `.apm/workflows/spec-kit.yml` for the station sequence.
2. **Always start at station 1 (constitution)** — never skip ahead to specification.
   Use the brownfield or greenfield constitution template accordingly.
3. For brownfield projects, execute the `brownfield-context` station next
   to produce `context-brief.md` with existing architecture and constraints.
4. Continue through the remaining stations in order:
   specification → clarification → architecture review → plan → tasks →
   test strategy → quality gate.
5. **Write every artifact as an actual file on disk** under `outputs/specs/features/<feature>/`. Do not merely display content in chat — use file-writing tools to create each file.
6. After each station, verify that declared output files exist on disk before proceeding.

## Inputs

- Feature name or description from user
- Project context: brownfield or greenfield

## Outputs

- `outputs/specs/features/<feature>/constitution.md`
- `outputs/specs/features/<feature>/context-brief.md` (brownfield only)
- `outputs/specs/features/<feature>/spec.md`
- `outputs/specs/features/<feature>/clarifications.md`
- `outputs/specs/features/<feature>/architecture-review.md`
- `outputs/specs/features/<feature>/plan.md`
- `outputs/specs/features/<feature>/tasks.md`
- `outputs/specs/features/<feature>/test-strategy.md`
- `outputs/specs/features/<feature>/quality-gate.md`
