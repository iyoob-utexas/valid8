# Test Categories

This section defines reusable categories of tests that apply across multiple data dimensions.

Each category is intended to be used in conjunction with a lifecycle dimension:

- raw ingestion testing
- transformation and pipeline testing
- final data product testing

Each test file contains both prose guidance and a DPPF test catalog: a structured table of test definitions with IDs, adversarial failure scenarios, standard mappings, and lifecycle stage assignments. These catalogs are the primary reference for the DPPF coverage evaluation checklist in `domains/data/framework/dppf.md`.

## Core test categories and DPPF domain mapping

| File | Focus | DPPF domain | DPPF IDs |
|---|---|---|---|
| `schema-and-types.md` | Structure, columns, data-type validation | Structural | STR-001 to STR-016 |
| `integrity-and-references.md` | Uniqueness, referential integrity, duplicate detection | Semantic | SEM-001 to SEM-015 |
| `anomaly-and-drift.md` | Distribution, trend, and data drift detection | Statistical | STAT-001 to STAT-015 |
| `performance-and-freshness.md` | Latency, freshness, SLA, throughput, scale | Temporal + Performance | TMP-001 to TMP-014, PERF-001 to PERF-012 |
| `observability-and-operations.md` | Logging, alerts, orchestration, environment parity, pipeline cutover | Operational | OPS-001 to OPS-016 |
| `adversarial.md` | Fault injection, bad data, chaos, replay | Adversarial | ADV-001 to ADV-015 |
| `quality-and-completeness.md` | Nulls, completeness, record coverage | Supporting (Structural + Semantic) | See STR-003, SEM-011, SEM-012 |
| `metadata-and-governance.md` | Metadata, lineage, ownership, standards compliance | Supporting (Operational) | See OPS-011, OPS-012 |
| `security-and-privacy.md` | Sensitive data classification, masking, access, compliance | Cross-cutting | See ADV-006, OPS-012 |

## Severity tiers

Tier definitions and the DPPF severity scoring model are in `domains/data/framework/README.md`. The full tier-to-dimension reference is in `domains/data/grid/tier-dimension-reference.md`.

## How to apply

1. Choose the data artifact and lifecycle dimension.
2. Use the categories below to identify the relevant checks.
3. Add any project-specific rules or business validations.
4. For a coverage gap analysis, complete the checklist in `domains/data/framework/dppf.md`.

## Real-world patterns

- See `domains/data/tests/real-world-patterns.md` for additional patterns extracted from existing data pipeline test scripts.
- Use that page for examples of schema sanity, functional step validation, integration alignment, referential integrity, idempotency, and edge-case handling.
