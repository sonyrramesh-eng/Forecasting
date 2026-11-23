
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "data/raw/ka-dengue-daily-summary.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(INPUT_FILE, low_memory=False)

# Filter Karnataka REVENUE records
df = df[
    df["location.admin1.name"].astype(str).str.strip().str.upper().eq("KARNATAKA")
    & df["location.admin.hierarchy"].astype(str).str.strip().str.upper().eq("REVENUE")
].copy()

# Standardize district names
df["location.admin2.name"] = (
    df["location.admin2.name"].astype("string").str.strip().str.upper()
)

# Correctly parse mixed date formats
df["record_date"] = pd.to_datetime(
    df["metadata.recordDate"],
    format="mixed",
    errors="coerce",
    utc=True
)

print("KARNATAKA DUPLICATE INVESTIGATION")
print("=" * 50)

print("Total Revenue records:", len(df))
print("Invalid dates:", df["record_date"].isna().sum())

# Find duplicate district-date records
keys = ["location.admin2.ID", "record_date"]

duplicates = df[
    df.duplicated(subset=keys, keep=False)
].copy()

print("Duplicate rows:", len(duplicates))
print("Duplicate groups:",
      duplicates.groupby(keys).ngroups)

# Display conflicting case values
columns = keys + [
    "location.admin2.name",
    "metadata.recordID",
    "daily.suspected",
    "daily.positive.total",
    "daily.deaths",
    "cumulative.positive.total",
    "cumulative.deaths"
]

print("\nDUPLICATE RECORD DETAILS")
print(duplicates[columns].sort_values(keys).to_string(index=False))

# Save investigation report
duplicates.to_csv(
    OUTPUT_DIR / "duplicate_investigation_corrected.csv",
    index=False
)

print("\nReport saved successfully!")
