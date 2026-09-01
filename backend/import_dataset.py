import pandas as pd
from cows.models import Cow, Scan

print("Reading Excel dataset...")

df = pd.read_excel(
    "audit/mastisense_dataset_v2_real_ec_with_as7343.xlsx"
)

print(f"Total rows found: {len(df)}")

for _, row in df.iterrows():

    cow_id = str(row["cow_id"]).strip()

    cow, created = Cow.objects.get_or_create(
        cow_id=cow_id
    )

    Scan.objects.get_or_create(
        cow=cow,
        scan_number=int(row["scan_number"]),
        defaults={
            "day": int(row["day"]),

            "conductivity_raw_mScm":
                float(row["conductivity_raw_mScm"]),

            "temperature_C":
                float(row["temperature_C"]),

            "conductivity_temp_adjusted_mScm":
                float(row["conductivity_temp_adjusted_mScm"]),

            "milk_pH":
                float(row["milk_pH"]),

            "somatic_cell_count":
                float(row["somatic_cell_count"]),

            "milk_yield_L":
                float(row["milk_yield_L"]),

            "clotting":
                bool(row["clotting"]),

            "as7343_F1": float(row["as7343_F1"]),
            "as7343_F2": float(row["as7343_F2"]),
            "as7343_FZ": float(row["as7343_FZ"]),
            "as7343_F3": float(row["as7343_F3"]),
            "as7343_F4": float(row["as7343_F4"]),
            "as7343_F5": float(row["as7343_F5"]),
            "as7343_FY": float(row["as7343_FY"]),
            "as7343_FXL": float(row["as7343_FXL"]),
            "as7343_F6": float(row["as7343_F6"]),
            "as7343_F7": float(row["as7343_F7"]),
            "as7343_F8": float(row["as7343_F8"]),
            "as7343_NIR": float(row["as7343_NIR"]),
            "as7343_VIS": float(row["as7343_VIS"]),
            "as7343_FD": float(row["as7343_FD"]),
        }
    )

print("IMPORT COMPLETED")
print("Cows:", Cow.objects.count())
print("Scans:", Scan.objects.count())