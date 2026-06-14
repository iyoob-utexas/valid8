"""
Step 4 of the valid8 test cycle: Transform.
Reads from landing layer, joins to product dimension, adds derived fields,
writes to output/transformed.csv.
"""

import pandas as pd
import os

LANDING_PATH = os.path.join(os.path.dirname(__file__), "../output/landing.csv")
DIM_PATH = os.path.join(os.path.dirname(__file__), "../data/dim_product.csv")
TRANSFORMED_PATH = os.path.join(os.path.dirname(__file__), "../output/transformed.csv")

df = pd.read_csv(LANDING_PATH)
dim = pd.read_csv(DIM_PATH)

# Join product dimension -- orphan rows get NaN category/name
df = df.merge(dim, on="product_id", how="left")

# Derived field: revenue per unit (used to check plausibility)
df["revenue_per_unit"] = df["revenue"] / df["quantity"]

# Parse date
df["date"] = pd.to_datetime(df["date"])
df["year_month"] = df["date"].dt.to_period("M").astype(str)

df.to_csv(TRANSFORMED_PATH, index=False)

print(f"Transformed {len(df)} rows.")
print(f"Orphan product_ids (no dimension match): {df['category'].isna().sum()}")
