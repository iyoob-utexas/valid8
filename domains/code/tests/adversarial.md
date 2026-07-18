# Adversarial

Adversarial tests validate that the codebase, its build pipeline, and the APIs it exposes survive conditions they were not designed to expect: hostile input, a compromised dependency, a malicious contributor, or an attacker replaying a captured request. Where the other seven domains confirm correct behavior under normal and expected-failure conditions, this domain deliberately tries to break the system the way an attacker would.

## What to test

- Fuzzing and malformed input
  - Feed randomized, oversized, and structurally invalid input to every parser and public entry point.

- Supply-chain tampering simulation
  - Simulate a compromised or typosquatted dependency and verify detection and containment.
  - Verify every dependency existed and was actively maintained before it was added, not just that it resolves today -- an AI coding assistant can hallucinate a plausible package name that an attacker later registers with malicious code.

- Privilege escalation attempts
  - Attempt to reach higher-privileged functionality through parameter tampering, forced browsing, or role manipulation.

- Malicious PR / contribution injection
  - Simulate an obfuscated payload, a typosquatted dependency addition, or a disguised backdoor submitted through a normal-looking pull request.

- Build and deploy pipeline chaos
  - Kill the pipeline mid-build, corrupt a build artifact, or inject an unauthorized step, and verify the pipeline fails safely.

- Replay and injection attacks against exposed APIs
  - Replay captured requests, tamper with tokens, and inject payloads designed to break API-layer assumptions.

## Why it matters

Every piece of code that accepts external input, pulls a dependency, or runs in a CI pipeline is a potential entry point. The adversarial domain assumes an attacker will find the weakest link in that chain, and tests for it deliberately instead of waiting for it to be found in production.

---

## DPPF adversarial test catalog

| ID | Name | What it verifies | Defends against | Standards | Lifecycle |
|---|---|---|---|---|---|
| ADV-001 | Fuzz testing of public entry points | Every public function, API endpoint, and parser handles randomized, malformed, and boundary-violating input without crashing or entering an undefined state | Crashes and hangs from unexpected input shapes, memory-safety bugs surfaced only under fuzzing | OWASP Testing Guide, CWE-20 | CI, Pre-deployment |
| ADV-002 | Oversized and malformed payload handling | Endpoints and parsers reject oversized, deeply nested, or structurally malformed payloads with a controlled error rather than resource exhaustion or a crash | Denial of service via payload bombs, decompression bombs, deeply nested JSON/XML causing stack exhaustion | CWE-400, OWASP API Security | CI, Pre-deployment |
| ADV-003 | Dependency tampering simulation | A simulated compromised or altered dependency (unexpected hash, unexpected postinstall script, unpinned version substitution) is detected before it reaches a build | Supply-chain compromise via a poisoned package, silent substitution of a malicious package version | OWASP A08:2021 Software and Data Integrity Failures, SLSA | CI, Pre-deployment |
| ADV-004 | Typosquatting dependency detection | A dependency name closely resembling a legitimate, popular package but not matching it exactly is flagged before installation | Typosquatting attacks that trick a developer into installing a malicious package with a similar name | OWASP A08:2021, CWE-1357 | CI, Pre-deployment |
| ADV-005 | Privilege escalation attempt containment | Attempts to reach higher-privileged functionality via parameter tampering, forced browsing to unlinked endpoints, or role-field manipulation are rejected by server-side authorization checks | Client-side-only authorization bypass, IDOR-based privilege escalation, hidden admin functionality reachable by URL guessing | OWASP A01:2021 Broken Access Control | CI, Pre-deployment |
| ADV-006 | Obfuscated payload / malicious PR detection | Code review and automated scanning detect obfuscated code, encoded payloads, or logic disguised to evade a casual review in a submitted change | Backdoors introduced through a plausible-looking pull request, obfuscated malicious code passing human review | OWASP A08:2021, supply-chain security practice | Review, CI |
| ADV-007 | Build pipeline fault injection | Killing the build process mid-run, corrupting an intermediate artifact, or interrupting network access during dependency resolution results in a failed build, not a corrupted or partially-built artifact shipped downstream | Corrupted artifacts silently promoted to a later stage, non-reproducible builds masking tampering | Chaos engineering practice, SLSA | Pre-deployment |
| ADV-008 | Unauthorized pipeline step injection | An injected or modified CI/CD step that was not present in the reviewed configuration is detected and blocks the pipeline | CI/CD configuration tampering, unauthorized script execution during build with access to deployment credentials | OWASP A08:2021, SLSA | Pre-deployment |
| ADV-009 | Secrets exposure under pipeline chaos | Simulated pipeline failures (killed job, redirected logs, forced verbose mode) do not cause secrets or credentials to be written to logs or artifacts | Credential leakage via debug output during an incident, secrets captured in a crash dump or log archive | CWE-532, OWASP A09:2021 | Pre-deployment |
| ADV-010 | Replay attack resistance | Replaying a previously captured, valid API request (including its authentication token) is rejected or has no unintended effect after the token or nonce has expired or been consumed | Session token replay, duplicate transaction from a captured and resent request | OWASP API Security, CWE-294 | CI, Pre-deployment |
| ADV-011 | Injection attack resistance at API boundary | Public API inputs are tested with SQL, command, and script injection payloads and confirmed to be rejected or safely neutralized at the boundary | Injection attacks reaching business logic or the database layer, boundary validation gaps exploited via the public API | OWASP A03:2021 Injection | CI, Pre-deployment |
| ADV-012 | Token and credential tampering resistance | Tampered, expired, or malformed authentication tokens (altered claims, stripped signature, algorithm confusion) are rejected without granting access | JWT algorithm confusion attacks, forged tokens, privilege escalation via claim tampering | OWASP A07:2021, CWE-347 | CI, Pre-deployment |
| ADV-013 | Chaos testing of dependency failure combinations | Simulated simultaneous failure of two or more dependencies (database plus cache, auth service plus queue) is handled without cascading into full system failure | Compound failures with no tested combined-failure behavior, single-dependency resilience masking multi-dependency fragility | Chaos engineering practice | Pre-deployment, Production |
| ADV-014 | Malicious input encoding and homoglyph resistance | Input containing control characters, null bytes, mixed encodings, or homoglyph/confusable Unicode characters is normalized, rejected, or safely handled without bypassing validation logic | Unicode normalization bypass of filters, homoglyph-based spoofing of identifiers, control-character injection breaking downstream parsers | CWE-176, CWE-838 | CI, Pre-deployment |
| ADV-015 | Hallucinated dependency detection | Every declared dependency is verified to have existed and been actively maintained on the public registry *before* it was added to the project, not merely that it resolves at install time | AI-assisted "slopsquatting": an AI coding assistant hallucinates a plausible but never-real package name, an attacker registers that exact name after the fact with malicious code, and a routine install silently pulls it in. Distinct from ADV-004 (typosquatting of an already-real package) -- here the package was never real to begin with | OWASP A08:2021 Software and Data Integrity Failures, supply-chain security practice | CI, Pre-deployment |
