# valid8 Master Gap Report -- Three-Experiment Synthesis

Three pipelines tested using the 8-step cycle from docs/process/test-cycle.md:
- **Experiment 1 (Sales):** Monthly sales CSV → product category revenue report
- **Experiment 2 (Finance):** GL journal entries → Income Statement + Balance Sheet
- **Experiment 3 (Supply Chain):** ERP purchase orders → Vendor performance + spend reports

Results summary:

| Pipeline | Tests run | Pass rate | Tier 1 failures | Gate |
|---|---|---|---|---|
| Sales | 16 | 62% | 3 | BLOCKED |
| Finance | 16 | 56% | 6 | BLOCKED |
| Supply Chain | 16 | 56% | 3 | BLOCKED |

Gaps below are ordered by priority. Source column shows which experiment(s) surfaced the gap.

---

## PRIORITY 1 -- Framework produces incomplete or unusable output without these

### G1: Threshold calibration -- all thresholds are placeholders

**Source:** All three experiments
**Where:** test-grid.md (every Anomaly Detection row); test-cycle.md Step 3
**What the framework says:** "Over X% change vs the rolling baseline triggers review"
**What's missing:** How to choose X, what defaults to start with, how to calibrate on a new dataset with no history

All three experiments required arbitrary threshold choices: 25% MoM for sales revenue, 25% MoM for GL revenue, 30% MoM for PO spend. The framework gives no starting points. Two of three experiments triggered the MoM check -- the threshold setting directly determines how many false positives you generate on first deployment.

**Suggested fix:** Add a threshold starter guide to docs/process/testing-strategy.md. Minimal table:

| Check | Conservative start | Tighten after |
|---|---|---|
| MoM revenue/spend | ±25% | 6 periods of clean data |
| Period volume | ±20% | 3 periods |
| Null rate | 0% (key fields), <5% (optional fields) | N/A |
| Freshness SLA | 24h (daily), 7 days (weekly) | Review with stakeholder |

---

### G2: No protocol for Run 1 when no prior period exists

**Source:** All three experiments (anomaly detection step would fail on first run)
**Where:** test-cycle.md Step 3 (Vs Last Pull)
**What the framework says:** "Compare this load to recent loads"
**What's missing:** What to do when there is no prior load; which checks to skip; how to record the run

Every new project hits this on the first cycle. Skipping Step 3 silently is dangerous; marking it as "N/A" needs to be an explicit status.

**Suggested fix:** Add a Run 1 callout to test-cycle.md Step 3: "If no prior period exists, record anomaly checks as BASELINE and skip gate evaluation for this step. Capture current values as the baseline for Run 2. Do not record a PASS -- the check did not run."

---

### G3: dim_test schema is never defined

**Source:** All three experiments
**Where:** docs/grid/summary-test-grid.md, "How to build it" step 1
**What the framework says:** "Export the test metadata from docs/grid/test-grid.md into a dim_test dimension"
**What's missing:** What columns dim_test should have; what "export" means for a markdown table

Each experiment's test runner produced a different schema because there's no specification. Teams implementing this separately will produce incompatible formats that can't be aggregated across projects.

**Suggested fix:** Define dim_test schema explicitly in summary-test-grid.md:
`test_id, tier, category, test_name, dama_dimension, dppf_ids, threshold, owner, lifecycle_stage`
Provide a CSV template file at `docs/grid/dim_test_template.csv`.

---

### G4: No blank result templates exist

**Source:** All three experiments
**Where:** docs/grid/summary-test-grid.md (defines schema but provides no file to start from)
**What's missing:** A fillable run_log template and summary scorecard template

Every practitioner starts from scratch. The result is inconsistent formats across teams and projects.

**Suggested fix:** Add two template files to docs/grid/:
- `result_log_template.csv` -- one row per test, columns from dim_test plus run_id, run_date, status, detail, remediation_taken
- `summary_template.md` -- the scorecard markdown table pre-populated with headers

---

## PRIORITY 2 -- Framework guidance is ambiguous; different readers will do different things

### G5: WARN vs FAIL is undefined for Tier 2 checks

**Source:** All three experiments (referential integrity, on-time rate, null category)
**Where:** docs/framework/README.md severity tiers; test-cycle.md failure behavior
**What's missing:** When a Tier 2 result is FAIL vs WARN

The supply chain run showed 5 vendors below the on-time rate floor and an orphan vendor_id. Both are Tier 2. But one should halt quarantine (orphan propagates to output) while the other is a monitoring flag. The framework offers no criteria to distinguish.

