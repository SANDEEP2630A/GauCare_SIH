"""
MastiSense — Full Dataset Audit Script
"""
import pandas as pd
import numpy as np

RAW_PATH = r"C:\Users\sande\OneDrive\Desktop\mastisense_dataset_v2_real_Bm.xlsx"
TRAIN_PATH = "data/mastisense_balanced_train.csv"
TEST_PATH = "data/mastisense_test.csv"

raw = pd.read_excel(RAW_PATH)
train = pd.read_csv(TRAIN_PATH)
test = pd.read_csv(TEST_PATH)

print("=" * 70)
print("1. DATASET HEALTH")
print("=" * 70)

for name, df in [("RAW", raw), ("TRAIN", train), ("TEST", test)]:
    print(f"\n--- {name} ---")
    print(f"Shape: {df.shape}")
    print(f"Columns ({len(df.columns)}): {list(df.columns)}")
    print(f"Missing values: {df.isnull().sum().sum()}")
    print(f"Exact duplicate rows: {df.duplicated().sum()}")

    cow_col = "cow_id"
    scan_col = "scan_number"
    print(f"Unique cow_ids: {df[cow_col].nunique()}")
    print(f"Unique (cow_id, scan_number): {df.groupby([cow_col, scan_col]).ngroups}")
    print(f"Duplicate (cow_id, scan_number): {df.duplicated(subset=[cow_col, scan_col]).sum()}")

    scans_per_cow = df.groupby(cow_col).size()
    print(f"Scans per cow: min={scans_per_cow.min()}, max={scans_per_cow.max()}, "
          f"mean={scans_per_cow.mean():.1f}, median={scans_per_cow.median():.1f}")
    print(f"Cows with >1 scan: {(scans_per_cow > 1).sum()}")
    print(f"Cows with exactly 1 scan: {(scans_per_cow == 1).sum()}")
    print(f"Cows with exactly 6 scans: {(scans_per_cow == 6).sum()}")
    print(f"\nDtype counts:\n{df.dtypes.value_counts().to_string()}")

    if "risk_label" in df.columns:
        print(f"\nClass distribution:")
        print(df["risk_label"].value_counts().to_string())

# ── Scan number patterns ──
print("\n" + "=" * 70)
print("2. SCAN NUMBER PATTERNS")
print("=" * 70)
for name, df in [("RAW", raw), ("TRAIN", train), ("TEST", test)]:
    print(f"\n--- {name} ---")
    print("Scan numbers present:", sorted(df["scan_number"].unique()))
    if "day" in df.columns:
        print("Days present:", sorted(df["day"].unique()))
        scan_day = df.groupby("scan_number")["day"].agg(["min", "max", "mean"])
        print("Scan-number to day mapping:")
        print(scan_day.to_string())

# ── Temporal checks ──
print("\n" + "=" * 70)
print("3. TEMPORAL / CHRONOLOGICAL CHECKS")
print("=" * 70)
for name, df in [("RAW", raw), ("TRAIN", train), ("TEST", test)]:
    print(f"\n--- {name} ---")
    if "day" in df.columns:
        day_range = df["day"].min(), df["day"].max()
        print(f"Day range: {day_range}")
        day_counts = df["day"].value_counts().sort_index()
        print("Rows per day:")
        print(day_counts.to_string())

# ── cow_id intersection ──
print("\n" + "=" * 70)
print("4. TRAIN/TEST cow_id INTERSECTION")
print("=" * 70)
train_cows = set(train["cow_id"].unique())
test_cows = set(test["cow_id"].unique())
intersection = train_cows & test_cows
print(f"Train cows: {len(train_cows)}")
print(f"Test cows: {len(test_cows)}")
print(f"Intersection: {len(intersection)}")
print(f"Train-only cows: {len(train_cows - test_cows)}")
print(f"Test-only cows: {len(test_cows - train_cows)}")
print(f"Leakage ratio (intersection / test cows): {len(intersection)/len(test_cows)*100:.1f}%")

if intersection:
    print(f"\nFirst 20 leaked cow_ids: {list(intersection)[:20]}")
    # Check if same cow has different scans in train vs test
    print("\nPer-cow scan analysis for leaked cows:")
    for cid in list(intersection)[:10]:
        t_scans = sorted(train[train["cow_id"] == cid]["scan_number"].unique())
        s_scans = sorted(test[test["cow_id"] == cid]["scan_number"].unique())
        common = set(t_scans) & set(s_scans)
        t_labels = train[train["cow_id"] == cid]["risk_label"].unique()
        s_labels = test[test["cow_id"] == cid]["risk_label"].unique()
        print(f"  {cid}: train_scans={t_scans}, test_scans={s_scans}, "
              f"shared_scans={common}, train_labels={t_labels}, test_labels={s_labels}")

# ── Class distribution per cow ──
print("\n" + "=" * 70)
print("5. CLASS DISTRIBUTION PER COW")
print("=" * 70)
for name, df in [("TRAIN", train), ("TEST", test)]:
    print(f"\n--- {name} ---")
    cow_classes = df.groupby("cow_id")["risk_label"].nunique()
    print(f"Cows with 1 class: {(cow_classes == 1).sum()}")
    print(f"Cows with 2 classes: {(cow_classes == 2).sum()}")
    print(f"Cows with 3 classes: {(cow_classes == 3).sum()}")

    # Check if cows change class across scans
    multi_class_cows = cow_classes[cow_classes > 1].index
    if len(multi_class_cows) > 0:
        print(f"\nCows that change class across scans (first 10):")
        for cid in list(multi_class_cows)[:10]:
            sub = df[df["cow_id"] == cid][["scan_number", "day", "risk_label"]].sort_values("scan_number")
            print(f"  {cid}:")
            for _, row in sub.iterrows():
                print(f"    scan {row['scan_number']} day={row.get('day','?')}: {row['risk_label']}")

