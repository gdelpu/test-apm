# Convention: Business Language Consistency

## Objective

This convention requires each agent to maintain strict consistency with the established business glossary. It applies to **all agents across all systems**.

---

## Rules

### 1. Mandatory use of the glossary

- Before drafting a deliverable, the agent MUST load the existing glossary (the `glossary.md` file from the scoping folder)
- Every business term used in the deliverable MUST correspond exactly to a term in the glossary
- If the agent needs a term that is not in the glossary, it MUST:
  1. Flag it in the "Attention Points" section of the deliverable
  2. Propose a definition
  3. NOT use the term without this flag

### 2. Forbidden synonyms

The glossary defines for each term the forbidden synonyms. The agent MUST NEVER use a forbidden synonym, even if it seems more "natural" in a sentence.

**Example:**
- Official term: `Commande`
- Forbidden synonyms: `Ordre`, `Order`, `Demande d'achat`
- The agent ALWAYS uses `Commande`

### 3. Consistency of identifiers

Entity names in the domain model MUST correspond exactly to the terms in the glossary.

**Correct:**
- Glossary: `Commande` — Entity: `[ENT-005] Commande`

**Incorrect:**
- Glossary: `Commande` — Entity: `[ENT-005] Order`

### 4. Propagation to derived deliverables

When an agent produces a deliverable that derives from another:
- User stories use the same terms as the domain model
- Screen specifications use the same terms as the user stories
- Test scenarios use the same terms as the acceptance criteria

**No rephrasing, no paraphrasing** of business terms.

---

## Verification

At the end of producing each deliverable, the agent runs a check:

1. Extract all business terms used in the deliverable
2. Verify that each one exists in the glossary
3. Verify that no forbidden synonyms are used
4. Flag any discrepancy in the "Attention Points" section
