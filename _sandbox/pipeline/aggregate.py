"""
Step 5 of the valid8 test cycle: Tie Aggregates.
Rolls up transformed data to monthly totals by category.
Writes to output/sales_report.csv (the final data product).
"""

import pandas as pd
import os

TRANSFORMED_PATH = os.path.join(os.path.dirname(__file__), "../output/transformed.csv")
REPORT_PATH = os.path.join(os.path.dirname(__file__), "../output/sales_report.csv")

df = pd.read_csv(TRANSFORMED_PATH)

# Aggregate: total revenue and order count by category and month
report = (
    df.groupby(["year_month", "category"], dropna=False)
    .agg(
        total_revenue=("revenue", "sum"),
        order_count=("order_id", "count"),
        total_quantity=("quantity", "sum"),
    )
    .reset_index()
)

report.to_csv(REPORT_PATH, index=False)

print(f"Aggregated to {len(report)} category-month rows.")
print(f"Total revenue in report: {report['total_revenue'].sum():.2f}")
