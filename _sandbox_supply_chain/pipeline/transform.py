"""
Transform PO records: join dimensions, calculate lead time, on-time flag,
cost variance. Writes output/transformed.csv.
"""
import pandas as pd, os

LANDING  = os.path.join(os.path.dirname(__file__), "../output/landing.csv")
VENDORS  = os.path.join(os.path.dirname(__file__), "../data/dim_vendors.csv")
PRODUCTS = os.path.join(os.path.dirname(__file__), "../data/dim_products.csv")
OUT      = os.path.join(os.path.dirname(__file__), "../output/transformed.csv")

df       = pd.read_csv(LANDING)
vendors  = pd.read_csv(VENDORS)
products = pd.read_csv(PRODUCTS)

df = df.merge(vendors,  on="vendor_id",  how="left")
df = df.merge(products, on="product_id", how="left")

# Derived fields
df["expected_delivery"] = pd.to_datetime(df["expected_delivery"])
df["actual_delivery"]   = pd.to_datetime(df["actual_delivery"])
df["order_date"]        = pd.to_datetime(df["order_date"])

df["lead_time_actual"]  = (df["actual_delivery"] - df["order_date"]).dt.days
df["days_late"]         = (df["actual_delivery"] - df["expected_delivery"]).dt.days
df["on_time"]           = df["days_late"] <= 0

# Cost variance: actual total_cost vs expected (quantity * unit_cost)
df["expected_total_cost"] = df["quantity"] * df["unit_cost"]
df["cost_variance"]       = df["total_cost"] - df["expected_total_cost"]
df["cost_variance_pct"]   = df["cost_variance"] / df["expected_total_cost"]

df["order_month"] = df["order_date"].dt.to_period("M").astype(str)

df.to_csv(OUT, index=False)
print(f"Transformed {len(df)} PO records.")
print(f"Orphan vendor_ids: {df['vendor_name'].isna().sum()} | Orphan product_ids: {df['product_name'].isna().sum()}")
