# Adversarial Testing

Adversarial tests validate that the pipeline survives conditions it was not designed to expect. Where standard tests confirm correct behavior on normal input, adversarial tests deliberately introduce fault, malice, and edge-case data to verify that the pipeline detects, rejects, or recovers gracefully from each condition.

The adversarial standard treats every external input as a potential attack vector and every upstream dependency as a potential failure source.

## What to test

- Fault injection
  - Simulate connector failures, storage outages, and network interruptions during active processing.
  - Verify the pipeline halts cleanly or degrades gracefully rather than producing corrupt output.

- Bad data injection
  - Inject records with malformed values, adversarial payloads, extreme values, and unexpected types.
  - Confirm detection, quarantine, or rejection before the values propagate downstream.

- Schema mutation
  - Introduce unauthorized schema changes: add columns, remove columns, rename fields, change types.
  - Verify that contract enforcement catches the mutation and blocks or flags the affected load.

- Chaos and dependency failure
  - Kill orchestration dependencies mid-run or inject delays that violate the dependency order.
  - Confirm the pipeline fails safely, alerts correctly, and does not produce silent partial output.

- Replay and duplication
  - Replay a previous run or flood the input with duplicate records.
  - Verify idempotency and deduplication logic prevent corrupted output.

- Encoding, size, and format attacks
  - Inject oversized records, malformed encoding, special characters, and lookalike characters.
  - Confirm the pipeline handles each case without silent data loss or state corruption.

## Why it matters

Every pipeline eventually encounters data it did not expect. The question is whether the failure is visible and contained or silent and compounding. Adversarial tests answer that question before production does.

---

## DPPF adversarial test catalog

| ID | Name | What it verifies | Defends against | Standards | Lifecycle |
|---|---|---|---|---|---|
| ADV-001 | Fault injection | The pipeline handles a simulated connector failure, storage outage, or network interruption without producing corrupt or partial output | Cascading failures from a single dependency, corrupt output written before failure is detected, missing alerts when infrastructure fails | Integrity, Traceability | Development, CI, Pre-deployment |
| ADV-002 | Bad data injection | Malformed, adversarial, or structurally invalid records are detected and quarantined before they reach transformation or serving | Poisoned input propagating to output, malformed values crashing downstream consumers, quarantine bypass from insufficient validation | Validity, Accuracy | CI, Production monitoring |
| ADV-003 | Schema mutation attack | Unauthorized schema changes (added columns, removed columns, renamed fields, changed types) are detected and blocked or flagged | Hidden schema shift breaking downstream code, contract breach undetected until a consumer fails, type change causing silent numeric corruption | Schema, Traceability, Validity | CI, Pre-deployment, Production monitoring |
| ADV-004 | Duplicate flood | A flood of duplicate records does not produce incorrect aggregations, inflated counts, or corruption in downstream outputs | Retry storms producing double-writes, upstream system resending an entire batch, merge logic failing under high-duplicate load | Uniqueness, Integrity | CI, Production monitoring |
| ADV-005 | Dependency kill simulation | When a dependency is killed mid-run, the pipeline either fails safely with a clear alert or completes the available portions with degraded-state flags | Silent execution against stale or missing upstream data, downstream running without required inputs, cascading job failures without notification | Traceability, Integrity | CI, Pre-deployment |
| ADV-006 | Lineage tampering check | Lineage metadata is consistent, complete, and matches the expected provenance chain with no unauthorized modifications | Tampered lineage masking a data source change, missing lineage nodes creating audit gaps, lineage records altered after the fact | Lineage, Traceability | Production monitoring |
| ADV-007 | Volume spike injection | A sudden order-of-magnitude increase in input volume does not cause record loss, incorrect output, or silent truncation | Buffer overflow dropping records, unbounded processing exhausting memory, output partition receiving a partial write under load | Completeness, Volume | CI, Pre-deployment |
| ADV-008 | Null flood injection | A batch with a high proportion of nulls in normally populated fields does not corrupt aggregations or bypass null-check gates | Null flood suppressing alerts, aggregation collapsing to incorrect totals from mass null, null propagating through joins to produce spurious matches | Completeness, Validity | CI, Production monitoring |
| ADV-009 | Special character injection | Records with control characters, SQL metacharacters, script tags, and format-breaking strings are handled without data corruption, code injection, or silent truncation | Injection through data values corrupting downstream SQL, control characters breaking delimited file parsing, script tags reaching a report layer | Validity, Integrity | CI, Pre-deployment |
| ADV-010 | Encoding attack | Records carrying malformed byte sequences, mixed encodings, or overlong UTF-8 sequences are detected and handled without crashing the pipeline or corrupting output | Malformed encoding crashing a string function, encoding inflation exceeding field length limits, mixed-encoding records serving corrupt values | Validity, Integrity | CI, Pre-deployment |
| ADV-011 | Future date injection | Records with timestamps materially beyond the current processing time are detected and not assigned to a period without explicit authorization | Future-dated records appearing in current-period aggregations, watermark advancing past legitimate events, test records left in production | Validity, Accuracy | CI, Production monitoring |
| ADV-012 | Negative value injection | Negative numeric values in non-negative fields are detected and quarantined before they affect aggregations or metrics | Negative amounts inverting totals, unsigned fields underflowing, negative quantity corrupting inventory or balance calculations | Validity, Accuracy | CI, Production monitoring |
| ADV-013 | Oversized record injection | Records with fields at or beyond the maximum defined length or byte size are handled without silent truncation, pipeline crash, or storage corruption | Field truncation producing incorrect values, oversized payload crashing a downstream parser, storage layer silently clipping values | Validity, Completeness | CI, Pre-deployment |
| ADV-014 | Replay attack simulation | Replaying a previously processed batch does not produce duplicate records, incorrect state, or corrupted aggregations | Replay from a failed run producing double-counts, orchestrator resubmitting a completed batch, consumer re-reading an already-processed event stream | Uniqueness, Integrity | CI, Pre-deployment |
| ADV-015 | Homoglyph and lookalike injection | Records containing visually similar but distinct characters (Cyrillic lookalikes, Unicode confusables) are detected and normalized or flagged | Homoglyph injection creating duplicate entity records that bypass deduplication, lookalike codes evading mapping table checks, confusable characters producing incorrect joins | Validity, Uniqueness | CI, Pre-deployment |
