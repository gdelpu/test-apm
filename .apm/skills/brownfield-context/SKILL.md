---
name: brownfield-context
description: 'Analyze an existing codebase to extract architectural context, patterns, constraints, and domain knowledge for brownfield projects.'
triggers: ['brownfield context', 'existing codebase analysis', 'legacy context', 'codebase discovery']
---

# Skill: brownfield-context

## Goal

Produce a context brief capturing the existing codebase's architecture, patterns, constraints, and domain terminology — enabling downstream specification and planning to respect the brownfield reality.

## When to use

- In idea-to-spec workflows when enriching an intent with existing system context
- In modernization workflows to establish the current-state baseline
- In refactoring workflows to understand existing patterns before proposing changes
- Whenever a feature must integrate into an existing system

## Procedure

1. Scan the repository structure for architectural patterns (monolith, microservices, monorepo, layered).
2. Identify frameworks, languages, and key dependencies from build/config files.
3. Document existing conventions (naming, folder structure, testing patterns).
4. Extract domain terms from code, comments, and documentation.
5. Identify integration points (APIs, databases, message queues, external services).
6. List do-not-break constraints (public APIs, shared contracts, database schemas).
7. Write the context brief.

## Output

`specs/features/<feature>/context-brief.md`

## Rules

- Focus on architectural facts and constraints, not implementation details.
- List discovered domain terms as a glossary section.
- Flag any anti-patterns or technical debt observed, but do not propose fixes.
