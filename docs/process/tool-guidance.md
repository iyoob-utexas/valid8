# Guide Usage for Humans and AI

This file explains how to navigate and use the repo, with specific instructions for AI agents that need to parse, select, or generate tests from the framework.

---

## For human engineers

Start at `docs/README.md` for the full navigation map. The short path is:

1. `docs/framework/README.md` to understand the severity model and testing standard.
2. `docs/grid/test-grid.md` to see every test with its tier, threshold, owner, and DPPF ID.
3. `docs/process/test-cycle.md` to run a test cycle step by step.
4. `docs/tests/<category>.md` when you need to understand a specific test type in depth.

When starting a new project, use `docs/process/testing-strategy.md` to scope the engagement and decide which test IDs apply. When assessing an existing pipeline, open `docs/framework/dppf.md` and mark each ID as Covered, Partial, or Gap.

---

## Python / pandas quick-start

The test grid's "Tool-Agnostic Approach" column describes what to check. This section maps the most common check categories to a Python / pandas pattern. These are not production-ready implementations -- they show the shape of each assertion so you can build from them.

| Check | pandas pattern |
|---|---|
| Schema presence | `assert set(expected_cols) == set(df.columns)` |
| Data type conformance | `pd.to_numeric(df[col], errors='coerce').isna().sum() == 0` |
| Null key check | `df[key_col].isna().sum() == 0` |
| Row count reconciliation | `len(source_df) == len(landing_df)` |
| Duplicate detection | `df[key_col].duplicated().sum() == 0` |
| Referential integrity | `df[~df[fk_col].isin(dim[pk_col])].shape[0] == 0` |
| Transformation logic | `(df['derived'] - (df['a'] * df['b'])).abs().max() < tolerance` |
| Aggregation tie-out | `abs(detail_df[val].sum() - agg_df[val].sum()) < tolerance` |
| KPI range validation | `df[kpi_col].between(lower, upper).all()` |
| Cross-validation tie-out | `abs(source_total - output_total) / source_total < tolerance` |
| Future-date check | `(pd.to_datetime(df[date_col]) <= load_date + pd.Timedelta(days=buffer)).all()` |
| Period cutoff check | `pd.to_datetime(df[date_col]).between(period_start, period_end).all()` |
| MoM change | `abs((curr - prior) / prior) <= threshold` |
| Null rate monitoring | `df[col].isna().mean() <= null_rate_threshold` |
| Paired-value invariant | `abs(df['debit_col'].sum() - df['credit_col'].sum()) < tolerance` |
| Missing dimension member | `set(prior_df[dim_col].unique()) - set(curr_df[dim_col].unique())` |

For dbt environments, the equivalent tests are `not_null`, `unique`, `relationships`, `accepted_values`, and custom `dbt test` blocks. For Great Expectations, use `expect_column_values_to_not_be_null`, `expect_column_values_to_be_unique`, and `expect_table_row_count_to_equal`.

---

## For AI agents

### What this repo contains

Every test in this framework is addressable by a DPPF ID. IDs follow this format:

```
<DOMAIN>-<NUMBER>
```

Domains:
- `STR` - Structural (schema, types, contracts)
- `SEM` - Semantic (business rules, referential integrity, reconciliation)
- `STAT` - Statistical (distributions, drift, volume)
- `TMP` - Temporal (freshness, latency, ordering)
- `OPS` - Operational (idempotency, retries, backfill)
- `ADV` - Adversarial (fault injection, chaos, poisoned data)
- `PERF` - Performance and scale (throughput, degradation, cost)
- `SEN` - Sensibility (outside-in plausibility and business coherence)

Each ID resolves to a test definition with the following fields, found in the DPPF catalog tables in `docs/tests/`:

| Field | What it means |
|---|---|
| ID | Unique DPPF identifier |
| Name | Short test name |
| What it verifies | The specific condition the test checks |
| Defends against | The failure or attack scenario the test prevents |
| Standards | The DAMA data quality dimensions and observability pillars it maps to |
| Lifecycle | Where in the pipeline lifecycle the test runs (Development, CI, Pre-deployment, Production monitoring) |

### How to select tests for a given pipeline

1. Read the attack surface map in `docs/framework/README.md` to identify which pipeline zones are in scope.
2. Map each zone to the relevant DPPF domains using the domain table in `docs/framework/README.md`.
3. For each in-scope domain, pull the catalog from `docs/tests/<matching file>.md`.
4. Filter by lifecycle stage to match the execution context (CI, production monitoring, etc.).
5. Filter by "Defends against" to select tests that match known risk patterns for the pipeline type.

### How to identify coverage gaps

Load the checklist from `docs/framework/dppf.md`. It lists all 111 test IDs organized by domain. Any ID marked Gap or Partial is a coverage gap. Score gaps using the severity model in `docs/framework/README.md`:

- Blast radius (1-5): how much of the pipeline or output is affected
- Detectability (1-5): how hard the failure is to detect (5 = silent)
- Data criticality (1-5): how critical the affected data is
- Recoverability (1-5): how difficult recovery is

Sum the four scores. Scores of 16-20 are Critical; 11-15 High; 7-10 Medium; 4-6 Low.

### How to generate a test implementation

Use the test catalog entry as a specification. The "What it verifies" field is the assertion to implement. The "Defends against" field is the failure scenario to use when writing test fixtures or injecting data. The "Lifecycle" field tells you which pipeline stage to instrument.

Example using STR-001:
- What it verifies: all expected fields exist; no unexpected fields are present
- Defends against: schema drift, contract failure, silent column drop
- Lifecycle: Development, CI, Production monitoring
- Implementation approach: compare the incoming dataset column list to the contracted schema definition; assert exact match or raise a schema violation

### How to map tests to the test grid

`docs/grid/test-grid.md` is the master checklist. Each row has a DPPF IDs column listing the test catalog entries that the row covers. Use this to cross-reference grid rows with catalog entries, or to add new grid rows for catalog entries not yet in the grid.

### How to use the lineage map

`docs/grid/lineage-map.md` defines the pipeline zone sequence and the test IDs that validate each zone-to-zone transition. Use this to confirm that lineage is intact for a given pipeline by checking whether each transition's required test IDs have an implementation.

### How to use the maturity model

`docs/framework/maturity-model.md` describes four maturity levels (Reactive, Defined, Automated, Adversarial). Map an existing pipeline to a maturity level by checking the domain coverage matrix against the DPPF gap assessment. The model also defines the specific test IDs needed to advance to each level.

### Key data structures to parse

| File | Primary structure | Key fields |
|---|---|---|
| `docs/grid/test-grid.md` | Table | Tier, Category, Test Type, DAMA Dimension, On Fail, DPPF IDs |
| `docs/tests/<domain>.md` | DPPF catalog table | ID, Name, What it verifies, Defends against, Standards, Lifecycle |
| `docs/framework/dppf.md` | Checklist table per domain | ID, Name, Status, Notes |
| `docs/grid/lineage-map.md` | Validation table | Transition, Test IDs, Supporting IDs |
| `docs/tests/cross-validation-suite.md` | Sensibility catalog | SEN-001 to SEN-010 with tier and evaluation guidance |
