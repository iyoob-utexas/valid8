# Framework Standard

This document describes the standard and principles behind the data testing framework.

## Purpose and scope

- Define repeatable, defensible data testing for client engagements.
- Move beyond minimal "pipeline ran" checks to confirm that the data is trustworthy.
- Apply a consistent baseline across source ingestion, pipeline processing, final output, anomaly detection, and cross-validation.
- Stay tool-agnostic while naming Microsoft Fabric/Azure options where helpful.

## What this standard requires

- Explicit pass/fail thresholds for every check.
- A named owner for every test category or test case.
- Severity tiers that determine whether a failure blocks, quarantines, or is monitored.
- Documentation of data quality expectations and business acceptance criteria.

## The reference principles

- DAMA-DMBOK data quality dimensions: completeness, uniqueness, validity, consistency, accuracy, timeliness, and integrity.
- DataOps testing principles: continuous, automated, observable, and owned by the team.
- A data-centric test pyramid: raw data checks at the base, transformation/integration checks in the middle, and end-to-end/output checks at the top.
- ISO references for clients that require formal data quality governance.
- Security and privacy principles: protect sensitive data, enforce access controls, and treat privacy as a first-class requirement.
- Operational readiness: ensure test results, alerts, and dashboards make data quality visible and actionable.

## Severity tiers

These tiers govern gate decisions: what to do when a test fails.

- Tier 1 / Critical: zero tolerance. Failures block the pipeline or quarantine data.
- Tier 2 / Important: warn and investigate. The run may continue under review, with quarantine actions for rows or alerts.
- Tier 3 / Good practice: monitor and trend. No hard gate, but surface drift and SLA risk for follow-up.

## Ownership and roles

- Each test should have one accountable owner.
- Use RACI to assign who is Responsible, Accountable, Consulted, and Informed.
- Common roles include Data Engineer, Data Analyst, Test Lead, and Stakeholder.

## Applying the standard

1. Define the engagement scope and relevant datasets.
2. Map those artifacts to the dimensions in `docs/dimensions/`.
3. Use `docs/tests/` to identify applicable checks.
4. Use `docs/grid/README.md` to build a project-specific grid and owner matrix.
5. Use `docs/framework/dppf.md` to run a coverage self-assessment and identify gaps.
6. Use `docs/framework/maturity-model.md` to position the pipeline at its current maturity level.
7. Log and monitor every run using the guidance in `docs/dashboards/README.md`.

---

## Adversarial reliability standard

Treat every data pipeline as a system operating under adversarial conditions. Just as penetration testing assumes an attacker will find the weakest point, this standard assumes data will arrive late, malformed, duplicated, poisoned, or not at all, and that code, infrastructure, and people will fail in combination.

The adversarial reliability standard extends the Tier model by adding a second lens: not just "what do we do when this fails" but "how bad is it that this failure mode exists at all."

### The eight test domains

Tests in this framework are organized into eight domains drawn from DAMA-DMBOK, ISO/IEC 25012, the five pillars of data observability, and chaos data engineering practice. Each domain maps to one or more test category files in `docs/tests/`.

| Domain | Focus | Primary location |
|---|---|---|
| Structural | Schema, types, contracts, evolution | `docs/tests/schema-and-types.md` |
| Semantic | Business rules, referential integrity, reconciliation | `docs/tests/integrity-and-references.md` |
| Statistical | Distributions, anomalies, drift, volume | `docs/tests/anomaly-and-drift.md` |
| Temporal | Freshness, latency, ordering, late arrival | `docs/tests/performance-and-freshness.md` |
| Operational | Idempotency, retries, backfill, orchestration | `docs/tests/observability-and-operations.md` |
| Adversarial | Chaos, fault injection, poisoned input, replay | `docs/tests/adversarial.md` |
| Performance and scale | Throughput, degradation, cost, concurrency | `docs/tests/performance-and-freshness.md` |
| Sensibility | Outside-in plausibility, business context checks | `docs/tests/cross-validation-suite.md` |

### Attack surface map

The following table enumerates every zone of a generic data pipeline, the failure classes that can occur in each zone, and the adversarial conditions that testing should simulate.

| Zone | Failure classes | Adversarial conditions | Observability pillars |
|---|---|---|---|
| Source systems | Missing feeds, malformed records, duplicate extracts, wrong schema | Data delayed, poisoned records, missing files, duplicate batches, schema swapped silently | Freshness, volume, distribution |
| Ingestion layer | Contract mismatch, type failure, partial load, schema evolution break | Schema mutation, bad payload injection, encoding attack, oversized record flood | Schema, lineage, volume |
| Landing layer | Incorrect partition, partial load, inconsistent formats, stale snapshots | Landing file contamination, mixed partitions, unauthorized change, stale-partition reuse | Lineage, schema, volume |
| Transformation layer | Incorrect joins, logic drift, silent error, metric corruption, duplicate propagation | Feature poisoning, mapping bugs, hidden duplicates, null flood surviving transforms | Distribution, lineage, consistency |
| Storage layer | Stale data, index mismatch, retention error, access gap, schema drift on read | Drifted partitions, tampered metadata, stale snapshots that bypass freshness checks | Lineage, freshness, schema |
| Serving layer | Stale reports, wrong output, missing slices, performance degradation | Stale caches, corrupted aggregation, missing materialization, concentration spikes reaching reports | Freshness, volume, distribution |
| Orchestration layer | Scheduling failure, dependency break, retry storm, partial success | Orchestrator kill, dependency misorder, backfill window failure, replay attack | Freshness, lineage, volume |
| Consumption layer | Bad dashboards, wrong joins, missing context, unauthorized exports | Report misuse, unverified exports, lineage tampering, stale data presented as current | Lineage, traceability, consistency |

---

## DPPF severity scoring model

This model complements the Tier model. Tiers govern gate actions. Severity scores measure the depth of risk when a test category has no coverage or a failure goes undetected. Apply this scoring model during pipeline assessments and coverage reviews.

Score each failure type on four factors, each rated 1 to 5. Sum the four scores to produce a total from 4 to 20, then map to a severity rating.

### Scoring factors

| Factor | What it measures | Score 1 | Score 3 | Score 5 |
|---|---|---|---|---|
| Blast radius | How much of the pipeline or business is affected | Single record or field | Moderate dataset subset | Entire pipeline, report suite, or business process |
| Detectability | How difficult the failure is to detect (higher = harder) | Immediate automated alert | Delayed manual detection | Silent failure with no signal |
| Data criticality | Importance of the affected data to the business | Peripheral metadata or audit log | Operational metrics or reporting | Financial, compliance, or regulatory data |
| Recoverability | Effort required to recover from the failure | Automatic self-healing | Manual intervention with time impact | Full rebuild or long restore required |

### Severity ratings

| Total score range | Rating | Recommended response |
|---|---|---|
| 16 to 20 | Critical | Treat as a blocking gap. Add or fix the test before the next production run. |
| 11 to 15 | High | Prioritize in the next sprint. Document risk until resolved. |
| 7 to 10 | Medium | Address in the next planning cycle. Monitor in the interim. |
| 4 to 6 | Low | Log as a known gap. Review at next framework refresh. |

### Relating severity to tiers

Tier and severity serve different purposes. Use both together.

- Tier answers: what action do we take when this test fails?
- Severity answers: how significant is it that we have no coverage here, or that this failure can occur silently?

A Tier 3 check can carry a High severity score if it covers silent degradation of critical data. A Tier 1 check can have a Low severity score if the failure is immediately visible and trivially recoverable. Score them independently.
