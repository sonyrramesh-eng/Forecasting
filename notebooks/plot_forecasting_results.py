import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("outputs/forecasting_model_predictions.csv")

df["month"] = pd.to_datetime(df["month"])

plt.figure(figsize=(12, 6))

plt.plot(df["month"], df["actual_cases"],
         marker="o", label="Actual Cases")

plt.plot(df["month"], df["baseline_prediction"],
         marker="o", label="Baseline")

plt.plot(df["month"], df["model_a_prediction"],
         marker="o", label="Dengue Only")

plt.plot(df["month"], df["model_b_prediction"],
         marker="o", label="Dengue + Rainfall")

plt.title("Actual vs Predicted Dengue Cases")
plt.xlabel("Month")
plt.ylabel("Dengue Cases")

plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.savefig("outputs/actual_vs_predicted_cases.png")
plt.show()

print("Forecast comparison graph saved!")