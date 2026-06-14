"""Ingest GL raw entries to landing layer."""
import pandas as pd, os

RAW     = os.path.join(os.path.dirname(__file__), "../data/gl_raw.csv")
LANDING = os.path.join(os.path.dirname(__file__), "../output/landing.csv")

df = pd.read_csv(RAW)
os.makedirs(os.path.dirname(LANDING), exist_ok=True)
df.to_csv(LANDING, index=False)
print(f"Ingested {len(df)} GL entries to landing.")
