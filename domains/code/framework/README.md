# Framework Standard

This document describes the standard and principles behind the code validation framework.

## Purpose and scope

- Define repeatable, defensible code review and testing practice for engineering teams and client engagements.
- Move beyond "it built and the tests are green" to confirm the code is correct, secure, maintainable, and operable.
- Apply a consistent baseline across authoring, PR review, CI, and production operation.
- Stay tool-agnostic while naming common tooling (ESLint, SonarQube, Semgrep, Snyk, Stryker, k6) where helpful.

## What this standard requires

- Explicit pass/fail thresholds for every check.
- A named owner for every test category or check.
- Severity tiers that determine whether a failure blocks a merge, requires a fix before release, or is tracked as advisory.
- Documentation of quality expectations and release acceptance criteria.

## The reference principles

- OWASP Top 10 (2021): the ten most critical web application security risk categories.
- CWE Top 25: the most dangerous software weaknesses by prevalence and severity.
- SOLID principles: single responsibility, open/closed, Liskov substitution, interface segregation, dependency inversion.
- Clean Code practice: naming, function size, comment discipline, and readability as first-class engineering concerns.
- ISO/IEC 25010 (SQuaRE) software quality model: functional suitability, performance efficiency, compatibility, usability, reliability, security, maintainability, portability.
- The testing pyramid (Cohn): a broad base of unit tests, a smaller layer of integration tests, and a thin layer of end-to-end tests.
- Google engineering practices: code review standards, small changes, readability, CI enforcement.
- Semantic Versioning and Conventional Commits: predictable, machine-parseable change communication.

## Severity tiers

These tiers govern gate decisions: what to do when a check fails.

- Tier 1 / Critical: zero tolerance. Failures block the merge or block the release. Examples: a critical/high vulnerability, a broken build, a failing Tier 1 correctness test.
- Tier 2 / Important: warn and investigate. The PR may merge under review, with a required-fix-before-release action or an alert.
- Tier 3 / Good practice: monitor and trend. No hard gate, but surface as tech debt for follow-up.

### FAIL vs WARN within Tier 2

Tier 2 results use two distinct statuses:

- **FAIL**: the required action is fix-before-release. Record as FAIL and block the release (not necessarily the merge) until resolved.
- **WARN**: the required action is flag, ticket, or review. Record as WARN and log for follow-up; the PR may merge and release.

Use FAIL when the defect is already reachable in a released or release-candidate build. Use WARN when the defect is contained to a code path not yet exposed, or is a maintainability concern rather than a behavioral one.

**Escalation rule:** If a Tier 2 failure is on a code path that becomes reachable from an external, unauthenticated surface -- for example, a missing authorization check on an internal-only endpoint that is then exposed publicly -- escalate to Tier 1 and block the release.

## Ownership and roles

- Each check should have one accountable owner.
- Use RACI to assign who is Responsible, Accountable, Consulted, and Informed.
- Common roles: Author, Reviewer, Security champion, Tech lead, SRE / on-call.

## Applying the standard

1. Define the engagement scope: which repositories, services, or PRs are in scope.
2. Map those artifacts to the stages in `domains/code/dimensions/`.
3. Use `domains/code/tests/` to identify applicable checks.
4. Use `domains/code/grid/test-grid.md` to build a project-specific grid and owner matrix.
5. Use `domains/code/framework/coverage-checklist.md` to run a coverage self-assessment and identify gaps.
6. Use `domains/code/framework/maturity-model.md` to position the team or repository at its current maturity level.
7. Log and monitor every run using the guidance in `domains/code/dashboards/README.md`.

---

## Adversarial reliability standard

Treat every codebase as a system operating under adversarial conditions. Just as penetration testing assumes an attacker will find the weakest point, this standard assumes input will be malformed or hostile, dependencies will be compromised, pipelines will be tampered with, and contributors -- malicious or careless -- will introduce defects that a shallow review misses.

The adversarial reliability standard extends the Tier model by adding a second lens: not just "what do we do when this fails" but "how bad is it that this failure mode exists at all."

### The eight test domains

Tests in this framework are organized into eight domains drawn from OWASP, CWE, SOLID, Clean Code, ISO/IEC 25010, the testing pyramid, and chaos/adversarial engineering practice. Each domain maps to one test category file in `domains/code/tests/`.

