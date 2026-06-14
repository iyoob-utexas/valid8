# Summary -- Finance Pipeline

**Run ID:** RUN-20260614-104531  
**Run Date:** 2026-06-14 10:45  

## Gate Status: `BLOCKED`

| Metric | Value |
|---|---|
| Total tests | 16 |
| Passed | 9 |
| Failed | 6 |
| Warnings | 1 |
| Pass rate | 56% |
| Tier 1 failures | 6 |
| Overall score | 52% |

## Failures and Warnings

| Tier | Category | Test | Status | Detail |
|---|---|---|---|---|
| Tier 1 | Source Ingestion | Null Key Check (je_id) | FAIL | 1 null je_id(s) found |
| Tier 1 | Anomaly Detection | Period-over-Period Revenue Change | FAIL | Current=470,000, Prior=360,000, MoM=30.6% (threshold ±25%) |
| Tier 1 | Pipeline Processing | Duplicate Detection (je_id) | FAIL | 1 duplicate je_id(s): ['JE2020'] |
| Tier 1 | Output Validation | Balance Sheet Equation (Assets = Liabilities + Equity) | FAIL | Assets=730,000.00, Liab=-401,000.00, Equity=-119,000.00, imbalance=210,000.00 |
| Tier 1 | Output Validation | Net Income Ties to Retained Earnings | FAIL | Net Income=803,000.00, RE change=69,000.00, gap=734,000.00 |
| Tier 1 | Cross-Validation | Double-Entry Balance (Total Debits = Total Credits) | FAIL | Total Debits=1,103,000.00, Total Credits=990,000.00, gap=113,000.00 |
| Tier 3 | Traditional Software | Regression Check | WARN | 6 Tier 1 failure(s) confirmed in this run |
