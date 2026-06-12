# Performance and Freshness

This category validates that data is delivered on time and that pipelines perform within acceptable limits.

## What to test

- Freshness
  - Verify the latest data is no older than expected.
  - Detect stale partitions or missing refresh cycles.
  - Confirm ingestion and processing windows complete within the expected schedule.

- Latency and timeliness
  - Track the time between source arrival and dataset availability.
  - Validate SLA compliance for delivery and refresh cadence.

- Pipeline performance
  - Monitor execution time and resource usage.
  - Detect regressions in processing duration or throughput.

- Data availability
  - Confirm final datasets and exports are accessible to consumers.
  - Validate that published artifacts are not empty or missing.

## Why it matters

Late or unavailable data causes stale analytics. These checks are critical for operational reliability and for building trust in data delivery.

---

## DPPF temporal test catalog

| ID | Name | What it verifies | Defends against | Standards | Lifecycle |
|---|---|---|---|---|---|
| TMP-001 | Freshness SLA compliance | The most recent data arrived before the agreed SLA deadline | Late arrivals, stalled pipelines, missed refresh cycles, upstream outage without alerting | Timeliness, Freshness, Traceability | CI, Production monitoring |
| TMP-002 | End-to-end latency measurement | The elapsed time from source event creation to dataset availability remains within the defined tolerance | Slow processing, downstream consumer receiving stale data while believing it fresh, hidden dependency bottleneck | Timeliness, Freshness | CI, Production monitoring |
| TMP-003 | Sequence ordering validation | Records that must be consumed in order arrive and are processed in the correct sequence | Out-of-order event application, replay producing incorrect state, ordering assumption violated by parallelism | Integrity, Traceability | CI, Production monitoring |
| TMP-004 | Late arrival handling | Records arriving after period close are correctly identified, quarantined, flagged, or re-routed to a late-arrival lane | Missed backfill, silent inclusion of late records in a closed period, delayed records corrupting published totals | Timeliness, Completeness | Production monitoring |
| TMP-005 | Time window completeness | Every expected time window contains a non-empty result with at least the minimum expected record count | Partial windows from incomplete batch, cut-off windows from early termination, missing partitions from dropped batches | Completeness, Accuracy | CI, Production monitoring |
| TMP-006 | Time continuity | Timestamp fields in a sequence follow the expected progression with no gaps or jumps beyond tolerance | Discontinuities from missed events, clock jumps from source system reset, time gaps from partial reprocessing | Consistency, Traceability | CI, Production monitoring |
| TMP-007 | Timezone normalization | All timestamp fields are stored in the agreed canonical timezone and not mixed across timezones within the same dataset | Mixed-timezone records producing incorrect period assignment, DST-naive handling creating hour gaps or duplicates | Consistency, Accuracy | Development, CI |
| TMP-008 | Event time vs processing time gap | The difference between an event's occurrence timestamp and its processing timestamp remains within the expected threshold | Large gaps indicating pipeline lag, gap widening as a sign of backlog accumulation, gap masking effective freshness | Timeliness, Freshness | CI, Production monitoring |
| TMP-009 | Watermark advancement correctness | The pipeline watermark advances to the correct position after each successful processing cycle | Stuck watermark blocking downstream processing, watermark advancing past unprocessed events, replay gaps from incorrect reset | Traceability, Integrity | CI, Production monitoring |
| TMP-010 | Future timestamp detection | No records carry a timestamp materially beyond the current processing time | Future-dated injection, clock skew at source producing far-future records, test records left in production | Validity, Accuracy | CI, Production monitoring |
| TMP-011 | DST transition handling | Processing windows that span a daylight saving time boundary produce correct record counts and time assignments | Missing hours, duplicate hours, incorrect period assignment for records at the DST boundary | Consistency, Accuracy | CI, Pre-deployment |
| TMP-012 | Clock skew detection | Source system timestamps do not deviate from the expected wall-clock time by more than the defined tolerance | Records from a skewed source clock misassigned to the wrong period, skew large enough to invert ordering | Accuracy, Consistency | CI, Production monitoring |
| TMP-013 | Backfill window coverage | A backfill operation fully covers the requested historical period without gaps and without overwriting records outside the target window | Incomplete backfill leaving gaps in history, backfill extending too far and corrupting adjacent periods | Completeness, Integrity | CI, Pre-deployment, Production monitoring |
| TMP-014 | Stale period reappearance detection | A previously closed and finalized period does not reappear or receive new records outside of a sanctioned restatement process | Stale snapshots reprocessed silently, replay reintroducing old data, watermark regression reopening closed windows | Traceability, Integrity | CI, Production monitoring |

