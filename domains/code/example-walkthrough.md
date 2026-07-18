# Example Walkthrough: Validating a Solo-Built App Before Sale

A fully worked example of the 7-phase engagement methodology from `process/testing-strategy.md`, run end to end by a solo builder preparing to sell an AI-assisted app. Use this as a template for your own pre-sale or pre-handoff validation.

## The scenario

**Dana** is a solo indie developer who built **SlotStack**, a small scheduling/booking API for service businesses (hair salons, tutors, dog groomers) to manage appointment slots and take deposits. SlotStack was built almost entirely through AI-assisted coding sessions -- roughly 40 sessions with an AI coding assistant over 10 weeks -- with no second developer, no code review, and no formal test plan. It's now functional, has a handful of paying pilot customers, and Dana wants to list it for sale on a micro-SaaS marketplace.

Stack: FastAPI backend (Python), Next.js frontend, Postgres via Supabase, Stripe for deposits, Twilio for SMS reminders, deployed on Railway (API) and Vercel (frontend), GitHub Actions for CI.

Because this is a solo operator with no separate reviewer, the guidance in `grid/raci-matrix.md`'s "Solo operator and small-team guidance" section applies throughout: Dana holds every RACI role, and Tier 1 checks are run in full regardless.

---

## Phase 1: Reconnaissance

Dana inventories the system against the attack surface map in `framework/README.md`:

| Zone | Asset |
|---|---|
| Input / API boundary | `POST /bookings`, `POST /bookings/confirm`, `GET /providers/{id}/slots` |
| Auth layer | Supabase-issued JWT, validated in FastAPI middleware |
| Business logic | Slot conflict resolution, deposit calculation |
| Data access layer | SQLAlchemy models over Postgres (Supabase) |
| External API calls | Stripe (deposits), Twilio (SMS reminders) |
| Build / CI pipeline | GitHub Actions: lint, unit tests, deploy to Railway/Vercel on merge to main |
| Deployment / runtime | Railway (API), Vercel (frontend), no staging environment |
| Dependency supply chain | 34 Python packages, 51 npm packages, several added on AI-assistant suggestion across sessions |

No prior test plan, no prior security review, no separate reviewer at any point. Existing coverage: GitHub Actions runs `pytest` and `eslint`, nothing else.

## Phase 2: Attack surface enumeration

Highest-risk zones identified: the dependency supply chain (accumulated over 40 unsupervised AI-assisted sessions with no dependency review), the business logic around payment confirmation (built early, revisited rarely), and the deployment zone (no documented runbook, no credential inventory -- a direct risk given the upcoming ownership transfer).

## Phase 3: Threat modeling

Dana maps each zone to test domains and scopes in 22 tests from `grid/test-grid.md`, deliberately weighting toward `dimensions/handoff-and-transfer.md` since the entire point of this engagement is a sale:

| # | Test ID | Tier | Why it's in scope |
|---|---|---|---|
| 1 | COR-001 | Tier 2 | Boundary handling on slot-time math (midnight/DST edge cases) |
| 2 | COR-002 | Tier 1 | Null safety on optional booking fields |
| 3 | COR-013 | Tier 1 | Deposit calculation matches the documented pricing rule |
| 4 | STY-003 | Tier 2 | Linter/formatter conformance (already in CI, re-verified) |
| 5 | STY-007 | Tier 3 | Dead code from abandoned features (an early "waitlist" feature) |
| 6 | SEC-001 | Tier 1 | Injection safety on the provider search endpoint |
| 7 | SEC-004 | Tier 1 | No secrets committed to the repo |
| 8 | SEC-007 | Tier 1 | Access control on booking-cancellation endpoint |
| 9 | SEC-009 | Tier 1 | XSS prevention on user-supplied provider bios |
| 10 | SEC-011 | Tier 1 | Dependency vulnerability scan (SCA) |
| 11 | **SEC-017** | **Tier 1** | **Placeholder/mock code reachability -- Handoff & Transfer priority** |
| 12 | **SEC-018** | **Tier 1** | **Dependency license compliance for commercial sale -- Handoff & Transfer priority** |
| 13 | ARC-001 | Tier 3 | Single-responsibility check on the booking service module |
| 14 | **ARC-014** | **Tier 2** | **Code provenance / non-infringement review -- Handoff & Transfer priority** |
| 15 | TST-001 | Tier 2 | Unit test presence on core booking logic |
| 16 | TST-004 | Tier 2 | Coverage threshold on changed/critical code |
| 17 | TST-006 | Tier 3 | Assertion strength spot-check |
| 18 | PERF-003 | Tier 2 | N+1 query check on the provider-slots listing endpoint |
| 19 | REL-002 | Tier 1 | Timeout enforcement on Stripe/Twilio calls |
| 20 | **REL-019** | **Tier 2** | **Handoff documentation sufficiency -- Handoff & Transfer priority** |
| 21 | **REL-020** | **Tier 1** | **Credential and access rotation at ownership transfer -- Handoff & Transfer priority** |
| 22 | **ADV-015** | **Tier 1** | **Hallucinated dependency detection -- Handoff & Transfer priority** |

