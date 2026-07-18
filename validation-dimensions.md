# Validation Dimensions

A fixed, nine-part checklist for validating any completed body of work -- a data pipeline, a code change, or any other domain this repo is later extended to cover. Every domain in this repo applies the same nine dimensions. What differs per domain is the test catalog, and the tier/severity model used to gate and prioritize failures.

This doc defines the dimensions only. It does not prescribe how to test for them -- that is each domain's job.

---

## How to use this doc

1. **Find your domain.** Today this repo has two built domains: data pipelines and data products at [`domains/data/README.md`](domains/data/README.md), and code (source, PRs, codebases) at [`domains/code/README.md`](domains/code/README.md). If your work fits either, go there now -- you likely don't need this doc directly, since each domain's test catalog already maps to these nine dimensions (see its coverage table).
2. **If your domain isn't built yet** (content review, infrastructure, etc.), use the nine dimensions below as your starting checklist. For each dimension, decide what "covered" looks like in your domain and build a test catalog for it, the way `domains/data/tests/` and `domains/code/tests/` do for their domains.
3. **Within any domain, use the checklist to find real gaps.** Walk the nine dimensions against the domain's existing tests. A dimension with no tests and no plan for the domain covering it is a gap worth naming, even if you decide not to close it yet.
4. **Run the domain's own process to get a test grid.** This doc doesn't produce a grid. Each domain has its own (for data: `domains/data/grid/test-grid.md` via `domains/data/process/test-cycle.md`).

---

## The nine dimensions

| # | Dimension | Question it asks |
|---|---|---|
| 1 | **Conformance** | Does this meet its defined spec, rule, or contract? |
| 2 | **Internal consistency** | Do multiple derivations of the same source agree with each other? |
| 3 | **Cross-validate** | Does an independent source, method, or reviewer -- one that hasn't seen the prior conclusion -- confirm this? |
| 4 | **Sensibility** | Does this make sense proportionally, and item by item, to a knowledgeable observer? |
| 5 | **Sensitivity** | How much does the conclusion change if a key assumption, threshold, or input were different? |
| 6 | **Robustness** | Does this hold up if applied repeatedly, at volume, or as a blanket rule? |
| 7 | **Durability** | Does this hold up over time, and for downstream consumers or future maintainers? |
| 8 | **Alignment** | Does this still serve the system's stated purpose and design principles? |
| 9 | **Vantage** | Does this hold up viewed through distinct accountability lenses -- a new user, an auditor, a maintainer six months from now, an adversary? |

### Two pairs that are easy to conflate

- **Internal consistency vs. Cross-validate** -- both compare a result against something else, but internal consistency checks it against *another derivation of the same source* (e.g., do two aggregation paths over the same data agree), while cross-validate checks it against a genuinely *independent* source or reviewer. A same-source check that gets called "cross-validation" is mislabeled -- see `domains/data/tests/cross-validation-suite.md` for a live example: its "mechanical cross-validation" section is same-source, so it maps to Internal consistency, not Cross-validate.
- **Sensibility vs. Sensitivity** -- sensibility asks whether a result is plausible as it stands; sensitivity asks whether the result would still hold if an assumption behind it were different. One is a plausibility check on the output, the other is a fragility check on the inputs.

---

## How relevance works

There is no separate relevance score to fill in. A dimension's relevance to a domain shows up in how much the domain has actually built for it: a dimension with many tests and Tier 1 gates is one the domain treats as important; a dimension with no tests at all is one the domain hasn't prioritized. Read relevance off the domain's own tier and severity model -- don't add a second scoring system on top of it.

---

## Adding a new domain

- Inherit the nine dimensions unchanged. Don't rename or drop one to fit a domain -- if a dimension genuinely doesn't fit any domain you can imagine, that's a reason to revisit this list itself, not to skip it silently in one domain.
- Define your own tier-equivalent (what happens when a check fails) and severity-equivalent (how bad it is that a check is missing). These don't need to match the data domain's Tier 1/2/3 or four-factor scoring -- they need to answer the same two questions in a way that fits the domain.
- Build your own test catalog. This doc defines *what* to check for, never *how*.
- Add the domain under `domains/<name>/`, with its own `README.md` as the entry point, following the shape of `domains/data/README.md`.
