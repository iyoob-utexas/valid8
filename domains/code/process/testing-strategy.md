# Building a Code Testing Strategy

This file covers two things: the standard steps for building a project-specific code validation plan, and the phased engagement methodology for running a full codebase assessment.

The engagement methodology (Phases 1 through 7 below) is strategic and runs once per engagement, at a major architecture change, or on a scheduled security review cycle. The operational runbook for executing a single PR or release cycle is in `domains/code/process/test-cycle.md`.

---

## Standard test strategy steps

1. Inventory artifacts
   - List repositories, services, libraries, and the APIs each one exposes.
   - Document ownership, release cadence, and consumer expectations (internal service, public API, library).

2. Select applicable dimensions
   - Determine which stages apply: planning and requirements, design and architecture, coding, integration and testing, deployment, operations and maintenance, and -- if ownership of the system will change hands -- handoff and transfer. Use `domains/code/dimensions/` to identify the relevant stage guidance.

3. Map test domains
   - Use `domains/code/tests/` to choose the applicable checks for each artifact.
   - Add project-specific validations on top of the generic catalog (e.g., a domain-specific business rule test).

4. Define acceptance criteria
   - Turn guidance into explicit conditions for success.
   - Capture thresholds, expected behaviors, and remediation steps.
   - Use the threshold starter table below when no historical data is available to calibrate from.

5. Maintain traceability
   - Document which tests apply to which artifact.
   - Track known limitations and open issues.

## Running this alone: solo operator and small-team guidance

Nothing in this strategy assumes a team large enough to staff every RACI role with a different person. See `domains/code/grid/raci-matrix.md` for the full guidance; the short version: the Owner/RACI columns in the grid name roles, not headcount, and one person -- a solo founder, an FDE working alone with a client -- can hold every role at once. Tier 1 checks do not become optional because there is no separate reviewer; run them against your own code using automated tooling (SAST, DAST, SCA, linting) as a substitute for the second-reviewer function, and treat any Tier 1 check you cannot personally verify as an open gap, not a skip.

This matters most for the engagement methodology below when the engagement is "validate my own solo-built app before I sell it" (see `domains/code/example-walkthrough.md` for a full worked example) -- Phases 1 through 7 still apply in full, run by one person, with `domains/code/dimensions/handoff-and-transfer.md` as mandatory scope rather than optional scope.

## Threshold calibration

All numeric thresholds in the grid ("set threshold", "project-configurable") must be replaced with explicit values before a check can produce a meaningful gate decision.

### Starter thresholds (use when no prior history is available)

These are conservative starting points. Tighten them after 2 to 3 release cycles of clean data.

| Check type | Starter threshold | Tighten after | Notes |
|---|---|---|---|
| Line coverage on changed code | >= 80% | 3 clean releases | Raise to 90%+ for payment/auth/compliance code paths |
| Branch coverage on changed code | >= 70% | 3 clean releases | |
| Mutation testing score (critical modules) | >= 60% | 2 clean cycles | Start with critical modules only; expand scope gradually |
| Cyclomatic complexity per function | <= 10 | Ongoing | Tighten to 8 for safety- or compliance-critical modules |
| Function length | <= 50 lines | Ongoing | Language-dependent; adjust for verbose languages |
| Duplicated code | <= 3% of codebase | Ongoing | Tighten as the codebase matures |
| Dependency vulnerability tolerance | Zero unresolved critical/high | Never relax | Medium/low findings tracked with a remediation SLA |
| p95 latency under load | Set per SLA; no default | After 1 load test baseline | Derive from the product's actual SLA commitment |
| Error budget / uptime | 99.9% default starting point | After 2 quarters of production data | Align to the team's SLO framework |
| Rollback time | <= 15 minutes | After 1 drill | Tighten as automation matures |
| Flaky test tolerance | Zero tests flaky across 10 consecutive CI runs | Ongoing | Quarantine and fix immediately; do not accumulate a "known flaky" list |

### How to calibrate from history

Once 2 or more clean release cycles are available:

1. Compute the pass rate and defect density for each monitored check across the baseline cycles.
2. Set the threshold at a level the team can sustain without becoming a false-positive generator, then tighten gradually.
3. Document the calibration date, the number of cycles used, and the resulting threshold in the project test plan.
4. Review and recalibrate quarterly or after any significant architecture or team change.

### Release-specific thresholds

For releases with a defined SLA or compliance requirement (uptime, latency, security certification), apply the same calibration approach. Define:

- A **floor threshold** below which a release is blocked (e.g., p95 latency above 500ms blocks the release)
- A **hard bound** the release must always satisfy regardless of history (e.g., zero unresolved critical CVEs)
- A **drift threshold** for release-over-release change (e.g., error rate increases more than 2x versus the prior release)

Document all release-specific thresholds in the project-specific test grid alongside the standard code quality thresholds.

## Continuous improvement

- Review this guide regularly as the project and stack evolve.
- Add new tests for novel languages, frameworks, or architecture patterns adopted by the team.
- Keep the hierarchy updated so AI code-review agents can reliably find the latest guidance.

