---
name: fa-discovery-elicitation
description: 'Structured BABOK V3 discovery and elicitation framework. Drives 10-round interview cycles with questions-first approach, contextual follow-up generation, source data acceleration, and lightweight note capture for functional analysis projects.'
triggers: ['start FA project', 'discovery round', 'elicitation', 'questionnaire analysis', 'contextual follow-up', 'source data', 'interview', 'FA discovery', 'next round', 'next questions']
version: '1.0.0'
author: 'soprasteria'
---

# Skill: FA Discovery & Elicitation

## Purpose

Provides the complete discovery and elicitation framework for functional analysis projects. Drives structured interviews using BABOK V3 knowledge areas, generates contextual follow-up questions, and manages lightweight discovery artifacts.

## When to Apply

Use this skill when:
- Starting a new FA project
- Running discovery rounds (1-10)
- Analyzing questionnaire answers
- Generating contextual follow-up questions
- Reviewing or accelerating discovery with source data

## Reference Handbooks

Primary BABOK and IREB references are bundled in `handbooks/` alongside this skill:
- `handbooks/BABOK-Guide.md` — Primary BABOK V3 reference (always consult first)
- `handbooks/` — All IREB (CPRE) handbooks, syllabi, factsheets, and glossary

---

## Operational Modes

### Speed Mode (Default — Questions-First)

**Priority order after receiving answers:**
1. **IMMEDIATE:** Generate NEXT 6 questions and present them
2. **BACKGROUND:** Process previous answers into lightweight notes

`yaml
mode: questions_first
questions_per_round: 6
auto_continue: true
note_format: lightweight bullet points
compilation_trigger: user_request_only
`

### Formal Mode (Optional)

`yaml
mode: formal
documentation_timing: real_time_per_round
note_format: comprehensive
compilation_trigger: automatic
`

**Switch commands:** `/fast` or `/formal`

---

## 10-Round Discovery Framework

| Round | Focus Area | BABOK Knowledge Area | Questions |
|-------|-----------|---------------------|-----------|
| 1 | Stakeholder & Context Discovery | Strategy Analysis, Planning | 6 |
| 2 | Business Objectives & Success Criteria | Strategy Analysis | 6 |
| 3 | Current State & Pain Points | Strategy Analysis | 6 |
| 4 | Future State Vision & Requirements | Strategy Analysis, Requirements Analysis | 6 |
| 5 | Constraints & Assumptions | Requirements Analysis | 6 |
| 6 | Solution Approach & Preferences | Requirements Analysis, Design Definition | 6 |
| 7 | Risk & Change Impact | Strategy Analysis, Solution Evaluation | 6 |
| 8 | Data & Integration Requirements | Requirements Analysis | 6 |
| 9 | User Experience & Process Flow | Requirements Analysis | 6 |
| 10 | Validation & Acceptance Criteria | Requirements Lifecycle, Solution Evaluation | 6 |

**Total: 60 questions across 10 rounds.**

### Round Flow

1. Present 6 questions (BABOK-aligned, progressive depth)
2. Receive answers
3. Generate NEXT 6 questions immediately (Priority 1)
4. Capture lightweight notes in `discovery/round-X-notes.md` (Priority 2)
5. Auto-continue unless user types `pause`

### Pause Options

When user types `pause` or `wait`:
`
Round X Complete — Choose next step:
1. Continue to Round X+1 (default)
2. Generate partial FA work (specific area)
3. Generate full FA documentation (comprehensive)
4. Deep-dive into specific topic
5. Export for Confluence/Jira/Client
`

---

## Source Data Acceleration

### Supported Locations

Check both locations on project initialization:
- **Recommended:** `Projects/[project-name]/source-data/`
- **Alternative:** `Sources[ProjectName]/`

### Supported Materials

| Material Type | Examples | How Used |
|--------------|----------|----------|
| Documentation | Requirements docs, RFPs, specifications | Context for requirements analysis |
| Questionnaire Answers | Pre-filled questionnaires, interview notes | Skip answered questions, focus on gaps |
| Regulatory/Legal | Compliance documents, contracts | Extract business rules and constraints |
| Existing Systems | Code repositories, database schemas | Current state analysis |
| Data Files | Spreadsheets, CSV, data dictionaries | Data modelling and integration |
| Meeting Notes | Previous minutes, decisions | Historical context |

### Initialization with Source Data

`
Checking for source data...
Found: Projects/[name]/source-data/ with X files:
- [List key materials]
This information will accelerate the FA process.
Discovery questions adjusted based on available information.
`

---

## Questionnaire Analysis & Contextual Follow-ups

When analyzing questionnaire answers, generate contextual follow-up questions by:

1. **Analyse each answer for key elements:**
   - Entities/organisations mentioned
   - Transformations or structural changes
   - New competencies, capabilities, or processes
   - Relationships and dependencies
   - Stated or implied impacts
   - Vague terms or incomplete statements

2. **Generate follow-up questions exploring:**
   - What: Details and specifics
   - How: Processes, methods, mechanisms
   - Why: Rationale, drivers, motivations
   - Impact: Effects, consequences, implications
   - Who: Stakeholders, roles, responsibilities
   - When: Timing, sequencing, timeline
   - Where: Location, scope, context

3. **Organise follow-ups in `follow-up-questions.md`:**
   - Group by original question section
   - Include reformulated questions for unclear responses (`?`, `TBD`)
   - Include contextual follow-ups based on answer content
   - Reference the specific content that triggered each follow-up

### Language Support

Generate follow-up questions in the language of the original answers (English, French, Dutch, or as appropriate to the project context).

---

## Project Initialization

When user says `Start FA project for [name]`:

1. Check for source data folder and report findings
2. Create project folder structure:
   `
   Projects/[project-name]/
   +-- PROJECT-OVERVIEW.md
   +-- discovery/
   +-- requirements/
   +-- user-stories/
   +-- diagrams/
   +-- models/
   +-- solution-design/
   +-- validation/
   `
3. Initialize `PROJECT-OVERVIEW.md` with BABOK framework
4. Present Round 1 questions (adjusted if source data found)

---

## Discovery Artifacts

### Per-Round Notes

File: `discovery/round-X-notes.md`
Format: Lightweight bullet points and fragments — quick captures, not formal prose.

### Discovery Summary (compiled on request)

File: `discovery/discovery-summary.md`
Contents: Executive summary, current state overview, business need, key stakeholders, core processes, success vision, BABOK KA coverage.

### Stakeholder Analysis (compiled on request)

File: `discovery/stakeholder-analysis.md`
Contents: Stakeholder register, 5-8 detailed personas, power/interest matrix, communication plan.
