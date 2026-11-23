
import pandas as pd

# ------------------------------------------------
# 1. LOAD DENGUE DATA
# ------------------------------------------------

dengue = pd.read_csv(
    "outputs/karnataka_dengue_rainfall_combined.csv"
)

dengue["date"] = pd.to_datetime(dengue["date"])
dengue["month"] = dengue["date"].dt.to_period("M")

dengue["district"] = dengue["district"].str.upper()

dengue_monthly = (
    dengue.groupby(["district", "month"])
    .agg(
        dengue_cases=("daily_cases", "sum"),
        dengue_reporting_days=("date", "nunique")
    )
    .reset_index()
)

# ------------------------------------------------
# 2. LOAD INDEPENDENT RAINFALL DATA
# ------------------------------------------------

rain = pd.read_csv(
    "data/processed/karnataka_district_daily_rainfall.csv"
)

rain["Monitoring Date"] = pd.to_datetime(
    rain["Monitoring Date"]
)

rain["month"] = rain["Monitoring Date"].dt.to_period("M")

rain["district"] = rain["District"].str.upper()

# Standardize district names
rain["district"] = rain["district"].replace({
    "BAGALKOT": "BAGALKOTE",
    "CHAMRAJNAGAR": "CHAMARAJANAGARA",
    "VIJAYANAGARA": "VIJAYANAGAR"
})

# Calculate monthly rainfall independently
rain_monthly = (
    rain.groupby(["district", "month"])
    .agg(
        monthly_rainfall_mm=("average_rainfall_mm", "sum"),
        rainfall_reporting_days=("Monitoring Date", "nunique")
    )
    .reset_index()
)

# ------------------------------------------------
# 3. MERGE DENGUE AND RAINFALL
# ------------------------------------------------

combined = pd.merge(
    dengue_monthly,
    rain_monthly,
    on=["district", "month"],
    how="left",
    validate="one_to_one"
)

# ------------------------------------------------
# 4. CALCULATE EXACT CALENDAR-MONTH LAGS
# ------------------------------------------------

results = []

for district, group in combined.groupby("district"):

    group = group.sort_values("month").copy()

    # Create a continuous calendar-month index
    full_months = pd.period_range(
        start="2017-01",
        end="2024-06",
        freq="M"
    )

    group = (
        group.set_index("month")
        .reindex(full_months)
    )

    group.index.name = "month"

    # Rainfall shifted by exact calendar months
    for lag in range(4):

        rainfall_lag = group["monthly_rainfall_mm"].shift(lag)

        valid = pd.concat(
            [
                group["dengue_cases"],
                rainfall_lag
            ],
            axis=1
        ).dropna()

        correlation = valid.iloc[:, 0].corr(
            valid.iloc[:, 1]
        )

        results.append({
            "district": district,
            "rainfall_lag_months": lag,
            "correlation": correlation,
            "months_compared": len(valid)
        })

# ------------------------------------------------
# 5. SAVE VALIDATED RESULTS
# ------------------------------------------------

result_df = pd.DataFrame(results)

result_df.to_csv(
    "outputs/validated_district_correlations.csv",
    index=False
)

print("\n========== VALIDATED DISTRICT CORRELATIONS ==========")

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
print("outputs/validated_district_correlations.csv")