**Suggested fix:** Add one sentence to tier definitions: "Tier 2 results are FAIL when the pipeline action is quarantine or block, and WARN when the action is alert, flag, or review. If the failure propagates to final output, escalate to Tier 1."

---

### G6: Referential integrity tier is too lenient when orphans reach final output

**Source:** Experiments 1 and 3 (null category in sales report; null vendor_name in vendor performance report)
**Where:** test-grid.md, Pipeline Processing > Referential Integrity (SEM-001)
**What it says:** Tier 2, action = Quarantine
**What happened:** Both pipelines produced final reports with null dimension values (category=NaN, vendor_name=NaN) that would appear in any dashboard built downstream

The framework treats all referential integrity failures as Tier 2. But when an orphan key propagates through a left join to become a null in a delivered output, it becomes a Tier 1 issue.

**Suggested fix:** Add a note to the referential integrity grid row: "Escalate to Tier 1 if orphan records are not quarantined before the transform stage and their null dimension values appear in final output."

---

### G7: run_id format is never specified

**Source:** All three experiments
**Where:** docs/grid/summary-test-grid.md, Key Fields
**What's missing:** Format, generation method, whether it must be unique globally or per-project

All three experiments generated different run_id formats (timestamp-based). Cross-project aggregation requires a consistent format.

**Suggested fix:** Specify format in summary-test-grid.md: "Recommended format: `YYYYMMDD-HHMMSS-<pipeline-name>`. Must be unique within a project. For multi-project dashboards, prefix with a project code."

---

### G8: maximum_possible_score denominator is ambiguous

**Source:** All three experiments
**Where:** README.md scoring rubric
**What it says:** `overall_score = numerator / maximum_possible_score`
**What's missing:** Whether the denominator is (a) all tests in the master grid, (b) all tests scoped for the project, or (c) all tests executed in this run

Interpretation (a) would penalize small-scope projects. Interpretation (c) lets a team game the score by running fewer tests.

**Suggested fix:** Add one sentence: "maximum_possible_score is the sum of tier weights for all tests in the project's scoped test list -- not just the tests that ran in this cycle, and not the full master grid."

---

### G9: No test dependency or abort rules

**Source:** All three experiments
**Where:** test-cycle.md (8 steps described with no conditional logic)
**What's missing:** What to do when an upstream step fails -- run downstream steps or abort

The finance pipeline had 6 Tier 1 failures. Running all 8 steps produced noise (Step 6 and 7 failures are largely caused by the Step 2 null key / Step 4 duplicate issues). The framework doesn't say whether to continue or stop.

**Suggested fix:** Add an "Abort policy" section to test-cycle.md: "If Step 1 or Step 2 produces a Tier 1 failure, record Steps 3-8 checks as SKIPPED and reference the upstream failure. Continuing to run downstream checks on a corrupt dataset produces misleading results."

---

### G10: Tool guidance covers only Fabric/Azure; no Python/pandas path

**Source:** All three experiments (runner built in pandas with no framework guidance)
**Where:** test-grid.md "Fabric / Azure Tooling" column; docs/process/tool-guidance.md
**What's missing:** Any implementation guidance for Python, pandas, dbt, Great Expectations, or SQL-only environments

The "Tool-Agnostic Approach" column helps but stays abstract. No practitioner running a pandas pipeline has a reference implementation for even the most common checks.

**Suggested fix:** Add a "Python / pandas quick-start" section to tool-guidance.md with one pattern per check category (null check, duplicate check, row count reconciliation, cross-validation). 10-15 lines total -- enough to unblock.

---

## PRIORITY 3 -- Domain-specific gaps (finance)

### G11: Double-entry invariant is not in the test grid

**Source:** Finance experiment
**Where:** test-grid.md (no row covers this); test-cycle.md Step 7 (Cross-Validate)
**What happened:** The finance runner added a custom check: "Total Debits = Total Credits." This is the most fundamental invariant in any GL system, and the balance sheet imbalance ($210k gap) only made sense once this check fired first. The framework has no equivalent check.

**Suggested fix:** Add a row to test-grid.md under Cross-Validation: "Double-Entry Balance -- Total debits equal total credits across all entries in the period. Zero tolerance. Tier 1." DPPF ID: SEM-015 applies but a dedicated test is warranted.

---

### G12: GL normal balance direction not addressed

