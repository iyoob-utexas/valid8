# Test Cycle Runbook

This page documents the eight-step test cycle for data projects.

## Start here

Before the cycle begins, know these inputs:

- the source system and source contract
- the expected schema and critical business keys
- the batch or period in scope
- the success criteria for the engagement

## Eight steps

1. Schema & Contract
   - Confirm incoming columns, data types, and nullability match the agreed contract.
   - Run schema validation.
   - Pass when there are zero mismatches; any difference blocks ingestion.

2. Pull & Ingest
   - Validate that the data pulled from the source matches the landing layer.
   - Confirm keys are never null and the load arrived on time.
   - Pass when row counts align, key columns are clean, and freshness is within SLA.

3. Vs Last Pull
   - Compare this load to recent loads for volume, null rates, and pattern changes.
   - Run anomaly detection against a rolling baseline.
   - Pass when the load sits inside normal variance bands.

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

## Remediations

When a test fails, do not just record the failure -- suggest a remediation before closing the run. A remediation note should answer three things: what broke, why it likely broke, and what action resolves it.

Common remediation patterns by failure type:

| Failure type | Likely cause | Suggested action |
|---|---|---|
| Schema mismatch | Upstream schema changed without notice | Re-align contract with source team; update mapping |
| Null in required field | Missing data at source or broken join | Trace nulls to origin; fix extraction or join logic |
| Row count anomaly | Late-arriving data, duplicate load, or truncation | Check load timestamps; inspect for double-loads or missed partitions |
| Referential integrity failure | Orphaned foreign keys after upstream delete | Identify orphan rows; decide whether to drop, flag, or hold |
| Aggregate tie-out variance | Rounding difference or filter mismatch | Compare grain-level detail; check filter scope and rounding logic |
| Cross-validation gap | System-of-record updated after extract | Re-extract or reconcile with the current snapshot |
| Drift alert (anomaly) | Seasonal pattern, source change, or silent pipeline failure | Compare to prior periods; determine if change is expected or a defect |

Record the remediation taken alongside the failure result so the run history shows both the problem and its resolution.

## Recommended practice

- Record every result for every step.
- Use a dashboard or run-history table for trend analysis.
- Keep the runbook aligned with the companion grid and the framework standard.
