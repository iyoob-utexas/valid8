# Tier and DAMA Dimension Reference

This file describes the severity tiers and the DAMA data quality dimensions used by the framework.

## Severity tiers

| Tier | Meaning | Behavior |
|---|---|---|
| Tier 1, Critical Path | Zero tolerance. Failure blocks or quarantines the pipeline. Bad data must not move downstream. Run on every load. | Block the refresh or quarantine the affected data. |
| Tier 2, Important | Warn and investigate. Quarantine rows or raise an alert; the run may proceed under review. Run on every load or daily. | Investigate and review; allow controlled continuation when appropriate. |
| Tier 3, Good Practice | Monitor and trend. Dashboarded to catch drift and SLA risk early; no hard gate. Reviewed on a cadence. | Track over time and improve the process. |

## DAMA data quality dimensions

| Dimension | What it means |
|---|---|
| Completeness | Is all expected data present? No missing rows, columns or required values. |
| Uniqueness | Is each entity represented once? No unintended duplicates. |
| Validity | Does data conform to defined format, type, range and allowed values? |
| Consistency | Does data agree with itself and prior loads, across systems and over time? |
| Accuracy | Does data correctly describe the real world value, vs a trusted source? |
| Timeliness | Is data available when expected and recent enough to be useful? |
| Integrity | Are relationships, references and security constraints preserved end to end? |
