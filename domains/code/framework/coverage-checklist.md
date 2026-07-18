# Coverage Evaluation Checklist

Use this checklist to assess how well an existing codebase's test and review practice covers this framework's catalog. For each test ID, mark the coverage status, note the current implementation or monitoring approach, and record any gaps.

This checklist is the primary output of the reconnaissance and threat-modeling phases of the engagement methodology described in `domains/code/process/testing-strategy.md`. Complete it before scoring findings and before setting a target maturity level.

---

## How to use this checklist

1. Work through each domain section.
2. For each test ID, mark one status:
   - **Covered**: a specific, automated check exists and runs at the defined lifecycle stage.
   - **Partial**: a check exists but is manual, incomplete, or not running at the right stage.
   - **Gap**: no check exists for this test category.
3. Fill in the Notes column with what is currently in place or why coverage is absent.
4. After completing all domains, use the scoring guide at the bottom to determine the current maturity level.
5. Score any Gap or Partial items using the severity model in `domains/code/framework/README.md`.

---

## Correctness and logic domain

Tests in this domain: `domains/code/tests/correctness-and-logic.md`

| ID | Name | Status | Notes |
|---|---|---|---|
| COR-001 | Boundary value handling | | |
| COR-002 | Null and undefined safety | | |
| COR-003 | Empty and degenerate input handling | | |
| COR-004 | Type coercion safety | | |
| COR-005 | Numeric precision and overflow | | |
| COR-006 | Error propagation completeness | | |
| COR-007 | Branch and condition coverage | | |
| COR-008 | Race-condition-free shared state | | |
| COR-009 | Async ordering correctness | | |
| COR-010 | Algorithm specification match | | |
| COR-011 | Idempotent computation correctness | | |
| COR-012 | Resource cleanup on error paths | | |
| COR-013 | Business rule fidelity | | |
| COR-014 | Requirement validation and testability | | |

Correctness and logic coverage: _____ Covered / _____ Partial / _____ Gap out of 14

---

## Structure and style domain

Tests in this domain: `domains/code/tests/structure-and-style.md`

| ID | Name | Status | Notes |
|---|---|---|---|
| STY-001 | Naming clarity | | |
| STY-002 | Naming convention consistency | | |
| STY-003 | Formatter and linter conformance | | |
| STY-004 | Cyclomatic complexity bound | | |
| STY-005 | Nesting depth bound | | |
| STY-006 | Duplication threshold | | |
| STY-007 | Dead code absence | | |
| STY-008 | Function length bound | | |
| STY-009 | File length bound | | |
| STY-010 | Comment-code alignment | | |
| STY-011 | Magic value elimination | | |
| STY-012 | Consistent error and null idiom | | |

Structure and style coverage: _____ Covered / _____ Partial / _____ Gap out of 12

---

## Security domain

Tests in this domain: `domains/code/tests/security.md`

| ID | Name | Status | Notes |
|---|---|---|---|
| SEC-001 | Injection input sanitization | | |
| SEC-002 | Authentication strength | | |
| SEC-003 | Session management integrity | | |
| SEC-004 | Secrets-in-code absence | | |
| SEC-005 | Sensitive data encryption | | |
| SEC-006 | Error message information disclosure | | |
| SEC-007 | Access control enforcement | | |
| SEC-008 | Security configuration hardening | | |
| SEC-009 | Output encoding / XSS prevention | | |
| SEC-010 | Deserialization safety | | |
| SEC-011 | Dependency vulnerability scan (SCA) | | |
| SEC-012 | Security event logging sufficiency | | |
| SEC-013 | Sensitive data logging exclusion | | |
| SEC-014 | SSRF request allowlisting | | |
| SEC-015 | XML external entity (XXE) prevention | | |
| SEC-016 | Dynamic application security testing (DAST) coverage | | |
| SEC-017 | Placeholder code reachability | | |
| SEC-018 | Dependency license compliance | | |

Security coverage: _____ Covered / _____ Partial / _____ Gap out of 18

---

## Architecture and design domain

Tests in this domain: `domains/code/tests/architecture-and-design.md`

| ID | Name | Status | Notes |
|---|---|---|---|
| ARC-001 | Single responsibility conformance | | |
| ARC-002 | Open/closed extensibility | | |
| ARC-003 | Liskov substitution safety | | |
| ARC-004 | Interface segregation | | |
| ARC-005 | Dependency inversion | | |
| ARC-006 | Coupling bound | | |
| ARC-007 | Cohesion strength | | |
| ARC-008 | Layering direction consistency | | |
| ARC-009 | Circular dependency absence | | |
| ARC-010 | Abstraction leak prevention | | |
| ARC-011 | Inappropriate intimacy absence | | |
| ARC-012 | API backward compatibility | | |
| ARC-013 | Threat modeling coverage | | |
| ARC-014 | Code provenance and non-infringement review | | |

Architecture and design coverage: _____ Covered / _____ Partial / _____ Gap out of 14

---

## Testing and coverage domain

Tests in this domain: `domains/code/tests/testing-and-coverage.md`

| ID | Name | Status | Notes |
|---|---|---|---|
| TST-001 | Unit test presence | | |
| TST-002 | Integration test presence | | |
| TST-003 | End-to-end test presence | | |
| TST-004 | Line and branch coverage threshold | | |
| TST-005 | Mutation testing score | | |
| TST-006 | Assertion strength | | |
| TST-007 | Flaky test detection | | |
| TST-008 | Test isolation | | |
| TST-009 | Mocking discipline | | |
| TST-010 | Regression test addition on bug fix | | |
| TST-011 | Test-to-code ratio sanity | | |
| TST-012 | CI gate enforcement | | |
| TST-013 | Test data realism | | |
| TST-014 | UI/UX usability testing | | |
| TST-015 | Smoke test coverage | | |
| TST-016 | UAT / acceptance sign-off coverage | | |
| TST-017 | Accessibility testing coverage | | |
| TST-018 | Localization and internationalization testing | | |
| TST-019 | Cross-browser and cross-device testing | | |

