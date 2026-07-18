# Operations and Maintenance: Code Running in Production

This dimension validates the code once it is deployed and serving real traffic, and for as long afterward as it keeps running. Correctness at review time does not guarantee correctness under production conditions: real data shapes, real concurrency, real dependency failures, real attackers, and -- over weeks and months -- gradual resource drift that no pre-deployment test window is long enough to catch.

## What to test

- Deployment safety
  - Confirm the rollout is incremental (canary or staged) and that a rollback path exists and has been exercised (see `dimensions/deployment.md`).
  - Confirm configuration was validated at startup and the process failed fast on any missing required value.

- Health checks and synthetic monitoring
  - Confirm health checks accurately reflect the ability to serve traffic, including dependency reachability.
  - Confirm scripted synthetic transactions simulating real user journeys run continuously against production, independent of health checks, and alert on failure.

- Real-user monitoring (RUM)
  - Confirm client-side telemetry tracks real user page load time, JavaScript error rate, and crash rate, distinct from server-side metrics -- a slow client-side regression on one browser can be invisible to server-side monitoring entirely.

- Reliability under real failure
  - Confirm timeouts, retries, and circuit breakers behave as designed when a dependency actually degrades.
  - Confirm graceful degradation triggers correctly rather than cascading into a full outage.

- Long-term resource trend monitoring
  - Confirm memory usage is tracked as a trend over days or weeks in production, not just checked once in a pre-deployment load test -- a slow leak can be invisible to a short test window and only visible in a long-term trend (PERF-005 in `tests/performance-and-scalability.md` covers both).

- Observability
  - Confirm logs, metrics, and traces provide enough signal to diagnose an incident without a code change.
  - Confirm alerting fires on Tier 1 signal degradation, not just on a hard crash.

- Security posture in production
  - Confirm dependency scanning continues on a cadence, not just at release time.
  - Confirm access control and rate limiting behave as intended against real traffic patterns.
  - Monitor for adversarial traffic patterns: repeated auth failures, unusual request shapes, replayed tokens.

- A/B testing of live feature variations
  - Confirm every live experiment has a defined success metric, a minimum sample size and duration, and a kill switch, separate from ordinary feature-flag default-safety.

- Post-incident learning
  - When a production defect surfaces, trace it back to which lifecycle stage should have caught it and close that gap in the catalog or the grid.

## Test IDs that apply here

| ID | Name | Catalog |
|---|---|---|
| REL-005 | Circuit breaker behavior | `tests/reliability-and-operability.md` |
| REL-006 | Graceful degradation | `tests/reliability-and-operability.md` |
| REL-007 | Structured logging sufficiency | `tests/reliability-and-operability.md` |
| REL-008 | Metrics and alerting coverage | `tests/reliability-and-operability.md` |
| REL-012 | Health check accuracy | `tests/reliability-and-operability.md` |
| REL-013 | Partial failure containment | `tests/reliability-and-operability.md` |
| REL-016 | Real-user monitoring (RUM) coverage | `tests/reliability-and-operability.md` |
| REL-017 | Synthetic monitoring coverage | `tests/reliability-and-operability.md` |
| REL-018 | A/B test experiment integrity | `tests/reliability-and-operability.md` |
| PERF-005 | Memory leak absence (including long-term production trend) | `tests/performance-and-scalability.md` |
| SEC-011 | Dependency vulnerability scan (SCA) | `tests/security.md` |
| SEC-016 | Dynamic application security testing (DAST) coverage | `tests/security.md` |

## Why it matters

Production is where every assumption made during earlier stages gets tested against reality, and where some defects -- a slow memory leak, a client-side-only regression, a losing A/B variant nobody turned off -- only become visible with enough elapsed time. This dimension exists to keep that testing deliberate -- monitored, alerted, and fed back into the earlier stages -- rather than something the team only discovers through an incident.