12 Tier 1, 7 Tier 2, 3 Tier 3. Six of the twenty-two are the Handoff and Transfer IDs, scoped in as mandatory per `grid/raci-matrix.md`'s solo-operator guidance -- not optional extras.

## Phase 4: Test execution -- Run 1 (`20260710-140000-slotstack-presale`)

| Tier | Test | Status | Evidence |
|---|---|---|---|
| Tier 1 | COR-002 | PASS | |
| Tier 1 | COR-013 | PASS | |
| Tier 1 | SEC-001 | PASS | |
| Tier 1 | **SEC-004** | **FAIL** | A real (test-mode) Stripe key and a live Twilio auth token are hardcoded in `.env.example`, committed in session 6, never scrubbed |
| Tier 1 | SEC-007 | PASS | |
| Tier 1 | SEC-009 | PASS | |
| Tier 1 | SEC-011 | PASS | no critical/high CVEs in current dependency tree |
| Tier 1 | **SEC-017** | **FAIL** | `verify_payment_mock()` -- a stub from early prototyping that always returns `True` -- is still wired into `POST /bookings/confirm` instead of real Stripe webhook signature verification |
| Tier 1 | SEC-018 | PASS | all dependency licenses are MIT/BSD/Apache-2.0, zero copyleft |
| Tier 1 | REL-002 | PASS | |
| Tier 1 | **REL-020** | **FAIL** | No credential inventory exists; no rotation plan for Stripe, Twilio, Supabase, or Railway/Vercel deploy tokens at handoff |
| Tier 1 | **ADV-015** | **FAIL** | `pytest-async-retry-lib`, added to `requirements.txt` in session 14 on an AI-assistant suggestion, has a PyPI publish date three weeks *after* the commit that added it -- it did not exist when suggested and was registered by an unknown party later. It resolves and installs today |
| Tier 2 | COR-001 | PASS | |
| Tier 2 | STY-003 | PASS | |
| Tier 2 | ARC-014 | **WARN** | The rate-limiting middleware closely matches a blog post's sample code with no attribution; permissively licensed but unattributed |
| Tier 2 | TST-001 | PASS | |
| Tier 2 | **TST-004** | **FAIL** | Coverage on booking/payment logic is 71%, threshold is 80% |
| Tier 2 | PERF-003 | PASS | |
| Tier 2 | **REL-019** | **WARN** | README covers the API and frontend but omits the SMS-reminder worker, a separate always-on Railway service with its own env vars |
| Tier 3 | STY-007 | PASS | |
| Tier 3 | ARC-001 | PASS | |
| Tier 3 | TST-006 | PASS | |

## Phase 5: Severity scoring

Scored against the four-factor model in `framework/README.md`:

