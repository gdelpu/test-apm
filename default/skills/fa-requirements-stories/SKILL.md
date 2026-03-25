---
name: fa-requirements-stories
description: 'Produces persona-driven user stories, epics, requirements documentation, MoSCoW prioritisation, and traceability matrices following BABOK V3 methodology for functional analysis projects.'
triggers: ['user story', 'persona', 'requirements', 'epic', 'MoSCoW', 'acceptance criteria', 'traceability matrix', 'backlog', 'requirements document', 'definition of done', 'story points']
version: '1.0.0'
author: 'soprasteria'
---

# Skill: FA Requirements & User Stories

## Purpose

Generates structured requirements documentation and persona-driven user stories aligned with BABOK V3. Covers persona development, epic/story hierarchies, Gherkin acceptance criteria, MoSCoW prioritisation, and full requirements traceability.

## When to Apply

Use this skill when:
- Creating or refining user stories and epics
- Developing stakeholder personas
- Writing requirements documentation (business, functional, non-functional)
- Building a requirements traceability matrix
- Applying MoSCoW prioritisation
- Defining acceptance criteria in Gherkin format
- Compiling a full deliverables catalogue after discovery

---

## Persona Template

Before writing user stories, develop detailed personas for each key stakeholder group.

### Persona Structure

```
### Persona: [Name] - [Role Title]

Archetype Name: [Memorable name]
Role: [Official role/title]
Category: [Primary / Secondary / Tertiary Stakeholder]

#### Demographics & Context
- Professional Background: [Experience, domain expertise]
- Technical Proficiency: [Low / Medium / High / Expert]
- Location/Environment: [Where they work]

#### Goals & Motivations
Primary Goals:
1. [Goal 1]
2. [Goal 2]
3. [Goal 3]

Personal Motivators:
- [What drives this person]
- [What success means to them]

#### Pain Points & Frustrations
Current Challenges:
1. [Pain point 1]
2. [Pain point 2]
3. [Pain point 3]

Impact: [How these problems affect their work]

#### Needs from Solution
Must Have: [Critical needs]
Should Have: [Important but not critical]
Nice to Have: [Enhancements]

#### Behaviour Patterns
- Technology usage and preferences
- Communication preferences
- Decision-making style

#### Stakeholder Relationships
Reports To: [Who]
Collaborates With: [Key collaborators]
Influences: [Who they influence]

#### Engagement Profile
System Interaction Frequency: [Daily / Weekly / Monthly]
Primary Use Context: [When/where they use the system]
```

---

## User Story Format (Mandatory)

All user stories must be persona-driven. Generic stories ("As a user") are not permitted.

### Story Template

```
### User Story: US-[NNN] - [Story Title]

Epic: [EPIC-ID] - [Epic Name]
Persona: [Persona Name] (Role: [Role Title])

As a [persona name], a [role] who [context about their situation and constraints],
I want to [specific goal or action],
So that [business value or outcome tied to persona goals].

#### Context & Background
Current Situation: [Pain point or opportunity]
Desired Outcome: [What changes for this persona]
Business Value: [Connected to strategic objectives]

#### Acceptance Criteria

Scenario 1: [Happy Path]
  GIVEN [initial context and preconditions]
  AND [additional context if needed]
  WHEN [action or trigger event]
  AND [additional action if needed]
  THEN [expected system response]
  AND [visible feedback to user]

Scenario 2: [Alternative Path]
  GIVEN [alternative context]
  WHEN [alternative action]
  THEN [alternative outcome]

Scenario 3: [Error Handling]
  GIVEN [error-prone context]
  WHEN [action that triggers error]
  THEN [expected error handling]
  AND [system remains in valid state]

Scenario 4: [Edge Case]
  GIVEN [edge case context]
  WHEN [edge case action]
  THEN [edge case outcome]

#### Fields
Business Value: [Clear value statement]
Priority: [MoSCoW: Must Have / Should Have / Could Have / Won't Have]
Effort Estimate: [Story Points: 1/2/3/5/8/13/21]
Dependencies: [Blocked by / Blocks]

#### Definition of Done
- Code implemented and reviewed
- Unit tests written and passing (>80% coverage)
- Integration tests passing
- Acceptance criteria verified
- Documentation updated
- Product Owner acceptance obtained
```
---

## Epic Structure

```
## Epic: EPIC-[NN] - [Epic Name]

Summary: [One-line, max 255 characters]

Business Context: [Why this epic exists]
Business Objective: [Which strategic objective it supports]
Scope: [What is included]
Out of Scope: [What is excluded]

### Epic Acceptance Criteria
- [High-level criterion 1]
- [High-level criterion 2]

### Stakeholders
Primary: [Most affected group]
Secondary: [Other groups]

### Child Stories
Story ID - Title - Priority - Points

### Dependencies
Depends On: [EPIC-NN] - [Reason]
Blocks: [EPIC-NN] - [Reason]

### Risks
Risk - Probability - Impact - Mitigation
```

---

## MoSCoW Prioritisation

### Definitions

**MUST HAVE (M)**
- Critical for launch/release
- System cannot function without it
- Legal/regulatory requirement
- No workaround exists

**SHOULD HAVE (S)**
- Important but not critical for launch
- Significant business value
- Workaround exists but is inconvenient
- Can be deferred to next release if necessary

**COULD HAVE (C)**
- Desirable enhancement
- Would improve user experience
- Can be easily deferred
- Low risk if excluded

**WON'T HAVE (W)**
- Acknowledged but explicitly excluded from current scope
- May be considered in future releases
- Documented for transparency

---

## Requirements Documentation

### Business Requirements
File: `requirements/business-requirements.md`

Structure per requirement: ID, Requirement description, Type (Business), Priority (MoSCoW), Source, Linked User Story, Status.

### Functional Requirements
File: `requirements/functional-requirements.md`
Same structure; type = Functional.

### Non-Functional Requirements
File: `requirements/non-functional-requirements.md`
Same structure; type = Non-Functional.

### Requirements Traceability Matrix
File: `requirements/requirements-traceability-matrix.md`

Maps each requirement to: Business Objective, Epic, User Story, Test Case, Status.

---

## Deliverables Catalogue

When compiling full FA work, generate:

1. **Business Analysis Plan** - Stakeholder engagement, elicitation approach, success criteria
2. **Requirements Documentation** - Business, Functional, Non-Functional, Traceability Matrix
3. **User Stories & Epics** - Persona-based stories, epic hierarchy, backlog structure
4. **Solution Design** - Solution options analysis, recommended architecture, technology decisions
5. **Validation Plan** - Acceptance criteria, test scenarios, success metrics
6. **Change Management Plan** - Impact analysis, training requirements, communication plan

---

## Quality Checklist

Every requirements deliverable must have:
- BABOK alignment confirmed
- Date and version
- Assumptions documented
- Business value articulated
- Stakeholder perspective considered
- Next steps identified

Every user story must have:
- Persona-driven (not generic)
- Clear Gherkin acceptance criteria
- Business value stated
- MoSCoW priority assigned
- Definition of Done included

---

## File Structure

```
Projects/[project-name]/
+-- requirements/
    +-- business-requirements.md
    +-- functional-requirements.md
    +-- non-functional-requirements.md
    +-- requirements-traceability-matrix.md
+-- user-stories/
    +-- epics/
        +-- epic-01-[name].md
        +-- epic-02-[name].md
    +-- personas/
        +-- persona-[role].md
```