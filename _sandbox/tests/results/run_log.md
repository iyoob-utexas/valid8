# Run Log

**Run ID:** RUN-20260614-083734  
**Run Date:** 2026-06-14 08:37  

| Step | Tier | Category | Test Name | Status | Detail | DPPF IDs |
|---|---|---|---|---|---|---|
| 1 | Tier 1 | Source Ingestion | Schema Presence | PASS | All 6 expected columns present, no extras | STR-001 |
| 1 | Tier 1 | Source Ingestion | Data Type Conformance | PASS | quantity and revenue are fully numeric | STR-002 |
| 2 | Tier 1 | Source Ingestion | Row Count Reconciliation | PASS | Source=39, Landing=39 | STAT-001, SEM-004 |
| 2 | Tier 1 | Source Ingestion | Null Key Check | FAIL | 1 row(s) with null order_id found -- quarantine required | STR-003 |
| 2 | Tier 1 | Source Ingestion | Data Freshness | PASS | Latest record: 2026-06-30 (-16d ago) | TMP-001 |
| 3 | Tier 1 | Anomaly Detection | Period-over-Period Revenue Change | FAIL | MoM change: 116.0% exceeds ±25% threshold -- review required | STAT-004 |
| 3 | Tier 1 | Anomaly Detection | KPI Zero/Null Check | PASS | No zero-revenue rows in current period | STAT-007 |
| 4 | Tier 1 | Pipeline Processing | Duplicate Detection | FAIL | 1 duplicate order_id(s): ['O2028'] | STR-004 |
| 4 | Tier 2 | Pipeline Processing | Referential Integrity | WARN | Orphan product_id(s) not in dim_product: ['P011'] | SEM-001 |
| 4 | Tier 1 | Pipeline Processing | Transformation Logic | PASS | revenue = quantity * unit_price holds for all rows | SEM-002 |
| 5 | Tier 2 | Pipeline Processing | Aggregation Accuracy | PASS | Detail=13379.54, Aggregate=13379.54, gap=0.0000 | SEM-007 |
| 6 | Tier 1 | Output Validation | Output Key Null Check (year_month) | PASS | No null year_month values in report | STR-003 |
| 6 | Tier 2 | Output Validation | Output Key Null Check (category) | WARN | 1 rows with null category (unmapped product_id in output) | STR-003 |
| 6 | Tier 2 | Output Validation | Derived Value Plausibility | PASS | revenue_per_unit within 10% of unit_price for all rows | SEM-006 |
| 7 | Tier 1 | Cross-Validation | Source vs Output Total | PASS | Source=13379.54, Output=13379.54, variance=0.0000% | SEM-004 |
| 8 | Tier 3 | Traditional Software | Regression Check | WARN | Re-ran 11 Tier 1 checks. 3 failure(s) confirmed (not new regressions -- defects from injected data). | OPS-001 |
