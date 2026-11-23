
import pandas as pd
from pathlib import Path

df = pd.read_csv(
    "data/raw/ka-dengue-daily-summary.csv",
    low_memory=False
)

df["metadata.recordDate"] = pd.to_datetime(
    df["metadata.recordDate"], errors="coerce", utc=True
)

districts = ["district_525", "district_537"]

df = df[
    (df["location.admin2.ID"].isin(districts)) &
    (df["location.admin.hierarchy"] == "REVENUE")
].copy()

numeric_cols = [
    "daily.suspected",
    "daily.tested",
    "daily.positive.total",
    "cumulative.suspected",
    "cumulative.tested",
    "cumulative.positive.total"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

group_cols = [
    "location.admin2.ID",
    "metadata.recordDate"
]

duplicates = df[
    df.duplicated(subset=group_cols, keep=False)
].copy()

# Rank the two records within each district-date group
duplicates["record_rank"] = (
    duplicates.groupby(group_cols)["cumulative.positive.total"]
    .rank(method="first", ascending=False)
)

duplicates["record_type"] = duplicates["record_rank"].map({
    1: "Higher cumulative record",
    2: "Lower cumulative record"
})

duplicates = duplicates.sort_values(
    ["location.admin2.ID", "record_type", "metadata.recordDate"]
)

# Calculate changes in cumulative values for diagnostic purposes
for col in [
    "cumulative.positive.total",
    "cumulative.suspected",
    "cumulative.tested"
]:
    duplicates[f"change_{col}"] = (
        duplicates.groupby(
            ["location.admin2.ID", "record_type"]
        )[col].diff()
    )

output_cols = [
    "location.admin2.name",
    "metadata.recordDate",
    "record_type",
    "daily.suspected",
    "daily.tested",
    "daily.positive.total",
    "cumulative.suspected",
    "cumulative.tested",
    "cumulative.positive.total",
    "change_cumulative.positive.total",
    "change_cumulative.suspected",
    "change_cumulative.tested"
]

print("\nGADAG CUMULATIVE TREND")
print("=" * 70)

print(
    duplicates[
        duplicates["location.admin2.ID"] == "district_537"
    ][output_cols].to_string(index=False)
)

print("\nBENGALURU URBAN CUMULATIVE TREND")
print("=" * 70)

print(
    duplicates[
        duplicates["location.admin2.ID"] == "district_525"
    ][output_cols].to_string(index=False)
)

Path("outputs").mkdir(exist_ok=True)

duplicates.to_csv(
    "outputs/cumulative_trend_investigation.csv",
    index=False
)

print("\nTrend investigation saved successfully!")
