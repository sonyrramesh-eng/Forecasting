
import pandas as pd

file_path = "outputs/karnataka_monthly_forecasting_dataset.csv"

df = pd.read_csv(file_path)

df["month"] = pd.to_datetime(df["month"])

print("\n========== FORECASTING DATASET VALIDATION ==========\n")

# Basic information
print("Total rows:", len(df))
print("Total columns:", len(df.columns))

# Check date range
print("\nDate range:")
print("Start:", df["month"].min())
print("End:", df["month"].max())

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# Check duplicate months
print("\nDuplicate months:", df["month"].duplicated().sum())

# Check missing months in the timeline
expected_months = pd.date_range(
    start=df["month"].min(),
    end=df["month"].max(),
    freq="MS"
)

missing_months = expected_months.difference(df["month"])

print("Missing months:", list(missing_months))

# Check invalid values
print("\nNegative dengue cases:",
      (df["total_cases"] < 0).sum())

print("Negative rainfall values:",
      (df["average_rainfall_mm"] < 0).sum())

# Display summary statistics
print("\nSummary statistics:")
print(df.describe().round(2))

# Final result
if (
    len(df) == 60
    and df["month"].is_monotonic_increasing
    and df["month"].is_unique
    and df.isnull().sum().sum() == 0
    and len(missing_months) == 0
):
    print("\nDataset validation successful!")
else:
    print("\nPlease investigate the validation results.")
