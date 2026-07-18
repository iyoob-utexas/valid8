# Example Walkthrough: Monthly Revenue Consolidation

A fully worked example of this domain's four questions, using a realistic small pipeline instead of abstract placeholders. Use this as a template for scoping your own project.

## The scenario

**Meridian Holdings** is a three-entity company (US, UK, and Singapore subsidiaries) that closes its books monthly. Each entity runs its own NetSuite instance. A Fabric pipeline pulls a monthly GL export from each entity, consolidates it into a single revenue table, converts non-USD entities at the period-close FX rate, and feeds a Power BI report the CFO reviews before the board deck goes out.

Pipeline: `meridian-revenue-consolidation`
Owner: Data Engineer (build and CI), Data Analyst (anomaly review and CFO-facing sign-off)
Cadence: monthly, first business day after entity close

---

## Question 1: What should I test?

Fifteen to twenty tests, not all 113. The team started from `grid/test-grid.md` and `framework/dppf.md`, walked the eight domains, and scoped in the checks that matter for a three-entity monthly revenue consolidation. Here is the scoped list and why each one made the cut:

| # | Test ID | Why it's in scope |
|---|---|---|
| 1 | STR-001 | Each entity's NetSuite export must have the agreed columns; a dropped column breaks the FX conversion step silently |
| 2 | STR-002 | Amount fields must stay numeric; NetSuite has silently exported currency-formatted strings before |
| 3 | STR-003 | Entity ID and account code must never be null -- both are join keys downstream |
| 4 | STR-004 | GL transaction ID must be unique per entity; duplicates would double revenue |
| 5 | STR-016 | The three-entity contract was only formally written down after the UK entity onboarded late; this closes that gap for any future entity added |
| 6 | SEM-001 | Every transaction's account code must resolve to the chart-of-accounts dimension, or revenue rolls up to the wrong line |
| 7 | SEM-004 | Source NetSuite total (by entity, by currency) must reconcile to the landed table before any transformation runs |
| 8 | SEM-007 | Detail-level transactions must sum to the published revenue rollup per entity |
| 9 | SEM-014 | The consolidated revenue equation (US + UK-converted + SG-converted = Total) must hold exactly, not just approximately |
| 10 | SEM-015 | The Power BI report total must tie to a direct SQL query against the same Lakehouse table -- this caught a stale dataset refresh once already |
| 11 | STAT-001 | Monthly transaction volume per entity should sit inside a normal band; a big drop usually means a partial extract |
| 12 | STAT-004 | Revenue MoM change per entity flagged if it moves more than the calibrated threshold (see grid below) |
| 13 | STAT-007 | Null rate on the FX rate field must stay at zero; a null rate silently zeroes out the converted amount |
| 14 | TMP-001 | The extract must land within the freshness SLA -- the close calendar has zero slack |
| 15 | TMP-004 | Late-arriving journal entries from a prior closed period must be flagged, not silently included in the current period |
| 16 | OPS-001 | Re-running the consolidation after a fix must produce byte-identical output, not accumulate duplicate rows |
| 17 | ADV-002 | Malformed or adversarial values (a stray formula string leaking from an Excel-adjacent NetSuite export) must be quarantined, not crash the pipeline |
| 18 | SEN-001 | Each entity's revenue must be plausible at its known scale -- catches an entity accidentally reporting in the wrong currency |
| 19 | SEN-005 | An impossible combination (e.g., positive revenue with a fully-reversed period flag) must be flagged before it reaches the CFO deck |

Nineteen tests, spanning six of the eight domains. Performance and scale, and most of Adversarial, were scoped out deliberately: monthly volume is small (under 50,000 rows across all three entities) and there's no adversarial threat model here beyond malformed source data -- this is an internal consolidation pipeline, not a public-facing system.

### Instantiated project test grid (`dim_test`)

Exported from `grid/test-grid.md` using the schema in `grid/dim_test_template.csv`, with calibrated thresholds from `process/testing-strategy.md`'s starter table:

