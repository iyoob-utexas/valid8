"""
valid8 test runner -- Financial GL pipeline.
Domain: monthly GL entries -> Income Statement + Balance Sheet.
Follows the 8-step test cycle from docs/process/test-cycle.md.
"""

import pandas as pd, os, collections
from datetime import datetime

BASE          = os.path.dirname(os.path.dirname(__file__))
RAW_PATH      = os.path.join(BASE, "data/gl_raw.csv")
PRIOR_PATH    = os.path.join(BASE, "data/gl_prior.csv")
DIM_ACCT_PATH = os.path.join(BASE, "data/dim_accounts.csv")
DIM_ENT_PATH  = os.path.join(BASE, "data/dim_entities.csv")
LANDING_PATH  = os.path.join(BASE, "output/landing.csv")
TRANS_PATH    = os.path.join(BASE, "output/transformed.csv")
IS_PATH       = os.path.join(BASE, "output/income_statement.csv")
BS_PATH       = os.path.join(BASE, "output/balance_sheet.csv")
LOG_PATH      = os.path.join(BASE, "tests/results/run_log.md")
SUMMARY_PATH  = os.path.join(BASE, "tests/results/summary.md")

RUN_ID   = datetime.now().strftime("RUN-%Y%m%d-%H%M%S")
RUN_DATE = datetime.now().strftime("%Y-%m-%d %H:%M")

EXPECTED_COLS = ["je_id", "period", "entity_id", "account_id", "debit", "credit"]
MOM_THRESHOLD = 0.25   # 25% MoM revenue change
BALANCE_TOL   = 0.01   # balance sheet must balance within $0.01

results = []

def record(step, tier, category, test_name, status, detail, dppf_ids):
    icon = {"PASS": "✓", "FAIL": "✗", "WARN": "⚠"}.get(status, "?")
    print(f"  [{icon}] {test_name}: {detail}")
    results.append({"run_id": RUN_ID, "run_date": RUN_DATE, "step": step,
                     "tier": tier, "category": category, "test_name": test_name,
                     "status": status, "detail": detail, "dppf_ids": dppf_ids})

raw     = pd.read_csv(RAW_PATH)
prior   = pd.read_csv(PRIOR_PATH)
accts   = pd.read_csv(DIM_ACCT_PATH)
ents    = pd.read_csv(DIM_ENT_PATH)
landing = pd.read_csv(LANDING_PATH)
trans   = pd.read_csv(TRANS_PATH)
is_df   = pd.read_csv(IS_PATH)
bs_df   = pd.read_csv(BS_PATH)

# ══ Step 1: Schema & Contract ════════════════════════════════════════════
print("\n── Step 1: Schema & Contract ─────────────────────────────────────")

missing = [c for c in EXPECTED_COLS if c not in raw.columns]
extra   = [c for c in raw.columns   if c not in EXPECTED_COLS]
record(1, "Tier 1", "Source Ingestion", "Schema Presence",
       "PASS" if not missing and not extra else "FAIL",
       f"Missing: {missing} | Extra: {extra}" if missing or extra else f"All {len(EXPECTED_COLS)} columns present",
       "STR-001")

debit_ok  = pd.to_numeric(raw["debit"],  errors="coerce").notna().all()
credit_ok = pd.to_numeric(raw["credit"], errors="coerce").notna().all()
record(1, "Tier 1", "Source Ingestion", "Data Type Conformance",
       "PASS" if debit_ok and credit_ok else "FAIL",
       f"debit_ok={debit_ok}, credit_ok={credit_ok}", "STR-002")

# ══ Step 2: Pull & Ingest ════════════════════════════════════════════════
print("\n── Step 2: Pull & Ingest ─────────────────────────────────────────")

record(2, "Tier 1", "Source Ingestion", "Row Count Reconciliation",
       "PASS" if len(raw) == len(landing) else "FAIL",
       f"Source={len(raw)}, Landing={len(landing)}", "STAT-001")

null_je = raw["je_id"].isna().sum()
record(2, "Tier 1", "Source Ingestion", "Null Key Check (je_id)",
       "PASS" if null_je == 0 else "FAIL",
       f"{null_je} null je_id(s) found" if null_je else "Zero null je_ids", "STR-003")

