
import pandas as pd

df = pd.read_csv(
    "outputs/karnataka_dengue_rainfall_combined.csv"
)

print("\n========== FINAL DATASET VALIDATION ==========")

print("Total records:", len(df))
print("Unique districts:", df["district"].nunique())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDistrict-wise record counts:")
print(df.groupby("district").size())

print("\nDate range:")
print("Start:", df["date"].min())
print("End:", df["date"].max())

print("\nRainfall summary:")
print(df["average_rainfall_mm"].describe())

print("\nDataset columns:")
print(df.columns.tolist())
