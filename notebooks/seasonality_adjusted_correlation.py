
import pandas as pd

# ==========================================
# 1. LOAD DENGUE DATA
# ==========================================

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

# ==========================================
# 2. LOAD INDEPENDENT RAINFALL DATA
# ==========================================

rain = pd.read_csv(
    "data/processed/karnataka_district_daily_rainfall.csv"
)

rain["Monitoring Date"] = pd.to_datetime(
    rain["Monitoring Date"]
)

rain["month"] = rain["Monitoring Date"].dt.to_period("M")
rain["district"] = rain["District"].str.upper()

rain["district"] = rain["district"].replace({
    "BAGALKOT": "BAGALKOTE",
    "CHAMRAJNAGAR": "CHAMARAJANAGARA",
    "VIJAYANAGARA": "VIJAYANAGAR"
})

rain_monthly = (
    rain.groupby(["district", "month"])
    .agg(
        rainfall_mm=("average_rainfall_mm", "sum"),
        rainfall_reporting_days=("Monitoring Date", "nunique")
    )
    .reset_index()
)

# ==========================================
# 3. MERGE BOTH DATASETS
# ==========================================

combined = pd.merge(
    dengue_monthly,
    rain_monthly,
    on=["district", "month"],
    how="left"
)

# ==========================================
# 4. SEASONALITY-ADJUSTED CORRELATION
# ==========================================

results = []

full_months = pd.period_range(
    start="2017-01",
    end="2024-06",
    freq="M"
)

for district, group in combined.groupby("district"):

    group = (
        group.set_index("month")
        .reindex(full_months)
        .sort_index()
    )

    # Remove normal month-of-year seasonal patterns
    group["dengue_anomaly"] = (
        group["dengue_cases"]
        - group.groupby(group.index.month)["dengue_cases"].transform("mean")
    )

    group["rainfall_anomaly"] = (
        group["rainfall_mm"]
        - group.groupby(group.index.month)["rainfall_mm"].transform("mean")
    )

    # Compare original and adjusted correlations
    for lag in range(4):

        shifted_rainfall = group["rainfall_mm"].shift(lag)
        shifted_anomaly = group["rainfall_anomaly"].shift(lag)

        original_data = pd.concat(
            [group["dengue_cases"], shifted_rainfall],
            axis=1
        ).dropna()

        adjusted_data = pd.concat(
            [group["dengue_anomaly"], shifted_anomaly],
            axis=1
        ).dropna()

        original_corr = original_data.iloc[:, 0].corr(
            original_data.iloc[:, 1]
        )

        adjusted_corr = adjusted_data.iloc[:, 0].corr(
            adjusted_data.iloc[:, 1]
        )

        results.append({
            "district": district,
            "rainfall_lag_months": lag,
            "original_correlation": original_corr,
            "adjusted_correlation": adjusted_corr,
            "months_compared": len(adjusted_data)
        })

# ==========================================
# 5. SAVE RESULTS
# ==========================================

result_df = pd.DataFrame(results)

result_df.to_csv(
    "outputs/seasonality_adjusted_correlations.csv",
    index=False
)

print("\n========== SEASONALITY-ADJUSTED ANALYSIS ==========")

for lag in range(4):

    print(f"\nRainfall lag: {lag} month(s)")

    subset = result_df[
        result_df["rainfall_lag_months"] == lag
    ]

    print(
        subset.sort_values(
            "adjusted_correlation",
            ascending=False
        ).to_string(index=False)
    )

print("\nSaved:")
print("outputs/seasonality_adjusted_correlations.csv")