Testing and coverage coverage: _____ Covered / _____ Partial / _____ Gap out of 19

---

## Performance and scalability domain

Tests in this domain: `domains/code/tests/performance-and-scalability.md`

| ID | Name | Status | Notes |
|---|---|---|---|
| PERF-001 | Algorithmic complexity bound | | |
| PERF-002 | Complexity regression detection | | |
| PERF-003 | N+1 query prevention | | |
| PERF-004 | Unbounded result set prevention | | |
| PERF-005 | Memory leak absence | | |
| PERF-006 | Unbounded cache and collection growth prevention | | |
| PERF-007 | Blocking I/O in async context prevention | | |
| PERF-008 | Lock contention bound | | |
| PERF-009 | Connection and resource pool sizing | | |
| PERF-010 | Cache invalidation correctness | | |
| PERF-011 | Load test threshold compliance | | |
| PERF-012 | Cold start and warm-up performance | | |

Performance and scalability coverage: _____ Covered / _____ Partial / _____ Gap out of 12

---

## Reliability and operability domain

Tests in this domain: `domains/code/tests/reliability-and-operability.md`

| ID | Name | Status | Notes |
|---|---|---|---|
| REL-001 | External call error handling | | |
| REL-002 | Timeout enforcement | | |
| REL-003 | Retry and backoff correctness | | |
| REL-004 | Idempotency of retryable operations | | |
| REL-005 | Circuit breaker behavior | | |
| REL-006 | Graceful degradation | | |
| REL-007 | Structured logging sufficiency | | |
| REL-008 | Metrics and alerting coverage | | |
| REL-009 | Safe deployment and rollback | | |
| REL-010 | Configuration validation at startup | | |
| REL-011 | Feature flag safety | | |
| REL-012 | Health check accuracy | | |
| REL-013 | Partial failure containment | | |
| REL-014 | Environment parity validation | | |
| REL-015 | Database migration validation | | |
| REL-016 | Real-user monitoring (RUM) coverage | | |
| REL-017 | Synthetic monitoring coverage | | |
| REL-018 | A/B test experiment integrity | | |
| REL-019 | Handoff documentation sufficiency | | |
| REL-020 | Credential and access rotation at ownership transfer | | |

Reliability and operability coverage: _____ Covered / _____ Partial / _____ Gap out of 20

---

## Adversarial domain

Tests in this domain: `domains/code/tests/adversarial.md`

| ID | Name | Status | Notes |
|---|---|---|---|
| ADV-001 | Fuzz testing of public entry points | | |
| ADV-002 | Oversized and malformed payload handling | | |
| ADV-003 | Dependency tampering simulation | | |
| ADV-004 | Typosquatting dependency detection | | |
| ADV-005 | Privilege escalation attempt containment | | |
| ADV-006 | Obfuscated payload / malicious PR detection | | |
| ADV-007 | Build pipeline fault injection | | |
| ADV-008 | Unauthorized pipeline step injection | | |
| ADV-009 | Secrets exposure under pipeline chaos | | |
| ADV-010 | Replay attack resistance | | |
| ADV-011 | Injection attack resistance at API boundary | | |
| ADV-012 | Token and credential tampering resistance | | |
| ADV-013 | Chaos testing of dependency failure combinations | | |
| ADV-014 | Malicious input encoding and homoglyph resistance | | |
| ADV-015 | Hallucinated dependency detection | | |

Adversarial coverage: _____ Covered / _____ Partial / _____ Gap out of 15

---

## Coverage summary

| Domain | Total tests | Covered | Partial | Gap | Coverage % |
|---|---|---|---|---|---|
| Correctness and logic | 14 | | | | |
| Structure and style | 12 | | | | |
| Security | 18 | | | | |
| Architecture and design | 14 | | | | |
| Testing and coverage | 19 | | | | |
| Performance and scalability | 12 | | | | |
| Reliability and operability | 20 | | | | |
| Adversarial | 15 | | | | |
| **Total** | **124** | | | | |

Coverage % = Covered / Total tests. Partial counts as 0.5 for scoring purposes.

---

## Maturity level guide

Use the domain coverage matrix from `domains/code/framework/maturity-model.md` alongside total coverage to estimate the team or repository's maturity level.

| Observed coverage pattern | Likely maturity level |
|---|---|
| Structure/style and correctness mostly covered by manual review; security, testing, performance, reliability, adversarial mostly gaps | Level 2: Defined |
| All domains partially covered; adversarial partially covered | Level 2 to 3 transition |
| All domains covered; adversarial partial | Level 3: Automated |
| All domains fully covered including adversarial | Level 4: Adversarial |

Any domain with more than 50% gaps that is not the Adversarial domain is a signal of Level 1 or Level 2 maturity regardless of total coverage percentage.

---

## Next steps after completing this checklist

1. Score every Gap and Partial item using the severity model in `domains/code/framework/README.md`.
2. Use the scores to prioritize the remediation backlog.
3. Add new test IDs to the project test grid in `domains/code/grid/test-grid.md`.
4. Re-run this checklist after remediation to confirm advancement.
