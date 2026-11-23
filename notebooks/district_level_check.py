
import pandas as pd
from pathlib import Path

df = pd.read_csv(
    "data/raw/ka-dengue-daily-summary.csv",
    low_memory=False
)

# Keep Karnataka REVENUE records
district_df = df[
    (df["location.admin1.name"].str.upper() == "KARNATAKA") &
    (df["location.admin.hierarchy"] == "REVENUE")
].copy()

district_df["record_date"] = pd.to_datetime(
    district_df["metadata.recordDate"],
    errors="coerce",
    utc=True
).dt.date

keys = ["location.admin2.ID", "record_date"]

metrics = [
    "daily.suspected",
    "daily.positive.total",
    "daily.deaths"
]

# Find repeated district-date records
repeated = district_df[
    district_df.duplicated(subset=keys, keep=False)
]

# Find groups with different daily values
variation = district_df.groupby(keys)[metrics].nunique()

conflicts = variation[
    (variation > 1).any(axis=1)
]

print("=" * 55)
print("KARNATAKA REVENUE DISTRICT INVESTIGATION")
print("=" * 55)

print("Total Karnataka REVENUE records:", len(district_df))

print("Unique districts:",
      district_df["location.admin2.ID"].nunique())

print("Repeated district-date rows:", len(repeated))

print("Conflicting district-date groups:", len(conflicts))

print("\nDistrict names:")
print(sorted(district_df["location.admin2.name"].dropna().unique()))

# Export repeated records for investigation
Path("outputs").mkdir(exist_ok=True)

repeated.to_csv(
    "outputs/repeated_district_records.csv",
    index=False
)

print("\nSaved: outputs/repeated_district_records.csv")

# Export conflicting records
conflict_details = district_df.merge(
    conflicts.reset_index()[keys],
    on=keys,
    how="inner"
)

conflict_details.to_csv(
    "outputs/conflicting_district_records.csv",
    index=False
)

print("Saved: outputs/conflicting_district_records.csv")

print("\nInvestigation completed!")
