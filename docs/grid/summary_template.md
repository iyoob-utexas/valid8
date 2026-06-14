# Summary Scorecard

**Run ID:** `YYYYMMDD-HHMMSS-<pipeline-name>`
**Run Date:** `YYYY-MM-DD HH:MM`
**Pipeline:** `<pipeline name>`

## Gate Status: `BLOCKED | REVIEW | READY`

| Metric | Value |
|---|---|
| Total tests | |
| Passed | |
| Failed | |
| Warnings | |
| Skipped | |
| Baseline (Run 1 anomaly checks) | |
| Pass rate | |
| Tier 1 failures | |
| Overall score | |

## By Tier

| Tier | Total | Passed | Failed | Warnings | Skipped | Pass Rate |
|---|---|---|---|---|---|---|
| Tier 1 | | | | | | |
| Tier 2 | | | | | | |
| Tier 3 | | | | | | |
| **Total** | | | | | | |

## Failures and Warnings

| Tier | Category | Test | Status | Detail | Remediation Taken |
|---|---|---|---|---|---|
| | | | | | |

## Skipped Tests

| Step | Test | Reason |
|---|---|---|
| | | |

## Gate Decision

- `READY` if `pass_rate >= 95%` and `tier1_failures == 0`
- `REVIEW` if `pass_rate >= 80%` and `tier1_failures == 0`
- `BLOCKED` if `tier1_failures > 0`

**Decision rationale:** `<explain the gate decision in one sentence>`

**Next action:** `<what happens next: promote, investigate, quarantine, re-run>`
