
import pandas as pd

# Load original dataset
df = pd.read_csv(
    "data/raw/ka-dengue-daily-summary.csv",
    low_memory=False
)

df["metadata.recordDate"] = pd.to_datetime(
    df["metadata.recordDate"], errors="coerce", utc=True
)

# Select only affected REVENUE records
districts = ["district_525", "district_537"]

df = df[
    (df["location.admin2.ID"].isin(districts)) &
    (df["location.admin.hierarchy"] == "REVENUE")
].copy()

# Find repeated district-date groups
group_columns = [
    "location.admin2.ID",
    "metadata.recordDate"
]

duplicates = df[
    df.duplicated(subset=group_columns, keep=False)
].copy()

# Identify columns with different values
ignored = [
    "metadata.recordID"
]

print("\nCONFLICTING COLUMN SUMMARY")
print("=" * 60)

conflict_counts = {}

for key, group in duplicates.groupby(group_columns):
    different = [
        col for col in group.columns
        if col not in ignored + group_columns
        and group[col].nunique(dropna=False) > 1
    ]

    for col in different:
        conflict_counts[col] = conflict_counts.get(col, 0) + 1

print("Number of conflicting groups:", duplicates.groupby(
    group_columns
).ngroups)

for col, count in sorted(
    conflict_counts.items(),
    key=lambda x: x[1],
    reverse=True
):
    print(f"{col}: {count} groups")

# Inspect representative records
print("\nGADAG SAMPLE: 16 MAY 2024")
print("=" * 60)

gadag = duplicates[
    (duplicates["location.admin2.ID"] == "district_537") &
    (duplicates["metadata.recordDate"] ==
     pd.Timestamp("2024-05-16", tz="UTC"))
]

print(gadag.to_string(index=False))

print("\nBENGALURU URBAN SAMPLE: 8 MAY 2024")
print("=" * 60)

bengaluru = duplicates[
    (duplicates["location.admin2.ID"] == "district_525") &
    (duplicates["metadata.recordDate"] ==
     pd.Timestamp("2024-05-08", tz="UTC"))
]

print(bengaluru.to_string(index=False))

# Save investigation
duplicates.to_csv(
    "outputs/revenue_conflicting_values.csv",
    index=False
)

print("\nInvestigation saved successfully!")
