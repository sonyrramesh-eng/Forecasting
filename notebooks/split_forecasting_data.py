
import pandas as pd

# Load forecasting features
df = pd.read_csv(
    "outputs/karnataka_forecasting_features.csv"
)

df["month"] = pd.to_datetime(df["month"])

df = df.sort_values("month").reset_index(drop=True)

# Chronological 80:20 split
split_index = int(len(df) * 0.80)

train = df.iloc[:split_index].copy()
test = df.iloc[split_index:].copy()

print("\n========== TIME SERIES DATA SPLIT ==========\n")

print("Total observations:", len(df))

print("\nTraining observations:", len(train))
print("Training start:", train["month"].min())
print("Training end:", train["month"].max())

print("\nTesting observations:", len(test))
print("Testing start:", test["month"].min())
print("Testing end:", test["month"].max())

# Save separate datasets
train.to_csv(
    "outputs/forecasting_train.csv",
    index=False
)

test.to_csv(
    "outputs/forecasting_test.csv",
    index=False
)

print("\nTraining and testing datasets saved!")
