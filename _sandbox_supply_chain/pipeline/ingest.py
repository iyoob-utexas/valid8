"""Ingest PO data to landing layer."""
import pandas as pd, os

RAW     = os.path.join(os.path.dirname(__file__), "../data/po_raw.csv")
LANDING = os.path.join(os.path.dirname(__file__), "../output/landing.csv")

df = pd.read_csv(RAW)
os.makedirs(os.path.dirname(LANDING), exist_ok=True)
df.to_csv(LANDING, index=False)
print(f"Ingested {len(df)} PO records to landing.")
