
import pandas as pd

df = pd.read_csv(
    "data/raw/ka-dengue-daily-summary.csv",
    low_memory=False
)

df["record_date"] = pd.to_datetime(
    df["metadata.recordDate"],
    errors="coerce",
    utc=True
).dt.date

keys = [
    "location.admin2.ID",
    "location.admin2.name",
    "record_date"
]

metrics = [
    "daily.suspected",
    "daily.positive.total",
    "daily.deaths"
]

# Find groups with different daily values
variation = df.groupby(keys)[metrics].nunique()

conflicting_groups = variation[
    (variation > 1).any(axis=1)
].reset_index()

# Get all records belonging to these groups
details = df.merge(
    conflicting_groups[keys],
    on=keys,
    how="inner"
)

# Save investigation output
details.to_csv(
    "outputs/duplicate_investigation.csv",
    index=False
)

print("Investigation completed.")
print("Conflicting groups:", len(conflicting_groups))
print("Records exported:", len(details))
print("Saved: outputs/duplicate_investigation.csv")