| test_id | tier | category | test_name | dama_dimension | dppf_ids | threshold | owner | lifecycle_stage | in_scope |
|---|---|---|---|---|---|---|---|---|---|
| T001 | Tier 1 | Source Ingestion | Schema Presence | Validity | STR-001 | Zero missing/extra columns per entity export | Data Engineer | CI; Production monitoring | TRUE |
| T002 | Tier 1 | Source Ingestion | Data Type Conformance | Validity | STR-002 | Zero type mismatches on amount fields | Data Engineer | CI; Production monitoring | TRUE |
| T003 | Tier 1 | Source Ingestion | Null Key Check | Completeness | STR-003 | Zero nulls on entity_id, account_code | Data Engineer | CI; Production monitoring | TRUE |
| T004 | Tier 1 | Pipeline Processing | Duplicate Detection | Uniqueness | STR-004 | Zero duplicate GL transaction IDs per entity | Data Engineer | CI; Production monitoring | TRUE |
| T005 | Tier 2 | Source Ingestion | Contract Design Review | Validity, Traceability | STR-016 | Contract sign-off on file before any new entity onboards | Data Engineer | Design | TRUE |
| T006 | Tier 1 | Pipeline Processing | Referential Integrity | Integrity | SEM-001 | Zero orphan account codes; escalate to Tier 1 if any reach the report | Data Engineer | CI; Production monitoring | TRUE |
| T007 | Tier 1 | Cross-Validation | Source vs Landed Total | Accuracy | SEM-004 | Variance under 0.01% per entity per currency | Data Analyst | Production monitoring | TRUE |
| T008 | Tier 2 | Pipeline Processing | Aggregation Accuracy | Consistency | SEM-007 | Detail sum equals rollup within $1 rounding | Data Engineer | CI; Production monitoring | TRUE |
| T009 | Tier 1 | Output Validation | Consolidated Revenue Equation | Accuracy | SEM-014 | US + UK-converted + SG-converted = Total, exact | Data Engineer | Production monitoring | TRUE |
| T010 | Tier 1 | Cross-Validation | Report vs Source Query | Accuracy | SEM-015 | Power BI total equals Lakehouse SQL total, exact | Data Analyst | Production monitoring | TRUE |
| T011 | Tier 3 | Anomaly Detection | Volume Shape | Completeness | STAT-001 | Transaction count per entity within ±20% of 3-month rolling average | Data Analyst | Production monitoring | TRUE |
| T012 | Tier 1 | Anomaly Detection | Revenue MoM Change | Consistency | STAT-004 | Flag if any entity's revenue moves >20% MoM | Data Analyst | Production monitoring | TRUE |
| T013 | Tier 1 | Source Ingestion | FX Rate Null Check | Completeness | STAT-007 | Zero nulls on fx_rate for non-USD entities | Data Engineer | Production monitoring | TRUE |
| T014 | Tier 1 | Source Ingestion | Freshness SLA | Timeliness | TMP-001 | Landed by 09:00 local on day 1 after close | Data Engineer | Production monitoring | TRUE |
| T015 | Tier 3 | Pipeline Processing | Late-Arriving Data | Timeliness | TMP-004 | Any record dated in a closed period is flagged, not silently included | Data Engineer | Production monitoring | TRUE |
| T016 | Tier 2 | Pipeline Processing | Idempotency | Consistency | OPS-001 | Re-run produces identical output, zero duplicate rows | Data Engineer | CI; Production monitoring | TRUE |
| T017 | Tier 2 | Adversarial | Bad Data Quarantine | Validity | ADV-002 | Malformed values quarantined, zero pass-through | Data Engineer | Production monitoring | TRUE |
| T018 | Tier 3 | Sensibility | Entity Scale Plausibility | Accuracy | SEN-001 | Each entity's revenue within known historical scale band | Data Analyst | Production monitoring | TRUE |
| T019 | Tier 2 | Sensibility | Impossible Business Combination | Consistency | SEN-005 | Zero rows combining positive revenue with a reversed-period flag | Data Analyst | Production monitoring | TRUE |

---

## Question 2: How do I run the tests I've selected?

The team implemented each check as a Fabric Notebook assertion or a dbt test, following `process/test-cycle.md`'s eight steps, and used `process/tool-guidance.md`'s pandas patterns as a starting point (e.g., `SEM-004` as `abs(source_total - landed_total) / source_total < tolerance`). `process/tool-guidance.md` maps each check category to the tool used.

---

## Question 3: Where do I see test results?

Results are logged to a `fact_results` table per `grid/summary-test-grid.md`'s schema, one row per test per run, using the `result_log_template.csv` shape. Below is the filled-in summary for two consecutive runs of the August 2026 close.

### Run 1 -- `20260805-090000-meridian-revenue` (first attempt)