**Source:** Finance experiment
**Where:** test-grid.md; docs/tests/ (no file covers GL-specific concepts)
**What happened:** Building the balance sheet required knowing that revenue accounts have a credit normal balance (net_amount is negative) while assets have a debit normal balance (net_amount is positive). The framework treats all numeric fields generically. A practitioner new to GL data would get the balance sheet equation wrong.

**Suggested fix:** Add a note to the Output Invariant Assertion row (or a finance-domain annex): "For GL-based pipelines, assets carry debit normal balances (positive net_amount) and liabilities/equity/revenue carry credit normal balances (negative net_amount). The balance check is: Assets + Liabilities + Equity = 0, not Assets = Liabilities + Equity as a simple sum."

---

### G13: Cumulative vs period GL not addressed

**Source:** Finance experiment
**Where:** Not mentioned anywhere in the framework
**What happened:** Some GL systems export period transactions (this experiment). Others export cumulative balances. The row count check, MoM comparison, and cross-validation all behave differently depending on which convention the source uses. The framework assumes period transactions without stating so.

**Suggested fix:** Add a "Source contract" question to test-cycle.md Step 1 inputs: "Does the source provide period transactions or cumulative balances? Document this in the engagement scope before running any numeric checks."

---

### G14: "Independent Dual-Path" check has no implementation guide

**Source:** Finance experiment
**Where:** test-grid.md, Cross-Validation > Independent Dual-Path (Bottom-Up vs Top-Down P&L)
**What it says:** "Two independent aggregation queries; assert match"
**What's missing:** How to construct the two paths, what they should compute, and what "independent" means in practice

This check is listed as Tier 1 Critical but there's no explanation of what makes a path "independent" or how to set it up. The test never ran in the finance experiment because the instruction wasn't actionable.

**Suggested fix:** Add an implementation note to the test grid row: "Path 1: sum P&L from detail-level GL entries by account type. Path 2: sum from pre-aggregated period totals table. Assert both produce identical net income. Independence means different source queries, not different filters on the same query."

---

### G15: Period close and cutoff testing not addressed

**Source:** Finance experiment
**Where:** Not mentioned in test-grid.md or test-cycle.md
**What's missing:** Any guidance on testing cutoff date compliance, adjusting entries, or post-close corrections

Financial pipelines have hard period-close deadlines. A GL entry dated after the cutoff corrupts the period's reported figures. The framework covers data freshness (data arrived on time) but not the inverse (entries must fall within the period being reported).

**Suggested fix:** Add a row to test-grid.md under Source Ingestion or Output Validation: "Period Cutoff Check -- No GL entries dated outside the reporting period appear in the period dataset. Tier 1 for financial reporting pipelines." This is distinct from data freshness.

---

## PRIORITY 3 -- Domain-specific gaps (supply chain)

### G16: KPI range validation not in the framework

**Source:** Supply chain experiment
**What happened:** The on_time_rate field in the vendor performance output showed a value of 1.5 for one vendor -- a rate that is mathematically impossible (must be between 0 and 1). The framework has no check for output column range validation on derived KPIs.

The STR-009 test (numeric range bounds) covers this conceptually, but it's framed around source data (raw values within expected bounds). It's not surfaced as a check on derived output metrics.

**Suggested fix:** Add a note to the STR-009 row and to docs/tests/schema-and-types.md: "Apply range checks to derived output KPIs (on_time_rate in [0,1], fill_rate in [0,1], margin_pct in [-1,1]) as part of Step 6 Output Checks. A derived KPI outside its natural range indicates a calculation error upstream."

---

### G17: Operational KPI thresholds are entirely absent

**Source:** Supply chain experiment
**Where:** test-grid.md (no rows for service-level KPIs)
**What's missing:** Any baseline or threshold guidance for vendor on-time rate, lead time, fill rate, or cost variance

The finance grid has Tier 1 thresholds for balance sheet invariants and income statement tie-outs. The supply chain has no equivalent for operational KPIs. Practitioners have to invent all thresholds from scratch.

**Suggested fix:** Add a supply chain / operational section to test-grid.md with rows for: vendor on-time rate floor, lead time variance vs target, cost variance per order, and fill rate. Tier 2 or Tier 3 initially, with guidance on calibration.

---

### G18: Bi-temporal data (multiple date fields) not addressed

**Source:** Supply chain experiment
**Where:** test-grid.md, Source Ingestion > Data Freshness (TMP-001)
**What happened:** PO records have three date fields: order_date, expected_delivery, actual_delivery. The freshness check only evaluates one (order_date). But actual_delivery can be in the future (orders not yet received), making a simple "most recent date" check misleading. The framework has no concept of bi-temporal or multi-date-field records.

