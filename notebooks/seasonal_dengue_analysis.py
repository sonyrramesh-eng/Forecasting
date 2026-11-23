
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "outputs" / "karnataka_primary_eda_dataset.csv"
OUTPUT_DIR = BASE_DIR / "outputs" / "dengue_eda"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

df["record_date"] = pd.to_datetime(df["record_date"], errors="coerce")
df["daily.positive.total"] = pd.to_numeric(
    df["daily.positive.total"], errors="coerce"
).fillna(0)

df["Year"] = df["record_date"].dt.year
df["Month"] = df["record_date"].dt.month

# Monthly dengue cases for each year
heatmap_data = df.pivot_table(
    index="Month",
    columns="Year",
    values="daily.positive.total",
    aggfunc="sum"
)

month_names = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

heatmap_data = heatmap_data.reindex(range(1, 13))
heatmap_data.index = month_names

print("\nMONTH-WISE DENGUE CASES BY YEAR")
print(heatmap_data.to_string())

# Save table
heatmap_data.to_csv(
    OUTPUT_DIR / "seasonal_dengue_heatmap_data.csv"
)

# Draw heatmap using Matplotlib
plt.figure(figsize=(12, 7))

plt.imshow(
    heatmap_data,
    aspect="auto",
    cmap="YlOrRd"
)

plt.colorbar(label="Confirmed Dengue Cases")

plt.xticks(
    range(len(heatmap_data.columns)),
    heatmap_data.columns
)

plt.yticks(
    range(12),
    month_names
)

plt.xlabel("Year")
plt.ylabel("Month")
plt.title("Seasonal Dengue Patterns in Karnataka (2017–2024)")

plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "seasonal_dengue_heatmap.png",
    dpi=300
)

plt.show()

print("\nSeasonal dengue analysis completed!")
