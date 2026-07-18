# Metadata and Governance

Data governance and metadata validation are essential cross-cutting tests for any data project.

## What to test

- Metadata completeness
  - Verify that every dataset has a documented schema, owner, refresh schedule, and description.
  - Confirm field-level metadata such as business meaning, data type, allowed values, and nullability.

- Lineage and provenance
  - Confirm data lineage is documented from source to final output.
  - Validate that each transformation step and data source is traceable.

- Ownership and stewardship
  - Verify each dataset and test has an assigned owner who is accountable for data quality.
  - Validate that escalation and remediation ownership is defined for failures.

- Data standards and definitions
  - Confirm business terms are defined consistently across sources and outputs.
  - Validate that code lists, lookup values, and reference data conform to agreed standards.

- Change management
  - Document schema changes, source changes, and test rule updates.
  - Validate that changed contracts are reviewed and approved before deployment.

## Why it matters

Metadata and governance tests give teams confidence that the data is understandable, auditable, and maintainable over time. Without this coverage, pipelines may produce correct numbers but still fail to meet enterprise data management requirements.
