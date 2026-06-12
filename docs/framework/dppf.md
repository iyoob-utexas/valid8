# DPPF Coverage Evaluation Checklist

Use this checklist to assess how well an existing pipeline's test plan covers the Data Pipeline Penetration Testing Framework. For each test ID, mark the coverage status, note the current implementation or monitoring approach, and record any gaps.

This checklist is the primary output of Phase 1 through Phase 3 of the DPPF engagement methodology described in `docs/process/testing-strategy.md`. Complete it before scoring findings and before setting a target maturity level.

---

## How to use this checklist

1. Work through each domain section.
2. For each test ID, mark one status:
   - **Covered**: a specific, automated check exists and runs on the defined lifecycle stage.
   - **Partial**: a check exists but is manual, incomplete, or not running at the right stage.
   - **Gap**: no check exists for this test category.
3. Fill in the Notes column with what is currently in place or why coverage is absent.
4. After completing all domains, use the scoring guide at the bottom to determine the current maturity level.
5. Score any Gap or Partial items using the DPPF severity model in `docs/framework/README.md`.

---

## Structural domain

Tests in this domain: `docs/tests/schema-and-types.md`

| ID | Name | Status | Notes |
|---|---|---|---|
| STR-001 | Schema presence | | |
| STR-002 | Data type conformance | | |
| STR-003 | Nullability contract | | |
| STR-004 | Primary key uniqueness | | |
| STR-005 | Compound key uniqueness | | |
| STR-006 | Field cardinality bounds | | |
| STR-007 | Enumerated value conformance | | |
| STR-008 | String length bounds | | |
| STR-009 | Numeric range bounds | | |
| STR-010 | Character encoding conformance | | |
| STR-011 | File and format contract | | |
| STR-012 | Default value application | | |
| STR-013 | Schema evolution backward compatibility | | |
| STR-014 | Partition and ingestion contract | | |
| STR-015 | Data contract version compliance | | |

Structural coverage: _____ Covered / _____ Partial / _____ Gap out of 15

---

## Semantic domain

Tests in this domain: `docs/tests/integrity-and-references.md`

| ID | Name | Status | Notes |
|---|---|---|---|
| SEM-001 | Referential integrity | | |
| SEM-002 | Business rule validation | | |
| SEM-003 | Cross-field logic consistency | | |
| SEM-004 | Source-to-target reconciliation | | |
| SEM-005 | Master data consistency | | |
| SEM-006 | Derived metric validation | | |
| SEM-007 | Aggregation rollup accuracy | | |
| SEM-008 | Hierarchical integrity | | |
| SEM-009 | State machine transition validity | | |
| SEM-010 | Temporal business rule compliance | | |
| SEM-011 | Conditional field rule validation | | |
| SEM-012 | Lookup and code table completeness | | |
| SEM-013 | Entity deduplication logic | | |
| SEM-014 | Financial equation validation | | |
| SEM-015 | Cross-dataset reconciliation | | |

Semantic coverage: _____ Covered / _____ Partial / _____ Gap out of 15

---

## Statistical domain

Tests in this domain: `docs/tests/anomaly-and-drift.md`

| ID | Name | Status | Notes |
|---|---|---|---|
| STAT-001 | Volume shape | | |
| STAT-002 | Distribution stability | | |
| STAT-003 | Outlier detection | | |
| STAT-004 | Statistical drift detection | | |
| STAT-005 | Cardinality drift | | |
| STAT-006 | Missing pattern detection | | |
| STAT-007 | Null rate monitoring | | |
| STAT-008 | Zero value rate monitoring | | |
| STAT-009 | Mean and median shift detection | | |
| STAT-010 | Variance stability | | |
| STAT-011 | Correlation stability | | |
| STAT-012 | Skewness monitoring | | |
| STAT-013 | Seasonal pattern compliance | | |
| STAT-014 | Percentile stability | | |
| STAT-015 | Concentration ratio monitoring | | |

Statistical coverage: _____ Covered / _____ Partial / _____ Gap out of 15

---

## Temporal domain

Tests in this domain: `docs/tests/performance-and-freshness.md`

| ID | Name | Status | Notes |
|---|---|---|---|
| TMP-001 | Freshness SLA compliance | | |
| TMP-002 | End-to-end latency measurement | | |
| TMP-003 | Sequence ordering validation | | |
| TMP-004 | Late arrival handling | | |
| TMP-005 | Time window completeness | | |
| TMP-006 | Time continuity | | |
| TMP-007 | Timezone normalization | | |
| TMP-008 | Event time vs processing time gap | | |
| TMP-009 | Watermark advancement correctness | | |
| TMP-010 | Future timestamp detection | | |
| TMP-011 | DST transition handling | | |
| TMP-012 | Clock skew detection | | |
| TMP-013 | Backfill window coverage | | |
| TMP-014 | Stale period reappearance detection | | |

Temporal coverage: _____ Covered / _____ Partial / _____ Gap out of 14

---

## Operational domain

Tests in this domain: `docs/tests/observability-and-operations.md`

