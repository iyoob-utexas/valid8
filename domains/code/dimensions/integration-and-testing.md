# Integration and Testing: Code Under PR Review, CI, and Staging

This dimension covers the checks that happen once a change is proposed and before it is deployed: automated CI, human PR review, and validation in a staging or test environment. PR review, CI execution, and staging validation are merged into one dimension here because in practice they overlap and iterate against the same change -- a CI failure sends a PR back for rework, a review comment triggers a new CI run, and staging validation often re-runs the same suite CI already ran, against a more production-like environment.

## What to test

- Correctness and intent match
  - Confirm the change does what the PR description claims, and that the description matches the actual diff.
  - Check edge cases the author may not have considered, especially at integration points the author doesn't own.

- Architecture and design fit
  - Confirm the change respects existing layering, doesn't introduce a circular dependency, and doesn't silently grow a module's responsibility.
  - Flag SOLID violations and coupling that will make the next change harder.

- Security review: static and dynamic
  - For any change touching input handling, auth, or a public endpoint, check for injection risk, missing authorization checks, and secrets (SEC-001 through SEC-010, SEC-015 -- collectively the SAST-covered checks).
  - Confirm Software Composition Analysis (SCA) has run and dependency changes carry no unresolved critical/high finding (SEC-011).
  - Confirm Dynamic Application Security Testing (DAST) has run against a deployed staging build, independent of static analysis (SEC-016).

- Test adequacy across the pyramid
  - Confirm new logic has unit tests (TST-001), integration tests where a component boundary changed (TST-002), and end-to-end coverage where a critical user journey changed (TST-003).
  - Confirm a bug fix includes a regression test (TST-010).
  - Confirm coverage metrics meet the project's line/branch threshold (TST-004), and that the tests assert meaningful outcomes, not just that a function ran (TST-006).

- Non-functional and cross-cutting test types
  - Performance and load testing against a staging environment at expected volume (PERF-011).
  - Cross-browser and cross-device testing for user-facing changes (TST-019).
  - Accessibility testing against the project's accessibility standard (TST-017).
  - Localization testing if the change touches user-facing text or formatting (TST-018).

- UAT / acceptance sign-off
  - For release-candidate features, confirm a stakeholder has signed off against acceptance criteria, distinct from and in addition to the automated tests above (TST-016).

- CI signal
  - Confirm the CI pipeline is green: linter, unit tests, integration tests, SAST, SCA, coverage threshold.
  - Do not approve a PR with a red or skipped required check.

- API and compatibility impact
  - For a public API or shared library change, confirm backward compatibility is preserved or the break is deliberate and versioned (ARC-012).

- Reviewer accountability
  - A named reviewer is accountable for the review, not just a rubber-stamp approval.
  - Security-sensitive changes get a second review from a security champion, including sign-off that DAST and SCA both ran clean.

## Test IDs that apply here

| ID | Name | Catalog |
|---|---|---|
| TST-002 | Integration test presence | `tests/testing-and-coverage.md` |
| TST-003 | End-to-end test presence | `tests/testing-and-coverage.md` |
| TST-004 | Line and branch coverage threshold | `tests/testing-and-coverage.md` |
| TST-010 | Regression test addition on bug fix | `tests/testing-and-coverage.md` |
| TST-016 | UAT / acceptance sign-off coverage | `tests/testing-and-coverage.md` |
| TST-017 | Accessibility testing coverage | `tests/testing-and-coverage.md` |
| TST-018 | Localization and internationalization testing | `tests/testing-and-coverage.md` |
| TST-019 | Cross-browser and cross-device testing | `tests/testing-and-coverage.md` |
| SEC-001, SEC-009, SEC-010, SEC-015 | Static analysis (SAST) coverage | `tests/security.md` |
| SEC-011 | Dependency vulnerability scan (SCA) | `tests/security.md` |
| SEC-016 | Dynamic application security testing (DAST) coverage | `tests/security.md` |
| PERF-011 | Load test threshold compliance | `tests/performance-and-scalability.md` |
| ARC-012 | API backward compatibility | `tests/architecture-and-design.md` |

Integration testing, e2e testing, regression testing, SAST, SCA, coverage metrics, and load testing were already covered by existing catalog IDs before this expansion (TST-002, TST-003, TST-010, SEC-001/009/010/015, SEC-011, TST-004, PERF-011, respectively) -- this dimension file makes that mapping explicit rather than introducing duplicate IDs. DAST (SEC-016), UAT (TST-016), accessibility (TST-017), localization (TST-018), and cross-browser/cross-device (TST-019) were genuine gaps and are new IDs as of this revision.

## Why it matters

Integration and testing is the last automated-plus-human gate before a change becomes part of the shared codebase and moves toward deployment. It's the point where a second set of eyes catches what the author's familiarity with the change caused them to miss, where the full test pyramid gets exercised against realistic conditions, and where the team's collective standard for correctness, security, and usability is actually enforced rather than aspirational.
