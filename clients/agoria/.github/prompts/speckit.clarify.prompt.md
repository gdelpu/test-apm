---
description: Identify underspecified areas in the current feature spec by asking up to 5 highly targeted clarification questions and encoding answers back into the spec.
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

Goal: Detect and reduce ambiguity or missing decision points in the active feature specification and record the clarifications directly in the spec file.

Note: This clarification workflow is expected to run (and be completed) BEFORE invoking `/speckit.plan`. If the user explicitly states they are skipping clarification (e.g., exploratory spike), you may proceed, but must warn that downstream rework risk increases.

Execution steps:

1. Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly` from repo root **once** (combined `--json --paths-only` mode / `-Json -PathsOnly`). Parse minimal JSON payload fields:
   - `FEATURE_DIR`
   - `FEATURE_SPEC`
   - (Optionally capture `IMPL_PLAN`, `TASKS` for future chained flows.)
   - If JSON parsing fails, abort and instruct user to re-run `/speckit.specify` or verify feature branch environment.
   - For single quotes in args like "I'm Groot", use escape syntax: e.g 'I'\''m Groot' (or double-quote if possible: "I'm Groot").

2. Load the current spec file. Perform a structured ambiguity & coverage scan using this taxonomy. For each category, mark status: Clear / Partial / Missing. Produce an internal coverage map used for prioritization (do not output raw map unless no questions will be asked).

<!-- CUSTOMIZATION: Agoria XY-Tool - Prototype Comparison -->
2a. **Prototype Comparison Phase (CUSTOMIZATION - Execute before generating questions)**:

   **Check for Prototype**:
   - Run `.specify/scripts/powershell/compare-with-prototype.ps1 -Json` from repo root
   - Parse JSON output: `exists`, `patterns`, `components`, `pages`, `features`, `instructions`
   - If `exists` is false, skip prototype comparison and log "No prototype found, continuing without comparison"
   
   **IF prototype exists, perform analysis**:
   
   1. **Analyze Prototype Structure**:
      - Note detected patterns (routing, styling, state management, API client)
      - Count of components, pages, features
      - Build tool and testing framework
   
   2. **Find Relevant Prototype Files**:
      - Use semantic_search with feature keywords from spec to find related prototype files
      - Search for: component names, page names, feature concepts, entity names
      - Example: If spec mentions "user authentication", search for "authentication login user auth"
      - Read top 3-5 most relevant prototype files
   
   3. **Compare Spec Against Prototype**:
      - For each functional requirement in spec:
        * Does similar functionality exist in prototype?
        * Mark as: ✅ Exists | ⚠️ Partial | ❌ Missing | 🔄 Different
        * Note file paths where found
      - For UI/form requirements:
        * Check for matching screens/components
        * Compare field lists, validation, styling patterns
        * Note Tailwind classes, component structure
      - For data entities:
        * Search for TypeScript interfaces/types
        * Compare field names and types
   
   4. **Generate Internal Prototype Report** (not shown to user yet):
      - Relevant prototype files and their purpose
      - Patterns identified (components, styling, forms, API calls)
      - Coverage: What exists, what's partial, what's missing, what differs
      - Conflicts: Where spec and prototype fundamentally differ
      - Recommendations: Follow prototype / Extend prototype / Resolve conflict
   
   5. **Integrate into Clarification Workflow**:
      - Add prototype-derived questions to candidate queue:
        * "Spec requires [X], but prototype implements [Y]. Which should we follow?"
        * "Prototype has [feature] in [file]. Should spec include this?"
        * "Spec omits [pattern] used in prototype. Intentional?"
      - Prioritize prototype conflict questions (these impact consistency)
      - Include prototype file references in question context
      - Use prototype as evidence when resolving ambiguities
   
   **IMPORTANT**: Prototype comparison results inform the clarification questions but are NOT posted yet.
   Final prototype report will be included in Jira comment at the end.

<!-- END CUSTOMIZATION -->

   Functional Scope & Behavior:
   - Core user goals & success criteria
   - Explicit out-of-scope declarations
   - User roles / personas differentiation

   Domain & Data Model:
   - Entities, attributes, relationships
   - Identity & uniqueness rules
   - Lifecycle/state transitions
   - Data volume / scale assumptions

   Interaction & UX Flow:
   - Critical user journeys / sequences
   - Error/empty/loading states
   - Accessibility or localization notes

   Non-Functional Quality Attributes:
   - Performance (latency, throughput targets)
   - Scalability (horizontal/vertical, limits)
   - Reliability & availability (uptime, recovery expectations)
   - Observability (logging, metrics, tracing signals)
   - Security & privacy (authN/Z, data protection, threat assumptions)
   - Compliance / regulatory constraints (if any)

   Integration & External Dependencies:
   - External services/APIs and failure modes
   - Data import/export formats
   - Protocol/versioning assumptions

   Edge Cases & Failure Handling:
   - Negative scenarios
   - Rate limiting / throttling
   - Conflict resolution (e.g., concurrent edits)

   Constraints & Tradeoffs:
   - Technical constraints (language, storage, hosting)
   - Explicit tradeoffs or rejected alternatives

   Terminology & Consistency:
   - Canonical glossary terms
   - Avoided synonyms / deprecated terms

   Completion Signals:
   - Acceptance criteria testability
   - Measurable Definition of Done style indicators

   Misc / Placeholders:
   - TODO markers / unresolved decisions
   - Ambiguous adjectives ("robust", "intuitive") lacking quantification

   For each category with Partial or Missing status, add a candidate question opportunity unless:
   - Clarification would not materially change implementation or validation strategy
   - Information is better deferred to planning phase (note internally)

3. Generate (internally) a prioritized queue of candidate clarification questions (maximum 5). Do NOT output them all at once. Apply these constraints:
    - Maximum of 10 total questions across the whole session.
    - Each question must be answerable with EITHER:
       * A short multiple‑choice selection (2–5 distinct, mutually exclusive options), OR
       * A one-word / short‑phrase answer (explicitly constrain: "Answer in <=5 words").
   - Only include questions whose answers materially impact architecture, data modeling, task decomposition, test design, UX behavior, operational readiness, or compliance validation.
   - Ensure category coverage balance: attempt to cover the highest impact unresolved categories first; avoid asking two low-impact questions when a single high-impact area (e.g., security posture) is unresolved.
   - Exclude questions already answered, trivial stylistic preferences, or plan-level execution details (unless blocking correctness).
   - Favor clarifications that reduce downstream rework risk or prevent misaligned acceptance tests.
   - If more than 5 categories remain unresolved, select the top 5 by (Impact * Uncertainty) heuristic.

4. Sequential questioning loop (interactive):
    - Present EXACTLY ONE question at a time.
    - For multiple‑choice questions render options as a Markdown table:

       | Option | Description |
       |--------|-------------|
       | A | <Option A description> |
       | B | <Option B description> |
       | C | <Option C description> | (add D/E as needed up to 5)
       | Short | Provide a different short answer (<=5 words) | (Include only if free-form alternative is appropriate)

    - For short‑answer style (no meaningful discrete options), output a single line after the question: `Format: Short answer (<=5 words)`.
    - After the user answers:
       * Validate the answer maps to one option or fits the <=5 word constraint.
       * If ambiguous, ask for a quick disambiguation (count still belongs to same question; do not advance).
       * Once satisfactory, record it in working memory (do not yet write to disk) and move to the next queued question.
    - Stop asking further questions when:
       * All critical ambiguities resolved early (remaining queued items become unnecessary), OR
       * User signals completion ("done", "good", "no more"), OR
       * You reach 5 asked questions.
    - Never reveal future queued questions in advance.
    - If no valid questions exist at start, immediately report no critical ambiguities.

5. Integration after EACH accepted answer (incremental update approach):
    - Maintain in-memory representation of the spec (loaded once at start) plus the raw file contents.
    - For the first integrated answer in this session:
       * Ensure a `## Clarifications` section exists (create it just after the highest-level contextual/overview section per the spec template if missing).
       * Under it, create (if not present) a `### Session YYYY-MM-DD` subheading for today.
    - Append a bullet line immediately after acceptance: `- Q: <question> → A: <final answer>`.
    - Then immediately apply the clarification to the most appropriate section(s):
       * Functional ambiguity → Update or add a bullet in Functional Requirements.
       * User interaction / actor distinction → Update User Stories or Actors subsection (if present) with clarified role, constraint, or scenario.
       * Data shape / entities → Update Data Model (add fields, types, relationships) preserving ordering; note added constraints succinctly.
       * Non-functional constraint → Add/modify measurable criteria in Non-Functional / Quality Attributes section (convert vague adjective to metric or explicit target).
       * Edge case / negative flow → Add a new bullet under Edge Cases / Error Handling (or create such subsection if template provides placeholder for it).
       * Terminology conflict → Normalize term across spec; retain original only if necessary by adding `(formerly referred to as "X")` once.
    - If the clarification invalidates an earlier ambiguous statement, replace that statement instead of duplicating; leave no obsolete contradictory text.
    - Save the spec file AFTER each integration to minimize risk of context loss (atomic overwrite).
    - Preserve formatting: do not reorder unrelated sections; keep heading hierarchy intact.
    - Keep each inserted clarification minimal and testable (avoid narrative drift).

