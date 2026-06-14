# Summary Scorecard

**Run ID:** RUN-20260614-083734  
**Run Date:** 2026-06-14 08:37  

## Gate Status: `BLOCKED`

| Metric | Value |
|---|---|
| Total tests | 16 |
| Passed | 10 |
| Failed | 3 |
| Warnings | 3 |
| Pass rate | 62% |
| Tier 1 failures | 3 |
| Overall score | 69% |

## By Tier

| Tier | Total | Passed | Failed | Warnings | Pass Rate |
|---|---|---|---|---|---|
| Tier 1 | 11 | 8 | 3 | 0 | 73% |
| Tier 2 | 4 | 2 | 0 | 2 | 50% |
| Tier 3 | 1 | 0 | 0 | 1 | 0% |

## Failures and Warnings

| Tier | Category | Test | Status | Detail |
|---|---|---|---|---|
| Tier 1 | Source Ingestion | Null Key Check | FAIL | 1 row(s) with null order_id found -- quarantine required |
| Tier 1 | Anomaly Detection | Period-over-Period Revenue Change | FAIL | MoM change: 116.0% exceeds ±25% threshold -- review required |
| Tier 1 | Pipeline Processing | Duplicate Detection | FAIL | 1 duplicate order_id(s): ['O2028'] |
| Tier 2 | Pipeline Processing | Referential Integrity | WARN | Orphan product_id(s) not in dim_product: ['P011'] |
| Tier 2 | Output Validation | Output Key Null Check (category) | WARN | 1 rows with null category (unmapped product_id in output) |
| Tier 3 | Traditional Software | Regression Check | WARN | Re-ran 11 Tier 1 checks. 3 failure(s) confirmed (not new regressions -- defects from injected data). |
