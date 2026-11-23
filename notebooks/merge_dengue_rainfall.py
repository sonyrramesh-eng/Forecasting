
import pandas as pd

# Load datasets
dengue = pd.read_csv(
    "outputs/karnataka_primary_eda_dataset.csv"
)

rainfall = pd.read_csv(
    "data/processed/karnataka_district_daily_rainfall.csv"
)

# Standardize district names
dengue["district"] = (
    dengue["location.admin2.name"].str.strip().str.upper()
)

rainfall["district"] = (
    rainfall["District"].str.strip().str.upper()
)

# Correct district spelling differences
rainfall["district"] = rainfall["district"].replace({
    "BAGALKOT": "BAGALKOTE",
    "CHAMRAJNAGAR": "CHAMARAJANAGARA",
    "VIJAYANAGARA": "VIJAYANAGAR"
})

# Standardize dates
dengue["date"] = pd.to_datetime(
    dengue["metadata.recordDate"], errors="coerce", utc=True
).dt.date

rainfall["date"] = pd.to_datetime(
    rainfall["Monitoring Date"], errors="coerce"
).dt.date

# Aggregate dengue to one row per district-date
dengue_daily = (
    dengue.groupby(["district", "date"], as_index=False)
    .agg(
        daily_cases=("daily.positive.total", "sum"),
        daily_suspected=("daily.suspected", "sum"),
        daily_deaths=("daily.deaths", "sum")
    )
)

# Keep rainfall measures needed for analysis
rainfall_daily = rainfall[
    [
        "district",
        "date",
        "average_rainfall_mm",
        "reporting_stations"
    ]
].copy()

# Merge
combined = pd.merge(
    dengue_daily,
    rainfall_daily,
    on=["district", "date"],
    how="left",
    validate="one_to_one"
)

# Check results
print("\n========== MERGE RESULTS ==========")
print("Dengue district-date records:", len(dengue_daily))
print("Rainfall district-date records:", len(rainfall_daily))
print("Combined records:", len(combined))
print("Missing rainfall values:", combined["average_rainfall_mm"].isna().sum())
print("Districts:", combined["district"].nunique())

# Save
output_path = "outputs/karnataka_dengue_rainfall_combined.csv"
combined.to_csv(output_path, index=False)

print("\nCombined dataset saved:", output_path)
print("\nSample:")
print(combined.head(10).to_string(index=False))
