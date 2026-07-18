# Handoff and Transfer

This dimension is distinct from Operations and Maintenance. That dimension assumes the original owner keeps running the system. This one covers the moment ownership itself changes hands: a solo builder or small team selling a small SaaS app, an FDE handing a client-built system to the client's own team, or any transfer to a new owner who was not involved in building the system and cannot rely on the prior owner's institutional memory.

This is especially relevant for software built fast and heavily AI-assisted across many short sessions -- a common pattern for solo builders and forward-deployed engineers -- where the original author may not have a complete mental model of everything an AI assistant generated along the way.

## What to test

- AI-generated dependency integrity
  - Every declared dependency is checked against the public registry's actual publish history, not just whether it currently resolves -- an AI assistant can suggest a package name that never existed, and an attacker can register that exact name later.

- Placeholder and mock code audit
  - Every stub, mock data source, hardcoded test credential, and TODO-marked shortcut introduced during rapid iteration is inventoried and confirmed either removed or explicitly, deliberately retained with a documented reason -- not silently shipped because a fast-moving session never circled back.

- License and provenance review
  - Every dependency's license is checked for compatibility with a commercial sale or distribution.
  - Any verbatim code block pulled from an external source (a forum answer, another repository, AI-assistant output trained on licensed code) is checked for attribution and license compatibility.

- Documentation sufficiency
  - A new owner with zero prior access to the original author can provision, run, and deploy the system to a working state using only what's in the repository.

- Credential and access rotation
  - Every credential, API key, and admin account the prior owner could access is rotated or revoked at the point of transfer, with no secret shared between seller and buyer surviving the handoff.

## Test IDs that apply here

| ID | Name | Catalog |
|---|---|---|
| ADV-015 | Hallucinated dependency detection | `tests/adversarial.md` |
| SEC-017 | Placeholder code reachability | `tests/security.md` |
| SEC-018 | Dependency license compliance | `tests/security.md` |
| ARC-014 | Code provenance and non-infringement review | `tests/architecture-and-design.md` |
| REL-019 | Handoff documentation sufficiency | `tests/reliability-and-operability.md` |
| REL-020 | Credential and access rotation at ownership transfer | `tests/reliability-and-operability.md` |

## Why it matters

A buyer or new team inherits everything the prior owner built, including whatever they didn't know they'd left behind: a hallucinated import an attacker could weaponize, an auth stub that was never wired to the real check, a dependency whose license blocks resale, or lingering admin access nobody thought to revoke. None of these fail a normal test suite -- the code runs fine for the seller, right up until it's someone else's problem. This dimension exists to surface them before the sale, not after.
