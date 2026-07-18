# Building a Data Testing Strategy

This file covers two things: the standard steps for building a project test plan, and the DPPF engagement methodology for running a full pipeline assessment.

The DPPF methodology (Phases 1 through 7 below) is strategic and runs once per engagement or major pipeline change. The operational runbook for executing a single test cycle is in `domains/data/process/test-cycle.md`.

---

## Standard test strategy steps

1. Inventory artifacts
   - List raw sources, intermediate datasets, and final data products.
   - Document ownership, frequency, and consumer expectations.

2. Select applicable dimensions
   - Determine which lifecycle dimensions apply to each artifact.
   - Use `domains/data/dimensions/` to identify the relevant stage.

3. Map test categories
   - Use `domains/data/tests/` to choose the applicable checks for each artifact.
   - Add business-specific validations on top of the generic categories.

4. Define acceptance criteria
   - Turn guidance into explicit conditions for success.
   - Capture thresholds, expected behaviors, and remediation steps.
   - Use the threshold starter table below when no historical data is available to calibrate from.

5. Maintain traceability
   - Document which tests apply to which artifact.
   - Track known limitations and open issues.

## Threshold calibration

All anomaly thresholds must be explicit before a test can produce a meaningful gate decision. The test grid uses "X%" as a placeholder throughout. Replace every placeholder with a project-specific value before the first production run.

### Starter thresholds (use when no prior history is available)

These are conservative starting points. Tighten them after 3 to 6 periods of clean data.

| Check type | Starter threshold | Tighten after | Notes |
|---|---|---|---|
| MoM volume / row count change | ±20% | 3 clean periods | Widen for known seasonal pipelines |
| MoM key metric change (revenue, spend, cost) | ±25% | 6 clean periods | Tighten to ±10-15% once baseline is stable |
| QoQ key metric change | ±30% | 4 clean quarters | |
| Null rate on optional fields | <5% | Establish per-field baseline | Key fields must be 0% |
| Null rate on key / required fields | 0% | Never relax | Zero tolerance |
| Duplicate rate | 0% | Never relax | Zero tolerance |
| Data freshness SLA | 24h for daily pipelines; 7 days for weekly; 1 business day after period close for batch | Confirm with stakeholders | |
| Cross-validation / tie-out tolerance | 0.01% for financial data; 0.1% for operational data | Confirm with stakeholders | Tighter for regulated outputs |
| KPI rate bounds | [0, 1] for rate and ratio metrics; [-1, 1] for margin and variance metrics | Per business definition | Values outside bounds indicate a calculation defect |
| Seasonal breach | ±2 standard deviations from same-period prior-year average | After 2+ years of history | Not applicable on Run 1 |

### How to calibrate from history

Once 3 or more clean periods are available:

1. Compute the mean and standard deviation for each monitored metric across the baseline periods.
2. Set the threshold at mean ± 2 standard deviations, or at the 5th and 95th percentile of observed values.
3. Document the calibration date, the number of periods used, and the resulting threshold in the project test plan.
4. Review and recalibrate annually or after any significant pipeline or business change.

### Operational KPI thresholds

For pipelines that produce service-level or performance KPIs (on-time rates, fill rates, lead times, error rates, SLA compliance), apply the same calibration approach. Define:

- A **floor threshold** below which a value triggers a Tier 2 alert (e.g., on-time delivery rate below 80%)
- A **range bound** that the KPI must always satisfy regardless of history (e.g., on-time rate cannot exceed 100%)
- A **drift threshold** for period-over-period change in the KPI (e.g., on-time rate drops more than 15 percentage points MoM)

Document all operational KPI thresholds in the project-specific test grid alongside the standard data quality thresholds.

## Continuous improvement

- Review the guide regularly as the project evolves.
- Add new tests for novel data patterns, sources, or business rules.
- Keep the hierarchy updated so AI tools can reliably find the latest guidance.

---

## DPPF engagement methodology

A DPPF assessment is a structured review of a data pipeline's test coverage and failure resilience. It follows the phases of a penetration testing engagement, applied to data reliability. Run this methodology at engagement kickoff, after significant pipeline changes, or on a scheduled review cycle.

### Phase 1: Reconnaissance

The goal of reconnaissance is to build an accurate map of the pipeline before any testing begins. Incomplete reconnaissance produces incomplete findings.

