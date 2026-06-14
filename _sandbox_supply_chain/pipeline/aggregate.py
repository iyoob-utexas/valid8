"""
Build vendor performance report and category spend summary.
Writes output/vendor_performance.csv and output/category_spend.csv.
"""
import pandas as pd, os

TRANSFORMED = os.path.join(os.path.dirname(__file__), "../output/transformed.csv")
VENDOR_PATH = os.path.join(os.path.dirname(__file__), "../output/vendor_performance.csv")
SPEND_PATH  = os.path.join(os.path.dirname(__file__), "../output/category_spend.csv")

df = pd.read_csv(TRANSFORMED)

# Vendor performance: on-time rate, avg lead time, total spend
vendor_perf = (
    df.groupby(["vendor_id", "vendor_name", "category_x"], dropna=False)
    .agg(
        total_orders      = ("po_id",       "count"),
        on_time_orders    = ("on_time",     "sum"),
        avg_lead_time     = ("lead_time_actual", "mean"),
        total_spend       = ("total_cost",  "sum"),
        avg_cost_variance = ("cost_variance_pct", "mean"),
    )
    .reset_index()
)
vendor_perf["on_time_rate"] = vendor_perf["on_time_orders"] / vendor_perf["total_orders"]
vendor_perf.to_csv(VENDOR_PATH, index=False)

# Category spend summary
spend = (
    df.groupby(["order_month", "category_x"], dropna=False)
    .agg(total_spend=("total_cost", "sum"), order_count=("po_id", "count"))
    .reset_index()
    .rename(columns={"category_x": "vendor_category"})
)
spend.to_csv(SPEND_PATH, index=False)

print(f"Vendor performance: {len(vendor_perf)} vendors")
print(f"Category spend: {len(spend)} rows")
print(vendor_perf[["vendor_id","vendor_name","on_time_rate","avg_lead_time","total_spend"]].to_string(index=False))
