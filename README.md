# Karnataka Dengue Trend Analysis and Outbreak Forecasting

## Project Overview

This project focuses on analyzing historical dengue cases in Karnataka and exploring the relationship between dengue trends and rainfall patterns.

It uses data analytics, exploratory data analysis, statistical correlation and machine learning techniques to understand disease trends and experiment with monthly dengue forecasting.

An interactive Streamlit dashboard is also developed to present the analysis and forecasting results.

## Objectives

- Analyze historical dengue cases across Karnataka.
- Study dengue trends across 31 districts.
- Investigate data quality issues and reporting gaps.
- Analyze rainfall patterns and their relationship with dengue cases.
- Explore whether rainfall information improves dengue forecasting.
- Build an interactive dashboard to visualize findings.

## Dataset Details

**Dengue Dataset**
- Disease: Dengue
- Region: Karnataka, India
- Data frequency: Daily district-level records
- Source file: `ka-dengue-daily-summary.csv`

**Rainfall Dataset**
- Region: Karnataka, India
- Period: 2017–2025
- Data frequency: Daily station-level observations
- Processed into district-level daily rainfall averages.

The dengue and rainfall datasets were standardized and combined using district names and dates.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Plotly
- Streamlit

## Project Methodology

### 1. Data Collection
Collected historical dengue and rainfall datasets for Karnataka.

### 2. Data Cleaning and Preparation
- Inspected missing values and duplicate records.
- Investigated conflicting district-date records.
- Standardized district names.
- Prepared district-level rainfall data.
- Integrated dengue and rainfall datasets.
- Examined reporting completeness and data quality.

### 3. Exploratory Data Analysis
- Monthly dengue trend analysis.
- Monthly rainfall trend analysis.
- Statewide dengue and rainfall comparison.
- District-wise correlation analysis.
- Seasonality-adjusted correlation analysis.

### 4. Forecasting
Prepared a monthly forecasting dataset and created lag-based features.

Compared three approaches:

1. Baseline model
2. Dengue-only Linear Regression
3. Dengue + Rainfall Linear Regression

### 5. Dashboard Development
Developed an interactive Streamlit dashboard with five sections:

- Overview
- Dengue Analysis
- Rainfall Analysis
- District Analysis
- Forecasting Results

## Forecasting Results

| Model | MAE | RMSE |
|---|---:|---:|
| Baseline | 75.71 | 78.99 |
| Dengue Only | 197.95 | 232.15 |
| Dengue + Rainfall | 224.28 | 258.44 |

The baseline model achieved the lowest error in the initial experiment.

Adding rainfall did not improve forecasting accuracy in this experiment.

## How to Run the Project

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the project folder

```bash
cd Forecasting
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Launch the dashboard

```bash
python -m streamlit run dashboard/app.py
```

## Project Limitations

- Some dengue records contain unresolved conflicting values.
- Reporting gaps may affect trend analysis.
- Rainfall and dengue correlation does not establish causation.
- The forecasting test dataset contains only seven monthly observations.
- Forecasting results are exploratory and require further validation.

## Conclusion

This project demonstrates how historical disease and rainfall data can be combined to explore dengue trends in Karnataka.

The analysis identifies patterns, examines possible rainfall relationships and evaluates initial forecasting approaches.

The interactive dashboard provides a convenient way to explore the findings.

The project is intended for analytical and educational purposes and does not provide a validated operational outbreak prediction system.