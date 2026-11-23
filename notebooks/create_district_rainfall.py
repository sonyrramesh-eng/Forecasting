
import pandas as pd
from pathlib import Path

files = [
    "karnataka_rainfall_data_2017_2018.csv",
    "karnataka_rainfall_data_2019_2020.csv",
    "karnataka_rainfall_data_2021_2022.csv",
    "karnataka_rainfall_data_2023_2025.csv"
]

raw_dir = Path("data/raw")
output_dir = Path("data/processed")
output_dir.mkdir(parents=True, exist_ok=True)

frames = []

for filename in files:
    print("Reading:", filename)

    df = pd.read_csv(
        raw_dir / filename,
        low_memory=False
    )

    df["Monitoring Date"] = pd.to_datetime(
        df["Monitoring Date"],
        dayfirst=True,
        errors="coerce"
    )

    df["Rainfall (MM)"] = pd.to_numeric(
        df["Rainfall (MM)"],
        errors="coerce"
    )

    frames.append(df)

rainfall = pd.concat(frames, ignore_index=True)

print("\nCombined records:", len(rainfall))

# Check complete station-date duplicates
duplicate_mask = rainfall.duplicated(
    subset=["Station Code", "Monitoring Date"],
    keep=False
)

print("Repeated station-date records:", duplicate_mask.sum())

# Preserve duplicate records for investigation
rainfall_duplicates = rainfall[duplicate_mask].copy()

rainfall_duplicates.to_csv(
    output_dir / "rainfall_station_date_duplicates.csv",
    index=False
)

# Exclude invalid dates and missing values
rainfall = rainfall.dropna(
    subset=["District", "Monitoring Date", "Rainfall (MM)", "Station Code"]
)

# Do not automatically delete duplicate observations.
# Stop if duplicates exist so we can investigate them first.
if duplicate_mask.sum() > 0:
    print("\nDuplicates found. Saved for investigation.")
    print("District rainfall aggregation has been paused.")
    raise SystemExit

# Aggregate station measurements by district and date
district_rainfall = (
    rainfall.groupby(["District", "Monitoring Date"])
    .agg(
        average_rainfall_mm=("Rainfall (MM)", "mean"),
        total_station_rainfall_mm=("Rainfall (MM)", "sum"),
        reporting_stations=("Station Code", "nunique")
    )
    .reset_index()
)

district_rainfall.to_csv(
    output_dir / "karnataka_district_daily_rainfall.csv",
    index=False
)

print("\nDistrict rainfall dataset created!")
print("Total district-date records:", len(district_rainfall))
print("Districts:", district_rainfall["District"].nunique())
print("Date range:",
      district_rainfall["Monitoring Date"].min(),
      "to",
      district_rainfall["Monitoring Date"].max())

print("\nSample:")
print(district_rainfall.head(10).to_string(index=False))
