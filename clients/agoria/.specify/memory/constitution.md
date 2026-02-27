<!--
Sync Impact Report:
- Version change: 1.2.0 → 1.3.0
- Modified principles: VII. Localization Support → Enhanced with mandatory i18n implementation requirements
- Added sections: X. Internationalization in Feature Development (new principle)
- Templates requiring updates: ✅ Updated constitution aligns with existing plan-template.md, spec-template.md, tasks-template.md
- Follow-up TODOs: None - all changes self-contained in constitution
- Rationale: MINOR version bump - new principle added for i18n implementation workflow without breaking existing principles
-->

# Agoria XY-Tool Constitution

## Core Principles

### I. Clean Architecture (NON-NEGOTIABLE)
All code MUST follow Clean Architecture principles with strict dependency flow: Domain → Application → Infrastructure → Web. Domain layer has no dependencies on other layers. Application layer depends only on Domain. Infrastructure implements Application interfaces. Web layer depends on Application, not Infrastructure directly. Business logic MUST remain in Domain layer only.

**Rationale**: Maintains separation of concerns, testability, and long-term maintainability. Ensures business rules are independent of external frameworks and infrastructure concerns.

### II. Test-Driven Development (MANDATORY)
TDD is strictly enforced: Tests written → Tests fail → Implementation → Tests pass → Refactor. ALL new backend code MUST have comprehensive NUnit unit tests. ALL new frontend features MUST have Playwright UI tests. Integration tests required for API endpoints with real database connections. Test coverage must be maintained or improved.

**Rationale**: Ensures code quality, prevents regressions, and enables confident refactoring. TDD drives better design and forces clear requirements understanding.

### III. Windows PowerShell Compatibility (NON-NEGOTIABLE)
ALL commands and scripts MUST be Windows PowerShell compatible. Use `Select-String` instead of `grep`, `;` instead of `&&` for command chaining. Always use absolute paths when changing directories. No Linux/Unix commands allowed without Windows alternatives.

**Rationale**: Target development environment is Windows with PowerShell 5.1. Consistency prevents environment-specific issues and ensures all team members can execute commands.

### IV. WCAG 2.1 AA Compliance (MANDATORY)
ALL frontend changes MUST be WCAG 2.1 AA compliant by design. Semantic HTML with proper heading hierarchy, ARIA support for screen readers, keyboard navigation for all interactive elements, 4.5:1 color contrast ratio for normal text, proper form accessibility with labels and error messages.

**Rationale**: Legal requirement and ethical imperative for inclusive design. Accessibility must be built in from the start, not retrofitted.

### V. Security-First Development (NON-NEGOTIABLE)
NO hardcoded secrets, connection strings, or API keys. Use Aspire configuration, environment variables, or Azure Key Vault. ALL user inputs MUST be validated. NO auto-suppressing security vulnerabilities. Implement proper authentication and authorization. Never log sensitive information.

**Rationale**: Security breaches can have severe business and legal consequences. Prevention is far cheaper than remediation.

### VI. Database Migration Protection (CRITICAL)
Entity Framework migrations MUST NOT be deleted unless absolutely necessary. PREFER adding new migrations or editing existing migrations to preserve migration history. Deleting migrations destroys history and breaks other developers' databases.

**Rationale**: Migration history is shared state across the development team. Breaking this history causes database inconsistencies and deployment failures.

### VII. Localization Support (MANDATORY)
ALL user-facing labels and text MUST be localized in Dutch (nl), French (fr), German (de), and English (en). Use proper localization keys and resource files. Apply to both backend APIs and frontend components.

**Rationale**: Multi-language support is a business requirement for the Belgian market serving Dutch, French, and German speaking users.

### VIII. Internationalization in Feature Development (MANDATORY)
ALL new pages, components, and features MUST include internationalization (i18n) translations during implementation, not as a follow-up task. When implementing any user-facing feature:

