
import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Load training and testing datasets
train = pd.read_csv("outputs/forecasting_train.csv")
test = pd.read_csv("outputs/forecasting_test.csv")

# Target variable
target = "total_cases"

# Model A: Dengue history only
features_a = [
    "cases_lag_1",
    "cases_lag_2",
    "cases_lag_3",
    "month_number"
]

# Model B: Dengue history + rainfall
features_b = features_a + [
    "rainfall_lag_1",
    "rainfall_lag_2"
]

# Prepare data
X_train_a = train[features_a]
X_test_a = test[features_a]

X_train_b = train[features_b]
X_test_b = test[features_b]

y_train = train[target]
y_test = test[target]

# Baseline prediction
baseline_predictions = test["cases_lag_1"].values

# Train Model A
model_a = LinearRegression()
model_a.fit(X_train_a, y_train)

predictions_a = model_a.predict(X_test_a)

# Train Model B
model_b = LinearRegression()
model_b.fit(X_train_b, y_train)

predictions_b = model_b.predict(X_test_b)

# Prevent negative predicted case counts
baseline_predictions = np.maximum(baseline_predictions, 0)
predictions_a = np.maximum(predictions_a, 0)
predictions_b = np.maximum(predictions_b, 0)

# Evaluation function
def evaluate(name, actual, predicted):
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))

    return {
        "Model": name,
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2)
    }

# Compare models
results = pd.DataFrame([
    evaluate("Baseline", y_test, baseline_predictions),
    evaluate("Model A - Dengue only", y_test, predictions_a),
    evaluate("Model B - Dengue + Rainfall", y_test, predictions_b)
])

print("\n========== MODEL PERFORMANCE ==========\n")
print(results.to_string(index=False))

# Save predictions
comparison = pd.DataFrame({
    "month": test["month"],
    "actual_cases": y_test,
    "baseline_prediction": baseline_predictions,
    "model_a_prediction": predictions_a,
    "model_b_prediction": predictions_b
})

comparison.to_csv(
    "outputs/forecasting_model_predictions.csv",
    index=False
)

results.to_csv(
    "outputs/forecasting_model_performance.csv",
    index=False
)

print("\n========== ACTUAL VS PREDICTED CASES ==========\n")
print(comparison.to_string(index=False))

print("\nPrediction and performance files saved!")
