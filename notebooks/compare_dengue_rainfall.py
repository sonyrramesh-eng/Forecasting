
import pandas as pd
import matplotlib.pyplot as plt

# Load monthly datasets
dengue = pd.read_csv(
    "outputs/karnataka_monthly_dengue_trend.csv"
)

rainfall = pd.read_csv(
    "outputs/karnataka_monthly_rainfall.csv"
)

# Convert month columns to datetime
dengue["month"] = pd.to_datetime(dengue["month"])
rainfall["month"] = pd.to_datetime(rainfall["month"])

# Merge only months available in both datasets
combined = pd.merge(
    dengue,
    rainfall,
    on="month",
    how="inner"
)

combined = combined.sort_values("month").reset_index(drop=True)

# Keep only the overlapping dengue period
combined = combined[
    combined["month"] <= "2024-06-01"
].copy()

# Save comparison dataset
combined.to_csv(
    "outputs/monthly_dengue_rainfall_comparison.csv",
    index=False
)

# Calculate correlations at different rainfall lags
print("\n========== DENGUE AND RAINFALL COMPARISON ==========")

print("Total overlapping months:", len(combined))

print("\nCorrelation between rainfall and dengue cases:")

for lag in range(4):
    rainfall_column = combined["average_district_rainfall_mm"].shift(lag)

    correlation = combined["total_dengue_cases"].corr(
        rainfall_column
    )

    if lag == 0:
        label = "Same month"
    else:
        label = f"Rainfall {lag} month(s) earlier"

    print(f"{label}: {correlation:.3f}")

# Plot dengue and rainfall patterns separately
fig, ax1 = plt.subplots(figsize=(14, 6))

ax1.plot(
    combined["month"],
    combined["total_dengue_cases"],
    color="blue",
    label="Dengue cases"
)

ax1.set_xlabel("Month")
ax1.set_ylabel("Total Dengue Cases", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")

ax2 = ax1.twinx()

ax2.plot(
    combined["month"],
    combined["average_district_rainfall_mm"],
    color="green",
    label="Average district rainfall"
)

ax2.set_ylabel("Average District Rainfall (mm)", color="green")
ax2.tick_params(axis="y", labelcolor="green")

plt.title("Monthly Dengue Cases and Rainfall in Karnataka (2017–June 2024)")
fig.autofmt_xdate()
plt.tight_layout()

plt.savefig(
    "outputs/dengue_rainfall_comparison.png",
    dpi=300
)

plt.show()

print("\nMonthly comparison dataset saved.")
print("outputs/monthly_dengue_rainfall_comparison.csv")
print("outputs/dengue_rainfall_comparison.png")
