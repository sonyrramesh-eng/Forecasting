
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "outputs" / "cumulative_record_audit_full.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load the 128 audited records
df = pd.read_csv(INPUT_FILE, low_memory=False)

print("=" * 60)
print("REPORTING STRUCTURE VALIDATION")
print("=" * 60)

# Prepare date for grouping
df["record_date"] = pd.to_datetime(
    df["metadata.recordDate"],
    errors="coerce",
    utc=True
).dt.date

group_columns = ["location.admin2.ID", "record_date"]

# Check that required columns exist
required = [
    "location.admin2.ID",
    "location.admin2.name",
    "metadata.recordID",
    "record_date"
]

missing = [col for col in required if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

# Administrative and metadata fields
metadata_columns = [
    col for col in df.columns
    if col.startswith("location.") or col.startswith("metadata.")
]

# Exclude record identifiers and date from variation checks
metadata_columns = [
    col for col in metadata_columns
    if col not in [
        "metadata.recordID",
        "metadata.recordDate"
    ]
]

group_results = []

for keys, group in df.groupby(group_columns, dropna=False):

    district_id, record_date = keys

    varying_fields = []

    for col in metadata_columns:
        if group[col].nunique(dropna=False) > 1:
            varying_fields.append(col)

    group_results.append({
        "district_id": district_id,
        "district_name": group["location.admin2.name"].iloc[0],
        "record_date": record_date,
        "record_count": len(group),
        "record_ids": " | ".join(
            group["metadata.recordID"].dropna().astype(str)
        ),
        "varying_metadata_fields": " | ".join(varying_fields)
            if varying_fields else "No metadata differences found",
        "metadata_difference_count": len(varying_fields)
    })

group_report = pd.DataFrame(group_results)

# Count how often each metadata field differs
field_results = []

for col in metadata_columns:
    differing_groups = 0

    for _, group in df.groupby(group_columns, dropna=False):
        if group[col].nunique(dropna=False) > 1:
            differing_groups += 1

    field_results.append({
        "metadata_field": col,
        "groups_with_differences": differing_groups
    })

field_report = pd.DataFrame(field_results)

# Save both reports
group_file = OUTPUT_DIR / "reporting_structure_group_check.csv"
field_file = OUTPUT_DIR / "reporting_structure_field_check.csv"

group_report.to_csv(group_file, index=False)
field_report.to_csv(field_file, index=False)

print("\nTotal repeated groups:", len(group_report))

print("\nDistrict-wise groups:")
print(group_report["district_name"].value_counts())

print("\nMetadata fields with differences:")
print(
    field_report[field_report["groups_with_differences"] > 0]
    .to_string(index=False)
)

print("\nFiles saved:")
print(group_file)
print(field_file)

print("\nReporting structure validation completed!")
