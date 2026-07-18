# Testing and Coverage

This domain validates the tests themselves: whether the test pyramid is shaped correctly, whether coverage numbers reflect real verification, and whether the test suite would actually catch a regression if one were introduced.

## What to test

- Test pyramid shape
  - A broad base of fast unit tests, a smaller layer of integration tests, and a thin layer of end-to-end tests.

- Coverage thresholds
  - Line, branch, and (where meaningful) mutation coverage meet the project's defined minimums.

- Test quality, not just quantity
  - Tests assert meaningful outcomes, not just that a function ran without throwing.
  - Mutation testing confirms tests actually fail when the underlying logic is broken.

- Flakiness
  - Tests produce the same result on every run given the same code and environment.

- Isolation and mocking
  - Unit tests do not depend on external systems, shared state, or execution order.
  - Mocks and stubs are used deliberately, not to hide untested integration points.

- User-facing test types
  - Usability testing on mockups/wireframes before code, and on the shipped UI after.
  - Accessibility, localization, and cross-browser/cross-device coverage for user-facing surfaces.
  - Smoke testing immediately post-deploy, and a documented UAT/acceptance sign-off before release.

## Why it matters

A green test suite with weak assertions or unstable coverage measurement gives false confidence, which is worse than no test suite at all because it hides the absence of verification behind a passing badge.

---

## DPPF testing and coverage test catalog

| ID | Name | What it verifies | Defends against | Standards | Lifecycle |
|---|---|---|---|---|---|
| TST-001 | Unit test presence | Every unit of business logic (function, method, small class) has at least one unit test covering its primary behavior | Untested logic shipping to production, regressions with no test to catch them | Testing pyramid (Cohn), ISTQB | Authoring, CI |
| TST-002 | Integration test presence | Interactions between components (database, external API, message queue) are covered by integration tests that exercise real or realistic boundaries | Interface mismatches between correctly-unit-tested components, contract drift between services | Testing pyramid (Cohn), ISTQB | CI |
| TST-003 | End-to-end test presence | Critical user journeys are covered by end-to-end tests that exercise the system as a user or external caller would | Integration-correct but user-journey-broken releases, regressions only visible in full-system context | Testing pyramid (Cohn), ISTQB | CI, Pre-deployment |
| TST-004 | Line and branch coverage threshold | Automated coverage tooling reports line and branch coverage at or above the project's defined minimum on new and changed code | Untested code paths merging silently, coverage regressions going unnoticed | Google engineering practices, ISTQB | CI |
| TST-005 | Mutation testing score | A mutation testing run confirms the test suite fails when a sample of code mutations (boundary flips, operator swaps) are introduced | Tests that achieve high line coverage but assert nothing meaningful, false confidence from coverage-without-verification | Mutation testing practice (Stryker, mutmut, PIT) | CI, Pre-deployment |
| TST-006 | Assertion strength | Tests assert on specific expected values and states, not merely that a call did not throw or that a result is non-null | Weak assertions that pass regardless of correctness, tests that provide coverage credit without verification | ISTQB, Clean Code testing principles | Review, CI |
| TST-007 | Flaky test detection | Tests produce the same pass/fail result across repeated runs on unchanged code and environment | Non-deterministic failures eroding trust in CI, developers ignoring red builds because "it's just flaky" | Google engineering practices | CI |
| TST-008 | Test isolation | Unit tests do not depend on shared mutable state, execution order, wall-clock time, or network access | Order-dependent test failures, tests that pass alone but fail in the full suite, hidden inter-test coupling | ISTQB, Google engineering practices | CI |
| TST-009 | Mocking discipline | Mocks and stubs replace only the specific external dependency under test, and integration points they hide are separately covered by an integration test | Over-mocking that hides real integration bugs, tests that verify the mock instead of the behavior | Google engineering practices | Review |
| TST-010 | Regression test addition on bug fix | Every merged bug fix includes a test that reproduces the original defect and fails without the fix | Bug recurrence after a fix is reverted or refactored away, silent regressions of previously fixed issues | ISTQB, Google engineering practices | Review, CI |
| TST-011 | Test-to-code ratio sanity | The volume and distribution of tests is proportionate to the complexity and risk of the code they cover, avoiding both under-testing critical logic and over-testing trivial code | Critical logic with thin coverage, wasted maintenance effort on exhaustively testing trivial getters | Testing pyramid (Cohn) | Review |
| TST-012 | CI gate enforcement | The test suite runs automatically on every change and blocks merge on failure | Broken code reaching the main branch, manual test execution being skipped under time pressure | Google engineering practices | CI |
| TST-013 | Test data realism | Test fixtures and generated data represent realistic value distributions and edge cases, not only trivial happy-path values | Tests that pass against unrealistic data but fail against production-shaped input | ISTQB | Authoring, Review |
| TST-014 | UI/UX usability testing | Mockups and wireframes are usability-tested with representative users or a structured heuristic review before implementation, and the shipped UI is spot-checked against the same usability criteria | Interfaces that are functionally correct but unusable, costly late-stage redesign after users struggle with a shipped flow | ISO/IEC 25010 Usability, Nielsen usability heuristics | Design, Review |
| TST-015 | Smoke test coverage | A minimal, fast-running suite of critical-path checks runs immediately after every deployment and confirms the system is basically functional before broader validation proceeds | A broken deployment going unnoticed until a user reports it, wasted investigation time on a full test suite run against a fundamentally down system | ISTQB | Pre-deployment, Production |
| TST-016 | UAT / acceptance sign-off coverage | Each release-candidate feature has a documented user acceptance test pass with explicit stakeholder sign-off before release, distinct from and in addition to automated business-rule tests (COR-013) | Features that pass every automated check but do not meet the stakeholder's actual intent, released work rejected after the fact | ISTQB, Testing pyramid (Cohn) | Pre-deployment |
| TST-017 | Accessibility testing coverage | User-facing interfaces are tested against a defined accessibility standard (e.g., WCAG 2.1 AA) using both automated scanning and manual checks (keyboard navigation, screen reader) | Interfaces unusable by users relying on assistive technology, compliance exposure under accessibility law | WCAG 2.1, ISO/IEC 25010 Usability | CI, Pre-deployment |
| TST-018 | Localization and internationalization testing | User-facing text, date/number/currency formatting, and layout are tested against every locale the product supports | Untranslated or truncated strings, incorrect date/currency formatting, layout breakage under text expansion in translated locales | ISO/IEC 25010 Portability | CI, Pre-deployment |
| TST-019 | Cross-browser and cross-device testing | User-facing functionality is tested across the browser, OS, and device matrix the product commits to supporting | Functionality that works in the developer's environment but breaks on a supported browser or device, silent regressions on a platform nobody manually checks | ISO/IEC 25010 Compatibility | CI, Pre-deployment |
