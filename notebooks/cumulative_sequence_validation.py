
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "raw" / "ka-dengue-daily-summary.csv"
DUPLICATE_FILE = BASE_DIR / "outputs" / "reporting_structure_group_check.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load original dataset and repeated-date groups
df = pd.read_csv(INPUT_FILE, low_memory=False)
duplicates = pd.read_csv(DUPLICATE_FILE)

# Filter Karnataka REVENUE records
df = df[
    df["location.admin1.name"].astype(str).str.upper().eq("KARNATAKA")
].copy()

df = df[
    df["location.admin.hierarchy"].astype(str).str.contains(
        "REVENUE", case=False, na=False
    )
].copy()

# Parse dates
df["record_date"] = pd.to_datetime(
    df["metadata.recordDate"], errors="coerce", utc=True
).dt.date

duplicates["record_date"] = pd.to_datetime(
    duplicates["record_date"], errors="coerce"
).dt.date

# Convert case metrics to numeric
metrics = [
    "daily.suspected",
    "daily.positive.total",
    "daily.deaths",
    "cumulative.suspected",
    "cumulative.positive.total",
    "cumulative.deaths"
]

for col in metrics:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Get affected district IDs
district_ids = duplicates["district_id"].dropna().unique()

# Select records around the repeated dates
selected = []

for district_id in district_ids:
    district_duplicates = duplicates[
        duplicates["district_id"] == district_id
    ]

    dates = pd.to_datetime(
        district_duplicates["record_date"]
    )

    start_date = (dates.min() - pd.Timedelta(days=7)).date()
    end_date = (dates.max() + pd.Timedelta(days=7)).date()

    district_data = df[
        (df["location.admin2.ID"] == district_id) &
        (df["record_date"] >= start_date) &
        (df["record_date"] <= end_date)
    ].copy()

    selected.append(district_data)

result = pd.concat(selected, ignore_index=True)

# Sort without removing repeated records
result = result.sort_values(
    ["location.admin2.name", "record_date", "metadata.recordID"]
)

# Save timeline
output_file = OUTPUT_DIR / "cumulative_sequence_validation.csv"
result.to_csv(output_file, index=False)

print("=" * 60)
print("CUMULATIVE SEQUENCE VALIDATION")
print("=" * 60)

print("Total timeline records:", len(result))
print("\nDistrict-wise records:")
print(result["location.admin2.name"].value_counts())

print("\nDate range:")
print(result["record_date"].min(), "to", result["record_date"].max())

print("\nRepeated district-date groups in timeline:",
      result.duplicated(
          subset=["location.admin2.ID", "record_date"],
          keep=False
      ).sum())

print("\nSaved:", output_file)
print("\nValidation timeline generated successfully!")
