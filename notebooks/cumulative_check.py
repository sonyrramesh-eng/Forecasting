
import pandas as pd

df = pd.read_csv(
    "data/raw/ka-dengue-daily-summary.csv",
    low_memory=False
)

df = df[
    (df["location.admin1.name"].str.upper() == "KARNATAKA") &
    (df["location.admin.hierarchy"] == "REVENUE") &
    (df["location.admin2.name"].isin(
        ["BENGALURU URBAN", "GADAG"]
    ))
].copy()

df["record_date"] = pd.to_datetime(
    df["metadata.recordDate"],
    errors="coerce",
    utc=True
)

# Convert cumulative columns to numeric for analysis
cols = [
    "cumulative.suspected",
    "cumulative.positive.total",
    "cumulative.deaths"
]

for col in cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.sort_values(
    ["location.admin2.name", "record_date"]
)

print("=" * 60)
print("CUMULATIVE DENGUE TREND CHECK")
print("=" * 60)

for district in ["BENGALURU URBAN", "GADAG"]:

    print("\nDISTRICT:", district)

    district_df = df[
        df["location.admin2.name"] == district
    ]

    print(
        district_df[
            [
                "record_date",
                "daily.positive.total",
                "cumulative.positive.total",
                "cumulative.suspected"
            ]
        ].to_string(index=False)
    )

print("\nCumulative trend investigation completed.")
duplicates = df[
    df.duplicated(
        subset=["location.admin2.ID", "record_date"],
        keep=False
    )
].copy()

columns = [
    "location.admin2.name",
    "location.admin2.ID",
    "record_date",
    "metadata.recordID",
    "location.admin3.ID",
    "location.admin.hierarchy",
    "daily.suspected",
    "daily.positive.total",
    "cumulative.suspected",
    "cumulative.positive.total",
    "cumulative.deaths"
]

duplicates[columns].sort_values(
    ["location.admin2.name", "record_date"]
).to_csv(
    "outputs/cumulative_record_audit.csv",
    index=False
)

print("Audit saved successfully!")