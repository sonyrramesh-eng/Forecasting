
import pandas as pd

# Load continuous forecasting dataset
df = pd.read_csv(
    "outputs/karnataka_monthly_forecasting_dataset.csv"
)

df["month"] = pd.to_datetime(df["month"])

df = df.sort_values("month").reset_index(drop=True)

# Previous dengue cases
df["cases_lag_1"] = df["total_cases"].shift(1)
df["cases_lag_2"] = df["total_cases"].shift(2)
df["cases_lag_3"] = df["total_cases"].shift(3)

# Previous rainfall
df["rainfall_lag_1"] = df["average_rainfall_mm"].shift(1)
df["rainfall_lag_2"] = df["average_rainfall_mm"].shift(2)

# Calendar month
df["month_number"] = df["month"].dt.month

# Remove rows without previous-month history
df_features = df.dropna().copy()

# Save feature dataset
df_features.to_csv(
    "outputs/karnataka_forecasting_features.csv",
    index=False
)

print("\n========== FORECASTING FEATURES ==========\n")

print("Original observations:", len(df))
print("Observations after creating lags:", len(df_features))

print("\nColumns:")
print(df_features.columns.tolist())

print("\nFirst 10 rows:")
print(df_features.head(10).to_string(index=False))

print("\nMissing values:")
print(df_features.isnull().sum())

print("\nSaved: outputs/karnataka_forecasting_features.csv")
