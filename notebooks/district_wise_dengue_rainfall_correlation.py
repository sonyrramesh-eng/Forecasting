
import pandas as pd

# Load combined daily dataset
df = pd.read_csv(
    "outputs/karnataka_dengue_rainfall_combined.csv"
)

df["date"] = pd.to_datetime(df["date"])

# Aggregate daily data into district-month data
df["month"] = df["date"].dt.to_period("M")

monthly = (
    df.groupby(["district", "month"])
    .agg(
        dengue_cases=("daily_cases", "sum"),
        rainfall_mm=("average_rainfall_mm", "sum"),
        reporting_days=("date", "nunique")
    )
    .reset_index()
)

results = []

# Calculate district-wise correlations
for district, group in monthly.groupby("district"):

    group = group.sort_values("month").copy()

    for lag in range(4):

        group["rainfall_lag"] = (
            group["rainfall_mm"].shift(lag)
        )

        valid = group[
            ["dengue_cases", "rainfall_lag"]
        ].dropna()

        correlation = valid["dengue_cases"].corr(
            valid["rainfall_lag"]
        )

        results.append({
            "district": district,
            "rainfall_lag_months": lag,
            "correlation": correlation,
            "months_compared": len(valid)
        })

result_df = pd.DataFrame(results)

result_df.to_csv(
    "outputs/district_wise_dengue_rainfall_correlation.csv",
    index=False
)

print("\n========== DISTRICT-WISE CORRELATION ==========")

for lag in range(4):

    print(f"\nRainfall lag: {lag} month(s)")

    subset = result_df[
        result_df["rainfall_lag_months"] == lag
    ]

    print(
        subset.sort_values(
            "correlation",
            ascending=False
        ).to_string(index=False)
    )

print("\nSaved:")
print("outputs/district_wise_dengue_rainfall_correlation.csv")
