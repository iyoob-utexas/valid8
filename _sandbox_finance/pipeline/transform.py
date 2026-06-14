"""
Transform GL entries: join to chart of accounts, compute net amounts,
classify by statement type. Writes to output/transformed.csv.
"""
import pandas as pd, os

LANDING     = os.path.join(os.path.dirname(__file__), "../output/landing.csv")
ACCOUNTS    = os.path.join(os.path.dirname(__file__), "../data/dim_accounts.csv")
TRANSFORMED = os.path.join(os.path.dirname(__file__), "../output/transformed.csv")

df  = pd.read_csv(LANDING)
coa = pd.read_csv(ACCOUNTS)

df = df.merge(coa, on="account_id", how="left")

# Net amount: debit minus credit (positive = debit balance)
df["net_amount"] = df["debit"].fillna(0) - df["credit"].fillna(0)

# Statement classification
df["statement"] = df["account_type"].map({
    "Asset": "Balance Sheet",
    "Liability": "Balance Sheet",
    "Equity": "Balance Sheet",
    "Revenue": "Income Statement",
    "Expense": "Income Statement",
})

df.to_csv(TRANSFORMED, index=False)
print(f"Transformed {len(df)} rows. Unmapped accounts: {df['account_type'].isna().sum()}")
