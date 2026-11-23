
import pandas as pd
from pathlib import Path

files = [
    "karnataka_rainfall_data_2017_2018.csv",
    "karnataka_rainfall_data_2019_2020.csv",
    "karnataka_rainfall_data_2021_2022.csv",
    "karnataka_rainfall_data_2023_2025.csv"
]

all_station_counts = {}
district_date_counts = {}
duplicate_count = 0

for filename in files:
    path = Path("data/raw") / filename

    print("\nProcessing:", filename)

    for chunk in pd.read_csv(path, chunksize=200000):

        chunk["Monitoring Date"] = pd.to_datetime(
            chunk["Monitoring Date"],
            dayfirst=True,
            errors="coerce"
        )

        # Check repeated station-date records within each chunk
        repeated = chunk.duplicated(
            subset=["Station Code", "Monitoring Date"],
            keep=False
        )

        duplicate_count += repeated.sum()

        # Count unique stations in each district
        for district, group in chunk.groupby("District"):
            if district not in all_station_counts:
                all_station_counts[district] = set()

            all_station_counts[district].update(
                group["Station Code"].dropna().unique()
            )

        # Count observations for each district and date
        counts = (
            chunk.groupby(["District", "Monitoring Date"])
            .size()
        )

        for key, value in counts.items():
            district_date_counts[key] = (
                district_date_counts.get(key, 0) + value
            )

print("\n" + "=" * 70)
print("RAINFALL STATION AUDIT")
print("=" * 70)

print("\nRepeated station-date records found:", duplicate_count)

print("\nUnique stations per district:")
for district in sorted(all_station_counts):
    print(district, ":", len(all_station_counts[district]))

print("\nDistrict-date observation summary:")

summary = pd.Series(district_date_counts)

print("Total district-date combinations:", len(summary))
print("Minimum station observations per district-date:", summary.min())
print("Maximum station observations per district-date:", summary.max())
print("Average station observations per district-date:", round(summary.mean(), 2))

print("\nAudit completed!")
