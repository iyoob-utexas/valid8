# Test Cycle Runbook

This page documents the runbook for a code validation cycle, from pre-commit through post-deploy monitoring. This is a per-change execution runbook, not the same as the six SDLC-phase dimensions in `domains/code/dimensions/` -- this runbook's six stages cover a single change moving through Coding, Integration and Testing, and Deployment; the dimensions folder additionally covers Planning and Requirements, Design and Architecture, and the ongoing Operations and Maintenance dimension that outlives any single change.

## Start here

Before the cycle begins, know these inputs:

- the repository, service, or PR in scope
- the acceptance criteria or specification the change implements
- the branch or release candidate in scope
- the success criteria for the merge and, separately, for the release
- whether the change touches a security-sensitive surface (auth, payments, PII, an externally-exposed API) -- this determines whether Security and Adversarial domain checks are mandatory rather than advisory
- whether the change is a hotfix (may compress the cycle) or a standard change (runs the full cycle)

## Six stages

1. Pre-commit
   - Run the formatter, linter, and fast unit tests locally before pushing.
   - Confirm no secrets are staged for commit.
   - Pass when the linter, formatter, and local unit test suite are clean.

2. PR review
   - A human reviewer checks correctness, structure and style, and architecture against the change's stated intent.
   - Confirm the PR includes tests for new logic and for any bug it fixes.
   - For security-sensitive changes, a security champion reviews access control, input handling, and secrets.
   - Pass when the reviewer approves and all reviewer-raised Tier 1 and Tier 2 findings are resolved.

3. CI
   - Run the full automated suite: unit, integration, linting, SAST, dependency scan, coverage threshold, and (on a cadence) mutation testing.
   - Pass when every Tier 1 check passes and the branch protection gate allows merge.

4. Pre-merge gate
   - Confirm CI is green, required reviews are approved, and no Tier 1 finding is open.
   - Confirm the PR title and commits follow the project's Conventional Commits and SemVer-impact conventions if the change touches a public API.
   - Pass when all pre-merge gate conditions are satisfied and the merge is authorized.

5. Pre-deployment
   - Run end-to-end tests, load tests, and adversarial checks (fuzzing, dependency tampering simulation) against a release candidate in a non-production environment.
   - Confirm the deployment plan includes a rollback path and a canary or staged rollout where applicable.
   - Pass when all Tier 1 pre-deployment checks pass and the release is authorized.

6. Post-deploy monitoring
   - Confirm health checks pass, error rates and latency are within expected bounds, and alerting is active for the new code path.
   - Run a short observation window before declaring the release stable; roll back if Tier 1 reliability signals degrade.
   - Pass when the observation window closes with no Tier 1 regression and the release is marked stable.

## Failure behavior

- Red / Tier 1: stop. Block the merge or block the release and fix the issue before moving forward.
- Amber / Tier 2: FAIL blocks release but not merge, pending fix; WARN logs the concern and the PR proceeds under review.
- Green / Tier 3: log and monitor. Continue, but escalate if the issue recurs or trends worse.

## Abort policy

If Stage 1 (Pre-commit) or Stage 3 (CI) produces a Tier 1 failure, running Stages 4 through 6 on the same change will generate misleading results -- downstream checks will fail for reasons caused by the upstream defect, not independently. Apply the following policy:

- If Stage 3 (CI) fails on a Tier 1 check: record Stages 4 through 6 as `SKIPPED` and reference the CI failure. Fix the defect and re-run CI before proceeding.
- If Stage 5 (Pre-deployment) produces a Tier 1 failure: record Stage 6 as `SKIPPED` with a reference to the Stage 5 failure. Do not deploy; fix and re-run from Stage 4 after the issue is resolved.
- A `SKIPPED` result does not count as a pass or fail in the pass rate calculation and does not affect `overall_score`. Document the skip reason in the run log.

## Remediations

When a check fails, do not just record the failure -- suggest a remediation before closing the run. A remediation note should answer three things: what broke, why it likely broke, and what action resolves it.

Common remediation patterns by failure type:

| Failure type | Likely cause | Suggested action |
|---|---|---|
| Null/undefined dereference | Missing null check on an optional field or API response | Add explicit null check or use a language null-safety feature; add a regression test |
| Boundary/edge-case test failure | Off-by-one error, unhandled empty input | Trace the failing boundary; fix the loop/range logic; add the missing edge-case test |
| Linter or formatter failure | New code not run through the pre-commit hook | Run the formatter and linter locally; add or fix the pre-commit hook |
| Cyclomatic complexity over threshold | Function accumulated too many branches over time | Extract sub-functions; consider a strategy or lookup-table pattern |
| Injection finding (SAST) | User input concatenated into a query, command, or template | Parameterize the query; use a safe templating API; add a regression test with the payload that triggered the finding |
| Secret detected in commit | Credential hardcoded during local development and not removed before commit | Revoke and rotate the exposed credential; remove from history; move to a secrets manager |
| Dependency vulnerability (critical/high) | Outdated or unpatched package | Upgrade to a patched version; if no patch exists, evaluate a replacement or apply a compensating control |
| Architecture / SOLID violation flagged in review | Responsibility crept into an existing class over multiple PRs | Extract the new responsibility into its own module; add an interface at the seam |
| Coverage threshold miss | New logic merged without a corresponding test | Add tests for the uncovered branches; do not lower the threshold to pass |
| Mutation testing score below target | Tests assert loosely (e.g., not-null checks only) | Strengthen assertions to check specific expected values, not just execution |
| Flaky test | Shared state, timing dependency, or unmocked wall-clock/network call | Isolate test state; mock time and network; rerun 10x to confirm the fix |
| N+1 query finding | Loop issuing one query per iteration instead of a batched query | Batch or eager-load the query; add a query-count assertion to the integration test |
| Memory leak in load test | Unbounded cache, unclosed listener, or retained reference | Add an eviction policy or explicit cleanup on the retained resource; re-run the load test to confirm |
| Missing timeout on external call | Call added without considering the caller's own SLA budget | Add an explicit timeout shorter than the caller's SLA; add a test simulating a hung dependency |
| Failed rollback drill | Rollback path never exercised, or requires a manual step | Automate the rollback path; add a rollback drill to the pre-deployment checklist |
| Fuzzing crash | Parser or entry point does not validate input shape before processing | Add input validation at the boundary; add the crashing input as a permanent regression test case |
| Dependency tampering / hash mismatch | Lockfile not enforced, or a dependency was manually edited | Regenerate the lockfile from a trusted source; enforce hash verification in CI |

Record the remediation taken alongside the failure result so the run history shows both the problem and its resolution.

## Recommended practice

- Record every result for every stage.
- Use a dashboard or run-history table for trend analysis.
- Keep the runbook aligned with the companion grid and the framework standard.
