"""
Build income statement and balance sheet from transformed GL data.
Writes output/income_statement.csv and output/balance_sheet.csv.
"""
import pandas as pd, os

TRANSFORMED = os.path.join(os.path.dirname(__file__), "../output/transformed.csv")
IS_PATH     = os.path.join(os.path.dirname(__file__), "../output/income_statement.csv")
BS_PATH     = os.path.join(os.path.dirname(__file__), "../output/balance_sheet.csv")

df = pd.read_csv(TRANSFORMED)

# Income statement: revenue minus expenses by account
is_df = (
    df[df["statement"] == "Income Statement"]
    .groupby(["period", "entity_id", "account_id", "account_name", "account_type"], dropna=False)
    .agg(net_amount=("net_amount", "sum"))
    .reset_index()
)
is_df.to_csv(IS_PATH, index=False)

# Balance sheet: assets, liabilities, equity by account
bs_df = (
    df[df["statement"] == "Balance Sheet"]
    .groupby(["period", "entity_id", "account_id", "account_name", "account_type", "sub_type"], dropna=False)
    .agg(net_amount=("net_amount", "sum"))
    .reset_index()
)
bs_df.to_csv(BS_PATH, index=False)

# Quick totals
total_assets      = bs_df[bs_df["account_type"] == "Asset"]["net_amount"].sum()
total_liabilities = bs_df[bs_df["account_type"] == "Liability"]["net_amount"].sum()
total_equity      = bs_df[bs_df["account_type"] == "Equity"]["net_amount"].sum()
total_revenue     = is_df[is_df["account_type"] == "Revenue"]["net_amount"].sum()
total_expenses    = is_df[is_df["account_type"] == "Expense"]["net_amount"].sum()

print(f"Income Statement: Revenue={-total_revenue:,.2f}  Expenses={total_expenses:,.2f}  Net Income={-total_revenue - total_expenses:,.2f}")
print(f"Balance Sheet:  Assets={total_assets:,.2f}  Liabilities={-total_liabilities:,.2f}  Equity={-total_equity:,.2f}")
print(f"Balance check:  Assets - (Liabilities + Equity) = {total_assets + total_liabilities + total_equity:,.2f}  (should be 0)")
