
import pandas as pd

dengue = pd.read_csv(
    "outputs/karnataka_primary_eda_dataset.csv"
)

rainfall = pd.read_csv(
    "data/processed/karnataka_district_daily_rainfall.csv"
)

# Apply the same district standardization used during merging
dengue["district"] = (
    dengue["location.admin2.name"].str.strip().str.upper()
)

rainfall["district"] = (
    rainfall["District"].str.strip().str.upper()
)


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

# Create unique district-date keys
dengue_keys = dengue[["district", "date"]].drop_duplicates()

rainfall_keys = rainfall[["district", "date"]].drop_duplicates()

# Find district-date combinations without rainfall
comparison = dengue_keys.merge(
    rainfall_keys,
    on=["district", "date"],
    how="left",
    indicator=True
)

missing = comparison[comparison["_merge"] == "left_only"].copy()

print("\n========== MISSING RAINFALL AUDIT ==========")
print("Unique dengue district-date combinations:", len(dengue_keys))
print("Unique rainfall district-date combinations:", len(rainfall_keys))
print("Missing district-date combinations:", len(missing))

print("\n========== MISSING RECORDS BY DISTRICT ==========")
print(missing.groupby("district").size().sort_values(ascending=False))

print("\n========== SAMPLE MISSING DATES ==========")
print(missing.head(20).to_string(index=False))

# Save missing combinations for further investigation
missing.to_csv(
    "outputs/missing_rainfall_district_dates.csv",
    index=False
)

print("\nSaved: outputs/missing_rainfall_district_dates.csv")
