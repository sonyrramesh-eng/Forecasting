
import csv
from datetime import datetime

file_path = "data/raw/ka-dengue-daily-summary.csv"

with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.DictReader(file)
    rows = list(reader)
    columns = reader.fieldnames

print("=" * 50)
print("KARNATAKA DENGUE DATASET SUMMARY")
print("=" * 50)

# 1. Total records
print("\nTotal Records:", len(rows))

# 2. Total columns
print("Total Columns:", len(columns))

# 3. Standardize district names
districts = sorted(set(
    row["location.admin2.name"].strip().upper()
    for row in rows
    if row["location.admin2.name"].strip()
))

print("\nTotal Districts:", len(districts))
print("\nDistrict Names:")

for district in districts:
    print("-", district)

# 4. Date range
dates = [
    datetime.strptime(
        row["metadata.recordDate"][:10], "%Y-%m-%d"
    ).date()
    for row in rows
    if row["metadata.recordDate"].strip()
]

print("\nEarliest Date:", min(dates))
print("Latest Date:", max(dates))

# 5. Missing values
print("\nMISSING VALUES:")

for column in columns:
    missing = sum(
        1 for row in rows
        if not row[column].strip()
    )
    print(column, ":", missing)

# 6. Duplicate record IDs
record_ids = [row["metadata.recordID"] for row in rows]

print("\nDuplicate Record IDs:",
      len(record_ids) - len(set(record_ids)))

# 7. Duplicate district-date combinations
combinations = [
    (
        row["metadata.recordDate"][:10],
        row["location.admin2.name"].strip().upper()
    )
    for row in rows
]

print("Duplicate District-Date Records:",
      len(combinations) - len(set(combinations)))

print("\nDATASET INSPECTION COMPLETED!")
