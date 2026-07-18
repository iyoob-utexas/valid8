# Test Grid

The Test Grid is the master checklist for data project validation.

## What it contains

- A matrix of tests by tier, category, and type.
- A clear description of what each check validates.
- A threshold or rule for passing and failing.
- DAMA data quality dimension mapping.
- A tool-agnostic approach plus optional Fabric/Azure tooling guidance.
- On-fail actions and owner assignment.
- An example row showing one concrete instance per test.

## How to use it

1. Use the grid as the baseline for every engagement.
2. Replace the example column with the client’s domain-specific instance.
3. Add client-specific rows below each category as needed.
4. Assign ownership and severity tier to each test.
5. Keep the grid aligned with the standard and the runbook.

## Tab structure

- `domains/data/grid/test-grid.md` — the core checklist of tests, with DPPF ID mappings.
- `domains/data/grid/summary-test-grid.md` — the summary scorecard for pass rate, gate readiness, and health metrics.
- `domains/data/grid/lineage-map.md` — the end-to-end lineage map: Mermaid pipeline diagram, zone-to-zone validation table, and lineage coverage checklist.
- `domains/data/grid/raci-matrix.md` — roles and accountability for each category.
- `domains/data/grid/tier-dimension-reference.md` — severity tier definitions and DAMA dimension mapping.
- `domains/data/grid/standards-references.md` — the credible standards this framework follows.
- `domains/data/grid/README.md` — the reference for how to use the text-based grid.

## Why it matters

The grid makes the framework operational. It turns abstract quality dimensions into concrete checks with a rule, owner, and action plan.
