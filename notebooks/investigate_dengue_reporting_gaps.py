
import pandas as pd

df = pd.read_csv(
    "outputs/karnataka_dengue_rainfall_combined.csv"
)

df["date"] = pd.to_datetime(df["date"])

# Use BAGALKOTE as a reference district
reference_dates = set(
    df.loc[df["district"] == "BAGALKOTE", "date"]
)

districts_to_check = [
    "BENGALURU RURAL",
    "BENGALURU URBAN",
    "GADAG",
    "YADGIR"
]

print("\n========== REPORTING GAP INVESTIGATION ==========")

for district in districts_to_check:
    district_dates = set(
        df.loc[df["district"] == district, "date"]
    )

    missing_dates = sorted(reference_dates - district_dates)

    print(f"\nDISTRICT: {district}")
    print("Available dates:", len(district_dates))
    print("Dates absent compared with reference:",
          len(missing_dates))

    if missing_dates:
        print("First absent date:", missing_dates[0].date())
        print("Last absent date:", missing_dates[-1].date())
        print("All absent dates:")
        print([d.strftime("%Y-%m-%d") for d in missing_dates])

print("\nInvestigation completed.")