| Finding | Blast radius | Detectability | Code criticality | Recoverability | Total | Rating |
|---|---|---|---|---|---|---|
| SEC-017 (mock payment stub live) | 5 (any booking confirms without real payment) | 5 (silent -- no error, no alert, just unpaid bookings) | 5 (payment path) | 3 (a code fix + reconciling any affected bookings) | **18** | Critical |
| ADV-015 (hallucinated dependency) | 4 (whole app depends on it transitively) | 5 (silent supply-chain risk, invisible to normal testing) | 4 (build-time trust) | 2 (remove and replace, low effort once found) | **15** | High |
| SEC-004 (leaked credentials) | 3 (scoped to Stripe test mode + Twilio account) | 4 (not visible without a dedicated scan) | 4 (external-service compromise potential) | 2 (rotate, low effort) | **13** | High |
| REL-020 (no rotation plan) | 4 (every credential the buyer would need to trust) | 3 (a diligent buyer would ask; a casual one wouldn't) | 4 (full operational control) | 2 (build the runbook, low effort) | **13** | High |
| TST-004 (coverage gap) | 2 (payment/booking module only) | 2 (visible in any coverage report) | 3 (core revenue logic) | 1 (add tests) | **8** | Medium |
| ARC-014 (unattributed code) | 1 (one middleware file) | 3 (only visible on close review) | 2 (non-critical utility) | 1 (rewrite) | **7** | Medium |
| REL-019 (incomplete docs) | 2 (one undocumented service) | 2 (discovered on first deploy attempt) | 2 (operational, not security) | 1 (write the docs) | **7** | Medium |

Compound-failure note: SEC-017 and ADV-015 together are the most serious combined exposure -- an app that can confirm unpaid bookings *and* carries an unverified, recently-registered dependency is a buyer's worst combination to inherit silently.

## Phase 6: Findings report (summary)

- **Scope:** SlotStack backend, frontend, CI/CD, and dependency tree. Engagement date: 2026-07-10. Participant: Dana (sole).
- **Maturity level (pre-remediation):** Level 1/2 boundary per `framework/maturity-model.md` -- linter and unit tests in CI, but no security scanning, no coverage gate, no adversarial or handoff-specific testing prior to this engagement.
- **Coverage summary:** 22 of 124 catalog IDs executed; 15 passed, 4 failed, 2 warned, 1 failed at Tier 2 (TST-004).
- **Scored findings:** 2 Critical/High-adjacent Tier 1 blockers (SEC-017, ADV-015), 2 further High findings (SEC-004, REL-020), 3 Medium findings.
- **Residual risk if unaddressed:** a buyer inherits a payment path that never actually verifies payment, a dependency that could be swapped for malicious code by its current registrant at any time, and no ability to safely take over credentials -- any one of these would very likely surface in a buyer's own due diligence and could kill the deal or trigger a post-sale dispute.

## Phase 7: Remediation and retest

- **SEC-017**: replaced `verify_payment_mock()` with real Stripe webhook signature verification; added an integration test that exercises the actual webhook path with a signed test event.
- **ADV-015**: removed `pytest-async-retry-lib` (confirmed unused -- a leftover from an abandoned retry-logic experiment); added ADV-015's registry-age check as a permanent CI step.
- **SEC-004**: rotated the exposed Stripe test key and Twilio token; scrubbed `.env.example` down to placeholder values only; added a gitleaks pre-commit hook.
- **REL-020**: built a credential inventory (Stripe, Twilio, Supabase, Railway, Vercel) and a handoff rotation runbook; rotated everything rotatable now rather than waiting for the actual buyer handoff.
- **TST-004**: added tests for booking-conflict and deposit-calculation edge cases; coverage on the payment/booking module moved to 86%.
- **ARC-014**: rewrote the rate-limiting middleware from scratch instead of the blog-derived version.
- **REL-019**: added an SMS-worker deployment section to the README, including its separate env vars and Railway service name.
- **PERF-003**: on retest, found and flagged (not yet fixed) one N+1 query pattern in `GET /providers/{id}/slots` -- acceptable at current pilot-customer volume, logged as a monitored WARN rather than blocked, since fixing it isn't required to ship the sale safely.

### Run 2 (`20260712-093000-slotstack-presale`, post-remediation)

| Metric | Value |
|---|---|
| Total tests | 22 |
| Passed | 21 |
| Failed | 0 |
| Warnings | 1 (PERF-003, N+1 query, logged as tech debt for the buyer) |
| Tier 1 failures | 0 |
| Pass rate | 21 / 22 = **95.5%** |
| Overall score | (12×5 + 6×2 + 3×1 + 1×1) / (12×5 + 7×2 + 3×1) = 76 / 77 = **98.7%** |

**Gate status: `READY`.** Zero Tier 1 failures, pass rate above the 95% threshold. SlotStack is sale-ready: the payment-confirmation path is real, the dependency tree is verified, credentials are rotated and inventoried for clean handoff, and a buyer following only the README can stand the system up. The one remaining WARN (a known, low-volume N+1 query) is disclosed to the buyer as a documented, monitored item rather than hidden -- exactly the kind of item `dimensions/handoff-and-transfer.md` exists to surface deliberately instead of silently.

---

## What this example shows

- The full 7-phase engagement methodology run solo, with `grid/raci-matrix.md`'s solo-operator guidance applied throughout rather than skipped for lack of a second reviewer.
- The Handoff and Transfer dimension's six IDs treated as mandatory scope, not optional, for exactly the persona it was built for.
- Two real, characteristic AI-assisted-development findings -- a hallucinated dependency and a leftover mock payment stub -- scored, remediated, and retested rather than asserted as hypothetical.
- A `BLOCKED`-shaped Run 1 (4 Tier 1 failures) resolving to a genuine `READY` Run 2, with one disclosed, non-blocking WARN carried forward transparently into the sale rather than hidden.
