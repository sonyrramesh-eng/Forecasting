
import pandas as pd

df = pd.read_csv(
    "data/raw/ka-dengue-daily-summary.csv",
    low_memory=False
)

df["metadata.recordDate"] = pd.to_datetime(
    df["metadata.recordDate"],
    errors="coerce",
    utc=True
)

districts = ["district_525", "district_537"]

df = df[
    (df["location.admin2.ID"].isin(districts)) &
    (df["location.admin.hierarchy"] == "REVENUE")
].copy()

group_cols = [
    "location.admin2.ID",
    "metadata.recordDate"
]

duplicates = df[
    df.duplicated(subset=group_cols, keep=False)
].copy()

metadata_cols = [
    "metadata.recordID",
    "metadata.recordDate",
    "metadata.ISOWeek",
    "metadata.diseaseName",
    "metadata.diseaseCode",
    "location.country.ID",
    "location.country.name",
    "location.admin.hierarchy",
    "location.admin1.ID",
    "location.admin1.name",
    "location.admin2.ID",
    "location.admin2.name",
    "location.admin3.ID",
    "location.admin3.name"
]

for district in districts:
    print("\n" + "=" * 80)
    print("DISTRICT:", district)
    print("=" * 80)

    sample = duplicates[
        duplicates["location.admin2.ID"] == district
    ]

    for date, group in sample.groupby("metadata.recordDate"):
        print("\nDATE:", date)

        print(
            group[metadata_cols].to_string(index=False)
        )

        break
