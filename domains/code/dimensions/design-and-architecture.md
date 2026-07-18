# Design and Architecture

This dimension covers the checks that apply once requirements are validated but before implementation begins: the architecture that will carry those requirements, and the interface the eventual user will interact with.

## What to test

- Threat modeling
  - Trust boundaries, data flow, and privilege boundaries are diagrammed and reviewed against a threat framework (e.g., STRIDE) before code is written.
  - Every identified threat has an assigned mitigation, an accepted risk, or a follow-up design change.

- Architecture fit
  - The proposed design is checked against SOLID, layering, and coupling/cohesion expectations before it is built, not only in review after the fact.
  - API surface and versioning strategy are decided before the first consumer integrates.

- UI/UX usability testing
  - Mockups and wireframes are usability-tested with representative users, or reviewed against a structured heuristic checklist, before implementation starts.
  - Accessibility and localization requirements are captured as design constraints, not retrofitted later.

## Test IDs that apply here

| ID | Name | Catalog |
|---|---|---|
| ARC-013 | Threat modeling coverage | `tests/architecture-and-design.md` |
| TST-014 | UI/UX usability testing | `tests/testing-and-coverage.md` |

The remaining SOLID, coupling/cohesion, and layering checks in `tests/architecture-and-design.md` (ARC-001 through ARC-012) apply here as design-time review criteria in addition to their role as PR-review checks in Integration and Testing -- the same architectural standard applies whether it's being designed or being reviewed after the fact.

## Why it matters

Architectural and usability defects are the most expensive to fix the later they're found, because fixing them after implementation means undoing work rather than adjusting a plan. This dimension exists to apply the same standard the codebase will eventually be reviewed against, before there's code to review.
