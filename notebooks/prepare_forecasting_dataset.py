
import pandas as pd

# Load monthly dengue coverage
coverage = pd.read_csv(
    "outputs/monthly_reporting_completeness.csv"
)

coverage["month"] = pd.to_datetime(coverage["month"])

# Select continuous high-coverage period
start = "2018-06-01"
end = "2021-03-01"

selected_months = coverage[
    (coverage["month"] >= start) &
    (coverage["month"] <= end) &
    (coverage["reporting_coverage_percent"] >= 95)
]["month"]

# Load cleaned dengue and rainfall datasets
dengue = pd.read_csv(
    "outputs/karnataka_primary_eda_dataset.csv"
)

rainfall = pd.read_csv(
    "data/processed/karnataka_district_daily_rainfall.csv"
)

# Prepare dates
dengue["date"] = pd.to_datetime(
    dengue["metadata.recordDate"],
    utc=True
).dt.tz_localize(None)

rainfall["date"] = pd.to_datetime(
    rainfall["Monitoring Date"]
)

# Create month column
dengue["month"] = dengue["date"].dt.to_period("M").dt.to_timestamp()
rainfall["month"] = rainfall["date"].dt.to_period("M").dt.to_timestamp()

# Aggregate statewide monthly dengue cases
monthly_dengue = dengue.groupby("month").agg(
    total_cases=("daily.positive.total", "sum"),
    total_suspected=("daily.suspected", "sum"),
    total_deaths=("daily.deaths", "sum"),
    district_date_records=("location.admin2.name", "count")
).reset_index()

# Aggregate rainfall independently of dengue reporting
monthly_rainfall = rainfall.groupby("month").agg(
    average_rainfall_mm=("average_rainfall_mm", "mean")
).reset_index()

# Merge monthly data
combined = monthly_dengue.merge(
    monthly_rainfall,
    on="month",
    how="left"
)

# Keep selected high-coverage months
combined = combined[
    combined["month"].isin(selected_months)
].sort_values("month")

# Save forecasting dataset
combined.to_csv(
    "outputs/karnataka_monthly_forecasting_dataset.csv",
    index=False
)

print("\n========== FORECASTING DATASET ==========\n")
print("Total months:", len(combined))
print("Start:", combined["month"].min())
print("End:", combined["month"].max())
print("\nMissing values:\n")
print(combined.isnull().sum())
print("\nFirst 10 rows:\n")
print(combined.head(10).to_string(index=False))

print("\nSaved: outputs/karnataka_monthly_forecasting_dataset.csv")
