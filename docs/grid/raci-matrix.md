# RACI Matrix

This matrix defines roles and accountability for each data testing category.

| Category / Test Area | Data Engineer | Data Analyst | Data Scientist | ML Engineer | BI / Reporting | Test Lead / QA |
|---|---|---|---|---|---|---|
| Source ingestion & schema | R | I | I | C | I | A |
| Anomaly detection | C | R | C | C | I | A |
| Pipeline processing / transforms | R | C | C | C | I | A |
| Output validation | C | R | I | I | C | A |
| Cross-validation | C | R | I | I | A | C |
| Multi-source consistency | R | C | I | I | I | A |
| Regression & idempotency | R | C | I | I | C | A |
| PII / security / access | R | I | I | I | I | A |
| Test logging & dashboard | R | C | C | C | C | A |

> Legend: R = Responsible (does the work), A = Accountable (owns the outcome), C = Consulted (gives input), I = Informed (kept in the loop)

> Note: Tailor per engagement; not every role appears on every project. The Test Lead / QA role oversees coverage and prevents duplicate or no-owner tests.