---

## DPPF performance and scale test catalog

| ID | Name | What it verifies | Defends against | Standards | Lifecycle |
|---|---|---|---|---|---|
| PERF-001 | Throughput validation | The pipeline processes the full expected production data volume within the defined time window | Performance bottlenecks discovered only at production scale, dropped records from buffer exhaustion | Volume, Timeliness | Development, CI, Pre-deployment |
| PERF-002 | Scale degradation behavior | Processing time and error rates remain within acceptable bounds as data volume increases toward and beyond production levels | Superlinear degradation, cascading failures from resource starvation, silent record loss under load | Volume, Timeliness | Pre-deployment, Production monitoring |
| PERF-003 | Cost anomaly detection | Compute and storage resource consumption remains within expected bounds for the data volume being processed | Runaway cost from inefficient query plans, unbounded scans from missing partition pruning, unexpected data expansion | Volume, Traceability | Production monitoring |
| PERF-004 | Latency under load | End-to-end latency remains within defined thresholds when the pipeline is processing at or near peak volume | Latency spike at high load degrading consumer SLAs, load-dependent slowdowns not visible in unit testing | Timeliness, Volume | Pre-deployment, Production monitoring |
| PERF-005 | Resource contention | Shared compute or storage resources do not cause data degradation, record loss, or throughput collapse under concurrent access | Queueing delays under concurrent load, throttling-induced partial writes, lock contention corrupting output | Volume, Integrity | Pre-deployment, Production monitoring |
| PERF-006 | Throughput stability | The rate of records processed per unit time remains stable over the duration of a pipeline run with no progressive slowdown | Jitter from memory pressure, throughput collapse from accumulated state, progressive GC pressure | Volume, Consistency | Production monitoring |
| PERF-007 | Memory pressure behavior | The pipeline completes correctly and without data loss when operating near the memory resource limit | Out-of-memory errors causing partial output, memory-pressure spill corrupting intermediate state, silent record drop | Volume, Integrity | Pre-deployment |
| PERF-008 | Concurrent execution safety | Multiple simultaneous runs against the same output target do not corrupt data or produce non-deterministic results | Race conditions on shared output tables, double-write from concurrent backfill, non-idempotent merge under concurrency | Integrity, Consistency | CI, Pre-deployment |
| PERF-009 | Query plan stability | The execution plan for key transformations does not degrade to a full scan or cross-join when data volume changes or statistics are stale | Query plan regression after data growth, predicate pushdown lost after schema change, partition pruning disabled by stale stats | Volume, Timeliness | Pre-deployment, Production monitoring |
| PERF-010 | Partition pruning effectiveness | Queries that filter on partition keys correctly prune partitions and do not scan the full dataset | Missing pruning from incorrect filter predicate, pruning disabled by implicit type cast, full scan on partitioned table | Volume, Timeliness | Pre-deployment, Production monitoring |
| PERF-011 | Checkpoint and restore performance | Writing and restoring from pipeline checkpoints completes within the defined time window without latency spikes | Checkpoint overhead dominating processing time, restore exceeding the acceptable recovery window | Timeliness, Integrity | Pre-deployment |
| PERF-012 | Cold start performance | A pipeline starting from a cold state meets its SLA on first execution | Cold start time exceeding SLA for scheduled jobs, cold-start latency masking as pipeline failure in monitoring | Timeliness, Traceability | Pre-deployment, Production monitoring |
