"""
Step 1-2 of the valid8 test cycle: Pull & Ingest.
Reads raw CSV and writes it to the landing layer (output/landing.csv).
No validation here -- that is the test runner's job.
"""

import pandas as pd
import os

RAW_PATH = os.path.join(os.path.dirname(__file__), "../data/sales_raw.csv")
LANDING_PATH = os.path.join(os.path.dirname(__file__), "../output/landing.csv")

df = pd.read_csv(RAW_PATH)

os.makedirs(os.path.dirname(LANDING_PATH), exist_ok=True)
df.to_csv(LANDING_PATH, index=False)

print(f"Ingested {len(df)} rows from source to landing layer.")
print(f"Landing file: {LANDING_PATH}")
