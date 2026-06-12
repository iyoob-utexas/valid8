# Quality and Completeness

Quality and completeness checks ensure data is present, valid, and usable.

## What to test

- Required field coverage
  - Verify required columns are not null where values are expected.
  - Check completeness for critical business dimensions.

- Row completeness
  - Confirm expected row counts for source loads or partitions.
  - Detect missing time windows, missing batches, or dropped records.

- Valid value checks
  - Flag malformed values, invalid formats, or disallowed content.
  - Validate business-specific rules such as valid status codes.

- Derived field sanity
  - Ensure computed fields produce expected results.
  - Verify derived totals, percentages, and category assignments.

## Why it matters

Incomplete or low-quality data undermines trust in analytics. These checks are essential to identify data gaps before they reach stakeholders.
