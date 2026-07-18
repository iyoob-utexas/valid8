# Testing Dimensions

This section defines the core lifecycle dimensions of data testing.

Each dimension represents a stage of the data project where dedicated validation is required.

- `domains/data/dimensions/design-and-contracts.md` — tests for schema and contract design before a pipeline is built.
- `domains/data/dimensions/raw-data.md` — tests for raw, ingested, and source data.
- `domains/data/dimensions/processing.md` — tests for transformation, enrichment, aggregation, and orchestration.
- `domains/data/dimensions/final-data.md` — tests for delivered datasets, exports, and analytics-ready output.
- `domains/data/dimensions/deployment-and-cutover.md` — tests for replacing an existing pipeline: historical migration and old-versus-new parity before decommissioning.

## Cross-cutting concerns

Some tests apply to every dimension:

- Data schema and type validation
- Completeness and null handling
- Referential integrity and duplicates
- Freshness, latency, and timeliness
- Documentation, lineage, and ownership
- Metadata and governance controls
- Security, privacy, and access controls
- Observability, logging, and operational readiness

## How this connects to the framework

- Use `domains/data/framework/README.md` to understand the standard, severity tiers, and ownership requirements.
- Use `domains/data/process/test-cycle.md` to execute the eight-step validation runbook.
- Use `domains/data/grid/README.md` and the companion test matrix to map each dimension into concrete checks.
