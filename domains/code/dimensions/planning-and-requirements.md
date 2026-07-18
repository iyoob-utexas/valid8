# Planning and Requirements

This is the first SDLC stage in this domain's dimension breakdown, and the first opportunity to catch a defect: before any code exists. A requirement that is ambiguous, untestable, or missing an edge case costs a conversation to fix here. The same gap costs a rewrite if it's discovered during Coding, and an incident if it's discovered in Production.

## What to test

- Requirement clarity
  - Each requirement states an observable, verifiable outcome, not an intention.
  - Ambiguous terms ("fast", "reasonable", "most users") are replaced with a measurable definition before implementation starts.

- Edge case identification
  - Boundary conditions, empty/null states, and error scenarios are enumerated as part of the requirement, not left for the implementer to guess.

- Testability
  - Every requirement has a corresponding acceptance condition that a test can be written against.
  - Requirements that cannot be stated as a pass/fail condition are flagged and clarified before they enter a sprint.

## Test IDs that apply here

| ID | Name | Catalog |
|---|---|---|
| COR-014 | Requirement validation and testability | `tests/correctness-and-logic.md` |

COR-013 (Business rule fidelity, in `tests/correctness-and-logic.md`) is the downstream check that confirms the implementation actually matches the requirement validated here -- treat the two as a pair, not a duplicate.

## Why it matters

A defect caught at this stage costs a clarifying question. The same defect, if it ships, costs a redesign, a stakeholder escalation, or a production incident traced back to a requirement nobody actually validated as testable.
