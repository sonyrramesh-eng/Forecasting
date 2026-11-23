
import pandas as pd

rainfall = pd.read_csv(
    "data/processed/karnataka_district_daily_rainfall.csv"
)

rainfall["Monitoring Date"] = pd.to_datetime(
    rainfall["Monitoring Date"]
)

for district, month in [
    ("Bidar", "2023-10"),
    ("Mysuru", "2023-12")
]:
    data = rainfall[
        (rainfall["District"].str.upper() == district.upper()) &
        (rainfall["Monitoring Date"].dt.strftime("%Y-%m") == month)
    ]

    print(f"\n========== {district.upper()} : {month} ==========")
    print("Rainfall district-date records:", len(data))

    if len(data) > 0:
        print("First available date:", data["Monitoring Date"].min())
        print("Last available date:", data["Monitoring Date"].max())
        print("Average reporting stations:",
              round(data["reporting_stations"].mean(), 2))
    else:
        print("No rainfall records found for this month.")
