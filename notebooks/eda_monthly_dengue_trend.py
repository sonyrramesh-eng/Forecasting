
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "outputs/karnataka_dengue_rainfall_combined.csv"
)

df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M")

monthly = (
    df.groupby("month")
    .agg(
        total_dengue_cases=("daily_cases", "sum"),
        total_suspected=("daily_suspected", "sum"),
        total_deaths=("daily_deaths", "sum"),
        districts_reporting=("district", "nunique"),
        district_date_records=("date", "count")
    )
    .reset_index()
)

monthly["month"] = monthly["month"].dt.to_timestamp()

monthly.to_csv(
    "outputs/karnataka_monthly_dengue_trend.csv",
    index=False
)

plt.figure(figsize=(14, 6))
plt.plot(
    monthly["month"],
    monthly["total_dengue_cases"]
)

plt.title("Monthly Dengue Cases in Karnataka (2017–2024)")
plt.xlabel("Month")
plt.ylabel("Total Dengue Cases")
plt.xticks(rotation=45)
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("outputs/monthly_dengue_trend.png", dpi=300)
plt.show()

print("\n========== MONTHLY DENGUE ANALYSIS ==========")
print("Total months:", len(monthly))
print("Total dengue cases:", monthly["total_dengue_cases"].sum())

print("\nMonthly reporting coverage:")
print(
    monthly[
        ["month", "districts_reporting", "district_date_records"]
    ].tail(8).to_string(index=False)
)

print("\nHighest monthly cases:")
print(
    monthly.loc[monthly["total_dengue_cases"].idxmax()].to_string()
)

print("\nSaved updated monthly analysis.")
