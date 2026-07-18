# Deployment

This dimension covers the checks that apply during the act of shipping a change: moving a built, tested artifact into a live environment.

## What to test

- Environment parity
  - Staging (or pre-production) configuration, dependency versions, and infrastructure topology are checked against production before the deployment is trusted as representative.

- Configuration and secret validation
  - Live environment variables, domain configuration, and SSL certificates are validated as correct and current for the target environment before traffic is routed to it.
  - This extends REL-010 (Configuration validation at startup, in `tests/reliability-and-operability.md`), which checks that the running process validates its own config, and SEC-008 (Security configuration hardening) and SEC-004 (Secrets-in-code absence), which check the code and deployed config don't carry defaults or leaked secrets. Deployment-stage validation checks the actual live values in the target environment, not just that the process would fail safely on a bad one.

- Database migration validation
  - Every schema migration is tested for forward application, rollback, and backward compatibility with the currently-deployed application version before it runs against production data.

- Smoke testing
  - A minimal, fast-running suite of critical-path checks runs immediately after deployment, before broader validation proceeds or traffic is fully shifted.

- Rollback procedure testing
  - The rollback path is exercised, not just documented, before it's needed under incident pressure.
  - This extends REL-009 (Safe deployment and rollback, in `tests/reliability-and-operability.md`), which defines the requirement that rollback be fast and code-change-free; this dimension is where that requirement gets rehearsed as part of the deployment process itself, not left untested until the first real rollback.

## Test IDs that apply here

| ID | Name | Catalog |
|---|---|---|
| REL-009 | Safe deployment and rollback | `tests/reliability-and-operability.md` |
| REL-010 | Configuration validation at startup | `tests/reliability-and-operability.md` |
| REL-014 | Environment parity validation | `tests/reliability-and-operability.md` |
| REL-015 | Database migration validation | `tests/reliability-and-operability.md` |
| TST-015 | Smoke test coverage | `tests/testing-and-coverage.md` |
| SEC-004 | Secrets-in-code absence | `tests/security.md` |
| SEC-008 | Security configuration hardening | `tests/security.md` |

## Why it matters

Most "it worked in every environment except production" incidents trace back to exactly the checks in this dimension: a config drift nobody diffed, a migration nobody rehearsed, a rollback nobody had actually run. This dimension exists to make the deployment act itself a tested procedure rather than a one-way door.