| ID | Name | Status | Notes |
|---|---|---|---|
| OPS-001 | Idempotency | | |
| OPS-002 | Retry behavior | | |
| OPS-003 | Partial failure handling | | |
| OPS-004 | Backfill correctness | | |
| OPS-005 | Dependency enforcement | | |
| OPS-006 | Execution observability | | |
| OPS-007 | Graceful degradation | | |
| OPS-008 | Checkpoint and recovery | | |
| OPS-009 | Dead letter queue handling | | |
| OPS-010 | SLA breach alerting | | |
| OPS-011 | Data lineage completeness | | |
| OPS-012 | Audit trail completeness | | |
| OPS-013 | Configuration drift detection | | |
| OPS-014 | Parallel execution safety | | |
| OPS-015 | Graceful shutdown behavior | | |

Operational coverage: _____ Covered / _____ Partial / _____ Gap out of 15

---

## Adversarial domain

Tests in this domain: `docs/tests/adversarial.md`

| ID | Name | Status | Notes |
|---|---|---|---|
| ADV-001 | Fault injection | | |
| ADV-002 | Bad data injection | | |
| ADV-003 | Schema mutation attack | | |
| ADV-004 | Duplicate flood | | |
| ADV-005 | Dependency kill simulation | | |
| ADV-006 | Lineage tampering check | | |
| ADV-007 | Volume spike injection | | |
| ADV-008 | Null flood injection | | |
| ADV-009 | Special character injection | | |
| ADV-010 | Encoding attack | | |
| ADV-011 | Future date injection | | |
| ADV-012 | Negative value injection | | |
| ADV-013 | Oversized record injection | | |
| ADV-014 | Replay attack simulation | | |
| ADV-015 | Homoglyph and lookalike injection | | |

Adversarial coverage: _____ Covered / _____ Partial / _____ Gap out of 15

---

## Performance and scale domain

Tests in this domain: `docs/tests/performance-and-freshness.md`

| ID | Name | Status | Notes |
|---|---|---|---|
| PERF-001 | Throughput validation | | |
| PERF-002 | Scale degradation behavior | | |
| PERF-003 | Cost anomaly detection | | |
| PERF-004 | Latency under load | | |
| PERF-005 | Resource contention | | |
| PERF-006 | Throughput stability | | |
| PERF-007 | Memory pressure behavior | | |
| PERF-008 | Concurrent execution safety | | |
| PERF-009 | Query plan stability | | |
| PERF-010 | Partition pruning effectiveness | | |
| PERF-011 | Checkpoint and restore performance | | |
| PERF-012 | Cold start performance | | |

Performance and scale coverage: _____ Covered / _____ Partial / _____ Gap out of 12

---

## Sensibility domain

Tests in this domain: `docs/tests/cross-validation-suite.md`

Sensibility checks are the outside-in layer. They ask whether the data makes business sense to a knowledgeable reviewer, not just whether it satisfies defined rules.

| ID | Name | Status | Notes |
|---|---|---|---|
| SEN-001 | Entity scale plausibility | | |
| SEN-002 | Margin and rate consistency | | |
| SEN-003 | Directional correlation check | | |
| SEN-004 | Zero-null coherence | | |
| SEN-005 | Impossible business combination | | |
| SEN-006 | Temporal plausibility | | |
| SEN-007 | Entity profile deviation | | |
| SEN-008 | New entity anomaly | | |
| SEN-009 | Identical period detection | | |
| SEN-010 | Cross-entity consistency | | |

Sensibility coverage: _____ Covered / _____ Partial / _____ Gap out of 10

---

## Coverage summary

| Domain | Total tests | Covered | Partial | Gap | Coverage % |
|---|---|---|---|---|---|
| Structural | 15 | | | | |
| Semantic | 15 | | | | |
| Statistical | 15 | | | | |
| Temporal | 14 | | | | |
| Operational | 15 | | | | |
| Adversarial | 15 | | | | |
| Performance and scale | 12 | | | | |
| Sensibility | 10 | | | | |
| **Total** | **111** | | | | |

Coverage % = Covered / Total tests. Partial counts as 0.5 for scoring purposes.

---

## Maturity level guide

Use the domain coverage matrix from `docs/framework/maturity-model.md` alongside total coverage to estimate the pipeline maturity level.

| Observed coverage pattern | Likely maturity level |
|---|---|
| Structural and semantic mostly covered; statistical, operational, adversarial mostly gaps | Level 2: Defined |
| All domains partially covered; adversarial partially covered | Level 2 to 3 transition |
| All domains covered; adversarial partial | Level 3: Automated |
| All domains fully covered including adversarial | Level 4: Adversarial |

Any domain with more than 50% gaps that is not the Adversarial domain is a signal of Level 1 or Level 2 maturity regardless of total coverage percentage.

---

## Next steps after completing this checklist

1. Score every Gap and Partial item using the DPPF severity model in `docs/framework/README.md`.
2. Use the scores to prioritize the remediation backlog.
3. Add new test IDs to the project test grid in `docs/grid/test-grid.md`.
4. Re-run this checklist after remediation to confirm advancement.
