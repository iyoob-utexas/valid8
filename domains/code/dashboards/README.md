# Test Results Dashboard Spec

This page describes how to close the test cycle with a reusable results dashboard.

## Purpose

The dashboard provides a single view of the latest test cycle across PRs and releases, showing whether a change is ready to merge or a release is ready to ship.

## Data model

- `fact_results`: the test run results table.
- `dim_test`: the test metadata exported from the grid.
- `dim_run`: one row per run, with `run_date` and `is_latest`.
- `dim_repo`: one row per repository or service in scope.
- `Date`: standard date dimension for trends.

## What to build

- Run Summary page: overall gate status, pass/fail counts, open failures by tier and domain.
- Trends page: pass rates and fail counts over time by tier, domain, and repository.
- Test Detail page: drillthrough to a single test's history with status and threshold details.
- Security posture page: open vulnerability count by severity, mean time to remediate, dependency scan freshness.

## Key behaviors

- Latest-run gate: show BLOCKED if any Tier 1 failure exists; REVIEW if pass_rate >= 80% with no Tier 1 failures; READY if pass_rate >= 95% with no Tier 1 failures.
- Conditional formatting: green for pass, amber for warnings, red for failures.
- Slicers: date range, tier, domain, repository, status.
- Drillthrough: enable detailed investigation from any failed test row, linking back to the PR or commit.

## Operational guidance

- Populate `fact_results` directly from CI pipeline output where possible, rather than manual entry.
- Refresh the dashboard on every CI run for near-real-time PR-level visibility.
- Add alerts on Tier 1 failures to notify the on-call channel automatically.
- Apply row-level or repository-level access control if multiple teams share the same workspace.

## Build checklist

1. Confirm the results table is populated by CI runs and scanner output.
2. Export `dim_test` from the grid and load it into the model.
3. Build `dim_run` with `run_date` and `is_latest`.
4. Build `dim_repo` with repository name, owner, and criticality tier.
5. Create relationships between fact and dimensions.
6. Add measures, charts, and drillthrough.
7. Add filters, conditional formatting, and alerting.
8. Publish and verify access.

## Reusability

This dashboard is domain-neutral. It works for any team or repository if the results table and test metadata are maintained consistently.
