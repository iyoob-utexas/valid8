# Summary Test Grid

This page defines the summary view for test execution results. It is the high-level scorecard that makes the master checklist actionable across runs.

## Purpose

- Summarize the total number of tests executed.
- Report pass, fail, and warning counts by tier and category.
- Calculate a pass rate for the latest run.
- Show whether the latest run meets the release gate for Tier 1 checks.

## When to use it

- After each test run to answer "Is the data ready?"
- In dashboards and executive scorecards.
- To compare test health across pipelines, domains, or time.

## Key fields

- `run_date` — date/time of the test execution.
- `run_id` — unique identifier for the run.
- `tier` — severity tier of the test.
- `category` — category or dimension of the test.
- `test_type` — the test name or rule.
- `status` — pass / fail / warning.
- `total_tests` — count of tests executed.
- `passed` — count of passing tests.
- `failed` — count of failing tests.
- `warnings` — count of non-blocking alerts.
- `pass_rate` — `passed / total_tests`. `total_tests` counts only the checks executed in this run -- tests scoped out of the project do not factor in.
- `tier1_failures` — count of Tier 1 failures.
- `overall_score` — weighted score: `(tier1_pass*5 + tier2_pass*2 + tier3_pass*1) / maximum_possible_score`.
- `gate_status` — `READY`, `REVIEW`, or `BLOCKED`. See scoring rubric in root README for thresholds.

## run_id format

`run_id` must be unique within a project. Recommended format: `YYYYMMDD-HHMMSS-<pipeline-name>` (e.g., `20260613-143022-sales`). For multi-project dashboards, prefix with a project code. Use a consistent format across all runs -- mixed formats prevent cross-run comparison and trend analysis.

## dim_test schema

`dim_test` is the test metadata dimension. Export it from `docs/grid/test-grid.md` before the first run and update it when the scoped test list changes. A starter template is available at `docs/grid/dim_test_template.csv`.

| Column | Description |
|---|---|
| `test_id` | Short unique identifier for this test within the project (e.g., `T001`) |
| `tier` | Severity tier: Tier 1, Tier 2, or Tier 3 |
| `category` | Test category from the grid (e.g., Source Ingestion, Pipeline Processing) |
| `test_name` | Name of the specific check |
| `dama_dimension` | DAMA data quality dimension(s) this test covers |
| `dppf_ids` | Corresponding DPPF catalog IDs |
| `threshold` | The pass/fail threshold or rule for this test |
| `owner` | Role accountable for this test |
| `lifecycle_stage` | When this test runs: Development, CI, Pre-deployment, or Production monitoring |
| `in_scope` | Boolean -- whether this test is active for the current project |

## How to build it

1. Export the test metadata from `docs/grid/test-grid.md` into a `dim_test` dimension using the schema above.
2. Collect run-level execution results into a `fact_results` table.
3. Aggregate by `run_id`, `tier`, and `category`.
4. Compute `pass_rate` and `tier1_failures`.
5. Use the summary grid as the source for dashboards and gate checks.

## Status values

Results use five status values. All five should appear in the run log as needed:

| Status | Meaning | Counts toward pass rate? |
|---|---|---|
| `PASS` | Check ran and met its threshold | Yes (numerator) |
| `FAIL` | Check ran and did not meet its threshold | Yes (denominator only) |
| `WARN` | Tier 2 check flagged a concern; run continues | Yes (denominator only) |
| `SKIPPED` | Check was not run due to an upstream Tier 1 failure (see abort policy) | No |
| `BASELINE` | Run 1 anomaly check; no prior period to compare against | No |

## Why it matters

A summary test grid converts the raw checklist into a single operational metric. It makes the framework usable for both technical teams and stakeholders by surfacing pass rate, gate readiness, and failure concentration.

## Example summary view

| Run | Tier | Category | Total | Passed | Failed | Warnings | Pass rate | Gate status |
|---|---|---|---|---|---|---|---|---|
| 2026-06-10 | Tier 1 | Source Ingestion | 12 | 11 | 1 | 0 | 92% | BLOCKED |
| 2026-06-10 | Tier 2 | Pipeline Processing | 10 | 9 | 0 | 1 | 90% | READY |
| 2026-06-10 | Tier 3 | Anomaly Detection | 8 | 8 | 0 | 0 | 100% | READY |

> Use this summary for run-level gating, trend analysis, and execution reviews.
