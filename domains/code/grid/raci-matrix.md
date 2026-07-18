# RACI Matrix

This matrix defines roles and accountability for each code validation test category.

| Category / Test Area | Author | Reviewer | Security champion | Tech lead | SRE / on-call |
|---|---|---|---|---|---|
| Correctness and logic | R | C | I | C | I |
| Structure and style | R | C | I | A | I |
| Security | C | C | R | I | I |
| Architecture and design | C | C | I | R | I |
| Testing and coverage | R | C | I | A | I |
| Performance and scalability | C | C | I | C | R |
| Reliability and operability | C | C | I | C | R |
| Adversarial | C | I | R | I | C |
| CI gate / merge decision | I | R | C | A | I |
| Release / deployment gate | I | I | C | A | R |
| Test logging & dashboard | C | I | I | C | A |

> Legend: R = Responsible (does the work), A = Accountable (owns the outcome), C = Consulted (gives input), I = Informed (kept in the loop)

> Note: Tailor per project; not every role appears on every repository. On small teams, Tech lead often also carries the Accountable role for Security and Reliability categories. The Tech lead role oversees coverage and prevents duplicate or no-owner tests, analogous to the Test Lead / QA role in the data domain's RACI matrix.

## Solo operator and small-team guidance

The columns above name **roles**, not headcount. A solo founder or a two-person forward-deployed team can legitimately hold every role in this matrix at once -- Author, Reviewer, Security champion, Tech lead, and SRE/on-call can all be the same person. That is a normal, supported way to run this framework.

What does not change when one person holds every role:

- **Tier 1 checks stay mandatory.** The checklist does not shrink because there is no separate reviewer to enforce it. A solo operator runs SEC-001 through SEC-018, ADV-002/003/005/008/009/010/011/012/015, and every other Tier 1 row in `grid/test-grid.md` against their own code, in full.
- **The Reviewer role still has to happen, just asynchronously or tool-assisted.** If there is no second human, the Reviewer function is discharged by automated tooling (SAST, DAST, SCA, linting, CI gates) plus a deliberate self-review pass using the same checklist a second reviewer would use -- not skipped.
- **Security champion and Tech lead sign-off still has to be recorded.** One person can check both boxes, but do it as two distinct, deliberate passes against the Security and Architecture catalogs, not folded silently into "I wrote it, it's fine."
- **The Handoff and Transfer dimension (`dimensions/handoff-and-transfer.md`) is not optional for a solo builder.** It is written specifically for this operator profile -- a solo or small-team builder preparing to sell or hand off a system -- and its six test IDs (ADV-015, SEC-017, SEC-018, ARC-014, REL-019, REL-020) are exactly the checks a solo operator is otherwise least likely to have anyone else catch.

In practice: run the full test grid solo, using automated tooling to substitute for the second-reviewer function wherever a human reviewer would normally provide it, and treat any Tier 1 row you cannot personally verify as a gap to close before shipping -- not a check to skip because "it's just me."
