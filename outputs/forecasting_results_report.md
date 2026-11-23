
# Karnataka Dengue Forecasting – Results Report

## 1. Objective

The objective of this experiment is to analyze historical dengue cases in Karnataka and explore whether rainfall information can improve monthly dengue case forecasting.

## 2. Dataset

- Region: Karnataka
- Disease: Dengue
- Data frequency: Monthly
- Forecasting period: June 2018 – March 2021
- Initial monthly observations: 34
- Observations after lag feature creation: 31

## 3. Training and Testing

A chronological 80:20 split was used.

- Training observations: 24
- Training period: September 2018 – August 2020
- Testing observations: 7
- Testing period: September 2020 – March 2021

## 4. Models Evaluated

1. Baseline model – uses previous month's dengue cases.
2. Dengue-only model – Linear Regression using historical dengue cases.
3. Dengue + Rainfall model – Linear Regression using historical dengue cases and rainfall features.

## 5. Model Performance

| Model | MAE | RMSE |
|---|---:|---:|
| Baseline | 75.71 | 78.99 |
| Dengue only | 197.95 | 232.15 |
| Dengue + Rainfall | 224.28 | 258.44 |

The baseline model achieved the lowest MAE and RMSE.

## 6. Findings

- The baseline model performed better than both Linear Regression models in this experiment.
- The Dengue-only model overestimated actual dengue cases.
- Adding rainfall did not improve forecasting accuracy in this experiment.
- Rainfall remains useful for exploratory analysis of seasonal patterns and dengue trends.

## 7. Visualization

The actual versus predicted dengue cases graph is saved at:

outputs/actual_vs_predicted_cases.png

## 8. Limitations

- The testing dataset contains only seven monthly observations.
- The forecasting results are exploratory and should not be treated as reliable outbreak predictions.
- Dengue reporting gaps and data quality issues may affect the results.
- The observed rainfall relationship does not establish causation.

## 9. Conclusion

The experiment compared a simple baseline with two Linear Regression models. The baseline achieved the best performance on the available test period. Including rainfall did not improve prediction accuracy in this initial experiment.

Further validation using more observations and improved forecasting methods would be needed before drawing stronger conclusions.
