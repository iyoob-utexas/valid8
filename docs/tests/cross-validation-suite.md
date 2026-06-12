# Cross-Validation Suite

This page defines a suite of cross-validation checks that compare results across different dimensions, stages, and sources. It includes mechanical cross-validation (comparing data against itself from multiple angles) and sensibility analysis (comparing data against business context and expectations).

## Purpose

- Validate the same truth from multiple perspectives.
- Catch silent failures that single-dimension checks may miss.
- Confirm that ingestion, processing, and final output remain aligned.
- Apply an outside-in smell test: does the data tell a coherent story that a knowledgeable person would believe?

## Why cross-validation matters

Data projects are inherently multi-dimensional. A pipeline can pass a schema check while still producing incorrect totals, a wrongly mapped account, or a mismatched delivery artifact. Cross-validation ensures the output is consistent across sources, transformations, and business expectations.

Sensibility analysis adds a layer that no automated rule fully covers: human business judgment. A result can be technically correct and still be wrong in context. If revenue doubled but nothing in the business explains it, the data deserves scrutiny before it reaches a stakeholder.

---

## Core cross-validation groups

- Source vs processed output
  - row count reconciliation
  - source total vs transformed total
  - schema and key alignment

- Processed output vs final report
  - mapping coverage
  - dual-path reconciliation (bottom-up vs top-down)
  - budget vs actual tie-outs

- Shared source and derived values
  - shared datasets and source feeds
  - FX and unit consistency across outputs
  - cross-table invariant checks

- Anomaly results vs expectation
  - outlier detection results compared with business thresholds
  - data drift alerts compared with final output validation

## Example suite checks

- `ERP Source vs Calculated Output` (source totals compared to output totals)
- `Bottom-Up vs Top-Down P&L` (two independent aggregation paths)
- `GL Account Mapping Coverage` (every source account maps to a report item)
- `Intercompany Elimination Check` (post-consolidation netting)
- `Aggregated Report vs Raw Query` (presentation totals vs direct source query)
- `Budget vs Actual Tie-Out` (budget and actuals using the same shared actuals source)
- `Currency / FX Consistency` (same FX source and rate date across outputs)

## Existing repo coverage

The repo already includes cross-validation guidance in the master `docs/grid/test-grid.md` matrix and the `docs/tests/integrity-and-references.md` category. The suite above makes those checks explicit and groups them into coordinated validation behavior.

## How to use it

1. Select the cross-validation checks that apply to the data domain.
2. Execute the checks as a coordinated suite after the pipeline reaches the final reporting layer.
3. Use results from ingestion, processing, and output to confirm alignment.
4. Surface mismatches as failures or exceptions, with a focus on Tier 1 and Tier 2 gate behavior.
5. Run sensibility analysis last, after mechanical cross-validation passes, to catch anything rules cannot see.

## Outcome

A cross-validation suite turns individual tests into a stronger system-level check. It validates that the pipeline is not only internally correct, but also coherent across source, transformation, and business-reporting dimensions.

---

## Sensibility analysis

Sensibility analysis is the outside-in view. Where mechanical tests ask "does the data match the rules," sensibility asks "does the data make sense to someone who understands the business?"

A sensibility failure is a result that is technically valid but contextually implausible: a revenue figure that doubled with no known explanation, a headcount that dropped to zero while payroll costs stayed flat, a balance that has never been this high in the company's history.

Sensibility checks cannot be fully automated because they require domain knowledge. But they can be structured and made consistent. The goal is to build a library of business-specific sanity checks that are run at the end of each pipeline cycle, before results are delivered to stakeholders.

### Why sensibility is different from statistical anomaly detection

Statistical anomaly detection (STAT-002, STAT-003, STAT-004) flags values that are unusual relative to a quantitative baseline. Sensibility analysis asks whether the values make sense relative to a qualitative business narrative.

A value can be within its statistical range and still be implausible. A value can be statistically unusual and perfectly explainable. Sensibility analysis requires context that statistical tests cannot hold.

### Categories of sensibility checks

**Business plausibility**
Does the magnitude of a value make sense for this entity type, industry, and period?
- A company with 10 employees reporting $500M in revenue without a known explanation.
- A monthly expense line larger than annual revenue from the prior year.
- A transaction amount that is orders of magnitude larger than any prior transaction for the same vendor.

**Ratio and margin consistency**
Do rates, margins, and proportions fall within expected ranges for the business?
- Gross margin outside the historically observed band by more than a defined threshold.
- Revenue per unit outside the expected price range given known pricing.
- Cost as a percentage of revenue moving in the opposite direction of industry norms after an operational change.

**Directional correlation**
When a driver metric moves, does its dependent metric move in the expected direction?
- Volume increases but revenue decreases, with no pricing change known.
- Headcount increases but productivity per employee stays identical to the decimal.
- Cost of goods sold decreases while units sold increases, with no efficiency change documented.

**Entity profile consistency**
For this specific entity, are the values consistent with what is known about it?
- A new customer with a first purchase order larger than the company's largest ever prior order.
- A vendor whose single invoice exceeds its entire prior-year contract value.
- A cost center recording transactions in a category it has no known activity in.

