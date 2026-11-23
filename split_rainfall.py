
import pandas as pd
from pathlib import Path

# Change this to your actual rainfall folder path
folder = Path(r"C:\Users\DELL\Downloads\dengue_2021.csv")

# Select one rainfall CSV file
file_path = folder / "karnataka_rainfall_data_2017_2018.csv"

# Create output folder
output_folder = folder / "small_parts"
output_folder.mkdir(exist_ok=True)

# Split into smaller parts of 50,000 rows
for i, chunk in enumerate(
    pd.read_csv(file_path, chunksize=50000)
):
    output_file = output_folder / f"rainfall_part_{i+1}.csv"
    chunk.to_csv(output_file, index=False)
    print("Saved:", output_file)

print("Splitting completed!")
