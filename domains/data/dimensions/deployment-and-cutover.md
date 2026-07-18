# Deployment and Cutover

This dimension covers replacing an existing pipeline with a new one: deploying the new pipeline, migrating historical data into it, and cutting traffic and trust over from the old pipeline before decommissioning it.

## What to test

- Historical data migration
  - All historical data required by the new pipeline's consumers has actually been migrated into its target store, not just data arriving after cutover.
  - Migrated row counts and key totals are checked against the source system, not assumed correct because the migration job completed without error.

- Old-versus-new parity
  - The old and new pipelines are run in parallel (dual-run) over the same historical periods, and their outputs are compared within an agreed tolerance before the old pipeline is trusted as replaceable.
  - Divergences are investigated and explained, not waved through because the new pipeline is "supposed to be better."

- Decommission gating
  - The old pipeline is not decommissioned until parity is proven and stakeholders have signed off on the cutover.
  - A rollback path back to the old pipeline exists until the new pipeline has run successfully in production for an agreed observation window.

## Why it matters

A pipeline replacement is one of the few moments where an independent, already-built system exists to check the new one against -- and that opportunity disappears the moment the old pipeline is decommissioned. This dimension exists to make sure that comparison happens deliberately, while it's still possible, rather than being skipped under deadline pressure and only discovered missing when a downstream number silently drifts.
