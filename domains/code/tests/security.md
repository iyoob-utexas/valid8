# Security

Security testing confirms the code does not introduce an exploitable weakness. The catalog below maps directly to the OWASP Top 10 (2021) and the CWE Top 25 most dangerous software weaknesses, so findings can be communicated in vocabulary that security reviewers and auditors already share.

## What to test

- Injection
  - SQL, command, template, and LDAP injection through unsanitized user input.

- Authentication and session management
  - Broken or missing authentication, weak session handling, credential stuffing exposure.

- Sensitive data exposure
  - Secrets in source, unencrypted sensitive data at rest or in transit, verbose error messages leaking internals.

- Access control
  - Missing or bypassable authorization checks, insecure direct object references, privilege escalation paths.

- Security misconfiguration
  - Default credentials, verbose stack traces in production, unnecessary services or ports exposed.

- XSS and output encoding
  - Unescaped output rendered into HTML, JavaScript, or other interpreted contexts.

- Insecure deserialization
  - Deserializing untrusted data without type or schema validation.

- Vulnerable and outdated dependencies
  - Known-vulnerable packages, unpinned versions, unmaintained transitive dependencies.

- Logging and monitoring
  - Insufficient security event logging, logging of sensitive data, no alerting on suspicious activity.

- SSRF
  - Server-side requests to attacker-influenced URLs without allowlisting.

- Static and dynamic analysis coverage
  - Software Composition Analysis (SCA) scans dependencies for known vulnerabilities (SEC-011); static analysis (SAST) scans source for the injection, XSS, deserialization, and XXE patterns above (SEC-001, SEC-009, SEC-010, SEC-015); Dynamic Application Security Testing (DAST) exercises the running application independently of source analysis (SEC-016).

- Incomplete-code reachability
  - Inventory every stub, mock, and TODO-marked shortcut, and confirm none of them sit on a live production path.

- License and provenance compliance for commercial distribution
  - Every dependency's license is compatible with how the software will actually be distributed; copyleft dependencies are flagged before a commercial sale, not discovered by the buyer's legal team after.

## Why it matters

A single unvalidated input path or leaked credential can compromise an entire system regardless of how correct or well-tested the surrounding logic is. Security defects are also disproportionately expensive to fix after release, since they often require incident response, disclosure, and remediation across every environment the vulnerable code shipped to.

---

## DPPF security test catalog

