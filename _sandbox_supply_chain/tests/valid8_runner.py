"""
valid8 test runner -- Supply Chain / ERP pipeline.
Domain: purchase orders -> vendor performance + category spend reports.
Follows the 8-step test cycle from docs/process/test-cycle.md.
"""

import pandas as pd, os, collections
from datetime import datetime

BASE          = os.path.dirname(os.path.dirname(__file__))
RAW_PATH      = os.path.join(BASE, "data/po_raw.csv")
PRIOR_PATH    = os.path.join(BASE, "data/po_prior.csv")
DIM_VEN_PATH  = os.path.join(BASE, "data/dim_vendors.csv")
DIM_PRD_PATH  = os.path.join(BASE, "data/dim_products.csv")
LANDING_PATH  = os.path.join(BASE, "output/landing.csv")
TRANS_PATH    = os.path.join(BASE, "output/transformed.csv")
VENDOR_PATH   = os.path.join(BASE, "output/vendor_performance.csv")
SPEND_PATH    = os.path.join(BASE, "output/category_spend.csv")
LOG_PATH      = os.path.join(BASE, "tests/results/run_log.md")
SUMMARY_PATH  = os.path.join(BASE, "tests/results/summary.md")

RUN_ID   = datetime.now().strftime("RUN-%Y%m%d-%H%M%S")
RUN_DATE = datetime.now().strftime("%Y-%m-%d %H:%M")

EXPECTED_COLS   = ["po_id", "vendor_id", "product_id", "order_date", "expected_delivery",
                    "actual_delivery", "quantity", "unit_cost", "total_cost", "status"]
MOM_SPEND_THR   = 0.30   # 30% MoM total spend change
COST_VAR_TOL    = 0.001  # 0.1% tolerance on total cost tie-out
ON_TIME_FLOOR   = 0.60   # vendor on-time rate below 60% is a Tier 2 alert

results = []

def record(step, tier, category, test_name, status, detail, dppf_ids):
    icon = {"PASS": "✓", "FAIL": "✗", "WARN": "⚠"}.get(status, "?")
    print(f"  [{icon}] {test_name}: {detail}")
    results.append({"run_id": RUN_ID, "run_date": RUN_DATE, "step": step,
                     "tier": tier, "category": category, "test_name": test_name,
                     "status": status, "detail": detail, "dppf_ids": dppf_ids})

raw     = pd.read_csv(RAW_PATH)
prior   = pd.read_csv(PRIOR_PATH)
vendors = pd.read_csv(DIM_VEN_PATH)
products= pd.read_csv(DIM_PRD_PATH)
landing = pd.read_csv(LANDING_PATH)
trans   = pd.read_csv(TRANS_PATH)
vperf   = pd.read_csv(VENDOR_PATH)
spend   = pd.read_csv(SPEND_PATH)

# ══ Step 1: Schema & Contract ════════════════════════════════════════════
print("\n── Step 1: Schema & Contract ─────────────────────────────────────")

missing = [c for c in EXPECTED_COLS if c not in raw.columns]
extra   = [c for c in raw.columns   if c not in EXPECTED_COLS]
record(1, "Tier 1", "Source Ingestion", "Schema Presence",
       "PASS" if not missing and not extra else "FAIL",
       f"Missing: {missing} | Extra: {extra}" if missing or extra else f"All {len(EXPECTED_COLS)} columns present",
       "STR-001")

qty_ok  = pd.to_numeric(raw["quantity"],   errors="coerce").notna().all()
cost_ok = pd.to_numeric(raw["unit_cost"],  errors="coerce").notna().all()
tot_ok  = pd.to_numeric(raw["total_cost"], errors="coerce").notna().all()
record(1, "Tier 1", "Source Ingestion", "Data Type Conformance",
       "PASS" if qty_ok and cost_ok and tot_ok else "FAIL",
       f"quantity={qty_ok}, unit_cost={cost_ok}, total_cost={tot_ok}", "STR-002")

# ══ Step 2: Pull & Ingest ════════════════════════════════════════════════
print("\n── Step 2: Pull & Ingest ─────────────────────────────────────────")

record(2, "Tier 1", "Source Ingestion", "Row Count Reconciliation",
       "PASS" if len(raw) == len(landing) else "FAIL",
       f"Source={len(raw)}, Landing={len(landing)}", "STAT-001")

null_po = raw["po_id"].isna().sum()
record(2, "Tier 1", "Source Ingestion", "Null Key Check (po_id)",
       "PASS" if null_po == 0 else "FAIL",
       f"{null_po} null po_id(s)" if null_po else "Zero null po_ids", "STR-003")

