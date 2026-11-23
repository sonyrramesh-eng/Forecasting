
import pandas as pd
from pathlib import Path

files = [
    "karnataka_rainfall_data_2017_2018.csv",
    "karnataka_rainfall_data_2019_2020.csv",
    "karnataka_rainfall_data_2021_2022.csv",
    "karnataka_rainfall_data_2023_2025.csv"
]

for filename in files:
    path = Path("data/raw") / filename

    print("\n" + "=" * 75)
    print("FILE:", filename)
    print("=" * 75)

    total_rows = 0
    missing_rainfall = 0
    invalid_dates = 0
    negative_rainfall = 0

    stations = set()
    districts = set()
    min_date = None
    max_date = None
    columns = None

    for chunk in pd.read_csv(path, chunksize=200000, low_memory=False):

        if columns is None:
            columns = chunk.columns.tolist()

        total_rows += len(chunk)

        chunk["Monitoring Date"] = pd.to_datetime(
            chunk["Monitoring Date"],
            dayfirst=True,
            errors="coerce"
        )

        chunk["Rainfall (MM)"] = pd.to_numeric(
            chunk["Rainfall (MM)"],
            errors="coerce"
        )

        missing_rainfall += chunk["Rainfall (MM)"].isna().sum()
        invalid_dates += chunk["Monitoring Date"].isna().sum()
        negative_rainfall += (chunk["Rainfall (MM)"] < 0).sum()

        stations.update(
            chunk["Station Code"].dropna().unique()
        )

        districts.update(
            chunk["District"].dropna().unique()
        )

        chunk_min = chunk["Monitoring Date"].min()
        chunk_max = chunk["Monitoring Date"].max()

        if pd.notna(chunk_min):
            min_date = chunk_min if min_date is None else min(min_date, chunk_min)

        if pd.notna(chunk_max):
            max_date = chunk_max if max_date is None else max(max_date, chunk_max)

    print("Total rows:", total_rows)
    print("Date range:", min_date, "to", max_date)
    print("Unique stations:", len(stations))
    print("Unique districts:", len(districts))
    print("Missing rainfall values:", missing_rainfall)
    print("Invalid dates:", invalid_dates)
    print("Negative rainfall values:", negative_rainfall)
    print("District names:", sorted(districts))
    print("Columns:", columns)

print("\nRAINfall COVERAGE CHECK COMPLETED!")