| Domain | Focus | Primary location |
|---|---|---|
| Correctness and logic | Edge cases, null handling, algorithm fidelity, error propagation | `domains/code/tests/correctness-and-logic.md` |
| Structure and style | Readability, naming, complexity, duplication, dead code | `domains/code/tests/structure-and-style.md` |
| Security | OWASP Top 10, CWE Top 25, secrets, access control | `domains/code/tests/security.md` |
| Architecture and design | SOLID, coupling/cohesion, layering, API compatibility | `domains/code/tests/architecture-and-design.md` |
| Testing and coverage | Unit/integration/e2e presence, coverage, mutation testing, flakiness | `domains/code/tests/testing-and-coverage.md` |
| Performance and scalability | Complexity, N+1 queries, memory, concurrency, caching | `domains/code/tests/performance-and-scalability.md` |
| Reliability and operability | Error handling, retries, idempotency, deployment safety | `domains/code/tests/reliability-and-operability.md` |
| Adversarial | Fuzzing, supply-chain tampering, privilege escalation, chaos | `domains/code/tests/adversarial.md` |

### Attack surface map

The following table enumerates every zone of a generic software system, the failure classes that can occur in each zone, and the adversarial conditions that testing should simulate.

| Zone | Failure classes | Adversarial conditions | Primary domains |
|---|---|---|---|
| Input / API boundary | Missing validation, injection, oversized payloads, malformed structure | Fuzzed input, injection payloads, decompression bombs, boundary-violating values | Security, Adversarial, Correctness |
| Auth layer | Broken authentication, session fixation, token forgery, privilege escalation | Credential stuffing, token tampering, algorithm confusion, replay of captured tokens | Security, Adversarial |
| Business logic | Logic defects, race conditions, incorrect calculations, broken invariants | Edge-case and boundary inputs, concurrent mutation of shared state, adversarial sequencing of operations | Correctness, Architecture |
| Data access layer | Injection, N+1 queries, missing authorization on queries, unbounded fetches | SQL/NoSQL injection payloads, forced large result sets, cross-tenant data access attempts | Security, Performance |
| External API / third-party calls | No timeout, no retry bound, SSRF, unvalidated response trust | Slow or hung third-party responses, malicious redirect targets, malformed third-party payloads | Reliability, Security |
| Build / CI pipeline | Unauthorized step injection, artifact tampering, secret leakage | Killed builds mid-run, injected pipeline steps, forced verbose logging capturing secrets | Adversarial, Security |
| Deployment / runtime | Bad rollout with no rollback, misconfiguration, resource exhaustion | Config validation bypass, forced canary skip, simulated resource starvation during deploy | Reliability, Performance |
| Dependency supply chain | Vulnerable packages, typosquatting, compromised transitive dependency | Simulated dependency substitution, unpinned version drift, malicious postinstall scripts | Security, Adversarial |

---

## DPPF severity scoring model

This model complements the Tier model. Tiers govern gate actions. Severity scores measure the depth of risk when a test category has no coverage or a failure goes undetected. Apply this scoring model during codebase assessments and coverage reviews.

Score each failure type on four factors, each rated 1 to 5. Sum the four scores to produce a total from 4 to 20, then map to a severity rating.

### Scoring factors

| Factor | What it measures | Score 1 | Score 3 | Score 5 |
|---|---|---|---|---|
| Blast radius | How much of the codebase, service, or product is affected | Single function or file | One service or module | Entire product, all services, or shared platform library |
| Detectability | How difficult the failure is to detect (higher = harder) | Caught by linter or CI on every run | Delayed manual detection in review or QA | Silent failure with no signal until a user or incident reports it |
| Code criticality | Importance of the affected code path to the business | Internal tooling or dev-only script | Standard product feature | Payment, auth, compliance, or safety-critical path |
| Recoverability | Effort required to recover from the failure | Automatic rollback or self-healing | Manual hotfix with time impact | Full incident response, data remediation, or customer notification required |

### Severity ratings

| Total score range | Rating | Recommended response |
|---|---|---|
| 16 to 20 | Critical | Treat as a blocking gap. Add or fix the test before the next release. |
| 11 to 15 | High | Prioritize in the next sprint. Document risk until resolved. |
| 7 to 10 | Medium | Address in the next planning cycle. Monitor in the interim. |
| 4 to 6 | Low | Log as a known gap. Review at next framework refresh. |

### Relating severity to tiers

Tier and severity serve different purposes. Use both together.

- Tier answers: what action do we take when this check fails?
- Severity answers: how significant is it that we have no coverage here, or that this failure can occur silently?

A Tier 3 check can carry a High severity score if it covers silent degradation of a critical path. A Tier 1 check can have a Low severity score if the failure is immediately visible in CI and trivially fixed. Score them independently.
