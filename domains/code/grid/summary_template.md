# Summary Scorecard

**Run ID:** `YYYYMMDD-HHMMSS-<repo-or-PR-id>`
**Run Date:** `YYYY-MM-DD HH:MM`
**Repository / PR:** `<repo name or PR link>`

## Gate Status: `BLOCKED | REVIEW | READY`

| Metric | Value |
|---|---|
| Total tests | |
| Passed | |
| Failed | |
| Warnings | |
| Skipped | |
| Baseline (first-run benchmark checks) | |
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

## By Domain

| Domain | Total | Passed | Failed | Warnings | Pass Rate |
|---|---|---|---|---|---|
| Correctness and logic | | | | | |
| Structure and style | | | | | |
| Security | | | | | |
| Architecture and design | | | | | |
| Testing and coverage | | | | | |
| Performance and scalability | | | | | |
| Reliability and operability | | | | | |
| Adversarial | | | | | |

## Failures and Warnings

| Tier | Domain | Test | Status | Detail | Remediation Taken |
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

**Next action:** `<what happens next: merge, release, investigate, block>`