- Inventory every pipeline zone in scope using the attack surface map in `domains/data/framework/README.md`.
- Catalog data assets: raw sources, intermediate tables, final products, and exported artifacts.
- Collect data contracts, SLAs, and freshness expectations for each asset.
- Document ownership: who is responsible for each pipeline zone and each data asset.
- Identify external inputs: source system feeds, file drops, APIs, and event streams.
- List all orchestration dependencies and their expected execution order.
- Note any existing tests, alerts, or monitoring currently in place.

Deliverable: a pipeline zone inventory table with assets, owners, contracts, and existing coverage noted per zone.

### Phase 2: Attack surface enumeration

Using the zone inventory from reconnaissance, walk each zone and enumerate the specific failure classes and adversarial conditions that apply.

- For each zone, apply the failure classes from the attack surface map.
- Identify trust boundaries: points where data crosses a system, team, or format boundary.
- Identify implicit contracts: assumptions baked into the pipeline that have never been explicitly documented or tested.
- Enumerate external inputs that arrive without validation, schema enforcement, or SLA monitoring.
- Note which zones have no alerting and would produce a silent failure if they degraded.

Deliverable: an annotated attack surface table identifying the highest-risk zones and trust boundaries.

### Phase 3: Threat modeling

Threat modeling translates the attack surface into a prioritized list of test scenarios.

- Map each identified failure class to the applicable DPPF domain and test IDs from `domains/data/tests/`.
- For each zone with no existing coverage, score the gap using the DPPF severity model from `domains/data/framework/README.md`.
- Identify which data quality dimensions from DAMA-DMBOK and which observability pillars are most critical for each asset.
- Prioritize the test scenarios by severity score, focusing on gaps with the highest blast radius and lowest detectability.
- Classify each scenario by lifecycle stage: development, CI, pre-deployment, or production monitoring.

Deliverable: a prioritized test scenario list with DPPF IDs, severity scores, and lifecycle assignments.

### Phase 4: Test execution

Execute tests from the DPPF catalogs in `domains/data/tests/` against the pipeline zones in scope.

- Run tests at the lifecycle stage assigned during threat modeling.
- For each test, collect: the test ID, the result (pass, fail, or not covered), the timestamp, the evidence, and any unexpected behavior observed.
- Execute adversarial tests from `domains/data/tests/adversarial.md` in a non-production or pre-deployment environment.
- For any failure, document the exact condition that triggered it and the zone where it occurred.
- Flag any behavior that is technically passing but suspicious, such as a test that passes because the threshold is too loose.

Deliverable: a raw test results log with one row per test executed, including result and evidence.

### Phase 5: Severity scoring

Apply the DPPF severity model from `domains/data/framework/README.md` to every failure and every identified coverage gap.

- Score each failure on blast radius, detectability, data criticality, and recoverability.
- Sum the four scores and apply the rating: Critical (16 to 20), High (11 to 15), Medium (7 to 10), Low (4 to 6).
- Group findings by severity rating and by pipeline zone.
- Identify compound failures: cases where two or more medium-severity gaps combine to create a high-severity exposure.
- Cross-reference severity ratings with the Tier model: a Critical-rated gap with no Tier 1 test coverage is the highest-priority finding.

Deliverable: a scored findings table with severity ratings, zone assignments, and compound failure notes.

### Phase 6: Findings report

Compile the scored findings into a structured report that stakeholders can act on.

The findings report includes the following sections:

- Assessment scope: which pipeline zones and data assets were in scope.
- Engagement dates and participants.
- Current maturity level from `domains/data/framework/maturity-model.md` and target level.
- Test coverage summary: a DPPF domain coverage table showing which test IDs were executed, which passed, which failed, and which were not covered.
- Scored findings table: one row per finding, with DPPF ID, zone, description, severity score, rating, and root cause.
- Compound failure analysis: any multi-gap exposures identified.
- Remediation recommendations: specific DPPF test IDs to implement, threshold changes to make, or architecture changes to address.
- Residual risk: findings that cannot be immediately addressed, with interim mitigation notes.
- Next steps: recommended timeline for retesting and maturity advancement.

### Phase 7: Remediation and retest

Findings do not close until they are retested.

- Prioritize remediation by severity: Critical and High findings address before the next production run if possible.
- For each remediation, implement the specific test from the DPPF catalog that would have detected the failure.
- Rerun the original test conditions to confirm the finding is resolved.
- Confirm no regression: validate that the fix did not introduce a new gap or degrade an adjacent test.
- Update the DPPF coverage checklist in `domains/data/framework/dppf.md` to reflect new coverage.
- Re-score the pipeline maturity after remediation.

Deliverable: an updated findings report with closed findings marked, retest evidence attached, and residual risk restated.
