# Structure and Style

Structure and style testing confirms the code is readable, maintainable, and consistent enough that the next person to touch it -- including a future version of the author -- can understand and safely change it.

## What to test

- Readability and naming
  - Names describe intent, not implementation detail or type.
  - Functions and variables follow a consistent, project-wide naming convention.

- Formatting and linting
  - Code is auto-formatted and passes the project's linter with zero suppressions that lack justification.

- Complexity
  - Cyclomatic complexity per function stays under a defined threshold.
  - Nesting depth is bounded; deeply nested conditionals are extracted.

- Duplication
  - Repeated logic is extracted rather than copy-pasted across files.

- Dead code
  - Unreachable code, unused imports, unused variables, and commented-out code blocks are removed.

- Size
  - Functions and files stay under agreed length thresholds; oversized units are a signal to decompose.

## Why it matters

Code that works but cannot be read safely is a liability the moment someone other than the author needs to change it. Structure and style tests keep the codebase legible as it grows, and catch complexity before it becomes a rewrite.

---

## DPPF structure and style test catalog

| ID | Name | What it verifies | Defends against | Standards | Lifecycle |
|---|---|---|---|---|---|
| STY-001 | Naming clarity | Identifiers (variables, functions, classes) describe intent and are unambiguous without needing a comment to explain them | Misleading names, single-letter variables outside tight loops, names that lie about behavior | Clean Code naming principles | Authoring, Review |
| STY-002 | Naming convention consistency | Naming follows one consistent convention (case style, prefix/suffix rules) across the codebase or module | Mixed conventions that slow reading, merge conflicts from style churn | Clean Code, project style guide | Review, CI |
| STY-003 | Formatter and linter conformance | Code is auto-formatted and passes the configured linter with no unjustified suppressions | Formatting bikeshedding in review, inconsistent whitespace diffs, linter-detectable bugs going unnoticed | ESLint/Prettier/Ruff class tooling | Authoring, CI |
| STY-004 | Cyclomatic complexity bound | Each function's cyclomatic complexity stays at or below the project's defined threshold | Untestable functions, logic that is impossible to reason about, hidden branch explosion | ISO/IEC 25010 Maintainability | Review, CI |
| STY-005 | Nesting depth bound | Conditional and loop nesting stays within a defined maximum depth before requiring extraction | Arrow-code / deeply nested conditionals, unreadable control flow | Clean Code, ISO/IEC 25010 Maintainability | Review, CI |
| STY-006 | Duplication threshold | Near-identical code blocks above a defined size or count are extracted into a shared function or module | Copy-paste drift where one copy is fixed and others are not, inconsistent bug fixes | ISO/IEC 25010 Maintainability, DRY principle | Review, CI |
| STY-007 | Dead code absence | No unreachable code, unused imports, unused variables, or commented-out code blocks remain in the codebase | Confusion about which code path is live, accidental re-activation of stale logic, bloated bundle size | ISO/IEC 25010 Maintainability | Review, CI |
| STY-008 | Function length bound | Functions stay under the project's defined maximum line count before requiring decomposition | God functions that mix multiple responsibilities, functions too large to review effectively | Clean Code, ISO/IEC 25010 Maintainability | Review, CI |
| STY-009 | File length bound | Files stay under the project's defined maximum line count before requiring a split | Monolithic files that are slow to navigate and prone to merge conflicts | ISO/IEC 25010 Maintainability | Review, CI |
| STY-010 | Comment-code alignment | Comments describe why, not what, and are not stale relative to the code they annotate | Misleading comments that describe removed behavior, comments substituting for unclear code | Clean Code commenting principles | Review |
| STY-011 | Magic value elimination | Literal numbers and strings with domain meaning are named constants, not inline magic values | Silent behavior drift when a magic value is changed in one place but not another, unclear intent | Clean Code, ISO/IEC 25010 Maintainability | Authoring, Review |
| STY-012 | Consistent error and null idiom | The codebase uses one consistent pattern for error handling and null representation (exceptions vs return codes, null vs Optional) rather than mixing idioms | Inconsistent handling causing missed error checks, integration bugs at idiom boundaries | ISO/IEC 25010 Maintainability | Review, CI |