6. Validation (performed after EACH write plus final pass):
   - Clarifications session contains exactly one bullet per accepted answer (no duplicates).
   - Total asked (accepted) questions ≤ 5.
   - Updated sections contain no lingering vague placeholders the new answer was meant to resolve.
   - No contradictory earlier statement remains (scan for now-invalid alternative choices removed).
   - Markdown structure valid; only allowed new headings: `## Clarifications`, `### Session YYYY-MM-DD`.
   - Terminology consistency: same canonical term used across all updated sections.

7. Write the updated spec back to `FEATURE_SPEC`.

<!-- CUSTOMIZATION: Agoria XY-Tool - Add Prototype Reference Section -->
7a. **Add Prototype Reference Section to Spec (if prototype comparison was performed)**:
   
   After writing the updated spec, append a `## Prototype Reference` section (if not already present):
   
   ```markdown
   ## Prototype Reference
   
   **Comparison Date**: [YYYY-MM-DD]
   **Prototype Files Analyzed**: [Count]
   **Prototype Language**: Dutch (translate to English for production)
   
   **Relevant Prototype Files**:
   - `prototype/src/[path]` - [Description of relevance]
   - `prototype/src/[path]` - [Description]
   
   **Patterns to Follow**:
   - [Pattern from prototype, e.g., "Form validation using react-hook-form"]
   - [Pattern, e.g., "API calls with React Query"]
   - [Pattern, e.g., "Tailwind component styling"]
   
   **Prototype Coverage**:
   - ✅ Existing: [List requirements that exist in prototype]
   - ⚠️ Partial: [List requirements partially implemented]
   - ❌ Missing: [List requirements not in prototype]
   - 🔄 Different: [List requirements implemented differently]
   
   **Dutch to English Translation Mapping**:
   | Dutch (Prototype) | English (Production) | Context |
   |-------------------|---------------------|---------|
   | [Dutch name] | [English equivalent] | [Field/Component/Type] |
   | gebruikersnaam | username | Form field |
   | bedrijfsnaam | companyName | Entity property |
   | [Add all identified Dutch names from prototype] | | |
   
   **Intentional Differences from Prototype**:
   - [Difference with rationale, e.g., "Spec requires multi-step form, prototype uses single page (spec overrides for better UX)"]
   
   **Implementation Notes**:
   - Reuse prototype components where possible for consistency
   - Follow prototype styling patterns (Tailwind classes, layout structure)
   - Translate all Dutch names to English (see mapping table above)
   - Maintain semantic equivalence when translating
   - Reference Dutch prototype names in code comments: `// Based on prototype 'BedrijfForm'`
   ```
   
   **IMPORTANT**: When analyzing prototype files, identify Dutch names (fields, variables, components, types) and create the translation mapping table. Common Dutch patterns:
   - Field suffixes: -naam (name), -datum (date), -nummer (number), -type (type)
   - Prefixes: bedrijf- (company), gebruiker- (user), product- (product)
   - Common words: gegevens (data), overzicht (overview), beheer (management), toevoegen (add), wijzigen (edit)
   
   Write this section with complete translation mapping, then save the spec file again.

<!-- END CUSTOMIZATION -->

8. Report completion (after questioning loop ends or early termination):
   - Number of questions asked & answered.
   - Path to updated spec.
   - Sections touched (list names).
   - Coverage summary table listing each taxonomy category with Status: Resolved (was Partial/Missing and addressed), Deferred (exceeds question quota or better suited for planning), Clear (already sufficient), Outstanding (still Partial/Missing but low impact).
   - If any Outstanding or Deferred remain, recommend whether to proceed to `/speckit.plan` or run `/speckit.clarify` again later post-plan.
   - Suggested next command.

<!-- CUSTOMIZATION: Agoria XY-Tool - Post Results to Jira -->
8a. **Post Clarification Results to Jira (if spec has Jira metadata)**:

   1. **Check for Jira Integration**:
      - Read spec file front matter for Jira metadata (added during `/speckit.specify from-jira`)
      - Look for: `**Source**: Jira Issue [KEY]` or similar markers
      - Extract Issue Key (e.g., XY-123) and CloudId (if present)
      - If no Jira metadata found, skip Jira posting and log "Spec not linked to Jira, skipping comment post"
   
   2. **Prepare Jira Comment** (using Jira markdown syntax):
      
      ```markdown
      h2. 📋 Specification Clarification Complete
      
      *Completed*: [YYYY-MM-DD]
      *Specification*: [Link to spec file in repo if available, or just file name]
      
      h3. Summary
      
      * *Questions Asked & Answered*: [Count]
      * *Spec Sections Updated*: [Comma-separated list]
      * *Prototype Comparison*: [Completed / Skipped - no prototype found]
      
      h3. Clarifications
      
      [For each answered question:]
      # *Q[N]*: [Question text]
      *Answer*: [Answer text]
      *Updated Section*: [Section name]
      
      [Blank line between questions]
      
      h3. Prototype Analysis
      
      [If prototype comparison was performed:]
      
      *Prototype Files Analyzed*: [Count]
      *Patterns Detected*: [List: routing, styling, state management, etc.]
      
      *Coverage Results*:
      * ✅ *Existing in Prototype*: [Count] requirements
        [List top 3-5 if many, with file references]
      * ⚠️ *Partial in Prototype*: [Count] requirements
        [List with gap descriptions]
      * ❌ *Missing from Prototype*: [Count] requirements
        [List - these need new implementation]
      * 🔄 *Different in Prototype*: [Count] requirements
        [List with recommendations]
      
      *Key Recommendations*:
      # [Recommendation 1, e.g., "Follow prototype form pattern in components/UserForm.tsx"]
      # [Recommendation 2]
      # [Recommendation 3]
      
      [If prototype was skipped:]
      _Prototype comparison skipped (no prototype directory found)_
      
      h3. Outstanding Items
      
      [If any NEEDS CLARIFICATION markers remain in spec:]
      *Unresolved Questions* (exceeded clarification quota):
      # [Question 1]
      # [Question 2]
      
      [If none:]
      _No outstanding clarifications - specification is complete_
      
      h3. Next Steps
      
      * ✅ Proceed to {{/speckit.plan}} for implementation planning
      [If prototype analysis done:]
      * 📁 Reference prototype files: [list top 3 files]
      * 🎨 Follow prototype patterns for consistency
      [If conflicts identified:]
      * ⚠️ Resolve spec/prototype conflicts before implementation
      
      ----
      _Generated by Spec-Kit clarify workflow_
      ```
   
   3. **Post Comment to Jira**:
      - If CloudId not in spec metadata, call `mcp_atlassian_atl_getAccessibleAtlassianResources` to get it
      - Call `mcp_atlassian_atl_addCommentToJiraIssue`:
        * cloudId: [from metadata or lookup]
        * issueIdOrKey: [from spec metadata]
        * commentBody: [formatted comment above]
      - Handle errors gracefully:
        * If MCP call fails, save comment to `FEATURE_DIR/jira-comment.md`
        * Log: "Could not post to Jira: [error]. Comment saved to jira-comment.md"
        * Include in user report: "⚠️ Jira comment not posted (saved locally). Please post manually from jira-comment.md"
      - If successful:
        * Log: "Posted clarification results to Jira issue [KEY]"
        * Include in user report: "✅ Posted results to Jira issue [KEY]"
   
   4. **Update Spec Metadata**:
      - Add to spec front matter:
        ```markdown
        **Clarified**: [YYYY-MM-DD]
        **Jira Comment Posted**: [Yes/No]
        **Prototype Compared**: [Yes/No]
        ```
      - Save spec file again

<!-- END CUSTOMIZATION -->

8b. Final Report (modified to include customizations):
   - Standard completion report (questions, sections, coverage)
   - **ADDED**: Prototype comparison summary (if performed)
     * "Prototype: [X] files analyzed, [Y] requirements mapped"
     * "See Prototype Reference section in spec for details"
   - **ADDED**: Jira integration status
     * "✅ Posted to Jira issue [KEY]" OR
     * "⚠️ Jira comment saved to jira-comment.md (post manually)" OR
     * "ℹ️ No Jira integration (spec not from Jira issue)"
   - Suggested next command

Behavior rules:
- If no meaningful ambiguities found (or all potential questions would be low-impact), respond: "No critical ambiguities detected worth formal clarification." and suggest proceeding.
- If spec file missing, instruct user to run `/speckit.specify` first (do not create a new spec here).
- Never exceed 5 total asked questions (clarification retries for a single question do not count as new questions).
- Avoid speculative tech stack questions unless the absence blocks functional clarity.
- Respect user early termination signals ("stop", "done", "proceed").
 - If no questions asked due to full coverage, output a compact coverage summary (all categories Clear) then suggest advancing.
 - If quota reached with unresolved high-impact categories remaining, explicitly flag them under Deferred with rationale.

Context for prioritization: $ARGUMENTS
