
import pandas as pd
from pathlib import Path

# Load original dataset
df = pd.read_csv(
    "data/raw/ka-dengue-daily-summary.csv",
    low_memory=False
)

# Keep Karnataka REVENUE records
df = df[
    (df["location.admin1.name"].str.upper() == "KARNATAKA") &
    (df["location.admin.hierarchy"] == "REVENUE")
].copy()

df["record_date"] = pd.to_datetime(
    df["metadata.recordDate"],
    errors="coerce",
    utc=True
).dt.date

# Identify repeated district-date records
keys = ["location.admin2.ID", "record_date"]

repeated = df[
    df.duplicated(subset=keys, keep=False)
].copy()

# Count groups per district
group_counts = repeated.groupby(
    keys,
    dropna=False
).size().reset_index(name="records_in_group")

print("=" * 60)
print("DISTRICT DUPLICATE AUDIT")
print("=" * 60)

print("\nRepeated groups by district:")

print(
    group_counts.groupby(
        "location.admin2.ID"
    ).size()
)

print("\nTotal repeated groups:", len(group_counts))

# Columns needed for comparison
columns = [
    "metadata.recordID",
    "metadata.recordDate",
    "metadata.ISOWeek",
    "location.admin2.ID",
    "location.admin2.name",
    "daily.suspected",
    "daily.tested",
    "daily.positive.igm",
    "daily.positive.ns1",
    "daily.positive.total",
    "daily.deaths",
    "cumulative.suspected",
    "cumulative.tested",
    "cumulative.positive.igm",
    "cumulative.positive.ns1",
    "cumulative.positive.total",
    "cumulative.deaths"
]

audit = repeated[columns].sort_values(
    ["location.admin2.name", "metadata.recordDate"]
)

# Save audit file
Path("outputs").mkdir(exist_ok=True)

audit.to_csv(
    "outputs/district_duplicate_audit.csv",
    index=False
)

print("\nSaved: outputs/district_duplicate_audit.csv")

print("\nDistrict duplicate audit completed!")
