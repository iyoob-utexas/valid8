# Real-World Data Test Patterns

This page captures data-related testing patterns discovered in existing test scripts from other projects.
Use these patterns when they apply to data pipelines, extraction logic, and analytics datasets.

## Applicable patterns

### Column sanity
- Validate each expected output field exists and no extras are present.
- Check required fields are never null.
- Verify common formats such as email, phone, IDs, or region codes.
- Treat all forms of missing values consistently.

Relevant repo categories:
- `domains/data/tests/schema-and-types.md`
- `domains/data/tests/quality-and-completeness.md`

### Row-level cross-column consistency
- Validate values across columns within the same row.
- Confirm derived fields are consistent with source fields in the same record.
- Catch issues like invalid region codes, mismatched address/region pairs, or inconsistent status values.

Relevant repo categories:
- `domains/data/tests/quality-and-completeness.md`
- `domains/data/tests/integrity-and-references.md`

### Functional step validation
- Test that each pipeline step returns the expected schema.
- Check that intermediate output files or tables contain the required fields.
- Validate wire dependencies between steps, such as the presence of expected downstream artifacts.

Relevant repo categories:
- `domains/data/dimensions/processing.md`
- `domains/data/tests/schema-and-types.md`

### Integration and artifact alignment
- Confirm all expected output artifacts exist.
- Validate row counts and key alignment across outputs.
- Ensure candidate or entity IDs align across every generated artifact.

Relevant repo categories:
- `domains/data/dimensions/processing.md`
- `domains/data/dimensions/final-data.md`
- `domains/data/tests/integrity-and-references.md`

### Referential integrity
- Check that reference IDs or foreign keys are present in the parent artifact.
- Validate there are no orphan rows.
- Detect duplicate key values where uniqueness is expected.

Relevant repo categories:
- `domains/data/tests/integrity-and-references.md`

### Idempotency and repeatability
- Confirm repeated runs over the same input produce identical output.
- Validate stable metrics do not drift across back-to-back executions.

Relevant repo categories:
- `domains/data/dimensions/processing.md`
- `domains/data/tests/performance-and-freshness.md`

### Edge-case handling
- Test empty, missing, malformed, or non-standard inputs.
- Verify the pipeline handles missing sections gracefully and does not crash.
- Ensure logic paths for unexpected input do not produce corrupted outputs.

Relevant repo categories:
- `domains/data/tests/anomaly-and-drift.md`
- `domains/data/dimensions/processing.md`

### Rule and tolerance boundary testing
- Validate business-rule thresholds and tolerance boundaries explicitly.
- Check behavior just inside and just outside the threshold.
- Ensure algorithmic heuristics (e.g. bucket selection, matching windows) behave as expected.

Relevant repo categories:
- `domains/data/dimensions/processing.md`
- `domains/data/tests/quality-and-completeness.md`

### Reference and external comparison
- Compare output values against validated reference files or source documents.
- Use cross-validation to catch silent errors that internal checks may miss.

Relevant repo categories:
- `domains/data/dimensions/final-data.md`
- `domains/data/tests/anomaly-and-drift.md`

## What to ignore for this repo
- UI rendering and browser-focused tests are out of scope.
- Only data-related tests should influence the repo’s guidance.

## How to use these patterns
1. Review this page when adding new checks for a data pipeline.
2. Map the pattern to the existing category in `domains/data/tests/`.
3. Keep the guidance tool-agnostic, but note the implementation style if it helps with adoption.
4. Use the patterns as a basis for both project-specific and generic checks.
