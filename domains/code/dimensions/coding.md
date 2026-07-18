# Coding: Code As It Is Written

Coding is where a validated requirement and a reviewed design become an actual implementation. Defects caught here never reach a reviewer, a CI pipeline, or a user, so this dimension is about the checks a developer can and should run before a change is pushed.

## What to test

- Local correctness
  - Run the function or module against the edge cases identified during Planning and Requirements before writing the PR description.
  - Confirm null, empty, and boundary inputs are handled deliberately, not by accident.

- Local style and hygiene
  - Run the formatter and linter before staging changes.
  - Remove dead code, debug prints, and commented-out blocks introduced during development.

- Secret detection
  - Scan local commits and the working tree for leaked API keys, passwords, and tokens before pushing, using a pre-commit hook rather than relying on catching it in review.
  - This is the same underlying check as SEC-004 (Secrets-in-code absence) in `tests/security.md`, applied at the earliest possible point -- local commit time, not CI. Do not treat it as a separate test ID; wire SEC-004's tooling (gitleaks, TruffleHog) into a local pre-commit hook.

- Test-first discipline
  - Write or update the unit test alongside the logic, not after the PR is opened.
  - For a bug fix, write the failing test first and confirm it fails before applying the fix.

- Naming and structure
  - Name things for what they do, not how they're implemented.
  - Keep functions small enough that their name can fully describe their behavior.

- Commit hygiene
  - Write commit messages that follow the project's convention (e.g., Conventional Commits) and describe why the change was made.
  - Keep commits small and reviewable; avoid bundling unrelated changes.

## Test IDs that apply here

Coding-stage checks draw primarily from `tests/correctness-and-logic.md` (COR-001 through COR-012), `tests/structure-and-style.md` (all of STY), and SEC-004 in `tests/security.md`. No new IDs are introduced at this stage -- see the note on secret detection above.

## Why it matters

Coding-stage testing is the cheapest place to catch a defect. A null check added while writing the function costs seconds; the same defect caught in production costs an incident. This dimension exists to keep that cost asymmetry working in the team's favor.
