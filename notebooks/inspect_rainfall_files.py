
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

    print("\n" + "=" * 80)
    print("FILE:", filename)
    print("=" * 80)

    # Read only 5 rows, not the entire large dataset
    df = pd.read_csv(path, nrows=5, low_memory=False)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.to_string(index=False))

    print("\nFile size (MB):", round(path.stat().st_size / (1024 * 1024), 2))

print("\nAll rainfall files inspected!")
