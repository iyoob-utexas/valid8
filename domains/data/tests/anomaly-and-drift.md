# Anomaly and Drift Detection

This category helps identify unexpected changes in data distribution, volumes, and patterns.

## What to test

- Volume anomalies
  - Detect sudden increases or decreases in row counts.
  - Flag missing or duplicated batch load sizes.

- Distribution changes
  - Monitor value distributions for key metrics and dimensions.
  - Detect shifts in category frequencies or numeric ranges.

- Trend and seasonality checks
  - Compare current data to historical patterns.
  - Identify unexpected spikes, drop-offs, or seasonal deviations.

- Schema drift
  - Detect new columns, removed columns, or type changes.
  - Validate evolving domain values and enumerations.

- Metadata drift
  - Monitor changes in partition structure, data formats, and source frequencies.

## Anomaly detectors

- Define out-of-range detectors for business-critical metrics and KPIs.
- Use thresholds, z-scores, or interquartile range logic to identify values outside expected ranges.
- Surface data points that are unexpected, not just overall dataset drift.
- Compare each anomaly trigger with the expected baseline and historical context.

- Examples:
  - a revenue line item that moves by more than 20% MoM.
  - a balance sheet account that changes by more than 15% vs prior period.
  - a previously non-null KPI field becoming null.

## Why it matters

Anomaly detectors act as early warning systems. They help teams isolate specific records, dimensions, or business metrics that require investigation before downstream reports are released.

Anomalies and drift often signal upstream issues or broken business processes. These checks help catch emerging problems before consumers are affected.

---

## DPPF statistical test catalog

| ID | Name | What it verifies | Defends against | Standards | Lifecycle |
|---|---|---|---|---|---|
| STAT-001 | Volume shape | Row counts for each dataset or partition remain within the contracted minimum and maximum | Missing loads, partial extracts, duplicate floods, truncated files | Volume, Completeness | CI, Production monitoring |
| STAT-002 | Distribution stability | The frequency distribution of values in key categorical or numeric fields does not shift materially between periods | Data poisoning at source, upstream encoding change, model drift affecting feature columns | Distribution, Consistency | CI, Production monitoring |
| STAT-003 | Outlier detection | Individual field values fall within the expected range defined by historical baselines, z-score bounds, or IQR logic | Adversarial or erroneous outlier values, injection of extreme values, unit conversion errors | Distribution, Accuracy | CI, Production monitoring |
| STAT-004 | Statistical drift detection | Statistical properties including mean, standard deviation, and quantile positions do not change significantly across successive periods | Slow upstream data degradation, gradual model drift, feature distribution shift | Distribution, Consistency | Production monitoring |
| STAT-005 | Cardinality drift | The count of distinct values in key fields does not change beyond expected bounds between periods | Duplicate floods inflating cardinality, missing entities collapsing cardinality, unexpected dimension expansion | Uniqueness, Volume | CI, Production monitoring |
| STAT-006 | Missing pattern detection | Records, identifiers, or time periods expected from prior history are present in the current load. Note: this covers two distinct cases -- (a) a recurring transaction absent from the current period (e.g., a monthly fee entry that did not post), and (b) a dimension member (e.g., a vendor, product, account, or entity) active in prior periods that is absent from the current period's data. The diagnostic path differs: missing transactions point to a source or process failure; missing dimension members point to a master data or scoping change. | Systematic data loss, source gaps, dropped batch segments, missing entity extracts | Completeness, Consistency | CI, Production monitoring |
| STAT-007 | Null rate monitoring | The proportion of null values in each field remains within the expected baseline range | Null flood injection, upstream field removal producing mass nulls, ETL bug silently nulling a column | Completeness, Validity | CI, Production monitoring |
| STAT-008 | Zero value rate monitoring | The proportion of zero values in numeric fields remains within the expected baseline range | Zero flood injection, failed calculation producing zeros instead of errors, upstream aggregation bug | Accuracy, Validity | CI, Production monitoring |
| STAT-009 | Mean and median shift detection | The central tendency of numeric fields does not shift materially between periods or loads | Subtle data poisoning, source system default value change, currency or unit change without conversion | Accuracy, Consistency | CI, Production monitoring |
| STAT-010 | Variance stability | The spread of numeric field values does not widen or collapse unexpectedly between periods | Normalization failure, precision loss, upstream calculation change expanding or compressing value range | Accuracy, Distribution | Production monitoring |
| STAT-011 | Correlation stability | Known correlations between related numeric fields remain within expected bounds | Decoupled field updates, partial load that updates one field without its correlated counterpart, transformation logic error | Consistency, Distribution | Production monitoring |
| STAT-012 | Skewness monitoring | The skewness of numeric distributions does not shift in a way inconsistent with known business behavior | Tail injection of adversarial values, systematic bias from a new source or mapping, one-sided data loss | Distribution, Accuracy | Production monitoring |
| STAT-013 | Seasonal pattern compliance | Values for a given period fall within the expected seasonal band from prior-year same-period history | Period performance anomaly not caught by simple MoM checks, calendar shift not accounted for, seasonal data gap | Consistency, Accuracy | Production monitoring |
| STAT-014 | Percentile stability | Key percentile values (5th, 25th, 75th, 95th) do not shift materially between periods | Tail manipulation, partial deduplication leaving edge duplicates, outlier contamination | Distribution, Accuracy | Production monitoring |
| STAT-015 | Concentration ratio monitoring | No single value or member drives a disproportionate share of a total relative to its historical contribution | Concentration spike from upstream error, adversarial value inflating a single entity, GL account coding error dominating a category | Distribution, Accuracy | CI, Production monitoring |
