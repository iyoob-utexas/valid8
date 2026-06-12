# Schema and Type Validation

Schema validation is one of the most fundamental checks across all data artifacts.

## What to test

- Column presence: confirm required fields exist; detect newly added or removed columns.
- Data types: verify each field has the expected type; detect type drift such as strings becoming numeric or dates becoming text.
- Domain constraints: validate values fall within expected ranges, match approved lists, and follow formatting rules for identifiers, codes, and timestamps.
- Field metadata: track nullability expectations and default values per field.

## Why it matters

Schema mismatches break downstream consumers silently. A column that changes type or disappears is rarely caught by the pipeline itself. Catching it at ingestion prevents compounding failures.

---

## DPPF structural test catalog

The table below defines the Structural domain. Each row is a specific test with the failure it prevents, the quality standards it maps to, and where in the pipeline lifecycle it belongs.

| ID | Name | What it verifies | Defends against | Standards | Lifecycle |
|---|---|---|---|---|---|
| STR-001 | Schema presence | All expected fields exist; no unexpected fields are present | Schema drift, contract failure, silent column drop | Validity, Traceability, Schema | Development, CI, Production monitoring |
| STR-002 | Data type conformance | Field values match the expected data type for each column | Type mutation, string-to-numeric drift, date becoming text | Validity, Consistency, Schema | Development, CI, Production monitoring |
| STR-003 | Nullability contract | Required fields contain no null or blank values | Missing keys, incomplete records, partial extracts | Completeness, Integrity | Development, CI, Production monitoring |
| STR-004 | Primary key uniqueness | The primary key column or columns contain no duplicate values | Duplicate key propagation, merge failures, incorrect upserts | Uniqueness, Integrity | Development, CI, Production monitoring |
| STR-005 | Compound key uniqueness | All combinations of the compound business key are unique across rows | Grain violations, duplicate business events, fan-out in joins | Uniqueness, Integrity | Development, CI, Production monitoring |
| STR-006 | Field cardinality bounds | The count of distinct values in a field stays within the contracted minimum and maximum | Exploding cardinality from enrichment failure, collapsed cardinality from corruption | Uniqueness, Consistency, Schema | Development, CI, Production monitoring |
| STR-007 | Enumerated value conformance | Values in a categorical field belong to the approved list of allowed values | Invalid codes, new upstream category not added to mapping, stale enumerations | Validity, Consistency | Development, CI, Production monitoring |
| STR-008 | String length bounds | Character lengths fall within the contracted minimum and maximum | Truncated values, oversized payloads, encoding-inflated lengths | Validity, Completeness | Development, CI |
| STR-009 | Numeric range bounds | Numeric fields fall within the contracted minimum and maximum values | Out-of-range injection, unit conversion errors, negative values in unsigned fields | Validity, Accuracy | Development, CI, Production monitoring |
| STR-010 | Character encoding conformance | String fields use the agreed encoding and contain no malformed byte sequences | Encoding attacks, UTF-8 corruption, multi-byte overflow | Validity, Integrity | CI, Pre-deployment |
| STR-011 | File and format contract | File structure, delimiter, header row, and compression match the source contract | Malformed files, format change at source, mixed-format landing | Validity, Traceability, Schema | CI, Production monitoring |
| STR-012 | Default value application | Fields that require a default when null receive the correct default during processing | Silent null propagation, incorrect aggregation on unset fields | Completeness, Accuracy | Development, CI |
| STR-013 | Schema evolution backward compatibility | Schema changes between versions are backward compatible or gated behind an explicit version bump | Silent breaking changes, downstream code failures after schema update | Traceability, Validity, Schema | Development, CI, Pre-deployment |
| STR-014 | Partition and ingestion contract | Partition keys, file names, and ingestion metadata match the data contract | Ingestion misalignment, landing in wrong partition, stale-partition reuse | Lineage, Traceability, Schema | CI, Pre-deployment, Production monitoring |
| STR-015 | Data contract version compliance | The source data carries a contract version identifier compatible with the consuming pipeline | Breaking contract changes going undetected, version mismatch between producer and consumer | Traceability, Validity | CI, Pre-deployment, Production monitoring |