**Suggested fix:** Add a note to TMP-001 and test-cycle.md Step 2: "For datasets with multiple date fields (e.g., order date, delivery date), define which date governs freshness. Document the load date vs event date distinction. Validate that event dates fall within the expected range for each date field independently."

---

### G19: Missing dimension member vs missing transaction is conflated

**Source:** Supply chain experiment
**Where:** test-grid.md, Anomaly Detection > Missing Expected Record (STAT-006)
**What it says:** "A recurring record does not appear in the period -- absent when present in all prior N periods"
**What happened:** The "Missing Expected Vendor" check in the supply chain experiment is different -- it asks whether a known dimension member (a vendor) is absent from the current period's transactions, not whether a specific recurring transaction is absent. These are different checks with different diagnostic paths.

**Suggested fix:** Split STAT-006 into two: (a) Missing recurring transaction (current definition) and (b) Missing expected dimension member (a vendor, product, or entity that was active last period is absent from this period's data). The diagnostic and remediation differ.

---

## Cross-experiment findings

### G20: Remediation table is incomplete

**Source:** All three experiments
**Where:** test-cycle.md, Remediations section (added recently -- 7 entries)
**Missing entries based on actual test failures:**

| Failure type encountered | Currently in table? |
|---|---|
| Null key (order_id, je_id, po_id) | Yes |
| Duplicate key | No |
| Row count mismatch (source vs landing) | No |
| Balance sheet imbalance | No |
| Double-entry out of balance | No |
| Referential integrity orphan propagating to output | No |
| KPI value outside valid range | No |
| Aggregation tie-out failure | No |

**Suggested fix:** Extend the remediation table to cover at minimum: duplicate keys, row count mismatch, balance/invariant failures, and KPI range violations.

---

### G21: Future-dated records not addressed anywhere

**Source:** Experiments 1 and 3 (data contained records dated ahead of current date)
**Where:** Not mentioned in test-grid.md or test-cycle.md
**What happened:** Both sales and supply chain data included future dates (month-end dates past today). The framework checks that data isn't *too old* (freshness) but has no check for records *too far in the future*.

**Suggested fix:** Add a "Future Date Check" row to test-grid.md under Source Ingestion: "No records dated more than N days after the expected load date. Tier 2 for operational pipelines; Tier 1 for financial pipelines where future dates corrupt period close reporting."

---

## Summary table

| Gap | Priority | Type | Experiments |
|---|---|---|---|
| G1: Threshold placeholders | 1 | Framework completeness | All |
| G2: Run 1 / no prior period | 1 | Protocol gap | All |
| G3: dim_test schema undefined | 1 | Spec gap | All |
| G4: No result templates | 1 | Usability | All |
| G5: WARN vs FAIL undefined | 2 | Ambiguity | All |
| G6: Referential integrity tier | 2 | Tier assignment | 1, 3 |
| G7: run_id format undefined | 2 | Spec gap | All |
| G8: maximum_possible_score | 2 | Ambiguity | All |
| G9: No abort rules | 2 | Protocol gap | All |
| G10: No Python/pandas path | 2 | Tool guidance | All |
| G11: Double-entry not in grid | 3 | Missing check | Finance |
| G12: GL normal balance | 3 | Domain gap | Finance |
| G13: Cumulative vs period GL | 3 | Domain gap | Finance |
| G14: Dual-Path no guide | 3 | Ambiguity | Finance |
| G15: Period cutoff not addressed | 3 | Missing check | Finance |
| G16: KPI range validation | 3 | Missing check | Supply Chain |
| G17: Operational KPI thresholds | 3 | Missing content | Supply Chain |
| G18: Bi-temporal data | 3 | Missing check | Supply Chain |
| G19: Missing dimension member | 3 | Conflated concepts | Supply Chain |
| G20: Remediation table incomplete | 2 | Content gap | All |
| G21: Future-dated records | 2 | Missing check | 1, 3 |

---

## What the framework does well (confirmed across all three experiments)

- The 8-step cycle structure is solid and transferable across all three domains with no changes
- Tier 1 checks (null keys, duplicates, row count, MoM anomaly) caught every injected defect across all three pipelines
- DPPF IDs are useful -- tracing from grid row to test catalog worked in every case
- The READY/REVIEW/BLOCKED gate model is immediately actionable and requires no customization
- The scoring rubric produced consistent, comparable scores across very different pipeline types
- The remediation table pattern is exactly right -- it just needs more entries