null_vendor = raw["vendor_id"].isna().sum()
record(2, "Tier 1", "Source Ingestion", "Null Key Check (vendor_id)",
       "PASS" if null_vendor == 0 else "FAIL",
       f"{null_vendor} null vendor_id(s)" if null_vendor else "Zero null vendor_ids", "STR-003")

# ══ Step 3: Vs Last Pull ═════════════════════════════════════════════════
print("\n── Step 3: Vs Last Pull ──────────────────────────────────────────")

curr_spend = raw["total_cost"].sum()
prev_spend = prior["total_cost"].sum()
mom = (curr_spend - prev_spend) / prev_spend if prev_spend else 0
record(3, "Tier 1", "Anomaly Detection", "Period-over-Period Spend Change",
       "PASS" if abs(mom) <= MOM_SPEND_THR else "FAIL",
       f"Current={curr_spend:,.2f}, Prior={prev_spend:,.2f}, MoM={mom:.1%} (threshold ±{MOM_SPEND_THR:.0%})",
       "STAT-004")

# Missing expected vendor: any vendor active last period now absent?
prior_vendors = set(prior["vendor_id"].dropna().unique())
curr_vendors  = set(raw["vendor_id"].dropna().unique())
missing_vendors = prior_vendors - curr_vendors
record(3, "Tier 2", "Anomaly Detection", "Missing Expected Vendor",
       "PASS" if not missing_vendors else "WARN",
       f"Vendors active last period but absent this period: {missing_vendors}" if missing_vendors else "All prior-period vendors present",
       "STAT-006")

# ══ Step 4: Transform ════════════════════════════════════════════════════
print("\n── Step 4: Transform ─────────────────────────────────────────────")

# Duplicate po_ids (excluding nulls)
non_null_po = raw["po_id"].dropna()
dupes = non_null_po[non_null_po.duplicated()]
record(4, "Tier 1", "Pipeline Processing", "Duplicate Detection (po_id)",
       "PASS" if len(dupes) == 0 else "FAIL",
       f"{len(dupes)} duplicate po_id(s): {list(dupes.unique())}" if len(dupes) else "No duplicate po_ids",
       "STR-004")

# Referential integrity: vendor_id
orphan_vend = raw[~raw["vendor_id"].isin(vendors["vendor_id"])]["vendor_id"].dropna().unique()
record(4, "Tier 2", "Pipeline Processing", "Referential Integrity (vendor_id)",
       "PASS" if len(orphan_vend) == 0 else "WARN",
       f"Orphan vendor_id(s): {list(orphan_vend)}" if len(orphan_vend) else "All vendor_ids valid",
       "SEM-001")

# Referential integrity: product_id
orphan_prod = raw[~raw["product_id"].isin(products["product_id"])]["product_id"].dropna().unique()
record(4, "Tier 2", "Pipeline Processing", "Referential Integrity (product_id)",
       "PASS" if len(orphan_prod) == 0 else "WARN",
       f"Orphan product_id(s): {list(orphan_prod)}" if len(orphan_prod) else "All product_ids valid",
       "SEM-001")

# Transformation check: total_cost should equal quantity * unit_cost
trans_num = trans.copy()
trans_num["expected_cost"] = trans_num["quantity"] * trans_num["unit_cost"]
trans_num["cost_diff"]     = (trans_num["total_cost"] - trans_num["expected_cost"]).abs()
bad_cost = trans_num[trans_num["cost_diff"] > 0.01]
record(4, "Tier 1", "Pipeline Processing", "Transformation Logic (total_cost = qty * unit_cost)",
       "PASS" if len(bad_cost) == 0 else "FAIL",
       f"{len(bad_cost)} rows where total_cost ≠ quantity * unit_cost" if len(bad_cost) else "All cost calculations correct",
       "SEM-002")

# ══ Step 5: Tie Aggregates ═══════════════════════════════════════════════
print("\n── Step 5: Tie Aggregates ────────────────────────────────────────")

detail_spend  = trans["total_cost"].sum()
vendor_spend  = vperf["total_spend"].sum()
gap           = abs(detail_spend - vendor_spend)
record(5, "Tier 2", "Pipeline Processing", "Aggregation Accuracy (spend tie-out)",
       "PASS" if gap < 0.01 else "FAIL",
       f"Detail={detail_spend:,.2f}, Vendor report={vendor_spend:,.2f}, gap={gap:.4f}", "SEM-007")

# ══ Step 6: Output Checks ════════════════════════════════════════════════
print("\n── Step 6: Output Checks ─────────────────────────────────────────")

