# Raw Data Testing

Raw data is the first test frontier. Failures here propagate downstream, so this dimension is about validating the source and ingestion layer.

## What to test

- Source inventory
  - Record every source system, file, table, stream, API, or external feed.
  - Capture source ownership, update cadence, and contract expectations.

- Schema contracts
  - Verify expected columns/fields are present.
  - Validate data types and allowable domains.
  - Detect schema drift or unannounced type changes.

- Completeness and record counts
  - Confirm row counts match source records when expected.
  - Validate presence of required fields.
  - Check for missing partitions or missing time windows.

- Data quality checks
  - Flag invalid values, malformed records, and corrupt payloads.
  - Detect unexpected nulls in required fields.
  - Validate IDs, timestamps, codes, and enumerations against known lists.

- Freshness and availability
  - Confirm the source arrived on schedule.
  - Detect late arrivals, missing batches, or stalled feeds.
  - Validate ingest timestamps and source delivery windows.

- Security and access
  - Verify source access permissions are correct.
  - Document any redaction, masking, or sensitivity requirements.

## Why it matters

Raw data testing prevents bad inputs from entering the pipeline. If raw sources are unreliable, downstream transformations and final outputs become impossible to trust.