null_entity = raw["entity_id"].isna().sum()
record(2, "Tier 1", "Source Ingestion", "Null Key Check (entity_id)",
       "PASS" if null_entity == 0 else "FAIL",
       f"{null_entity} null entity_id(s) found" if null_entity else "Zero null entity_ids", "STR-003")

# ══ Step 3: Vs Last Pull (Anomaly Detection) ═════════════════════════════
print("\n── Step 3: Vs Last Pull ──────────────────────────────────────────")

# Revenue = sum of credit on revenue accounts
rev_acct_ids = accts[accts["account_type"] == "Revenue"]["account_id"].tolist()
curr_rev = raw[raw["account_id"].isin(rev_acct_ids)]["credit"].sum()
prev_rev = prior[prior["account_id"].isin(rev_acct_ids)]["credit"].sum()
mom = (curr_rev - prev_rev) / prev_rev if prev_rev else 0
record(3, "Tier 1", "Anomaly Detection", "Period-over-Period Revenue Change",
       "PASS" if abs(mom) <= MOM_THRESHOLD else "FAIL",
       f"Current={curr_rev:,.0f}, Prior={prev_rev:,.0f}, MoM={mom:.1%} (threshold ±{MOM_THRESHOLD:.0%})",
       "STAT-004")

# ══ Step 4: Transform ════════════════════════════════════════════════════
print("\n── Step 4: Transform ─────────────────────────────────────────────")

# Duplicate JE IDs
non_null_je = raw["je_id"].dropna()
dupes = non_null_je[non_null_je.duplicated()]
record(4, "Tier 1", "Pipeline Processing", "Duplicate Detection (je_id)",
       "PASS" if len(dupes) == 0 else "FAIL",
       f"{len(dupes)} duplicate je_id(s): {list(dupes.unique())}" if len(dupes) else "No duplicate je_ids",
       "STR-004")

# Referential integrity: all account_ids in GL must exist in chart of accounts
orphan_accts = raw[~raw["account_id"].isin(accts["account_id"])]["account_id"].unique()
record(4, "Tier 2", "Pipeline Processing", "Referential Integrity (account_id)",
       "PASS" if len(orphan_accts) == 0 else "WARN",
       f"Orphan account_ids: {list(orphan_accts)}" if len(orphan_accts) else "All account_ids valid",
       "SEM-001")

# Referential integrity: entity_ids
orphan_ents = raw[~raw["entity_id"].isin(ents["entity_id"])]["entity_id"].dropna().unique()
record(4, "Tier 2", "Pipeline Processing", "Referential Integrity (entity_id)",
       "PASS" if len(orphan_ents) == 0 else "WARN",
       f"Orphan entity_ids: {list(orphan_ents)}" if len(orphan_ents) else "All entity_ids valid",
       "SEM-001")

# Transformation check: net_amount = debit - credit
trans_check = trans.copy()
trans_check["debit"]  = trans_check["debit"].fillna(0)
trans_check["credit"] = trans_check["credit"].fillna(0)
trans_check["expected_net"] = trans_check["debit"] - trans_check["credit"]
bad = trans_check[(trans_check["net_amount"] - trans_check["expected_net"]).abs() > 0.01]
record(4, "Tier 1", "Pipeline Processing", "Transformation Logic",
       "PASS" if len(bad) == 0 else "FAIL",
       f"{len(bad)} rows where net_amount ≠ debit - credit" if len(bad) else "net_amount correct for all rows",
       "SEM-002")

# ══ Step 5: Tie Aggregates ═══════════════════════════════════════════════
print("\n── Step 5: Tie Aggregates ────────────────────────────────────────")

# Detail net sum must equal IS + BS combined net sum
detail_net  = trans["net_amount"].sum()
is_net      = is_df["net_amount"].sum()
bs_net      = bs_df["net_amount"].sum()
combined    = is_net + bs_net
gap         = abs(detail_net - combined)
record(5, "Tier 2", "Pipeline Processing", "Aggregation Accuracy (detail vs statements)",
       "PASS" if gap < 0.01 else "FAIL",
       f"Detail={detail_net:.2f}, IS+BS={combined:.2f}, gap={gap:.4f}", "SEM-007")

# ══ Step 6: Output Checks ════════════════════════════════════════════════
print("\n── Step 6: Output Checks ─────────────────────────────────────────")

