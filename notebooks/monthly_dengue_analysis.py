
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

# Extract month and year
df["month"] = df["record_date"].dt.month
df["year"] = df["record_date"].dt.year

# Monthly totals across all years
monthly_cases = (
    df.groupby("month")["daily.positive.total"]
    .sum()
    .reindex(range(1, 13), fill_value=0)
    .reset_index()
)

monthly_cases.columns = ["Month", "Total_Dengue_Cases"]

month_names = {
    1: "January", 2: "February", 3: "March",
    4: "April", 5: "May", 6: "June",
    7: "July", 8: "August", 9: "September",
    10: "October", 11: "November", 12: "December"
}

monthly_cases["Month_Name"] = monthly_cases["Month"].map(month_names)

print("\nMONTH-WISE DENGUE CASES")
print(monthly_cases[["Month_Name", "Total_Dengue_Cases"]].to_string(index=False))

# Save results
monthly_cases.to_csv(
    OUTPUT_DIR / "monthly_dengue_cases.csv", index=False
)

# Plot
plt.figure(figsize=(11, 6))

plt.plot(
    monthly_cases["Month_Name"],
    monthly_cases["Total_Dengue_Cases"],
    marker="o"
)

plt.title("Monthly Dengue Cases in Karnataka (2017–2024)")
plt.xlabel("Month")
plt.ylabel("Total Confirmed Dengue Cases")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "monthly_dengue_cases.png", dpi=300)
plt.show()

# Check yearly date coverage
print("\nDATE COVERAGE BY YEAR")
print(
    df.groupby("year")["record_date"]
    .agg(["min", "max"])
    .to_string()
)

print("\nMonthly analysis completed!")
