# Integrity and Referential Validation

Integrity checks confirm that relationships within and across datasets hold. Data can be individually valid but still broken at the relationship level: a foreign key pointing to nothing, a duplicate skewing a total, an entity that appears differently in two systems.

## What to test

- Referential integrity: foreign keys reference existing parent rows; lookup and dimension joins resolve correctly.
- Uniqueness and duplicates: primary key uniqueness; no duplicate rows or business keys.
- Cardinality expectations: one-to-many or many-to-one relationships behave as expected; no unexpected fan-out or missing join results.
- Cross-artifact consistency: the same entity carries consistent attributes across multiple sources.

## Why it matters

Broken relationships and duplicates are the most common source of incorrect analytics. A join that fans out doubles totals. An orphan record mismatches source and output. These checks protect against numbers that pass schema validation but tell the wrong story.

---

## DPPF semantic test catalog

| ID | Name | What it verifies | Defends against | Standards | Lifecycle |
|---|---|---|---|---|---|
| SEM-001 | Referential integrity | Foreign key values resolve to a valid row in the referenced parent or dimension table | Orphan records, broken joins, incomplete dimension coverage | Integrity, Consistency | Development, CI, Production monitoring |
| SEM-002 | Business rule validation | Rows satisfy all domain rules: valid status codes, valid amounts, required conditional fields | Incorrect calculations, rule drift from upstream changes, unmapped edge cases | Accuracy, Validity | Development, CI, Production monitoring |
| SEM-003 | Cross-field logic consistency | Related fields within a row are mutually consistent: end date after start date, amount sign matching transaction type, status matching activity flags | Contradictory field combinations, logic bugs in transformation, upstream encoding inconsistencies | Consistency, Accuracy | Development, CI, Production monitoring |
| SEM-004 | Source-to-target reconciliation | Aggregate totals, row counts, and key sums at source match the same values in the transformed or loaded target | Silent data loss, mapping errors, partial loads, truncation without alerting | Accuracy, Completeness | CI, Pre-deployment, Production monitoring |
| SEM-005 | Master data consistency | A shared entity such as a vendor, cost center, or employee carries identical attributes across all source systems and pipeline stages | Conflicting entity records, golden record failure, merge survivor logic errors | Uniqueness, Consistency | Development, CI, Production monitoring |
| SEM-006 | Derived metric validation | Computed fields match the expected result of the stated derivation formula using the same input rows | Corrupted metrics, formula drift after a logic change, silent rounding or precision loss | Accuracy, Traceability | Development, CI, Production monitoring |
| SEM-007 | Aggregation rollup accuracy | The sum of detail-level rows matches the rolled-up aggregate at every level of the hierarchy | Incorrect subtotals, aggregation filter bugs, double-counting from bad joins | Accuracy, Consistency | CI, Pre-deployment, Production monitoring |
| SEM-008 | Hierarchical integrity | Parent-child relationships in a hierarchy are valid: no circular references, no orphan children, rollup from leaves to root is complete | Broken org hierarchies, invalid GL account trees, circular rollup paths | Integrity, Consistency | Development, CI, Production monitoring |
| SEM-009 | State machine transition validity | Status or lifecycle fields only advance through allowed state transitions and never skip required intermediates | Invalid status jumps, state corruption from retry or replay, out-of-order event application | Validity, Integrity | Development, CI |
| SEM-010 | Temporal business rule compliance | Fields governed by effective-date or validity-period logic return the correct value for the reporting period being evaluated | Applying a future rate to a past period, using an expired mapping, missing period-over-period isolation | Accuracy, Consistency | Development, CI, Production monitoring |
| SEM-011 | Conditional field rule validation | Fields that are required or prohibited based on the value of another field satisfy those conditional rules | Silent nulls in conditionally required fields, prohibited values leaking through, logic gaps in transformation | Validity, Completeness | Development, CI |
| SEM-012 | Lookup and code table completeness | Every code, category, or identifier in the fact data has a corresponding entry in the applicable lookup or mapping table | Unmapped GL codes, unknown product categories, missing entity mappings causing silent drop | Completeness, Integrity | Development, CI, Production monitoring |
| SEM-013 | Entity deduplication logic | Deduplication or survivorship logic produces a single canonical record per entity with the correct attribute values | Duplicate entities surviving dedup, wrong survivor selected, merge artifacts in downstream aggregations | Uniqueness, Accuracy | CI, Pre-deployment |
| SEM-014 | Financial equation validation | Balance sheet equations, netting rules, and elimination rules hold on the final output for every reporting period | Assets not equaling liabilities plus equity, intercompany not netting to zero, equation breach from rounding | Accuracy, Integrity | CI, Pre-deployment, Production monitoring |
| SEM-015 | Cross-dataset reconciliation | Totals or metrics that should agree across two independently built datasets do agree within the defined tolerance | Dual-path P&L divergence, budget versus actual using different source actuals, report versus query mismatches | Accuracy, Consistency | CI, Pre-deployment, Production monitoring |
