import pandas as pd
dengue_path = "outputs/karnataka_primary_eda_dataset.csv"
rainfall_path = "data/processed/karnataka_district_daily_rainfall.csv"

dengue = pd.read_csv(dengue_path)
rainfall = pd.read_csv(rainfall_path)

dengue["metadata.recordDate"] = pd.to_datetime(
    dengue["metadata.recordDate"], errors="coerce"
)

rainfall["Monitoring Date"] = pd.to_datetime(
    rainfall["Monitoring Date"], errors="coerce"
)

print("\n========== DENGUE DATE COVERAGE ==========")
print("Start:", dengue["metadata.recordDate"].min())
print("End:", dengue["metadata.recordDate"].max())
print("Unique dates:", dengue["metadata.recordDate"].nunique())

print("\n========== RAINFALL DATE COVERAGE ==========")
print("Start:", rainfall["Monitoring Date"].min())
print("End:", rainfall["Monitoring Date"].max())
print("Unique dates:", rainfall["Monitoring Date"].nunique())

print("\n========== OVERLAPPING DATES ==========")
dengue_dates = set(dengue["metadata.recordDate"].dropna().dt.date)
rainfall_dates = set(rainfall["Monitoring Date"].dropna().dt.date)

common_dates = dengue_dates.intersection(rainfall_dates)

print("Common dates:", len(common_dates))
print("Dengue-only dates:", len(dengue_dates - rainfall_dates))
print("Rainfall-only dates:", len(rainfall_dates - dengue_dates))
