# valid8

A living, markdown-first Validation Framework. It defines a fixed checklist of nine validation dimensions -- what "fully validated" means -- and lets each domain (data pipelines, code, or whatever comes next) implement its own tests and gating rules against that checklist.

This repository is a reference guide for humans and AI tools validating completed work. It is tool-agnostic and implementation-free: it defines the checks, not the code.

## How this repo works

1. **Read [`validation-dimensions.md`](validation-dimensions.md).** It defines the nine dimensions every domain validates against -- Conformance, Internal consistency, Cross-validate, Sensibility, Sensitivity, Robustness, Durability, Alignment, Vantage.
2. **Pick your domain** from the table below and go to its own `README.md`. Each domain owns its test catalog, tier/severity model, and test grid -- this repo root does not.
3. **Use the domain's own process to build a project-specific test grid and score it.** The nine dimensions tell you *what* to cover; the domain tells you *how*.

## Domains

| Domain | Status | Entry point |
|---|---|---|
| Data pipelines & data products | Built | [`domains/data/README.md`](domains/data/README.md) |
| Code (source, PRs, codebases) | Built | [`domains/code/README.md`](domains/code/README.md) |

More domains get added as `domains/<name>/`, each inheriting the same nine dimensions and inventing its own mechanics -- see "Adding a new domain" in [`validation-dimensions.md`](validation-dimensions.md).

## What this repo is good for

- defining a domain-neutral checklist of what "validated" means
- letting each domain build its own test catalog, severity model, and gate against that checklist
- keeping the guidance in markdown so both people and automation can navigate it

## What this repo does not include

- execution code or test harnesses
- domain-specific mechanics prescribed at the repo-root level -- those belong to each domain
- non-validation documentation
