# Run Log -- Finance Pipeline

**Run ID:** RUN-20260614-104531  
**Run Date:** 2026-06-14 10:45  

| Step | Tier | Category | Test Name | Status | Detail | DPPF IDs |
|---|---|---|---|---|---|---|
| 1 | Tier 1 | Source Ingestion | Schema Presence | PASS | All 6 columns present | STR-001 |
| 1 | Tier 1 | Source Ingestion | Data Type Conformance | PASS | debit_ok=True, credit_ok=True | STR-002 |
| 2 | Tier 1 | Source Ingestion | Row Count Reconciliation | PASS | Source=31, Landing=31 | STAT-001 |
| 2 | Tier 1 | Source Ingestion | Null Key Check (je_id) | FAIL | 1 null je_id(s) found | STR-003 |
| 2 | Tier 1 | Source Ingestion | Null Key Check (entity_id) | PASS | Zero null entity_ids | STR-003 |
| 3 | Tier 1 | Anomaly Detection | Period-over-Period Revenue Change | FAIL | Current=470,000, Prior=360,000, MoM=30.6% (threshold ±25%) | STAT-004 |
| 4 | Tier 1 | Pipeline Processing | Duplicate Detection (je_id) | FAIL | 1 duplicate je_id(s): ['JE2020'] | STR-004 |
| 4 | Tier 2 | Pipeline Processing | Referential Integrity (account_id) | PASS | All account_ids valid | SEM-001 |
| 4 | Tier 2 | Pipeline Processing | Referential Integrity (entity_id) | PASS | All entity_ids valid | SEM-001 |
| 4 | Tier 1 | Pipeline Processing | Transformation Logic | PASS | net_amount correct for all rows | SEM-002 |
| 5 | Tier 2 | Pipeline Processing | Aggregation Accuracy (detail vs statements) | PASS | Detail=113000.00, IS+BS=113000.00, gap=0.0000 | SEM-007 |
| 6 | Tier 1 | Output Validation | Balance Sheet Equation (Assets = Liabilities + Equity) | FAIL | Assets=730,000.00, Liab=-401,000.00, Equity=-119,000.00, imbalance=210,000.00 | SEM-014, SEM-007 |
| 6 | Tier 1 | Output Validation | Net Income Ties to Retained Earnings | FAIL | Net Income=803,000.00, RE change=69,000.00, gap=734,000.00 | SEM-015, SEM-004 |
| 6 | Tier 2 | Cross-Validation | Intercompany Elimination Check | PASS | IC net across E01 and E04 on account 4100 = 0.00 (should be 0) | SEM-014, SEM-015 |
| 7 | Tier 1 | Cross-Validation | Double-Entry Balance (Total Debits = Total Credits) | FAIL | Total Debits=1,103,000.00, Total Credits=990,000.00, gap=113,000.00 | SEM-004, SEM-015 |
| 8 | Tier 3 | Traditional Software | Regression Check | WARN | 6 Tier 1 failure(s) confirmed in this run | OPS-001 |
