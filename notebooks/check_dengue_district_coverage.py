
import pandas as pd

df = pd.read_csv(
    "outputs/karnataka_dengue_rainfall_combined.csv"
)

df["date"] = pd.to_datetime(df["date"])

coverage = (
    df.groupby("district")
    .agg(
        total_records=("date", "count"),
        first_date=("date", "min"),
        last_date=("date", "max"),
        unique_dates=("date", "nunique")
    )
    .reset_index()
)

coverage["missing_dates_within_global_range"] = (
    2380 - coverage["unique_dates"]
)

print("\n========== DISTRICT COVERAGE REPORT ==========")
print(coverage.to_string(index=False))

coverage.to_csv(
    "outputs/dengue_district_coverage_report.csv",
    index=False
)

print("\nSaved: outputs/dengue_district_coverage_report.csv")