**Temporal plausibility**
Given what happened last period, is this period's result explainable?
- A metric that was trending gradually for 12 months reverting to zero with no restatement.
- A seasonal pattern that inverts with no known operational or calendar explanation.
- A period that is identical to the prior period down to the cent for a large and varied dataset.

**Zero and null coherence**
When a value is zero or null, are the related fields in a state consistent with that?
- Revenue is zero but cost of goods sold is non-zero for the same period and entity.
- An employee record has no salary but does have benefits, bonuses, and tax withholding.
- A transaction record has a non-null amount but a null vendor, payment method, and approval.

**Impossible business combinations**
Some field combinations are technically valid but logically impossible.
- An invoice dated before the vendor contract start date.
- A shipment marked delivered before it was marked dispatched.
- A hire date after a termination date for the same employee record.
- A financial close date before the end of the reporting period.

### How to run sensibility analysis

Sensibility analysis is best run as a structured review session after mechanical cross-validation passes.

1. Assemble the domain-knowledgeable reviewer alongside the test results.
2. Present the key output metrics: totals, ratios, period-over-period changes, and top-N contributors.
3. For each metric, ask: is there a business narrative that explains this result?
4. Flag any metric where no narrative is available. This is a sensibility concern, not necessarily a data error.
5. Investigate flagged metrics: confirm the result is correct (and update the narrative) or identify the upstream cause.
6. Document findings in the sensibility check log below.

Sensibility analysis does not produce a hard gate by default. Results are surfaced as Tier 2 review flags unless the concern is severe enough to indicate a data error, in which case it escalates to Tier 1.

### Sensibility check catalog

The table below defines structured sensibility checks that apply across data projects. Adapt thresholds and entity types to the domain. The SEN prefix identifies sensibility checks for tracking in the coverage checklist.

| ID | Name | What it asks | Defends against | How to evaluate | Tier |
|---|---|---|---|---|---|
| SEN-001 | Entity scale plausibility | Is the magnitude of key metrics consistent with what is known about this entity's size and type? | Misattributed transactions, wrong entity code, orders of magnitude errors | Compare each entity's metrics to its known profile; flag outliers with no known explanation | Tier 2 |
| SEN-002 | Margin and rate consistency | Do margins, rates, and ratios fall within the historically observed or industry-expected range? | Formula errors producing implausible rates, unit errors, wrong numerator or denominator | Calculate period margin/rate; compare to rolling historical band and known business events | Tier 2 |
| SEN-003 | Directional correlation check | When a driver metric changes, does its dependent metric move in the expected direction? | Decoupled updates, partial loads updating one side of a relationship, logic error in derived fields | Identify correlated metric pairs; assert directional relationship holds within tolerance | Tier 2 |
| SEN-004 | Zero-null coherence | When a value is zero or null, are the related fields in a state that is consistent with that? | Partial load leaving orphan non-null fields, logic error nulling one field but not its dependents | For each zero or null on a critical field, check that dependent fields are also in a consistent state | Tier 1 |
| SEN-005 | Impossible business combination | Are there field combinations that are technically valid but logically impossible given business rules? | Date ordering violations, status contradictions, role or approval combinations that cannot coexist | Enumerate known impossible combinations; assert none appear in the output | Tier 1 |
| SEN-006 | Temporal plausibility | Is the current period's result explainable given the prior period's result and known business events? | Unexplained reversals, stale data presented as current, period re-processing producing a different result | Compare current period to prior; flag any change above a threshold with no documented business event | Tier 2 |
| SEN-007 | Entity profile deviation | Does this entity's behavior in the current period deviate significantly from its own established pattern? | Wrong entity key, misattributed transactions, new entity with no baseline being treated as normal | Build a per-entity baseline; flag entities whose current period deviates beyond a defined band | Tier 2 |
| SEN-008 | New entity anomaly | Does a new entity in the data carry values that are implausibly large or inconsistent for a first-time entry? | Test records left in production, wrong entity key, first batch of a new feed being unusually large | Flag first-period entries for any entity above a size threshold; require manual review before publishing | Tier 2 |
| SEN-009 | Identical period detection | Is any period's result identical to the prior period down to a suspicious level of precision, with no known explanation? | Stale snapshot served as current, watermark regression, cached result served instead of recomputed | Compare period-over-period at the row and aggregate level; flag exact matches on large datasets | Tier 2 |
| SEN-010 | Cross-entity consistency | For entities that should behave similarly, are the results consistent in direction and magnitude? | One entity's data being from a different period, entity-level processing failure affecting a subset | Group similar entities; flag outlier entities whose result diverges from the group trend | Tier 2 |

### Sensibility check log template

Use this log to record the results of each sensibility review session.

| Period | Metric | Observed value | Prior period value | Change | Business narrative available? | Status | Owner | Action |
|---|---|---|---|---|---|---|---|---|
| | | | | | Yes / No | Clear / Review / Escalate | | |
