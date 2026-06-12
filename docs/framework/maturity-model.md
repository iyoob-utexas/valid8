# Testing Maturity Model

This model defines four levels of testing maturity for data pipelines. Each level describes the test domains covered, the degree of automation, and the overall posture of the team toward data reliability.

Use this model to assess where a pipeline or team currently sits, and to set a target level for a given engagement or roadmap cycle. For a coverage self-assessment, use `docs/framework/dppf.md`.

---

## The four levels

| Level | Name | Gate model | Automation | Adversarial readiness |
|---|---|---|---|---|
| 1 | Reactive | Informal or none | Manual, incident-driven | None |
| 2 | Defined | Documented tiers with explicit thresholds | Partial CI automation | Minimal |
| 3 | Automated | Full CI plus production monitoring | Comprehensive automation | Partial |
| 4 | Adversarial | Severity-scored, chaos-tested, self-assessed | End-to-end including fault injection | Full |

---

## Level 1: Reactive

The team runs checks only after incidents expose a problem. There is no proactive test strategy and no shared vocabulary for what "good" means. Tests exist as ad-hoc scripts or manual inspection steps that are not consistently applied or documented.

**What is covered:**
- Structural: ad-hoc column checks, if anything
- Semantic: manual review of outputs after a complaint
- Statistical: not covered
- Temporal: not covered except informally
- Operational: not covered
- Adversarial: not covered
- Performance and scale: not covered

**Characteristics:**
- Tests are triggered by failure, not planned before it
- No standardized test IDs or outcome vocabulary
- No gate model; failures produce ad-hoc responses
- No dashboard or results history

**How to advance to Level 2:** document the test cases that already exist, assign explicit thresholds, and add them to a CI step that runs on every load.

---

## Level 2: Defined

The team has documented test cases with explicit thresholds and owners. Structural and semantic checks run in CI. The Tier model is in use and stakeholders know what each tier means. Some anomaly detection is in place. Schema contracts exist even if not formally versioned.

**What is covered:**
- Structural: full (STR-001 through STR-015 addressed)
- Semantic: full (SEM-001 through SEM-015 addressed)
- Statistical: partial (volume shape and basic outlier detection)
- Temporal: full (freshness and latency SLAs defined and checked)
- Operational: partial (idempotency and retries tested; backfill and checkpoints informal)
- Adversarial: minimal (schema mutation detection only)
- Performance and scale: partial (throughput validated at development scale, not production)

**Characteristics:**
- DPPF IDs in use as a common reference language
- Tier 1 failures block the pipeline; Tier 2 triggers investigation
- Test results logged but not always trended
- No chaos testing; fault injection not practiced

**How to advance to Level 3:** automate all Tier 1 and Tier 2 checks in CI and production monitoring, implement statistical drift detection on key metrics, and establish a dead letter queue with observability.

---

## Level 3: Automated

The team has comprehensive CI automation across all eight test domains except full adversarial chaos. Statistical monitoring and anomaly detection run in production. The dead letter queue is active. Lineage is captured. The test grid is maintained and regularly reviewed.

**What is covered:**
- Structural: full
- Semantic: full
- Statistical: full (all STAT-001 through STAT-015)
- Temporal: full (all TMP-001 through TMP-014)
- Operational: full (all OPS-001 through OPS-015)
- Adversarial: partial (bad data injection and schema mutation; chaos and replay not yet systematic)
- Performance and scale: full (all PERF-001 through PERF-012 at production scale)

**Characteristics:**
- DPPF coverage self-assessment completed at least once
- Severity scoring used to prioritize gaps
- Maturity model reviewed at each engagement kickoff
- Fault injection practiced in pre-deployment environments
- SLA alerting active with defined ownership

**How to advance to Level 4:** implement all adversarial domain tests including chaos, replay attack, encoding and homoglyph injection, and dependency kill simulation; run DPPF coverage reviews on a scheduled cycle; apply severity scoring to every known gap.

---

## Level 4: Adversarial

The team operates the full DPPF test catalog across all eight domains. Chaos testing and fault injection are regular practices in CI and pre-deployment environments. The DPPF coverage checklist is used as a periodic self-assessment. Severity scoring is applied to every uncovered test and findings drive the remediation backlog.

**What is covered:**
- Structural: full
- Semantic: full
- Statistical: full
- Temporal: full
- Operational: full
- Adversarial: full (all ADV-001 through ADV-015)
- Performance and scale: full

**Characteristics:**
- Coverage review completed on a scheduled cycle using `docs/framework/dppf.md`
- Every gap scored with the DPPF severity model from `docs/framework/README.md`
- Findings report produced and remediation backlog maintained
- Adversarial tests run in pre-deployment and selected in production
- Maturity level is formally reviewed per engagement or per quarter

---

## Domain coverage matrix

| Domain | Level 1 | Level 2 | Level 3 | Level 4 |
|---|---|---|---|---|
| Structural | Partial | Full | Full | Full |
| Semantic | Partial | Full | Full | Full |
| Statistical | Minimal | Partial | Full | Full |
| Temporal | Minimal | Full | Full | Full |
| Operational | Minimal | Partial | Full | Full |
| Adversarial | None | Minimal | Partial | Full |
| Performance and scale | Minimal | Partial | Full | Full |

---

## Using the maturity model in an engagement

1. At kickoff, use the attack surface map in `docs/framework/README.md` to identify which pipeline zones are in scope.
2. Complete the coverage self-assessment in `docs/framework/dppf.md` to identify which DPPF test categories are currently covered.
3. Map the results to the domain coverage matrix above to determine the current maturity level.
4. Set a target maturity level for the engagement and identify the specific test IDs needed to close the gap.
5. Score any uncovered gaps using the DPPF severity model and prioritize remediation accordingly.
6. Re-run the self-assessment at the close of the engagement to confirm advancement.
