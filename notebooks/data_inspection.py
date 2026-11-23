
import csv

file_path = "data/raw/ka-dengue-daily-summary.csv"

with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
    reader = csv.reader(file)

    headers = next(reader)
    first_row = next(reader)

    print("NUMBER OF COLUMNS:", len(headers))
    print("NUMBER OF VALUES:", len(first_row))

    print("\nCOLUMN DETAILS:")

    for i, header in enumerate(headers):
        print(i, header)

    print("\nFIRST RECORD:")

    for i, value in enumerate(first_row):
        print(i, value)
