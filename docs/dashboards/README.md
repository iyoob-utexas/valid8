# Test Results Dashboard Spec

This page describes how to close the test cycle with a reusable results dashboard.

## Purpose

The dashboard provides a single view of the latest test cycle, showing whether the data is ready to be released.

## Data model

- `fact_results`: the test run results table.
- `dim_test`: the test metadata exported from the grid.
- `dim_run`: one row per run, with `run_date` and `is_latest`.
- `Date`: standard date dimension for trends.

## What to build

- Run Summary page: overall gate status, pass/fail counts, open failures by tier and category.
- Trends page: pass rates and fail counts over time by tier and category.
- Test Detail page: drillthrough to a single test history with status and threshold details.

## Key behaviors

- Latest-run gate: show BLOCKED if any Tier 1 failure exists; REVIEW if pass_rate >= 80% with no Tier 1 failures; READY if pass_rate >= 95% with no Tier 1 failures.
- Conditional formatting: green for pass, amber for warnings, red for failures.
- Slicers: date range, tier, category, table name, status.
- Drillthrough: enable detailed investigation from any failed test row.

## Operational guidance

- Use Direct Lake for near-real-time dashboards on a Lakehouse results table.
- If using import mode, refresh the semantic model after the run.
- Add alerts on Tier 1 failures to notify the on-call channel automatically.
- Apply row-level security if multiple clients share the same workspace.

## Build checklist

1. Confirm the results table is populated by test runs.
2. Export `dim_test` from the grid and load it into the model.
3. Build `dim_run` with `run_date` and `is_latest`.
4. Create relationships between fact and dimensions.
5. Add measures, charts, and drillthrough.
6. Add filters, conditional formatting, and alerting.
7. Publish and verify access.

## Reusability

This dashboard is domain-neutral. It works for any client if the results table and test metadata are maintained consistently.