| ID | Name | What it verifies | Defends against | Standards | Lifecycle |
|---|---|---|---|---|---|
| SEC-001 | Injection input sanitization | All user-controlled input reaching a SQL query, shell command, template engine, or LDAP query is parameterized or escaped, never string-concatenated | SQL injection, OS command injection, template injection, LDAP injection | OWASP A03:2021 Injection, CWE-89, CWE-78, CWE-94 | Authoring, Review, CI |
| SEC-002 | Authentication strength | Authentication mechanisms enforce credential strength, rate-limit login attempts, and do not expose valid-username signals | Credential stuffing, brute force, username enumeration, session fixation | OWASP A07:2021 Identification and Authentication Failures, CWE-287 | Review, CI, Production |
| SEC-003 | Session management integrity | Session tokens are generated with sufficient entropy, expire appropriately, and are invalidated on logout and privilege change | Session hijacking, session fixation, stale sessions surviving password reset | OWASP A07:2021, CWE-384 | Review, CI |
| SEC-004 | Secrets-in-code absence | No API keys, passwords, tokens, or private keys are committed to source control or hardcoded in the codebase | Credential leakage via repository history, secret scraping from public repos, lateral movement after a leak | OWASP A02:2021 Cryptographic Failures, CWE-798 | Authoring, Review, CI |
| SEC-005 | Sensitive data encryption | Sensitive data (PII, credentials, financial data) is encrypted at rest and in transit using current, non-deprecated algorithms | Data exposure from storage compromise or network interception, use of broken ciphers (MD5, SHA1, DES) | OWASP A02:2021 Cryptographic Failures, CWE-327 | Review, CI |
| SEC-006 | Error message information disclosure | Error responses returned to clients do not include stack traces, internal paths, query text, or system versions | Attacker reconnaissance via verbose errors, internal architecture disclosure | OWASP A05:2021 Security Misconfiguration, CWE-209 | Review, CI, Production |
| SEC-007 | Access control enforcement | Every endpoint and resource access checks authorization, not just authentication, before returning data or performing an action | Broken access control, insecure direct object reference, horizontal and vertical privilege escalation | OWASP A01:2021 Broken Access Control, CWE-862, CWE-639 | Review, CI |
| SEC-008 | Security configuration hardening | Deployed services do not run with default credentials, debug mode, verbose framework banners, or unnecessary exposed ports/services | Default-credential compromise, information disclosure via framework fingerprinting, unnecessary attack surface | OWASP A05:2021 Security Misconfiguration, CWE-16 | Pre-deployment, Production |
| SEC-009 | Output encoding / XSS prevention | Data rendered into HTML, JavaScript, or URL contexts is encoded for that context, using framework-provided escaping rather than manual string building | Stored, reflected, and DOM-based cross-site scripting | OWASP A03:2021 Injection (XSS), CWE-79 | Authoring, Review, CI |
| SEC-010 | Deserialization safety | Data from an untrusted source is deserialized only into an expected, validated schema, never into a type that permits arbitrary object instantiation | Insecure deserialization leading to remote code execution, object injection | OWASP A08:2021 Software and Data Integrity Failures, CWE-502 | Review, CI |
| SEC-011 | Dependency vulnerability scan (SCA) | All direct and transitive dependencies are scanned via Software Composition Analysis (SCA) against a known-vulnerability database and have no unresolved critical or high findings | Vulnerable dependency exploitation, supply-chain compromise via an unpatched library | OWASP A06:2021 Vulnerable and Outdated Components, CWE-1104 | CI, Pre-deployment |
| SEC-012 | Security event logging sufficiency | Authentication attempts, authorization failures, and administrative actions are logged with enough context to support an investigation | Insufficient logging masking an active breach, no audit trail for incident response | OWASP A09:2021 Security Logging and Monitoring Failures, CWE-778 | Review, Production |
| SEC-013 | Sensitive data logging exclusion | Logs, error messages, and telemetry never contain passwords, tokens, full card numbers, or other sensitive fields, even at debug verbosity | Sensitive data exposure via log aggregation systems, compliance violation from PII in logs | OWASP A09:2021, CWE-532 | Review, CI |
| SEC-014 | SSRF request allowlisting | Server-initiated requests to a URL derived from user input are restricted to an allowlist of destinations and cannot reach internal network ranges | Server-side request forgery reaching internal metadata endpoints or internal services | OWASP A10:2021 Server-Side Request Forgery, CWE-918 | Review, CI |
| SEC-015 | XML external entity (XXE) prevention | XML parsers used on untrusted input have external entity resolution and DTD processing disabled | XXE-based file disclosure, SSRF via XML parser, denial of service via entity expansion | OWASP A05:2021 (XXE historically A04:2017), CWE-611 | Review, CI |
| SEC-016 | Dynamic application security testing (DAST) coverage | A deployed, running instance of the application is scanned by an automated DAST tool exercising real HTTP requests against it, independent of and in addition to static analysis (SEC-001, SEC-009, SEC-010, SEC-015) | Runtime-only vulnerabilities invisible to source-level static analysis (misconfigured runtime headers, exposed debug endpoints, auth bypass only reachable through a live request path) | OWASP Testing Guide, OWASP A05:2021 | Pre-deployment, Production |
| SEC-017 | Placeholder code reachability | Stubbed auth checks, mock data sources, hardcoded test credentials, and TODO-marked incomplete logic are inventoried, and none of them are reachable from a live production code path | Live traffic silently hitting a mock auth check or a "temporary" bypass that was never removed before ship, distinct from SEC-004 (a real leaked secret) and STY-007 (dead code that is unreachable, not live-but-incomplete) | OWASP A05:2021 Security Misconfiguration, CWE-489 | Review, CI, Pre-deployment |
| SEC-018 | Dependency license compliance | Every dependency's license is reviewed and compatible with the project's distribution model; zero unreviewed copyleft (GPL/AGPL-class) dependencies in a codebase being sold or commercially distributed | Copyleft-license obligations triggered by commercial resale or distribution, undisclosed license incompatibility discovered by a buyer's legal review after the sale | OSI license classifications, SPDX | Review, Pre-deployment |