**Implementation Requirements**:
- Add translation keys to ALL four language files (nl, fr, en, de) in the same commit as the feature implementation
- Use react-i18next with `useTranslation` hook for frontend components
- Replace ALL hardcoded UI strings with `t()` translation calls
- Follow the existing namespaced translation pattern (e.g., `business.json`, `common.json`)
- Update component tests to expect translation keys (matching the mocked i18n behavior)
- Pass translation function `t` as parameter to helper functions that return user-facing text

**File Organization**:
- Frontend translations: `frontend/src/locales/{nl,fr,en,de}/*.json`
- Backend translations: Resource files per language in appropriate feature folders
- Group related translations in logical namespaces matching feature domains

**Test Requirements**:
- Mock i18n in tests to return translation keys as-is: `t: (key: string) => key`
- Update test expectations to check for translation keys, not translated text
- Verify translation keys exist in all four language files (optional lint step)

**Quality Gates**:
- NO feature is considered complete without translations in all four languages
- Code reviews MUST verify all UI strings use translation keys
- TypeScript errors for new translation keys are acceptable until type definitions are regenerated
- Runtime functionality MUST work correctly even with type definition lag

**Rationale**: Internationalization is a core business requirement, not an optional enhancement. Adding translations during implementation is more efficient than retrofitting later, ensures consistent multi-language support, and prevents translation debt. The Belgian market legally and practically requires Dutch, French, German, and English support from day one.

### IX. Honesty Over Helpfulness (MANDATORY)
Always express uncertainty when not completely confident. Base responses on actual code and verifiable information from the workspace. Use phrases like "I need to see [specific file] to provide an accurate answer" when uncertain. Never invent API methods, properties, or configurations without verification.

**Rationale**: Accurate guidance prevents technical debt and reduces debugging time. False confidence leads to incorrect implementations and wasted development effort.

### X. Prototype-Driven Design (MANDATORY)
The prototype/ folder serves as the authoritative design reference. Study prototype components, layouts, styling, and user interactions before building production features. Maintain visual and functional consistency with prototype design patterns. ALL frontend implementations MUST reference the prototype first and follow its patterns unless explicitly overridden by the specification.

**Implementation Requirements**:
- Before implementing any frontend feature, search the prototype/ directory for similar functionality
- Reuse prototype components, layouts, and styling patterns wherever possible
- Match prototype UI/UX patterns: forms, tables, navigation, modals, error handling
- Follow prototype Tailwind CSS class patterns and component structure
- Maintain prototype accessibility patterns and ARIA attributes
- Only deviate from prototype when specification explicitly requires different behavior
- Document any intentional deviations from prototype with rationale in code comments

**Dutch Prototype Translation** (CRITICAL):
- The prototype uses Dutch names for fields, variables, components, and elements
- ALL production code MUST use English names following standard naming conventions
- During clarify phase, identify Dutch names in prototype and document English equivalents
- Map Dutch field names to English: e.g., "gebruikersnaam" → "username", "bedrijfsnaam" → "companyName"
- Maintain semantic equivalence: translate meaning, not just words literally
- Add translation mapping table in spec's "Prototype Reference" section
- In code comments, reference Dutch prototype name when adapting patterns: `// Based on prototype 'BedrijfForm' component`

**Rationale**: Ensures consistent user experience across the application, reduces design decision overhead, provides clear design reference for implementation teams, and prevents UI/UX fragmentation. The prototype represents validated design patterns that should be leveraged rather than reinvented. English code ensures international maintainability while Dutch prototype reflects user-facing language requirements.

## Technology Standards

**Backend Stack**: .NET 8 Web API with Clean Architecture, Entity Framework Core with SQL Server, MediatR for CQRS, NUnit for testing, Aspire for orchestration, Microsoft.Identity.Web for JWT authentication, Microsoft.Graph SDK 5.68.0 for Entra user invitations.

**Frontend Stack**: React with TypeScript, Vite for build tooling, Tailwind CSS for styling, NSwag for API client generation, Playwright for UI testing, MSAL (@azure/msal-browser, @azure/msal-react) for Entra authentication with redirect flow.

**Architecture Patterns**: Clean Architecture with Domain-Driven Design, CQRS with MediatR, Repository pattern, Value Objects with ComplexProperty over OwnsOne, Screaming Architecture for frontend features.

