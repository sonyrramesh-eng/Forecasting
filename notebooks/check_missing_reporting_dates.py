
import pandas as pd

# Load cleaned dengue dataset
df = pd.read_csv(
    "outputs/karnataka_primary_eda_dataset.csv"
)

df["date"] = pd.to_datetime(
    df["metadata.recordDate"],
    errors="coerce",
    utc=True
).dt.date

df = df.dropna(subset=["date"])

# Expected districts by year
df["year"] = pd.to_datetime(df["date"]).dt.year

# Count districts reporting on each date
daily = df.groupby("date").agg(
    districts_reporting=("location.admin2.name", "nunique"),
    records=("location.admin2.name", "count")
).reset_index()

daily["year"] = pd.to_datetime(daily["date"]).dt.year

daily["expected_districts"] = daily["year"].apply(
    lambda year: 30 if year <= 2022 else 31
)

# Identify dates with fewer districts than expected
daily["missing_districts"] = (
    daily["expected_districts"] -
    daily["districts_reporting"]
)

problem_dates = daily[
    daily["missing_districts"] > 0
]

print("\n========== REPORTING DATE INVESTIGATION ==========\n")

print("Total observed dates:", len(daily))
print("Dates with fewer districts than expected:", len(problem_dates))

print("\nFirst 50 dates with incomplete district reporting:\n")
print(problem_dates.head(50).to_string(index=False))

print("\nMonthly summary of incomplete dates:\n")

problem_dates["month"] = pd.to_datetime(
    problem_dates["date"]
).dt.strftime("%Y-%m")

summary = problem_dates.groupby("month").agg(
    incomplete_dates=("date", "count"),
    total_missing_districts=("missing_districts", "sum")
).reset_index()

print(summary.to_string(index=False))

# Save reports
daily.to_csv(
    "outputs/daily_reporting_coverage.csv",
    index=False
)

problem_dates.to_csv(
    "outputs/incomplete_reporting_dates.csv",
    index=False
)

print("\nReports saved successfully!")