# Vendor on-time rate floor: any vendor below threshold is a quality flag
low_ontime = vperf[vperf["on_time_rate"] < ON_TIME_FLOOR]
record(6, "Tier 2", "Output Validation", "Vendor On-Time Rate Floor",
       "PASS" if len(low_ontime) == 0 else "WARN",
       f"{len(low_ontime)} vendor(s) below {ON_TIME_FLOOR:.0%} on-time rate: {list(low_ontime['vendor_id'].values)}" if len(low_ontime) else f"All vendors >= {ON_TIME_FLOOR:.0%} on-time",
       "SEM-006, STAT-004")

# Null vendor_name in output (orphan propagated)
null_vendor_name = vperf["vendor_name"].isna().sum()
record(6, "Tier 2", "Output Validation", "Null Vendor Name in Output",
       "PASS" if null_vendor_name == 0 else "WARN",
       f"{null_vendor_name} vendor(s) with null name in performance report" if null_vendor_name else "No null vendor names",
       "STR-003")

# ══ Step 7: Cross-Validate ═══════════════════════════════════════════════
print("\n── Step 7: Cross-Validate ────────────────────────────────────────")

source_total = raw["total_cost"].sum()
output_total = vperf["total_spend"].sum()
var_pct = abs(source_total - output_total) / source_total if source_total else 1
record(7, "Tier 1", "Cross-Validation", "Source vs Output Total Spend",
       "PASS" if var_pct <= COST_VAR_TOL else "FAIL",
       f"Source={source_total:,.2f}, Output={output_total:,.2f}, variance={var_pct:.4%}", "SEM-004")

# ══ Step 8: Regress, Log, Surface ════════════════════════════════════════
print("\n── Step 8: Regress, Log, Surface ─────────────────────────────────")

t1_fails = sum(1 for r in results if r["tier"] == "Tier 1" and r["status"] == "FAIL")
record(8, "Tier 3", "Traditional Software", "Regression Check",
       "PASS" if t1_fails == 0 else "WARN",
       f"{t1_fails} Tier 1 failure(s) in this run", "OPS-001")

# ══ Write outputs ════════════════════════════════════════════════════════
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

with open(LOG_PATH, "w") as f:
    f.write(f"# Run Log -- Supply Chain Pipeline\n\n**Run ID:** {RUN_ID}  \n**Run Date:** {RUN_DATE}  \n\n")
    f.write("| Step | Tier | Category | Test Name | Status | Detail | DPPF IDs |\n|---|---|---|---|---|---|---|\n")
    for r in results:
        f.write(f"| {r['step']} | {r['tier']} | {r['category']} | {r['test_name']} | {r['status']} | {r['detail']} | {r['dppf_ids']} |\n")

tier_weights = {"Tier 1": 5, "Tier 2": 2, "Tier 3": 1}
total_all  = len(results)
passed_all = sum(1 for r in results if r["status"] == "PASS")
failed_all = sum(1 for r in results if r["status"] == "FAIL")
warn_all   = sum(1 for r in results if r["status"] == "WARN")
pass_rate  = passed_all / total_all
t1_fails   = sum(1 for r in results if r["tier"] == "Tier 1" and r["status"] == "FAIL")
max_score  = sum(tier_weights.get(r["tier"], 0) for r in results)
act_score  = sum(tier_weights.get(r["tier"], 0) for r in results if r["status"] == "PASS")
overall    = act_score / max_score if max_score else 0
gate = "BLOCKED" if t1_fails > 0 else ("READY" if pass_rate >= 0.95 else "REVIEW")

with open(SUMMARY_PATH, "w") as f:
    f.write(f"# Summary -- Supply Chain Pipeline\n\n**Run ID:** {RUN_ID}  \n**Run Date:** {RUN_DATE}  \n\n")
    f.write(f"## Gate Status: `{gate}`\n\n")
    f.write(f"| Metric | Value |\n|---|---|\n| Total tests | {total_all} |\n| Passed | {passed_all} |\n")
    f.write(f"| Failed | {failed_all} |\n| Warnings | {warn_all} |\n| Pass rate | {pass_rate:.0%} |\n")
    f.write(f"| Tier 1 failures | {t1_fails} |\n| Overall score | {overall:.0%} |\n\n")
    f.write("## Failures and Warnings\n\n| Tier | Category | Test | Status | Detail |\n|---|---|---|---|---|\n")
    for r in results:
        if r["status"] in ("FAIL", "WARN"):
            f.write(f"| {r['tier']} | {r['category']} | {r['test_name']} | {r['status']} | {r['detail']} |\n")

print(f"\n── Results ───────────────────────────────────────────────────────")
print(f"Gate: {gate} | Pass rate: {pass_rate:.0%} ({passed_all}/{total_all}) | Tier 1 failures: {t1_fails} | Score: {overall:.0%}")
