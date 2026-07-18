# Reliability and Operability

This domain validates how the code behaves when something around it fails: a dependency times out, a deploy goes wrong, a config value is missing. Correctness under normal conditions is necessary but not sufficient -- production is where dependencies fail, and reliability testing is what determines whether that failure stays contained.

## What to test

- Error handling completeness
  - Every external call has defined behavior for failure, timeout, and partial response.

- Observability
  - Logs, metrics, and traces provide enough signal to diagnose an incident without reading source code live.

- Retries and backoff
  - Retries use backoff and jitter; retries are safe to repeat (idempotent) where they touch state.

- Idempotency
  - Operations that may be retried or replayed produce the same end state, not duplicated side effects.

- Graceful degradation
  - When a non-critical dependency fails, the system degrades a feature rather than failing the whole request.

- Timeouts and circuit breakers
  - Every external call has a timeout; repeated failures trip a circuit breaker instead of cascading.

- Deployment safety
  - Rollout is incremental and reversible; rollback is fast and does not require a code change.

- Configuration management
  - Configuration is externalized, validated at startup, and does not silently default to an unsafe value.

- Deployment-time validation
  - Staging and production stay in parity; database migrations are tested for forward and rollback safety before touching production data.

- Production monitoring depth
  - Synthetic transactions and real-user monitoring (RUM) run continuously in production, in addition to liveness/readiness health checks and server-side metrics.
  - Live feature-variation (A/B) experiments have a defined success metric and a kill switch.

- Ownership transfer readiness
  - A new owner with no prior access can stand the system up from documentation alone.
  - Every credential the prior owner could access is rotated or revoked at handoff, with zero shared secrets surviving the transfer.

## Why it matters

Most production incidents are not caused by a logic bug -- they are caused by a dependency behaving unexpectedly and the calling code having no defined behavior for that case. Reliability testing is what turns "the database was slow for ten seconds" from a full outage into a blip nobody notices.

---

## DPPF reliability and operability test catalog

