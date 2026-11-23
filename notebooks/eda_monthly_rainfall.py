
import pandas as pd
import matplotlib.pyplot as plt

# Load processed district-level rainfall data
df = pd.read_csv(
    "data/processed/karnataka_district_daily_rainfall.csv"
)

df["Monitoring Date"] = pd.to_datetime(df["Monitoring Date"])

df["month"] = df["Monitoring Date"].dt.to_period("M")

# Calculate monthly rainfall for each district
district_monthly = (
    df.groupby(["District", "month"])
    .agg(
        monthly_rainfall_mm=("average_rainfall_mm", "sum"),
        reporting_days=("Monitoring Date", "nunique")
    )
    .reset_index()
)

# Calculate average monthly rainfall across districts
monthly_rainfall = (
    district_monthly.groupby("month")
    .agg(
        average_district_rainfall_mm=("monthly_rainfall_mm", "mean"),
        districts_reporting=("District", "nunique")
    )
    .reset_index()
)

monthly_rainfall["month"] = (
    monthly_rainfall["month"].dt.to_timestamp()
)

# Save results
monthly_rainfall.to_csv(
    "outputs/karnataka_monthly_rainfall.csv",
    index=False
)

# Plot rainfall trend
plt.figure(figsize=(14, 6))

plt.plot(
    monthly_rainfall["month"],
    monthly_rainfall["average_district_rainfall_mm"]
)

plt.title("Average Monthly Rainfall in Karnataka (2017–2025)")
plt.xlabel("Month")
plt.ylabel("Average District Rainfall (mm)")
plt.xticks(rotation=45)
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig(
    "outputs/monthly_rainfall_trend.png",
    dpi=300
)

plt.show()

print("\n========== MONTHLY RAINFALL ANALYSIS ==========")

print("Total months:", len(monthly_rainfall))

print("\nHighest average district rainfall:")
print(
    monthly_rainfall.loc[
        monthly_rainfall["average_district_rainfall_mm"].idxmax()
    ].to_string()
)

print("\nMonthly rainfall summary:")
print(monthly_rainfall.tail(12).to_string(index=False))

print("\nSaved:")
print("outputs/karnataka_monthly_rainfall.csv")
print("outputs/monthly_rainfall_trend.png")
