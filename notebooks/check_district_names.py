import pandas as pd

dengue = pd.read_csv(
    "outputs/karnataka_primary_eda_dataset.csv"
)

rainfall = pd.read_csv(
    "data/processed/karnataka_district_daily_rainfall.csv"
)

print("\n========== DENGUE DISTRICTS ==========")
print(sorted(dengue["location.admin2.name"].dropna().unique()))

print("\n========== RAINFALL DISTRICTS ==========")
print(sorted(rainfall["District"].dropna().unique()))