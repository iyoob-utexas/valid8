# Test Cycle Runbook

This page documents the eight-step test cycle for data projects.

## Start here

Before the cycle begins, know these inputs:

- the source system and source contract
- the expected schema and critical business keys
- the batch or period in scope
- the success criteria for the engagement
- whether source data is **cumulative** (running totals or balances) or **period-based** (incremental transactions for the period only) -- this affects row count checks, period-over-period comparisons, and cross-validation logic
- for datasets with multiple date fields (e.g., event date, load date, delivery date, effective date), which date governs freshness checks and period assignment for each field

## Eight steps

1. Schema & Contract
   - Confirm incoming columns, data types, and nullability match the agreed contract.
   - Run schema validation.
   - Pass when there are zero mismatches; any difference blocks ingestion.

2. Pull & Ingest
   - Validate that the data pulled from the source matches the landing layer.
   - Confirm keys are never null and the load arrived on time.
   - For datasets with multiple date fields, validate each date field independently: check freshness against the load date, check that no dates fall outside the expected range (including future-dated records), and verify that event dates align with the declared period.
   - Pass when row counts align, key columns are clean, and freshness is within SLA.

3. Vs Last Pull
   - Compare this load to recent loads for volume, null rates, and pattern changes.
   - Run anomaly detection against a rolling baseline.
   - Pass when the load sits inside normal variance bands.
   - **Run 1 protocol:** If no prior load exists, record all anomaly checks in this step as `BASELINE` rather than PASS or FAIL. Do not evaluate gate status for this step on Run 1. Capture current values as the baseline for Run 2. A `BASELINE` result is not a pass -- the check did not run.

4. Transform
   - Verify transformation logic rules, joins, filters, and business mappings.
   - Check duplicates, referential integrity, and domain validity.
   - Pass when every rule produces expected output and there are no orphan or duplicate rows.

5. Tie Aggregates
   - Confirm detail-level data aggregates to the rolled-up totals.
   - Reconcile related outputs to each other where they should agree.
   - Pass when all cross-step tie-outs reconcile within tolerance.

6. Output Checks
   - Validate final output invariants, domain rules, and consumer contract expectations.
   - Check cardinality, null rates, and derived values.
   - Pass when the final dataset meets the agreed quality and shape requirements.

7. Cross-Validate
   - Reconcile final data against an independent external source or system of record.
   - Compare totals, counts, or business metrics to the external reference.
   - Pass when variance is within the agreed tolerance.

8. Regress, Log, and Surface
   - Re-run stable metrics, log every result, and review the dashboard before sign off.
   - Pass when there are zero regressions and the latest run shows green status for critical checks.

## Failure behavior

- Red / Tier 1: stop. Quarantine the batch and fix the issue before moving forward.
- Amber / Tier 2: quarantine rows or alert; investigate while the run continues under review.
- Green / Tier 3: log and monitor. Continue the run, but escalate if drift persists.

## Abort policy

If Step 1 or Step 2 produces a Tier 1 failure, running Steps 3 through 8 on the same data will generate misleading results -- downstream checks will fail for reasons caused by the upstream defect, not independently. Apply the following policy:

- If Step 1 (Schema & Contract) fails: record Steps 2 through 8 as `SKIPPED` and reference the schema failure. Fix the contract mismatch before re-running.
- If Step 2 (Pull & Ingest) produces a Tier 1 failure on null keys or row count: record Steps 3 through 8 as `SKIPPED` with a reference to the Step 2 failure. Quarantine the batch and re-run from Step 1 after the source issue is resolved.
- A `SKIPPED` result does not count as a pass or fail in the pass rate calculation and does not affect `overall_score`. Document the skip reason in the run log.

## Remediations

When a test fails, do not just record the failure -- suggest a remediation before closing the run. A remediation note should answer three things: what broke, why it likely broke, and what action resolves it.

Common remediation patterns by failure type:

| Failure type | Likely cause | Suggested action |
|---|---|---|
| Schema mismatch | Upstream schema changed without notice | Re-align contract with source team; update mapping |
| Null in required field | Missing data at source or broken join | Trace nulls to origin; fix extraction or join logic |
| Duplicate key | Source resent a batch, merge logic failed, or keying error | Identify duplicates by key; determine which copy is authoritative; dedup before transform |
| Row count anomaly | Late-arriving data, duplicate load, or truncation | Check load timestamps; inspect for double-loads or missed partitions |
| Referential integrity orphan | Key in fact data has no match in the dimension; escalate if null propagates to output | Identify orphan keys; quarantine affected rows before transform; notify source owner |
| Referential integrity orphan propagated to output | Orphan was not quarantined; null dimension value reached a delivered report or dashboard | Roll back or suppress the affected output; quarantine the rows; re-run from transform after resolving the source key |
| Aggregate tie-out variance | Rounding difference, filter mismatch, or excluded rows | Compare grain-level detail; check filter scope, rounding logic, and row exclusion rules |
| Paired-value imbalance | Missing entry on one side of a paired structure, or a transform that only updated one side | Identify which side has the gap; trace to the source entry or the transform that produced the imbalance |
| KPI value outside valid range | Calculation error, aggregation defect, or incorrect denominator (e.g., division by zero, count exceeding total) | Assert denominator > 0 before division; inspect the aggregation grain; check for duplicate rows inflating numerators |
| Cross-validation gap | System-of-record updated after extract | Re-extract or reconcile with the current snapshot |
| Drift alert (anomaly) | Seasonal pattern, source change, or silent pipeline failure | Compare to prior periods; determine if change is expected or a defect |
| Future-dated record | Incorrect source timestamp, timezone error, or pre-loaded forward data | Identify affected records; confirm whether forward dates are intentional (pre-load) or erroneous; quarantine if unintended |
| Period cutoff violation | Extract includes records from an adjacent closed or future period | Filter to the agreed period boundary; confirm the extract query uses the correct date range |

Record the remediation taken alongside the failure result so the run history shows both the problem and its resolution.

## Recommended practice

- Record every result for every step.
- Use a dashboard or run-history table for trend analysis.
- Keep the runbook aligned with the companion grid and the framework standard.
