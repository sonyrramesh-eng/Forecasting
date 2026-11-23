
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = BASE_DIR / "outputs" / "karnataka_primary_eda_dataset.csv"
OUTPUT_DIR = BASE_DIR / "outputs" / "dengue_eda"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(INPUT_FILE)

# Convert relevant columns to numeric
columns = ["daily.suspected", "daily.positive.total"]

for col in columns:
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

# Calculate statewide totals
comparison = pd.DataFrame({
    "Case_Type": ["Suspected Cases", "Confirmed Cases"],
    "Total_Cases": [
        df["daily.suspected"].sum(),
        df["daily.positive.total"].sum()
    ]
})

print("\nSUSPECTED VS CONFIRMED DENGUE CASES")
print(comparison.to_string(index=False))

# Calculate positivity among suspected cases
suspected = df["daily.suspected"].sum()
confirmed = df["daily.positive.total"].sum()

if suspected > 0:
    percentage = (confirmed / suspected) * 100
    print(f"\nConfirmed cases as a percentage of suspected cases: {percentage:.2f}%")

# Save results
comparison.to_csv(
    OUTPUT_DIR / "suspected_vs_confirmed.csv",
    index=False
)

# Plot comparison
plt.figure(figsize=(8, 5))

plt.bar(
    comparison["Case_Type"],
    comparison["Total_Cases"]
)

plt.title("Suspected vs Confirmed Dengue Cases in Karnataka")
plt.xlabel("Case Type")
plt.ylabel("Total Cases")
plt.tight_layout()

plt.savefig(
    OUTPUT_DIR / "suspected_vs_confirmed.png",
    dpi=300
)

plt.show()

print("\nSuspected vs confirmed analysis completed!")
