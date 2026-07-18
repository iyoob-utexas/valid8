# Guide Usage for Humans and AI

This file explains how to navigate and use the repo, with specific instructions for AI agents (including code-review agents) that need to parse, select, or generate tests from the framework. It also maps each test category to common real-world tools.

---

## For human engineers

Start at `domains/code/README.md` for the full navigation map. The short path is:

1. `domains/code/framework/README.md` to understand the severity model and testing standard.
2. `domains/code/grid/test-grid.md` to see every test with its tier, threshold, owner, and catalog ID.
3. `domains/code/process/test-cycle.md` to run a test cycle step by step.
4. `domains/code/tests/<domain>.md` when you need to understand a specific test category in depth.

When starting a new project, use `domains/code/process/testing-strategy.md` to scope the engagement and decide which test IDs apply. When assessing an existing codebase, open `domains/code/framework/coverage-checklist.md` and mark each ID as Covered, Partial, or Gap.

---

## Tool mapping by test domain

This maps each test domain to common, real tooling. These are illustrative, not mandated -- swap in whatever the project's stack already supports.

| Test domain | Common tools |
|---|---|
| Correctness and logic | pytest, Jest, JUnit; property-based testing: Hypothesis, fast-check, QuickCheck; static typing: mypy, TypeScript strict mode |
| Structure and style | ESLint, Prettier, Ruff, Black, gofmt, StyleCop; complexity/duplication: SonarQube, radon, jscpd |
| Security | Semgrep, CodeQL, SonarQube security rules; dependency scanning: Snyk, Dependabot, npm audit, pip-audit; secret scanning: gitleaks, TruffleHog, GitHub secret scanning; DAST: OWASP ZAP, Burp Suite |
| Architecture and design | dependency-cruiser, madge, ArchUnit; API compatibility: openapi-diff, buf breaking, api-extractor |
| Testing and coverage | Coverage: pytest-cov, Istanbul/nyc, JaCoCo; mutation testing: Stryker, mutmut, PIT; flaky test detection: pytest-randomly, repeated CI run analysis |
| Performance and scalability | Load testing: k6, JMeter, Locust, Gatling; profiling: py-spy, Chrome DevTools, pprof; N+1 detection: Bullet, django-debug-toolbar |
| Reliability and operability | Resilience libraries: resilience4j, Polly; observability: Prometheus, Datadog, New Relic, OpenTelemetry; chaos: Gremlin, Chaos Monkey |
| Adversarial | Fuzzing: AFL, libFuzzer, Atheris, go-fuzz; supply chain: Sigstore/cosign, npm ci with hash checking; penetration testing: OWASP ZAP, sqlmap, Burp Suite |

For CI environments, most of these tools run as a pipeline step gated on a pass/fail exit code. Wire Tier 1 tools to block the pipeline; wire Tier 2 tools to annotate the PR without blocking; wire Tier 3 tools to a scheduled scan that reports to a dashboard.

---

## For AI agents

### What this repo contains

Every test in this framework is addressable by a catalog ID. IDs follow this format:

```
<DOMAIN>-<NUMBER>
```

Domains:
- `COR` - Correctness and logic (edge cases, null handling, algorithm fidelity)
- `STY` - Structure and style (readability, naming, complexity, duplication)
- `SEC` - Security (OWASP Top 10, CWE, secrets, access control)
- `ARC` - Architecture and design (SOLID, coupling/cohesion, API compatibility)
- `TST` - Testing and coverage (unit/integration/e2e, coverage, mutation testing)
- `PERF` - Performance and scalability (complexity, N+1, memory, concurrency)
- `REL` - Reliability and operability (error handling, retries, deployment safety)
- `ADV` - Adversarial (fuzzing, supply-chain tampering, chaos, replay)

Each ID resolves to a test definition with the following fields, found in the catalog tables in `domains/code/tests/`:

| Field | What it means |
|---|---|
| ID | Unique catalog identifier |
| Name | Short test name |
| What it verifies | The specific condition the test checks |
| Defends against | The failure or attack scenario the test prevents |
| Standards | The reference standard(s) it maps to (OWASP, CWE, SOLID, ISO/IEC 25010, SemVer) |
| Lifecycle | Where in the code lifecycle the test runs (Planning, Design, Authoring, Review, CI, Pre-deployment, Deployment, Production) |

### How to select tests for a given codebase

1. Read the attack surface map in `domains/code/framework/README.md` to identify which system zones are in scope.
2. Map each zone to the relevant test domains using the domain table in `domains/code/framework/README.md`.
3. For each in-scope domain, pull the catalog from `domains/code/tests/<matching file>.md`.
4. Filter by lifecycle stage to match the execution context (PR review, CI, pre-deployment, etc.).
5. Filter by "Defends against" to select tests that match known risk patterns for the codebase type (e.g., a payment service prioritizes SEC-001, SEC-007, ADV-011).

### How to identify coverage gaps

Load the checklist from `domains/code/framework/coverage-checklist.md`. It lists all 124 test IDs organized by domain. Any ID marked Gap or Partial is a coverage gap. Score gaps using the severity model in `domains/code/framework/README.md`:

- Blast radius (1-5): how much of the codebase or product is affected
- Detectability (1-5): how hard the failure is to detect (5 = silent)
- Code criticality (1-5): how critical the affected code path is
- Recoverability (1-5): how difficult recovery is

Sum the four scores. Scores of 16-20 are Critical; 11-15 High; 7-10 Medium; 4-6 Low.

### How to generate a test implementation

Use the test catalog entry as a specification. The "What it verifies" field is the assertion to implement. The "Defends against" field is the failure scenario to use when writing test fixtures or adversarial inputs. The "Lifecycle" field tells you which stage to instrument.

Example using SEC-001:
- What it verifies: all user-controlled input reaching a SQL query, shell command, template engine, or LDAP query is parameterized or escaped
- Defends against: SQL injection, OS command injection, template injection, LDAP injection
- Lifecycle: Authoring, Review, CI
- Implementation approach: grep for string concatenation feeding into query/command execution functions; replace with parameterized queries or an escaping library; add a Semgrep rule to catch regressions; add a test case using a known injection payload that must be rejected or safely neutralized.

### How to map tests to the test grid

`domains/code/grid/test-grid.md` is the master checklist. Each row has a catalog-ID-bearing domain and name. Use this to cross-reference grid rows with catalog entries, or to add new grid rows for catalog entries not yet in the grid.

### How to use the maturity model

`domains/code/framework/maturity-model.md` describes four maturity levels (Reactive, Defined, Automated, Adversarial). Map a codebase to a maturity level by checking the domain coverage matrix against the coverage-checklist gap assessment. The model also defines the specific test IDs needed to advance to each level.

### Key data structures to parse

| File | Primary structure | Key fields |
|---|---|---|
| `domains/code/grid/test-grid.md` | Table | ID, Domain, Tier, Acceptance threshold, Tooling, Owner, Lifecycle stage |
| `domains/code/tests/<domain>.md` | Catalog table | ID, Name, What it verifies, Defends against, Standards, Lifecycle |
| `domains/code/framework/coverage-checklist.md` | Checklist table per domain | ID, Name, Status, Notes |
| `domains/code/dimensions/*.md` | Prose + checklist | Stage-specific guidance for authoring, review, and production |