**Compliance Requirements**: WCAG 2.1 AA accessibility, Windows PowerShell compatibility, Multi-language localization (nl/fr/de/en), Security best practices with no hardcoded secrets.

**Authentication & Authorization (XY-98)**: Microsoft Entra External ID integration for invitation-based user onboarding. Frontend uses MSAL redirect flow (not popup). Backend validates JWT tokens via Microsoft.Identity.Web. User invitation workflow: Admin creates user → IInvitationService.SendInvitationAsync → Graph API POST /invitations → User receives email → User signs in → EntraAuthenticationMiddleware marks as Registered. Database schema includes User.EntraUserId (NVARCHAR 100, indexed), User.InvitationStatus (enum: NotYetInvited/Invited/Failed/Registered), User.InvitationFailureReason (NVARCHAR 500), User.InvitationSentAt, User.InvitationAcceptedAt. Configuration requires VITE_ENTRA_CLIENT_ID, VITE_ENTRA_AUTHORITY, VITE_ENTRA_REDIRECT_URI for frontend; AzureAd:ClientId, AzureAd:TenantId, AzureAd:Instance for backend.

## Development Workflow

**GitFlow Process**: Feature branches from main, merge requests required, main branch always releasable, production branch for releases. Branch naming: feat/XY-###-feature-name, fix/XY-###-bug-name, hotfix/XY-###-critical-fix.

**Spec-Kit Workflow**: All features MUST follow the Spec-Kit workflow: `/speckit.specify` (from Jira or natural language) → `/speckit.clarify` (with prototype comparison) → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`. The clarify step MUST compare specifications against the prototype directory when available and post results to originating Jira issues. Implementation steps MUST reference prototype patterns identified during clarification.

**Definition of Done**: Everything builds without errors, no existing functionality broken, all unit tests pass, all UI tests pass, no security vulnerabilities, no hardcoded credentials, proper input validation, authentication/authorization implemented.

**Quality Gates**: Build verification on both backend and frontend, comprehensive test execution (NUnit + Playwright), security vulnerability scanning, manual testing of new functionality and existing features.

**Cleanup Requirements**: Terminate all running processes before cleanup (test runners, dev servers), remove debug/inspection files, remove generated documentation files, remove test results and build artifacts.

**Specification Compliance (MANDATORY)**: Implementation MUST strictly follow functional requirements without deviation. NO business rules, validation limits, or behavioral constraints may be added without explicit specification basis. ALL validation logic MUST reference specific FR-### functional requirements in code comments. Tests MUST validate specification compliance, not implementation assumptions. Implementation compliance checklist MUST be completed before any code implementation begins.

## Governance

This constitution supersedes all other development practices and guidelines. ALL pull requests and code reviews MUST verify compliance with these principles. Any complexity or deviation MUST be explicitly justified and documented. Security violations are never acceptable and will block all progress until resolved.

**Amendment Process**: Constitutional changes require version increment following semantic versioning (MAJOR for backward incompatible changes, MINOR for new principles, PATCH for clarifications), documentation of rationale, and team approval.

**Compliance Review**: Weekly compliance audits of new code, security scanning integration in CI/CD pipeline, accessibility testing as part of UI test suite, migration history validation before database deployments.

**Version**: 1.3.0 | **Ratified**: 2025-10-10 | **Last Amended**: 2025-11-18

**Amendment 1.2.0**: Added Specification Compliance principle to prevent implementation drift. Mandatory implementation compliance checklist and traceability requirements added to enforce spec-first development.

**Amendment 1.3.0**: Enhanced Localization Support principle (VII) and added new Internationalization in Feature Development principle (VIII) to enforce mandatory i18n translation implementation during feature development. All new features must include translations in all four languages (nl, fr, en, de) in the same commit, preventing translation debt and ensuring consistent multi-language support from day one.

**Amendment 1.3.0**: Enhanced Localization Support principle (VII) and added new Internationalization in Feature Development principle (VIII) to enforce mandatory i18n translation implementation during feature development. All new features must include translations in all four languages (nl, fr, en, de) in the same commit, preventing translation debt and ensuring consistent multi-language support from day one.