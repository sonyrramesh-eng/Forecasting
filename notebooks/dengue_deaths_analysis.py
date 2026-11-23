
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "outputs" / "karnataka_primary_eda_dataset.csv"
OUTPUT_DIR = BASE_DIR / "outputs" / "dengue_eda"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

df["record_date"] = pd.to_datetime(df["record_date"], errors="coerce")
df["daily.deaths"] = pd.to_numeric(
    df["daily.deaths"], errors="coerce"
).fillna(0)

df["year"] = df["record_date"].dt.year

# Year-wise deaths
yearly_deaths = (
    df.groupby("year")["daily.deaths"]
    .sum()
    .reset_index()
)

yearly_deaths.columns = ["Year", "Total_Deaths"]

print("\nYEAR-WISE DENGUE DEATHS")
print(yearly_deaths.to_string(index=False))

# District-wise deaths
district_deaths = (
    df.groupby("location.admin2.name")["daily.deaths"]
    .sum()
    .reset_index()
)

district_deaths.columns = ["District", "Total_Deaths"]

district_deaths = district_deaths.sort_values(
    "Total_Deaths", ascending=False
)

print("\nDISTRICT-WISE DENGUE DEATHS")
print(district_deaths.to_string(index=False))

# Save results
yearly_deaths.to_csv(
    OUTPUT_DIR / "yearly_dengue_deaths.csv", index=False
)

district_deaths.to_csv(
    OUTPUT_DIR / "district_wise_dengue_deaths.csv", index=False
)

# Yearly deaths graph
plt.figure(figsize=(10, 6))

plt.bar(
    yearly_deaths["Year"].astype(str),
    yearly_deaths["Total_Deaths"]
)

plt.title("Year-wise Dengue Deaths in Karnataka")
plt.xlabel("Year")
plt.ylabel("Total Reported Deaths")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "yearly_dengue_deaths.png", dpi=300
)

plt.show()

print("\nDengue deaths analysis completed!")
