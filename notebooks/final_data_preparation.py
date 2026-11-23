
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "raw" / "ka-dengue-daily-summary.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. LOAD ORIGINAL DATASET
# --------------------------------------------------

df = pd.read_csv(INPUT_FILE, low_memory=False)

print("=" * 60)
print("FINAL DATA PREPARATION")
print("=" * 60)

print("\nOriginal dataset records:", len(df))

# --------------------------------------------------
# 3. FILTER KARNATAKA REVENUE RECORDS
# --------------------------------------------------

df = df[
    df["location.admin1.name"].astype(str).str.upper().eq("KARNATAKA")
].copy()

df = df[
    df["location.admin.hierarchy"].astype(str).str.contains(
        "REVENUE", case=False, na=False
    )
].copy()

print("Karnataka REVENUE records:", len(df))

# --------------------------------------------------
# 4. CONVERT DATE AND NUMERIC COLUMNS
# --------------------------------------------------

df["record_date"] = pd.to_datetime(
    df["metadata.recordDate"],
    errors="coerce",
    utc=True
)

numeric_columns = [
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
    "cumulative.deaths",
    "daily.positive.other",
    "cumulative.positive.other"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# --------------------------------------------------
# 5. IDENTIFY CONFLICTING DISTRICT-DATE GROUPS
# --------------------------------------------------

group_columns = [
    "location.admin2.ID",
    "record_date"
]

valid_key = (
    df["location.admin2.ID"].notna() &
    df["record_date"].notna()
)

group_sizes = (
    df.loc[valid_key]
    .groupby(group_columns)["metadata.recordID"]
    .transform("size")
)

conflict_mask = pd.Series(False, index=df.index)
conflict_mask.loc[valid_key] = group_sizes.gt(1).values

df["data_quality_status"] = "OK"
df.loc[conflict_mask, "data_quality_status"] = (
    "CONFLICTING_DISTRICT_DATE"
)

# --------------------------------------------------
# 6. SEPARATE CONFLICTING RECORDS
# --------------------------------------------------

conflicting_records = df[conflict_mask].copy()

# Conservative primary dataset:
# Exclude all records from conflicting district-date groups.
primary_dataset = df[~conflict_mask].copy()

# --------------------------------------------------
# 7. SORT DATASETS
# --------------------------------------------------

sort_columns = [
    "location.admin2.name",
    "record_date",
    "metadata.recordID"
]

df = df.sort_values(sort_columns)
conflicting_records = conflicting_records.sort_values(sort_columns)
primary_dataset = primary_dataset.sort_values(sort_columns)

# --------------------------------------------------
# 8. SAVE THREE OUTPUT FILES
# --------------------------------------------------

df.to_csv(
    OUTPUT_DIR / "karnataka_revenue_with_quality_flags.csv",
    index=False
)

conflicting_records.to_csv(
    OUTPUT_DIR / "karnataka_conflicting_records.csv",
    index=False
)

primary_dataset.to_csv(
    OUTPUT_DIR / "karnataka_primary_eda_dataset.csv",
    index=False
)

# --------------------------------------------------
# 9. VALIDATION SUMMARY
# --------------------------------------------------

print("\n" + "=" * 60)
print("FINAL DATA PREPARATION SUMMARY")
print("=" * 60)

print("Total Karnataka REVENUE records:", len(df))
print("Conflicting records flagged:", len(conflicting_records))
print("Primary EDA dataset records:", len(primary_dataset))

print(
    "Remaining repeated district-date groups:",
    primary_dataset.duplicated(
        subset=group_columns,
        keep=False
    ).sum()
)

print("\nDistricts in primary dataset:")
print(primary_dataset["location.admin2.name"].nunique())

print("\nMissing dates:", df["record_date"].isna().sum())

print("\nFiles saved successfully:")
print("1. karnataka_revenue_with_quality_flags.csv")
print("2. karnataka_conflicting_records.csv")
print("3. karnataka_primary_eda_dataset.csv")

print("\nFinal data preparation completed!")