| Tier | Category | Test | Status | Detail |
|---|---|---|---|---|
| Tier 1 | Pipeline Processing | Referential Integrity (T006 / SEM-001) | **FAIL** | 3 Singapore-entity vendor-linked account codes have no match in the chart-of-accounts dimension |
| Tier 1 | Source Ingestion | Schema Presence (T001) | PASS | |
| Tier 1 | Source Ingestion | Data Type Conformance (T002) | PASS | |
| Tier 1 | Source Ingestion | Null Key Check (T003) | PASS | |
| Tier 1 | Pipeline Processing | Duplicate Detection (T004) | PASS | |
| Tier 1 | Cross-Validation | Source vs Landed Total (T007) | PASS | |
| Tier 1 | Output Validation | Consolidated Revenue Equation (T009) | PASS | |
| Tier 1 | Cross-Validation | Report vs Source Query (T010) | PASS | |
| Tier 1 | Anomaly Detection | Revenue MoM Change (T012) | **WARN** | UK entity revenue +22% MoM, threshold is ±20% -- large new contract, flagged for CFO context, not a data defect |
| Tier 1 | Source Ingestion | FX Rate Null Check (T013) | PASS | |
| Tier 1 | Source Ingestion | Freshness SLA (T014) | PASS | |
| Tier 2 | Source Ingestion | Contract Design Review (T005) | PASS | |
| Tier 2 | Pipeline Processing | Aggregation Accuracy (T008) | PASS | |
| Tier 2 | Pipeline Processing | Idempotency (T016) | PASS | |
| Tier 2 | Adversarial | Bad Data Quarantine (T017) | PASS | |
| Tier 2 | Sensibility | Impossible Business Combination (T019) | PASS | |
| Tier 3 | Anomaly Detection | Volume Shape (T011) | PASS | |
| Tier 3 | Pipeline Processing | Late-Arriving Data (T015) | PASS | |
| Tier 3 | Sensibility | Entity Scale Plausibility (T018) | PASS | |

**Remediation:** the three orphan account codes trace to a new Singapore vendor category added mid-month that the chart-of-accounts sync job hadn't picked up yet. The Data Engineer added the three codes to the dimension table and re-ran from Step 4 (Transform) per the abort policy in `process/test-cycle.md`.

#### Summary scorecard -- Run 1

| Metric | Value |
|---|---|
| Total tests | 19 |
| Passed | 17 |
| Failed | 1 |
| Warnings | 1 |
| Pass rate | 17 / 19 = **89.5%** |
| Tier 1 failures | 1 |
| Overall score | (9×5 + 5×2 + 3×1 + 1×1) / (10×5 + 6×2 + 3×1) = 59 / 65 = **90.8%** |

**Gate status: `BLOCKED`** -- one Tier 1 failure (SEM-001 referential integrity orphan). Per the rubric, `BLOCKED` overrides pass rate regardless of how high it is.

### Run 2 -- `20260805-113000-meridian-revenue` (after remediation)

All 19 tests re-run from Step 4 forward. SEM-001 now passes. The UK revenue variance (T012) is investigated, confirmed as a legitimate large contract win, and left as a documented WARN rather than suppressed -- the threshold stays at ±20% rather than being loosened to make one month's variance disappear.

| Metric | Value |
|---|---|
| Total tests | 19 |
| Passed | 18 |
| Failed | 0 |
| Warnings | 1 |
| Pass rate | 18 / 19 = **94.7%** |
| Tier 1 failures | 0 |
| Overall score | (10×5 + 5×2 + 3×1 + 1×1) / 65 = 64 / 65 = **98.5%** |

**Gate status: `REVIEW`** -- zero Tier 1 failures, but pass rate (94.7%) sits just under the 95% `READY` threshold because of the still-open UK revenue WARN. Per the rubric, `REVIEW` means acceptable for release under supervision. The CFO deck goes out with a footnote on the UK variance; the Data Analyst monitors next month's close to confirm the new baseline.

---

## Question 4: How do I know if the results are acceptable?

Run 1 was `BLOCKED` -- the pipeline did not promote, and the CFO deck was not built from that run. Run 2 is `REVIEW` -- it promotes, but with a flagged, documented variance carried forward rather than silently accepted. Neither run reached `READY` this cycle; that's normal for a month with a genuine business anomaly, and the rubric is working as intended by not rounding a real variance up to a clean pass.

## What this example shows

- Scoping down from 113 to 19 tests, with an explicit reason for each inclusion.
- A project-specific `dim_test` grid, not the master grid, with calibrated thresholds instead of placeholder "X%" values.
- A realistic two-run arc: a genuine Tier 1 failure, a traced and fixed remediation, and a second run that lands on `REVIEW` rather than a too-convenient `READY`.
- The scoring rubric applied with real arithmetic, not asserted.
