
import pandas as pd

# Load cleaned dengue dataset
df = pd.read_csv(
    "outputs/karnataka_primary_eda_dataset.csv"
)

# Convert date column
df["metadata.recordDate"] = pd.to_datetime(
    df["metadata.recordDate"],
    errors="coerce",
    utc=True
)

df = df.dropna(subset=["metadata.recordDate"])

# Extract month
df["month"] = (
    df["metadata.recordDate"]
    .dt.strftime("%Y-%m")
)

# Count records and districts reporting each month
monthly = df.groupby("month").agg(
    district_date_records=("location.admin2.name", "count"),
    districts_reporting=("location.admin2.name", "nunique"),
    total_cases=("daily.positive.total", "sum")
).reset_index()

print("\n========== MONTHLY DENGUE COVERAGE ==========\n")
print(monthly.to_string(index=False))

# Save report
monthly.to_csv(
    "outputs/monthly_dengue_coverage_check.csv",
    index=False
)

print("\nReport saved successfully!")