# ── Derived features analysis ──
print("\n" + "=" * 70)
print("6. DERIVED FEATURES ANALYSIS")
print("=" * 70)
derived_cols = ["risk_score", "prev_risk_score", "risk_moving_avg_3scan",
                "risk_slope", "conductivity_deviation"]
for col in derived_cols:
    if col in train.columns:
        print(f"\n--- {col} ---")
        print(f"  Train stats: mean={train[col].mean():.4f}, std={train[col].std():.4f}, "
              f"min={train[col].min():.4f}, max={train[col].max():.4f}")
        print(f"  Test  stats: mean={test[col].mean():.4f}, std={test[col].std():.4f}, "
              f"min={test[col].min():.4f}, max={test[col].max():.4f}")
        if col in ["risk_score", "prev_risk_score"]:
            for label in ["Healthy", "Subclinical", "Clinical"]:
                t_mean = train[train["risk_label"] == label][col].mean()
                s_mean = test[test["risk_label"] == label][col].mean() if label in test["risk_label"].values else float("nan")
                print(f"  {label}: train_mean={t_mean:.4f}, test_mean={s_mean:.4f}")

# ── Check if rolling features use cross-split data ──
print("\n" + "=" * 70)
print("7. ROLLING FEATURE CROSS-SPLIT CHECK")
print("=" * 70)
# Check if risk_moving_avg_3scan for cow X in train uses scans from test
# by examining whether the value changes with scan order
sample_cows = list(intersection)[:5] if intersection else list(train_cows)[:5]
for cid in sample_cows:
    all_scans = pd.concat([
        train[train["cow_id"] == cid][["cow_id", "scan_number", "day", "risk_moving_avg_3scan", "risk_label"]],
        test[test["cow_id"] == cid][["cow_id", "scan_number", "day", "risk_moving_avg_3scan", "risk_label"]]
    ]).sort_values("scan_number")
    print(f"\n{cid}:")
    print(all_scans.to_string(index=False))

# ── Raw dataset: is it the authoritative source? ──
print("\n" + "=" * 70)
print("8. RAW DATASET vs TRAIN+TEST")
print("=" * 70)
raw_rows = set()
for _, row in raw.iterrows():
    raw_rows.add((row["cow_id"], row["scan_number"]))
train_pairs = set(zip(train["cow_id"], train["scan_number"]))
test_pairs = set(zip(test["cow_id"], test["scan_number"]))
combined_pairs = train_pairs | test_pairs

print(f"Raw (cow_id, scan_number) pairs: {len(raw_rows)}")
print(f"Train pairs: {len(train_pairs)}")
print(f"Test pairs: {len(test_pairs)}")
print(f"Combined pairs: {len(combined_pairs)}")
print(f"Raw - Combined (missing from train+test): {len(raw_rows - combined_pairs)}")
print(f"Combined - Raw (extra in train+test): {len(combined_pairs - raw_rows)}")
print(f"In both train and test: {len(train_pairs & test_pairs)}")

# ── Check for (cow_id, scan_number) overlap ──
overlap = train_pairs & test_pairs
if overlap:
    print(f"\nCRITICAL: {len(overlap)} exact (cow_id, scan_number) duplicates across train/test!")
    print("First 10:", list(overlap)[:10])
else:
    print("\nNo exact (cow_id, scan_number) duplicates across train/test.")

# ── Check label leakage across cow_id ──
print("\n" + "=" * 70)
print("9. LABEL LEAKAGE ACROSS cow_id")
print("=" * 70)
if intersection:
    labels_in_train = {}
    labels_in_test = {}
    for cid in intersection:
        labels_in_train[cid] = set(train[train["cow_id"] == cid]["risk_label"].unique())
        labels_in_test[cid] = set(test[test["cow_id"] == cid]["risk_label"].unique())

    same_label = sum(1 for cid in intersection if labels_in_train[cid] == labels_in_test[cid])
    diff_label = sum(1 for cid in intersection if labels_in_train[cid] != labels_in_test[cid])
    print(f"Leaked cows with SAME label in train+test: {same_label}")
    print(f"Leaked cows with DIFFERENT label in train+test: {diff_label}")
    if diff_label > 0:
        print("\nCows with different labels in train vs test:")
        for cid in intersection:
            if labels_in_train[cid] != labels_in_test[cid]:
                print(f"  {cid}: train={labels_in_train[cid]}, test={labels_in_test[cid]}")

# ── Summary ──
print("\n" + "=" * 70)
print("10. SUMMARY")
print("=" * 70)
print(f"Total raw rows: {len(raw)}")
print(f"Train rows: {len(train)}")
print(f"Test rows: {len(test)}")
print(f"Total combined: {len(train) + len(test)}")
print(f"Train+Test pairs matching raw: {len(combined_pairs & raw_rows)}/{len(raw_rows)}")
print(f"Cow-id leakage: {len(intersection)} cows in both train and test")
print(f"Exact (cow_id, scan) leakage: {len(overlap)}")
