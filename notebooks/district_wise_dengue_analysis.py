
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "outputs" / "karnataka_primary_eda_dataset.csv"
OUTPUT_DIR = BASE_DIR / "outputs" / "dengue_eda"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load cleaned dataset
df = pd.read_csv(INPUT_FILE)

# Prepare columns
df["daily.positive.total"] = pd.to_numeric(
    df["daily.positive.total"], errors="coerce"
).fillna(0)

# District-wise total confirmed cases
district_cases = (
    df.groupby("location.admin2.name")["daily.positive.total"]
    .sum()
    .reset_index()
)

district_cases.columns = ["District", "Total_Dengue_Cases"]

district_cases = district_cases.sort_values(
    by="Total_Dengue_Cases", ascending=False
)

print("\nDISTRICT-WISE DENGUE CASES IN KARNATAKA")
print(district_cases.to_string(index=False))

# Save complete district results
district_cases.to_csv(
    OUTPUT_DIR / "district_wise_dengue_cases.csv",
    index=False
)

# Plot all districts
plt.figure(figsize=(12, 10))

plt.barh(
    district_cases["District"],
    district_cases["Total_Dengue_Cases"]
)

plt.title("District-wise Dengue Cases in Karnataka (2017–2024)")
plt.xlabel("Total Confirmed Dengue Cases")
plt.ylabel("District")
plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "district_wise_dengue_cases.png",
    dpi=300
)

plt.show()

print("\nDistrict-wise analysis completed!")
