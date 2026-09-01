import pandas as pd

kaggle = pd.read_csv(r"C:\Users\sande\Downloads\cow_milk_mastitis_dataset.csv")
our = pd.read_csv("data/mastisense_balanced_train.csv")

mapping = {
    "Cow_ID": "cow_id",
    "Day": "day",
    "Milk_Temperature": "temperature_C",
    "Milk_pH": "milk_pH",
    "Milk_Conductivity": "conductivity_raw_mScm",
    "Somatic_Cell_Count": "somatic_cell_count",
    "Milk_Yield": "milk_yield_L",
    "Clotting": "clotting",
}

print("=== KAGGLE DATASET ===")
print(f"Rows: {len(kaggle)}")
print(f"Unique cows: {kaggle['Cow_ID'].nunique()}")
sizes = kaggle.groupby("Cow_ID").size()
print(f"Scans per cow: {sizes.min()} to {sizes.max()}")
print(f"Days: {sorted(kaggle['Day'].unique())}")
print(f"Columns: {list(kaggle.columns)}")
print(f"\nKaggle class1 dist: {kaggle['class1'].value_counts().to_dict()}")
print(f"Kaggle cow_ids (first 5): {kaggle['Cow_ID'].unique()[:5].tolist()}")

print("\n=== OUR DATASET ===")
print(f"Rows: {len(our)}")
print(f"Unique cows: {our['cow_id'].nunique()}")
print(f"Columns: {list(our.columns)}")

print("\n=== COLUMN MAPPING ===")
for k, v in mapping.items():
    in_k = k in kaggle.columns
    in_o = v in our.columns
    status = "BOTH" if (in_k and in_o) else "MISSING"
    print(f"  Kaggle '{k}' -> Our '{v}': {status}")

print("\n=== WHAT KAGGLE HAS (real) ===")
for c in kaggle.columns:
    print(f"  {c}")

print("\n=== WHAT WE ADDED (synthetic/engineered) ===")
our_model_cols = [c for c in our.columns if c not in ["cow_id", "scan_number", "day", "risk_label"]]
for c in our_model_cols:
    in_kaggle = False
    for k, v in mapping.items():
        if v == c:
            in_kaggle = True
            break
    source = "REAL (Kaggle)" if in_kaggle else "SYNTHETIC/ENGINEERED"
    print(f"  {c}: {source}")

print("\n=== VALUE RANGES ===")
for k, v in mapping.items():
    if k in kaggle.columns and v in our.columns:
        k_col = kaggle[k]
        o_col = our[v]
        if k_col.dtype in ["float64", "int64"] and o_col.dtype in ["float64", "int64"]:
            print(f"  {v}:")
            print(f"    Kaggle: min={k_col.min():.2f}, max={k_col.max():.2f}, mean={k_col.mean():.2f}")
            print(f"    Ours:   min={o_col.min():.2f}, max={o_col.max():.2f}, mean={o_col.mean():.2f}")

print("\n=== SAME COW IDS? ===")
kaggle_cows = set(kaggle["Cow_ID"].unique())
our_cows = set(our["cow_id"].unique())
print(f"Kaggle cows: {len(kaggle_cows)}")
print(f"Our cows: {len(our_cows)}")
print(f"Overlap: {len(kaggle_cows & our_cows)}")
print(f"Kaggle sample: {sorted(kaggle_cows)[:5]}")
print(f"Our sample: {sorted(our_cows)[:5]}")
