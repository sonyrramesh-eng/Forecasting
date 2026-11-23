
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data" / "raw" / "ka-dengue-daily-summary.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load dataset
df = pd.read_csv(INPUT_FILE, low_memory=False)

print("=" * 60)
print("CUMULATIVE RECORD AUDIT")
print("=" * 60)

# Required columns
required_columns = [
    "metadata.recordID",
    "metadata.recordDate",
    "location.admin1.name",
    "location.admin.hierarchy",
    "location.admin2.ID",
    "location.admin2.name",
    "location.admin3.ID",
    "daily.suspected",
    "daily.positive.total",
    "daily.deaths",
    "cumulative.suspected",
    "cumulative.positive.total",
    "cumulative.deaths"
]

missing = [col for col in required_columns if col not in df.columns]

if missing:
    raise ValueError(f"Missing columns: {missing}")

# Filter Karnataka REVENUE records
df = df[
    df["location.admin1.name"].astype(str).str.upper().eq("KARNATAKA")
].copy()

df = df[
    df["location.admin.hierarchy"].astype(str).str.contains(
        "REVENUE", case=False, na=False
    )
].copy()

# Convert dates
df["record_date"] = pd.to_datetime(
    df["metadata.recordDate"], errors="coerce", utc=True
).dt.date

# Convert numerical columns
numeric_columns = [
    "daily.suspected",
    "daily.positive.total",
    "daily.deaths",
    "cumulative.suspected",
    "cumulative.positive.total",
    "cumulative.deaths"
]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Find repeated district-date records
duplicate_mask = df.duplicated(
    subset=["location.admin2.ID", "record_date"],
    keep=False
)

audit = df.loc[duplicate_mask].copy()
audit["record_date"] = df.loc[duplicate_mask, "record_date"]

# Sort records
audit = audit.sort_values(
    ["location.admin2.name", "record_date", "metadata.recordID"]
)

# Save audit
output_file = OUTPUT_DIR / "cumulative_record_audit_full.csv"
audit.to_csv(output_file, index=False)

# Summary
print("\nTotal Karnataka REVENUE records:", len(df))
print("Repeated district-date records:", len(audit))
print(
    "Repeated district-date groups:",
    audit.groupby(
        ["location.admin2.ID", "record_date"]
    ).ngroups
)

print("\nAffected districts:")
print(audit["location.admin2.name"].value_counts())

print("\nAudit saved successfully!")
print("Output:", output_file)
