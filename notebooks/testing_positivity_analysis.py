
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "outputs" / "karnataka_primary_eda_dataset.csv"
OUTPUT_DIR = BASE_DIR / "outputs" / "dengue_eda"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

df["record_date"] = pd.to_datetime(df["record_date"], errors="coerce")

for col in ["daily.tested", "daily.positive.total"]:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Overall testing summary
total_tested = df["daily.tested"].sum()
total_confirmed = df["daily.positive.total"].sum()

positivity_rate = (
    total_confirmed / total_tested * 100
    if total_tested > 0 else 0
)

print("\nOVERALL DENGUE TESTING SUMMARY")
print("Total tests:", total_tested)
print("Total confirmed cases:", total_confirmed)
print(f"Testing positivity rate: {positivity_rate:.2f}%")

# Year-wise testing analysis
df["year"] = df["record_date"].dt.year

yearly_testing = (
    df.groupby("year")
    .agg(
        Total_Tested=("daily.tested", "sum"),
        Confirmed_Cases=("daily.positive.total", "sum")
    )
    .reset_index()
)

yearly_testing["Positivity_Rate_Percent"] = (
    yearly_testing["Confirmed_Cases"] /
    yearly_testing["Total_Tested"].replace(0, float("nan")) * 100
)

print("\nYEAR-WISE TESTING AND POSITIVITY")
print(yearly_testing.to_string(index=False))

# Save results
yearly_testing.to_csv(
    OUTPUT_DIR / "yearly_testing_positivity.csv",
    index=False
)

# Plot yearly positivity rate
plt.figure(figsize=(10, 6))

plt.plot(
    yearly_testing["year"],
    yearly_testing["Positivity_Rate_Percent"],
    marker="o"
)

plt.title("Year-wise Dengue Testing Positivity Rate")
plt.xlabel("Year")
plt.ylabel("Positivity Rate (%)")
plt.grid(True)
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "yearly_testing_positivity.png",
    dpi=300
)

plt.show()

print("\nTesting and positivity analysis completed!")