# THE KEY FINANCIAL INVARIANT: Assets = Liabilities + Equity
total_assets = bs_df[bs_df["account_type"] == "Asset"]["net_amount"].sum()
total_liab   = bs_df[bs_df["account_type"] == "Liability"]["net_amount"].sum()
total_equity = bs_df[bs_df["account_type"] == "Equity"]["net_amount"].sum()
# In double-entry: assets (debit) + liabilities (credit, negative net) + equity (credit, negative net) = 0
bs_balance = total_assets + total_liab + total_equity
record(6, "Tier 1", "Output Validation", "Balance Sheet Equation (Assets = Liabilities + Equity)",
       "PASS" if abs(bs_balance) <= BALANCE_TOL else "FAIL",
       f"Assets={total_assets:,.2f}, Liab={total_liab:,.2f}, Equity={total_equity:,.2f}, imbalance={bs_balance:,.2f}",
       "SEM-014, SEM-007")

# Income statement net income sanity: revenue - expenses = net income
total_rev = is_df[is_df["account_type"] == "Revenue"]["net_amount"].sum()
total_exp = is_df[is_df["account_type"] == "Expense"]["net_amount"].sum()
net_income = -total_rev + total_exp   # revenue is credit (negative net); expense is debit (positive net)
# Net income should equal the change in retained earnings
re_change = bs_df[bs_df["account_id"] == 3100]["net_amount"].sum()
# Note: re_change is negative (credit) so net_income should ≈ -re_change
ni_re_gap = abs(net_income - (-re_change))
record(6, "Tier 1", "Output Validation", "Net Income Ties to Retained Earnings",
       "PASS" if ni_re_gap < 1.0 else "FAIL",
       f"Net Income={net_income:,.2f}, RE change={-re_change:,.2f}, gap={ni_re_gap:,.2f}",
       "SEM-015, SEM-004")

# Intercompany elimination: IC entry in E04 should net to zero when paired with E01
ic_entities = ents[ents["is_intercompany"] == "Y"]["entity_id"].tolist()
ic_entries  = trans[trans["entity_id"].isin(ic_entities + ["E01"])]
ic_net      = ic_entries[ic_entries["account_id"].isin([4100])]["net_amount"].sum()
record(6, "Tier 2", "Cross-Validation", "Intercompany Elimination Check",
       "PASS" if abs(ic_net) < 0.01 else "WARN",
       f"IC net across E01 and E04 on account 4100 = {ic_net:,.2f} (should be 0)",
       "SEM-014, SEM-015")

# ══ Step 7: Cross-Validate ═══════════════════════════════════════════════
print("\n── Step 7: Cross-Validate ────────────────────────────────────────")

# Source total debits must equal source total credits (double-entry invariant)
total_debits  = raw["debit"].fillna(0).sum()
total_credits = raw["credit"].fillna(0).sum()
debit_credit_gap = abs(total_debits - total_credits)
record(7, "Tier 1", "Cross-Validation", "Double-Entry Balance (Total Debits = Total Credits)",
       "PASS" if debit_credit_gap < 0.01 else "FAIL",
       f"Total Debits={total_debits:,.2f}, Total Credits={total_credits:,.2f}, gap={debit_credit_gap:,.2f}",
       "SEM-004, SEM-015")

# ══ Step 8: Regress, Log, Surface ════════════════════════════════════════
print("\n── Step 8: Regress, Log, Surface ─────────────────────────────────")

t1_fails = sum(1 for r in results if r["tier"] == "Tier 1" and r["status"] == "FAIL")
record(8, "Tier 3", "Traditional Software", "Regression Check",
       "PASS" if t1_fails == 0 else "WARN",
       f"{t1_fails} Tier 1 failure(s) confirmed in this run", "OPS-001")

# ══ Write outputs ════════════════════════════════════════════════════════
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

with open(LOG_PATH, "w") as f:
    f.write(f"# Run Log -- Finance Pipeline\n\n**Run ID:** {RUN_ID}  \n**Run Date:** {RUN_DATE}  \n\n")
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
    f.write(f"# Summary -- Finance Pipeline\n\n**Run ID:** {RUN_ID}  \n**Run Date:** {RUN_DATE}  \n\n")
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
