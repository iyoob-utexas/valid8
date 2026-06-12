# Final Data Product Testing

This dimension validates the delivered datasets, analytics models, and exported artifacts that are consumed by reporting, BI, or further analysis.

## What to test

- Business rule correctness
  - Confirm final values match the expected business logic.
  - Validate translated metrics, ratios, and KPI definitions.
  - Check that derived fields adhere to documented formulas.

- Consumer expectations
  - Verify dataset shape, column names, and data types match contracts.
  - Confirm published partitions, segments, or views are correct.
  - Track downstream expectations for freshness and completeness.

- Final quality checks
  - Validate aggregates, totals, and derived summaries.
  - Check for unexpected nulls, duplicates, or zero values.
  - Confirm expected cardinality and growth patterns.

- Data delivery and exports
  - Ensure exports, feeds, or published datasets are available.
  - Validate delivery targets, file formats, and destination schemas.
  - Confirm any retention, archival, or pruning behavior.

- Documentation and acceptance
  - Capture acceptance criteria for the final artifact.
  - Document intended consumers and usage context.
  - Track any disclaimers or known limitations.

## Why it matters

Final data product testing gives confidence that the output delivered to stakeholders is accurate, complete, and usable. It is the last gate before a dataset becomes operational.