---

## Engagement methodology

A code validation assessment is a structured review of a codebase's test coverage and failure resilience. It follows the phases of a penetration testing engagement, applied to software quality and security. Run this methodology at engagement kickoff, after a significant architecture change, or on a scheduled review cycle.

### Phase 1: Reconnaissance

The goal of reconnaissance is to build an accurate map of the codebase before any testing begins. Incomplete reconnaissance produces incomplete findings.

- Inventory every system zone in scope using the attack surface map in `domains/code/framework/README.md`.
- Catalog code assets: repositories, services, shared libraries, and public APIs.
- Collect API contracts, SLAs, and compliance requirements for each asset.
- Document ownership: who is responsible for each repository and each service.
- Identify external inputs: public API endpoints, webhooks, file uploads, third-party integrations.
- List all build and deployment pipeline stages and their expected order.
- Note any existing tests, scanners, or monitoring currently in place.

Deliverable: a codebase inventory table with assets, owners, contracts, and existing coverage noted per zone.

### Phase 2: Attack surface enumeration

Using the zone inventory from reconnaissance, walk each zone and enumerate the specific failure classes and adversarial conditions that apply.

- For each zone, apply the failure classes from the attack surface map.
- Identify trust boundaries: points where data crosses a network, process, or privilege boundary.
- Identify implicit contracts: assumptions baked into the code that have never been explicitly documented or tested.
- Enumerate external inputs that arrive without validation, authentication, or rate limiting.
- Note which zones have no alerting and would produce a silent failure if they degraded.

Deliverable: an annotated attack surface table identifying the highest-risk zones and trust boundaries.

### Phase 3: Threat modeling

Threat modeling translates the attack surface into a prioritized list of test scenarios.

- Map each identified failure class to the applicable test domain and test IDs from `domains/code/tests/`.
- For each zone with no existing coverage, score the gap using the severity model from `domains/code/framework/README.md`.
- Identify which ISO/IEC 25010 quality characteristics are most critical for each asset.
- Prioritize the test scenarios by severity score, focusing on gaps with the highest blast radius and lowest detectability.
- Classify each scenario by lifecycle stage: authoring, review, CI, pre-deployment, or production.

Deliverable: a prioritized test scenario list with test IDs, severity scores, and lifecycle assignments.

### Phase 4: Test execution

Execute tests from the catalogs in `domains/code/tests/` against the codebase zones in scope.

- Run tests at the lifecycle stage assigned during threat modeling.
- For each test, collect: the test ID, the result (pass, fail, or not covered), the timestamp, the evidence, and any unexpected behavior observed.
- Execute adversarial tests from `domains/code/tests/adversarial.md` in a non-production or pre-deployment environment.
- For any failure, document the exact condition that triggered it and the zone where it occurred.
- Flag any behavior that is technically passing but suspicious, such as a coverage threshold met only because trivial code was over-tested.

Deliverable: a raw test results log with one row per test executed, including result and evidence.

### Phase 5: Severity scoring

Apply the severity model from `domains/code/framework/README.md` to every failure and every identified coverage gap.

- Score each failure on blast radius, detectability, code criticality, and recoverability.
- Sum the four scores and apply the rating: Critical (16 to 20), High (11 to 15), Medium (7 to 10), Low (4 to 6).
- Group findings by severity rating and by system zone.
- Identify compound failures: cases where two or more medium-severity gaps combine to create a high-severity exposure (e.g., a missing rate limit combined with a weak lockout policy).
- Cross-reference severity ratings with the Tier model: a Critical-rated gap with no Tier 1 test coverage is the highest-priority finding.

Deliverable: a scored findings table with severity ratings, zone assignments, and compound failure notes.

### Phase 6: Findings report

Compile the scored findings into a structured report that stakeholders can act on.

The findings report includes the following sections:

- Assessment scope: which repositories, services, and zones were in scope.
- Engagement dates and participants.
- Current maturity level from `domains/code/framework/maturity-model.md` and target level.
- Test coverage summary: a domain coverage table showing which test IDs were executed, which passed, which failed, and which were not covered.
- Scored findings table: one row per finding, with test ID, zone, description, severity score, rating, and root cause.
- Compound failure analysis: any multi-gap exposures identified.
- Remediation recommendations: specific test IDs to implement, threshold changes to make, or architecture changes to address.
- Residual risk: findings that cannot be immediately addressed, with interim mitigation notes.
- Next steps: recommended timeline for retesting and maturity advancement.

### Phase 7: Remediation and retest

Findings do not close until they are retested.

- Prioritize remediation by severity: Critical and High findings address before the next release if possible.
- For each remediation, implement the specific test from the catalog that would have detected the failure.
- Rerun the original test conditions to confirm the finding is resolved.
- Confirm no regression: validate that the fix did not introduce a new gap or degrade an adjacent test.
- Update the coverage checklist in `domains/code/framework/coverage-checklist.md` to reflect new coverage.
- Re-score the codebase maturity after remediation.

Deliverable: an updated findings report with closed findings marked, retest evidence attached, and residual risk restated.
