# docs/0-inputs/ — Client documents

This directory is the **single drop-off point** for all documents provided by the client or project sponsor. Agents read their client inputs here; they never write to this directory.

## Directory naming convention

Each subdirectory follows the `{domain}/{system}/` convention matching the target agent's domain and system. Agents automatically know where to look for their client documents using this convention.

### Structure

```
docs/0-inputs/
  ba/
    source/                      # Raw initial documents (specs, notes, PPT, emails, meeting notes...)
    0-audit/                     # Existing system documentation to audit (brownfield)
    1-scoping/                   # Supplements for vision, glossary, actors, requirements
    2-spec/                      # Supplements for domain model, business rules
    3-design/                    # Supplements for functional design
      ft-NNN-slug/               # Per feature (created at scaffold after epic discovery)
  tech/
    source/                      # Existing technical documents (architecture diagrams, code, infra...)
    0-audit/                     # Technical documentation of the existing system (brownfield)
    1-archi/                     # Supplements for architecture decisions
    2-design/                    # Supplements for technical design (API, data model...)
  steer/                         # Steering committee decisions, arbitrations, scope changes
```

## Rules

1. **Agents read, you write.** Agents never deposit files here. Only the user (you) adds documents.
2. **Name your folders descriptively.** Inside each system subdirectory, you may freely create subfolders to organise your documents (by date, by workshop, by topic...).
3. **All formats are accepted.** Markdown, PDF, Word, PowerPoint, images, CSV... Agents adapt to the format provided.
4. **An empty directory never blocks anything.** If no client document is available for an agent, it proceeds using only its upstream deliverables.

## Which directory for which agent?

| Directory | Target agents | When to deposit |
|-----------|---------------|-----------------|
| `ba/_source/` | `ba-discovery` | Before launching the BA pipeline — requirements doc, workshop notes, presentations |
| `ba/0-audit/` | `ba-0.1`, `ba-0.2` | Before the S0 pipeline (brownfield) — existing specs, manuals, screenshots |
| `ba/1-scoping/` | `ba-1.1` to `ba-1.4` | Supplements after discovery — meeting notes, sponsor clarifications |
| `ba/2-spec/` | `ba-2.1` to `ba-2.3` | Supplements for specification — business rule documents, entity diagrams |
| `ba/3-design/ft-NNN/` | `ba-3.1` to `ba-3.6` | Feature-targeted documents — wireframes, client feedback, screen workshop notes. To target a specific US, name the file with the US number (e.g. `feedback-us-003-validation.pdf`) |
| `tech/_source/` | `tech-t0.1` | Before the Tech pipeline — architecture diagrams, source code, infra config |
| `tech/0-audit/` | `tech-t0.1`, `tech-t0.2` | Technical documentation of the existing system |
| `tech/1-archi/` | `tech-t1.1` to `tech-t1.4` | Technical constraints, security docs, existing decisions |
| `tech/2-design/` | `tech-t2.1` to `tech-t2.6` | Technical design supplements — DB diagrams, existing API specs |
| `steer/` | `steer-p0.1` to `steer-p3.2` | Steering committee decisions, arbitrations, scope changes |

## Concrete examples

```
docs/0-inputs/
  ba/
    source/
      requirements-document-v2.pdf
      scoping-workshop-notes-2025-03-10.md
      sponsor-presentation.pptx
    0-audit/
      functional-spec-v3.docx
      existing-app-screenshots/
    1-scoping/
      meeting-notes-2025-03-15-scope-clarification.md
    3-design/
      ft-001-booking-management/
        figma-wireframes-export/
        feedback-us-003-validation-screen.pdf
      ft-002-availability-engine/
        workshop-notes-calculation-rules.md
  tech/
    source/
      architecture-diagram-2024.pdf
      docker-compose-prod.yml
    1-archi/
      security-constraints-it.pdf
  steer/
    steering-committee-minutes-2025-03-20.md
```

## Automatic scaffold

The base directory tree (`ba/_source/`, `ba/0-audit/`, `tech/_source/`, etc.) is created automatically by the scaffold tool at the start of each pipeline. Per-feature subdirectories (`ba/3-design/ft-NNN/`) are created dynamically after epic and feature discovery.
