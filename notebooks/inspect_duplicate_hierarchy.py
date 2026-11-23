
import pandas as pd
from pathlib import Path

# Load original dataset
df = pd.read_csv(
    "data/raw/ka-dengue-daily-summary.csv",
    low_memory=False
)

df["metadata.recordDate"] = pd.to_datetime(
    df["metadata.recordDate"], errors="coerce", utc=True
)

# Select the two affected districts
districts = ["district_525", "district_537"]

filtered = df[
    df["location.admin2.ID"].isin(districts)
].copy()

# Columns needed for investigation
columns = [
    "location.admin.hierarchy",
    "location.admin1.name",
    "location.admin2.ID",
    "location.admin2.name",
    "location.admin3.ID",
    "location.admin3.name",
    "metadata.recordDate",
    "metadata.recordID",
    "daily.suspected",
    "daily.tested",
    "daily.positive.total",
    "daily.deaths",
    "cumulative.suspected",
    "cumulative.positive.total",
    "cumulative.deaths"
]

# Keep only columns available in the dataset
columns = [c for c in columns if c in filtered.columns]

result = filtered[columns].sort_values(
    ["location.admin2.ID", "metadata.recordDate"]
)

# Display hierarchy summary
print("\nDISTRICT HIERARCHY SUMMARY")
print("=" * 60)

print(
    result.groupby(
        ["location.admin2.ID", "location.admin2.name",
         "location.admin.hierarchy"],
        dropna=False
    ).agg(
        records=("metadata.recordID", "count"),
        subdistricts=("location.admin3.ID", "nunique")
    ).to_string()
)

print("\nSUBDISTRICT ID AND NAME SUMMARY")
print("=" * 60)

print(
    result.groupby(
        ["location.admin2.name",
         "location.admin3.ID",
         "location.admin3.name"],
        dropna=False
    ).size().to_string()
)

# Save detailed records
Path("outputs").mkdir(exist_ok=True)

result.to_csv(
    "outputs/duplicate_hierarchy_investigation.csv",
    index=False
)

print("\nDetailed investigation saved successfully!")
print("File: outputs/duplicate_hierarchy_investigation.csv")
