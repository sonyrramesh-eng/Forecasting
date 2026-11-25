
import pandas as pd

df = pd.read_csv("outputs/forecasting_model_predictions.csv")

df["month"] = pd.to_datetime(df["month"], errors="coerce")

print("\nFIRST 10 ROWS:")
print(df.head(10).to_string(index=False))

print("\nLAST 10 ROWS:")
print(df.tail(10).to_string(index=False))

print("\nDATE RANGE:")
print("First date:", df["month"].min())
print("Last date:", df["month"].max())

print("\nACTUAL CASES:")
print("Available:", df["actual_cases"].notna().sum())
print("Missing:", df["actual_cases"].isna().sum())

print("\nMODEL A PREDICTIONS:")
print(df["model_a_prediction"].tail(10).to_list())

print("\nMODEL B PREDICTIONS:")
print(df["model_b_prediction"].tail(10).to_list())
