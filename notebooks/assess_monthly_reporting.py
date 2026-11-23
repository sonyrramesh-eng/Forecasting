
import pandas as pd

# Load the monthly coverage report
df = pd.read_csv("outputs/monthly_dengue_coverage_check.csv")

# Convert month to datetime
df["month"] = pd.to_datetime(df["month"])

# Create a complete monthly calendar
all_months = pd.date_range(
    start=df["month"].min(),
    end=df["month"].max(),
    freq="MS"
)

monthly = (
    df.set_index("month")
    .reindex(all_months)
    .rename_axis("month")
    .reset_index()
)

# Expected active districts
monthly["expected_districts"] = monthly["month"].apply(
    lambda x: 30 if x.year <= 2022 else 31
)

# Number of calendar days
monthly["days_in_month"] = monthly["month"].dt.days_in_month

# Expected district-day records
monthly["expected_records"] = (
    monthly["expected_districts"] *
    monthly["days_in_month"]
)

# Missing record counts are treated as zero for coverage calculation only
monthly["district_date_records"] = (
    monthly["district_date_records"].fillna(0)
)

# Calculate reporting completeness
monthly["reporting_coverage_percent"] = (
    monthly["district_date_records"] /
    monthly["expected_records"] * 100
).round(2)

# Classify months provisionally
monthly["coverage_status"] = monthly[
    "reporting_coverage_percent"
].apply(
    lambda x: "GOOD" if x >= 95 else "INCOMPLETE"
)

# Display report
print("\n========== MONTHLY REPORTING COMPLETENESS ==========\n")

print(
    monthly[
        [
            "month",
            "district_date_records",
            "expected_records",
            "reporting_coverage_percent",
            "coverage_status"
        ]
    ].to_string(index=False)
)

# Save result
monthly.to_csv(
    "outputs/monthly_reporting_completeness.csv",
    index=False
)

print("\nSaved: outputs/monthly_reporting_completeness.csv")
