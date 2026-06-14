# Run Log -- Supply Chain Pipeline

**Run ID:** RUN-20260614-104545  
**Run Date:** 2026-06-14 10:45  

| Step | Tier | Category | Test Name | Status | Detail | DPPF IDs |
|---|---|---|---|---|---|---|
| 1 | Tier 1 | Source Ingestion | Schema Presence | PASS | All 10 columns present | STR-001 |
| 1 | Tier 1 | Source Ingestion | Data Type Conformance | PASS | quantity=True, unit_cost=True, total_cost=True | STR-002 |
| 2 | Tier 1 | Source Ingestion | Row Count Reconciliation | PASS | Source=20, Landing=20 | STAT-001 |
| 2 | Tier 1 | Source Ingestion | Null Key Check (po_id) | FAIL | 1 null po_id(s) | STR-003 |
| 2 | Tier 1 | Source Ingestion | Null Key Check (vendor_id) | PASS | Zero null vendor_ids | STR-003 |
| 3 | Tier 1 | Anomaly Detection | Period-over-Period Spend Change | FAIL | Current=84,120.00, Prior=58,565.00, MoM=43.6% (threshold ±30%) | STAT-004 |
| 3 | Tier 2 | Anomaly Detection | Missing Expected Vendor | PASS | All prior-period vendors present | STAT-006 |
| 4 | Tier 1 | Pipeline Processing | Duplicate Detection (po_id) | FAIL | 1 duplicate po_id(s): ['PO2001'] | STR-004 |
| 4 | Tier 2 | Pipeline Processing | Referential Integrity (vendor_id) | WARN | Orphan vendor_id(s): ['V008'] | SEM-001 |
| 4 | Tier 2 | Pipeline Processing | Referential Integrity (product_id) | PASS | All product_ids valid | SEM-001 |
| 4 | Tier 1 | Pipeline Processing | Transformation Logic (total_cost = qty * unit_cost) | PASS | All cost calculations correct | SEM-002 |
| 5 | Tier 2 | Pipeline Processing | Aggregation Accuracy (spend tie-out) | PASS | Detail=84,120.00, Vendor report=84,120.00, gap=0.0000 | SEM-007 |
| 6 | Tier 2 | Output Validation | Vendor On-Time Rate Floor | WARN | 5 vendor(s) below 60% on-time rate: ['V001', 'V003', 'V004', 'V006', 'V007'] | SEM-006, STAT-004 |
| 6 | Tier 2 | Output Validation | Null Vendor Name in Output | WARN | 1 vendor(s) with null name in performance report | STR-003 |
| 7 | Tier 1 | Cross-Validation | Source vs Output Total Spend | PASS | Source=84,120.00, Output=84,120.00, variance=0.0000% | SEM-004 |
| 8 | Tier 3 | Traditional Software | Regression Check | WARN | 3 Tier 1 failure(s) in this run | OPS-001 |
