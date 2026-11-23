
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "outputs" / "karnataka_primary_eda_dataset.csv"
OUTPUT_DIR = BASE_DIR / "outputs" / "dengue_eda"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load cleaned dengue dataset
df = pd.read_csv(INPUT_FILE)

# Convert date and case columns
df["record_date"] = pd.to_datetime(df["record_date"], errors="coerce")
df["daily.positive.total"] = pd.to_numeric(
    df["daily.positive.total"], errors="coerce"
).fillna(0)

# Extract year
df["year"] = df["record_date"].dt.year

# Calculate yearly dengue cases across districts
yearly_cases = (
    df.groupby("year")["daily.positive.total"]
    .sum()
    .reset_index()
)

yearly_cases.columns = ["Year", "Total_Dengue_Cases"]

print("\nYEAR-WISE DENGUE CASES IN KARNATAKA")
print(yearly_cases.to_string(index=False))

# Save results
yearly_cases.to_csv(
    OUTPUT_DIR / "yearly_dengue_cases.csv", index=False
)

# Create bar chart
plt.figure(figsize=(10, 6))
plt.bar(
    yearly_cases["Year"].astype(str),
    yearly_cases["Total_Dengue_Cases"]
)

plt.title("Year-wise Dengue Cases in Karnataka")
plt.xlabel("Year")
plt.ylabel("Total Confirmed Dengue Cases")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "yearly_dengue_cases.png",
    dpi=300
)

plt.show()

print("\nYear-wise analysis completed!")
print("Outputs saved in:", OUTPUT_DIR)
