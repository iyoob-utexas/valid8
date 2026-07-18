# Design and Contracts

This is the first test frontier, earlier than raw data: before a single row has flowed through a pipeline that doesn't exist yet. A schema or contract that is ambiguous, unversioned, or has no agreed reconciliation method costs a design conversation to fix here. The same gap costs a rebuild if it's discovered during processing, or a silent reconciliation failure if it's discovered after the pipeline is already in production.

## What to test

- Contract completeness before build
  - The proposed schema defines nullability, types, and allowed values for every field up front, not left to be inferred once real data starts arriving.
  - The contract carries an explicit version identifier and a stated policy for how future changes will be versioned.

- Reconciliation method agreement
  - Before implementation starts, the pipeline's stakeholders agree on how the eventual output will be reconciled against the source: which totals must tie out, at what tolerance, and against which system of record.
  - A contract with no defined reconciliation method is treated as incomplete, regardless of how detailed its schema is.

- SLA and ownership definition
  - Freshness expectations, delivery windows, and escalation ownership are defined as part of the contract, not discovered the first time a load is late.

## Why it matters

A contract finalized only after the pipeline is built almost always means the reconciliation method gets invented after the fact, to match whatever the pipeline happened to produce, rather than the pipeline being built to satisfy an agreed method. This dimension exists to catch that ordering problem before it's expensive to fix.
