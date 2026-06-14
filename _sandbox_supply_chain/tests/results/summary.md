# Summary -- Supply Chain Pipeline

**Run ID:** RUN-20260614-104545  
**Run Date:** 2026-06-14 10:45  

## Gate Status: `BLOCKED`

| Metric | Value |
|---|---|
| Total tests | 16 |
| Passed | 9 |
| Failed | 3 |
| Warnings | 4 |
| Pass rate | 56% |
| Tier 1 failures | 3 |
| Overall score | 62% |

## Failures and Warnings

| Tier | Category | Test | Status | Detail |
|---|---|---|---|---|
| Tier 1 | Source Ingestion | Null Key Check (po_id) | FAIL | 1 null po_id(s) |
| Tier 1 | Anomaly Detection | Period-over-Period Spend Change | FAIL | Current=84,120.00, Prior=58,565.00, MoM=43.6% (threshold ±30%) |
| Tier 1 | Pipeline Processing | Duplicate Detection (po_id) | FAIL | 1 duplicate po_id(s): ['PO2001'] |
| Tier 2 | Pipeline Processing | Referential Integrity (vendor_id) | WARN | Orphan vendor_id(s): ['V008'] |
| Tier 2 | Output Validation | Vendor On-Time Rate Floor | WARN | 5 vendor(s) below 60% on-time rate: ['V001', 'V003', 'V004', 'V006', 'V007'] |
| Tier 2 | Output Validation | Null Vendor Name in Output | WARN | 1 vendor(s) with null name in performance report |
| Tier 3 | Traditional Software | Regression Check | WARN | 3 Tier 1 failure(s) in this run |