| ID | Name | What it verifies | Defends against | Standards | Lifecycle |
|---|---|---|---|---|---|
| REL-001 | External call error handling | Every call to an external service, database, or dependency has explicit handling for failure, timeout, and unexpected response shape | Unhandled exceptions crashing the request, silent failures returning incorrect defaults | ISO/IEC 25010 Reliability | Review, CI |
| REL-002 | Timeout enforcement | Every network call and external dependency invocation has an explicit timeout shorter than the caller's own SLA budget | Hung requests exhausting thread or connection pools, cascading latency from one slow dependency | ISO/IEC 25010 Reliability | Review, CI |
| REL-003 | Retry and backoff correctness | Retried operations use exponential backoff with jitter and a bounded maximum retry count | Retry storms amplifying an outage, thundering herd against a recovering dependency | ISO/IEC 25010 Reliability | Review, CI |
| REL-004 | Idempotency of retryable operations | Operations that may be retried or replayed (payment, write, message processing) produce the same end state without duplicating side effects | Duplicate charges or writes from a retried request, double-processing of a replayed message | ISO/IEC 25010 Reliability | Review, CI |
| REL-005 | Circuit breaker behavior | Repeated failures against a dependency trip a circuit breaker that fails fast instead of continuing to call a known-broken dependency | Cascading failure across services, resource exhaustion from repeated calls to a down dependency | ISO/IEC 25010 Reliability | Review, Production |
| REL-006 | Graceful degradation | When a non-critical dependency is unavailable, the system serves a degraded response (cached data, reduced feature set) instead of failing the entire request | Total outage caused by a non-critical dependency, unnecessary blast radius from a minor failure | ISO/IEC 25010 Reliability | Review, Production |
| REL-007 | Structured logging sufficiency | Logs include structured, correlatable context (request ID, user context where appropriate, error detail) sufficient to diagnose an incident without redeploying with extra logging | Incidents that cannot be root-caused from existing logs, mean-time-to-resolution inflated by missing context | ISO/IEC 25010 Reliability, Maintainability | Review, Production |
| REL-008 | Metrics and alerting coverage | Key operations emit metrics (latency, error rate, saturation) and alerting thresholds exist for the metrics that matter | Silent degradation with no alert until a user complains, missing signal for on-call to act on | ISO/IEC 25010 Reliability | Review, Production |
| REL-009 | Safe deployment and rollback | Deployments roll out incrementally (canary or staged) and can be rolled back quickly without requiring a new code change | Full-fleet bad deploys with no fast recovery path, rollback requiring an emergency hotfix under pressure | Google engineering practices, ISO/IEC 25010 Reliability | Pre-deployment, Production |
| REL-010 | Configuration validation at startup | Required configuration values are validated at process startup and the process fails fast with a clear error rather than starting in a partially-configured state | Silent misconfiguration causing incorrect behavior discovered hours later, unsafe default values masking a missing config | ISO/IEC 25010 Reliability | Pre-deployment, Production |
| REL-011 | Feature flag safety | Feature flags default to the safe/off state, are independently toggleable, and do not leave dead code paths permanently branching on a flag that will never change | Incomplete rollback when a flag cannot be safely disabled, flag debt accumulating untested code paths | ISO/IEC 25010 Reliability, Maintainability | Review, Production |
| REL-012 | Health check accuracy | Liveness and readiness health checks accurately reflect whether the process can serve traffic, including checking critical dependency reachability | Traffic routed to an unhealthy instance, a hung process passing a shallow health check | ISO/IEC 25010 Reliability | Pre-deployment, Production |
| REL-013 | Partial failure containment | A failure in one request, one shard, or one tenant does not affect unrelated requests, shards, or tenants sharing the same process | Noisy-neighbor outages, one bad tenant degrading the whole platform | ISO/IEC 25010 Reliability | Review, Production |
| REL-014 | Environment parity validation | Staging (or pre-production) configuration, dependency versions, and infrastructure topology match production closely enough that a passing staging test is predictive of production behavior | "Works in staging, breaks in production" failures caused by silent environment drift, config or version mismatch masking a defect until release | ISO/IEC 25010 Reliability, Portability | Deployment |
| REL-015 | Database migration validation | Schema migrations are tested for forward application, rollback, and backward compatibility with the currently-deployed application version before running against production data | Data loss or corruption from a failed migration, downtime from a migration that locks a production table, a migration that breaks the still-running previous application version during a rolling deploy | ISO/IEC 25010 Reliability | Pre-deployment, Deployment |
| REL-016 | Real-user monitoring (RUM) coverage | Client-side telemetry captures real user page load time, JavaScript error rate, and crash rate in production, distinct from server-side metrics (REL-008) | Client-side degradation invisible to server-side monitoring, regressions that only manifest in specific real-world browsers, networks, or devices | ISO/IEC 25010 Reliability, Usability | Production |
| REL-017 | Synthetic monitoring coverage | Scripted transactions simulating real user journeys run continuously against production on a schedule, independent of and in addition to liveness/readiness health checks (REL-012) | Silent degradation of a critical path that a shallow health check would not catch, outages first discovered by a real user instead of monitoring | ISO/IEC 25010 Reliability | Production |
| REL-018 | A/B test experiment integrity | Live feature-variation experiments have a defined success metric, statistically valid sample size and duration, and a kill switch, independent of feature-flag default-safety (REL-011) | Decisions made on underpowered or contaminated experiment data, a losing variant left running past its intended test window | ISO/IEC 25010 Reliability | Production |
| REL-019 | Handoff documentation sufficiency | A new owner with no prior access to the original author can provision, run, and deploy the system to a working state using only the repository's own documentation | Tribal knowledge that only exists in the original builder's head, a buyer or new team unable to stand up the system after transfer, a sale or handoff that stalls on undocumented setup steps | ISO/IEC 25010 Maintainability | Review, Deployment |
| REL-020 | Credential and access rotation at ownership transfer | 100% of credentials, API keys, and admin access created by the prior owner are rotated or revoked at handoff; zero shared secrets between seller and buyer post-transfer | A former owner retaining silent access to a system they no longer own, a leaked or reused credential from before the transfer compromising the new owner's environment | OWASP A07:2021 Identification and Authentication Failures, CWE-798 | Deployment |
