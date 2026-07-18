# Testing Maturity Model

This model defines four levels of validation maturity for a codebase or engineering team. Each level describes the test domains covered, the degree of automation, and the overall posture toward code quality and security.

Use this model to assess where a team or repository currently sits, and to set a target level for a given engagement or roadmap cycle. For a coverage self-assessment, use `domains/code/framework/coverage-checklist.md`.

---

## The four levels

| Level | Name | Gate model | Automation | Adversarial readiness |
|---|---|---|---|---|
| 1 | Reactive | Informal or none | Manual, incident-driven review | None |
| 2 | Defined | Documented tiers with explicit thresholds | Linting and unit tests in CI | Minimal |
| 3 | Automated | Full CI plus security scanning and production monitoring | Comprehensive automation across most domains | Partial |
| 4 | Adversarial | Severity-scored, chaos-tested, self-assessed | End-to-end including fuzzing and supply-chain checks | Full |

---

## Level 1: Reactive

The team reviews code only informally, and testing happens after a bug is reported rather than before a change ships. There is no proactive test strategy and no shared vocabulary for what "good" means. Checks exist as ad-hoc habits that vary by reviewer and are not consistently applied or documented.

**What is covered:**
- Correctness and logic: ad-hoc, dependent on individual reviewer diligence
- Structure and style: informal, no linter enforced
- Security: not covered except by chance
- Architecture and design: not covered
- Testing and coverage: some unit tests exist, no coverage target
- Performance and scalability: not covered
- Reliability and operability: not covered
- Adversarial: not covered

**Characteristics:**
- Checks are triggered by an incident, not planned before one
- No standardized test IDs or outcome vocabulary
- No gate model; failures produce ad-hoc responses
- No dashboard or results history

**How to advance to Level 2:** adopt a linter and formatter in CI, require unit tests on new code, and document explicit severity tiers for what blocks a merge.

---

## Level 2: Defined

The team has a linter, a formatter, and unit tests enforced in CI. The Tier model is in use for security and correctness findings, and reviewers know what each tier means. PR review is a required gate. Some dependency scanning is in place. API versioning exists even if not formally enforced.

**What is covered:**
- Correctness and logic: partial (unit tests on new code; edge cases inconsistent)
- Structure and style: full (linter and formatter enforced in CI)
- Security: partial (dependency scan on a cadence; no SAST)
- Architecture and design: informal (reviewed by convention, not checked)
- Testing and coverage: partial (unit tests required; coverage threshold not enforced)
- Performance and scalability: minimal (no load testing)
- Reliability and operability: partial (timeouts used inconsistently)
- Adversarial: minimal (dependency vulnerability scan only)

**Characteristics:**
- DPPF-style IDs in use as a common reference language
- Tier 1 findings block the merge; Tier 2 triggers investigation
- Results logged in PR comments but not trended
- No fuzzing or chaos testing practiced

**How to advance to Level 3:** add SAST and mutation testing to CI, enforce coverage thresholds, add load testing before release, and formalize timeout/retry/circuit-breaker patterns as reviewed requirements.

---

## Level 3: Automated

The team has comprehensive CI automation across correctness, structure, security scanning (SAST/dependency), architecture linting, testing coverage thresholds, and load testing, with production monitoring for reliability. Mutation testing runs on a cadence. Feature flags and safe deployment practice are standard. Adversarial testing (fuzzing, chaos) is not yet systematic.

**What is covered:**
- Correctness and logic: full
- Structure and style: full
- Security: full (SAST, dependency scanning, secret scanning in CI)
- Architecture and design: full (architecture linting and review checklist enforced)
- Testing and coverage: full (coverage thresholds enforced; mutation testing on a cadence)
- Performance and scalability: full (load testing before major releases)
- Reliability and operability: full (timeouts, retries, circuit breakers standard; deployment is canaried)
- Adversarial: partial (dependency tampering and basic fuzzing; chaos and replay testing not yet systematic)

**Characteristics:**
- Coverage self-assessment completed at least once
- Severity scoring used to prioritize gaps
- Maturity model reviewed at each engagement kickoff
- Fuzz testing practiced on public entry points in CI
- Alerting active on Tier 1 categories with defined on-call ownership

**How to advance to Level 4:** implement all adversarial domain tests including chaos testing of dependency combinations, replay attack resistance, malicious PR / obfuscated payload detection, and supply-chain tampering simulation; run coverage reviews on a scheduled cycle; apply severity scoring to every known gap.

---

## Level 4: Adversarial

The team operates the full test catalog across all eight domains. Fuzzing, chaos testing, and supply-chain tampering simulation are regular practices in CI and pre-deployment environments. The coverage checklist is used as a periodic self-assessment. Severity scoring is applied to every uncovered test and findings drive the remediation backlog.

**What is covered:**
- Correctness and logic: full
- Structure and style: full
- Security: full
- Architecture and design: full
- Testing and coverage: full
- Performance and scalability: full
- Reliability and operability: full
- Adversarial: full (all ADV-001 through ADV-014)

**Characteristics:**
- Coverage review completed on a scheduled cycle using `domains/code/framework/coverage-checklist.md`
- Every gap scored with the severity model from `domains/code/framework/README.md`
- Findings report produced and remediation backlog maintained
- Adversarial tests run in pre-deployment and selected in production
- Maturity level is formally reviewed per engagement or per quarter

---

## Domain coverage matrix

| Domain | Level 1 | Level 2 | Level 3 | Level 4 |
|---|---|---|---|---|
| Correctness and logic | Partial | Partial | Full | Full |
| Structure and style | Minimal | Full | Full | Full |
| Security | None | Partial | Full | Full |
| Architecture and design | None | Informal | Full | Full |
| Testing and coverage | Minimal | Partial | Full | Full |
| Performance and scalability | None | Minimal | Full | Full |
| Reliability and operability | None | Partial | Full | Full |
| Adversarial | None | Minimal | Partial | Full |

---

## Using the maturity model in an engagement

1. At kickoff, use the attack surface map in `domains/code/framework/README.md` to identify which system zones are in scope.
2. Complete the coverage self-assessment in `domains/code/framework/coverage-checklist.md` to identify which test categories are currently covered.
3. Map the results to the domain coverage matrix above to determine the current maturity level.
4. Set a target maturity level for the engagement and identify the specific test IDs needed to close the gap.
5. Score any uncovered gaps using the severity model and prioritize remediation accordingly.
6. Re-run the self-assessment at the close of the engagement to confirm advancement.
