# Performance and Scalability

Performance testing confirms the code behaves acceptably not just on a developer's laptop with a handful of rows, but at production scale, under concurrent load, and over the lifetime of a running process.

## What to test

- Algorithmic complexity
  - Big-O behavior of hot-path code, and regressions from a lower complexity class to a higher one.

- Database and I/O access patterns
  - N+1 query patterns, unbounded result sets, missing indexes implied by query shape.

- Memory behavior
  - Memory leaks, unbounded cache growth, unbounded in-memory collections.

- Blocking operations
  - Synchronous I/O or CPU-bound work on a thread that should remain non-blocking.

- Concurrency and contention
  - Lock contention, thread pool exhaustion, connection pool exhaustion under load.

- Caching correctness
  - Cache invalidation matches data mutation; stale cache reads are bounded and intentional.

## Why it matters

Performance defects are often invisible in development and expensive in production: a query that is fine at 100 rows can take the system down at 10 million, and a leak that is invisible in a short-lived test run can exhaust memory in a long-lived process.

---

## DPPF performance and scalability test catalog

| ID | Name | What it verifies | Defends against | Standards | Lifecycle |
|---|---|---|---|---|---|
| PERF-001 | Algorithmic complexity bound | Hot-path functions have a documented and verified Big-O complexity appropriate to their expected input size | Quadratic or worse algorithms on large collections, complexity regressions introduced by a refactor | ISO/IEC 25010 Performance efficiency | Review, CI |
| PERF-002 | Complexity regression detection | A code change does not silently move a hot path from a lower complexity class to a higher one | Performance cliffs discovered only in production at scale, gradual degradation across many small changes | ISO/IEC 25010 Performance efficiency | Review, CI |
| PERF-003 | N+1 query prevention | Database access in a loop is batched, joined, or eager-loaded rather than issuing one query per iteration | N+1 query explosion under realistic data volume, database load spikes from a single request | ISO/IEC 25010 Performance efficiency | Review, CI |
| PERF-004 | Unbounded result set prevention | Queries and API calls that can return large result sets are paginated or explicitly bounded | Out-of-memory failures from unbounded fetches, slow responses from unnecessarily large payloads | ISO/IEC 25010 Performance efficiency | Review, CI |
| PERF-005 | Memory leak absence | Long-running processes do not accumulate unreleased memory across repeated operations, both in a bounded pre-deployment load test and as a tracked RAM trend over days or weeks in production | Gradual memory growth leading to crash or forced restart, degraded performance over process lifetime, a slow leak too gradual for a short load test to catch but visible in a long-term production trend | ISO/IEC 25010 Reliability, CWE-401 | CI, Pre-deployment, Production |
| PERF-006 | Unbounded cache and collection growth prevention | In-memory caches and collections have an eviction policy or explicit size bound | Unbounded cache growth exhausting memory, stale entries accumulating indefinitely | ISO/IEC 25010 Performance efficiency | Review, CI |
| PERF-007 | Blocking I/O in async context prevention | Code running in an event loop or async context does not perform blocking synchronous I/O or CPU-bound work on the same thread | Event loop starvation, request latency spikes from one slow blocking call, thread pool exhaustion | ISO/IEC 25010 Performance efficiency | Review, CI |
| PERF-008 | Lock contention bound | Critical sections are minimized in scope and duration; locks are not held across I/O or long-running operations | Throughput collapse under concurrent load, deadlocks from lock ordering violations | ISO/IEC 25010 Performance efficiency, CWE-667 | Review, CI |
| PERF-009 | Connection and resource pool sizing | Database connection pools, thread pools, and other bounded resource pools are sized appropriately and exhaustion is handled gracefully | Connection pool exhaustion cascading into total outage, silent request queuing with no timeout | ISO/IEC 25010 Performance efficiency, Reliability | Review, Production |
| PERF-010 | Cache invalidation correctness | Cache entries are invalidated or refreshed whenever the underlying data they represent changes | Stale cache reads serving incorrect data, cache-and-source divergence under concurrent writes | ISO/IEC 25010 Performance efficiency | Review, CI |
| PERF-011 | Load test threshold compliance | The system meets its defined latency and throughput targets under a load test at expected production volume | Performance regressions undetected until real production traffic, latency SLA breaches under peak load | ISO/IEC 25010 Performance efficiency, k6/JMeter class tooling | Pre-deployment |
| PERF-012 | Cold start and warm-up performance | Process startup, connection establishment, and cache warm-up complete within the time budget required by the deployment platform | Failed health checks during rolling deploys, request timeouts during autoscaling events | ISO/IEC 25010 Performance efficiency | Pre-deployment, Production |
