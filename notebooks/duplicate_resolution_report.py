
import pandas as pd
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "outputs" / "cumulative_record_audit_full.csv"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load full audit
df = pd.read_csv(INPUT_FILE, low_memory=False)

print("=" * 60)
print("DUPLICATE RESOLUTION REPORT")
print("=" * 60)

# Convert date
df["metadata.recordDate"] = pd.to_datetime(
    df["metadata.recordDate"], errors="coerce", utc=True
)

# Identify repeated groups
group_columns = [
    "location.admin2.ID",
    "metadata.recordDate"
]

grouped = df.groupby(group_columns, dropna=False)

report = grouped.agg(
    district_name=("location.admin2.name", "first"),
    record_count=("metadata.recordID", "count"),
    record_ids=("metadata.recordID",
                lambda x: " | ".join(x.dropna().astype(str))),
    subdistrict_ids=("location.admin3.ID",
                     lambda x: " | ".join(x.dropna().astype(str))),
    daily_suspected_values=("daily.suspected",
                            lambda x: " | ".join(x.dropna().astype(str))),
    daily_positive_values=("daily.positive.total",
                           lambda x: " | ".join(x.dropna().astype(str))),
    cumulative_suspected_values=("cumulative.suspected",
                                  lambda x: " | ".join(x.dropna().astype(str))),
    cumulative_positive_values=("cumulative.positive.total",
                                lambda x: " | ".join(x.dropna().astype(str)))
).reset_index()

# Flag records for manual investigation
report["resolution_status"] = "UNRESOLVED - DO NOT DELETE"
report["recommended_action"] = (
    "Investigate source reporting structure before selecting a record"
)

# Save report
output_file = OUTPUT_DIR / "duplicate_resolution_report.csv"
report.to_csv(output_file, index=False)

print("\nTotal repeated groups:", len(report))
print("\nDistrict-wise groups:")
print(report["district_name"].value_counts())

print("\nResolution status:")
print(report["resolution_status"].value_counts())

print("\nReport saved successfully!")
print("Output:", output_file)
