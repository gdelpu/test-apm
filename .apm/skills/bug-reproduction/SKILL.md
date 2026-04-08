---
name: bug-reproduction
description: 'Create reliable reproduction scenarios for bugs with documented steps, environment conditions, and expected vs actual behavior.'
triggers: ['bug reproduction', 'reproduce bug', 'reproduction steps', 'repro scenario']
---

# Skill: bug-reproduction

## Goal

Produce a reliable reproduction scenario for a bug, documenting exact steps, environment conditions, and the gap between expected and actual behavior.

## When to use

- In incident-resolution workflows to verify the incident can be reproduced
- In bug-fixing workflows after triage to confirm the bug before root-cause analysis
- Whenever a bug report needs verification

## Procedure

1. Load the bug report or incident analysis for context.
2. Identify the minimal conditions needed to trigger the bug.
3. Document the environment: OS, runtime version, dependencies, configuration.
4. Write step-by-step reproduction instructions.
5. State expected behavior vs actual behavior.
6. Verify the reproduction is reliable (triggers consistently, not intermittent).
7. If intermittent, document the frequency and any correlation patterns.
8. Note any simplifications made (reduced dataset, mock services, etc.).

## Output

`specs/features/<feature>/reproduction.md`

## Rules

- Reproduction steps must be executable by someone unfamiliar with the code.
- Environment conditions must be specific (versions, not "latest").
- If the bug cannot be reproduced, document what was attempted and why it failed.
