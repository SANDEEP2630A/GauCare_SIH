"""
GauCare — Dataset Balancing Script
Applies SVMSMOTE + SMOTE + undersampling to produce a balanced 3-class dataset.
Target: ~1500 Healthy / ~600 Subclinical / ~400 Clinical
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE, SVMSMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.combine import SMOTEENN
from collections import Counter

# ── Config ────────────────────────────────────────────────────────────────
INPUT_XLSX = r"C:\Users\sande\OneDrive\Desktop\mastisense_dataset_v2_real_Bm.xlsx"
TARGET_COL = "risk_label"
ID_COLS = ["cow_id", "scan_number", "day"]  # non-feature columns to preserve
TEST_SIZE = 0.2
RANDOM_STATE = 42

# Target counts after balancing
TARGET_DIST = {
    "Healthy": 1500,
    "Subclinical": 600,
    "Clinical": 400,
}

# Label encoding
LABEL_MAP = {"Healthy": 0, "Subclinical": 1, "Clinical": 2}
INV_LABEL_MAP = {v: k for k, v in LABEL_MAP.items()}


def load_data():
    print("Loading dataset...")
    df = pd.read_excel(INPUT_XLSX)
    print(f"  Raw shape: {df.shape}")
    print(f"  Class distribution:\n{df[TARGET_COL].value_counts()}\n")
    return df


def prepare_features(df):
    """Separate features, ids, and target."""
    y = df[TARGET_COL].map(LABEL_MAP)
    ids = df[ID_COLS]
    # Drop non-feature columns
    drop_cols = [TARGET_COL] + ID_COLS + ["source_class1_final", "risk_label"]
    X = df.drop(columns=[c for c in drop_cols if c in df.columns])
    return X, y, ids


def split_data(X, y, ids):
    """Stratified 80/20 train/test split."""
    X_train, X_test, y_train, y_test, ids_train, ids_test = train_test_split(
        X, y, ids, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    print(f"Train: {len(X_train)} rows | Test: {len(X_test)} rows")
    print(f"Train distribution: {dict(Counter(y_train))}")
    print(f"Test distribution:  {dict(Counter(y_test))}\n")
    return X_train, X_test, y_train, y_test, ids_train, ids_test


def balance_train(X_train, y_train):
    """
    Apply SVMSMOTE to Subclinical (1), SMOTE to Clinical (2),
    then undersample Healthy (0) to target.
    """
    print("=== Balancing Training Set ===")
    print(f"Before: {dict(Counter(y_train))}")

    # Step 1: Oversample minority classes
    # SVMSMOTE for Subclinical (small minority, decision-boundary focused)
    # SMOTE for Clinical (more samples, safe interpolation)
    sampling_strategy = {
        1: TARGET_DIST["Subclinical"],  # Subclinical → 600
        2: TARGET_DIST["Clinical"],     # Clinical → 400
    }

    # Use SVMSMOTE for the overall resampling (works well for multi-class)
    smote = SVMSMOTE(
        sampling_strategy=sampling_strategy,
        random_state=RANDOM_STATE,
        k_neighbors=5,
        m_neighbors=10,
        out_step=0.5,
    )
    X_res, y_res = smote.fit_resample(X_train, y_train)
    print(f"After SVMSMOTE: {dict(Counter(y_res))}")

    # Step 2: Undersample Healthy to target
    rus = RandomUnderSampler(
        sampling_strategy={0: TARGET_DIST["Healthy"]},
        random_state=RANDOM_STATE,
    )
    X_bal, y_bal = rus.fit_resample(X_res, y_res)
    print(f"After undersample: {dict(Counter(y_bal))}")

    # Shuffle the balanced dataset
    shuffle_idx = np.random.RandomState(RANDOM_STATE).permutation(len(X_bal))
    X_bal = X_bal.iloc[shuffle_idx].reset_index(drop=True)
    y_bal = y_bal.iloc[shuffle_idx].reset_index(drop=True)

    print(f"Final balanced training set: {len(X_bal)} rows\n")
    return X_bal, y_bal


def export_csv(X, y, ids, filepath, label_map_inv):
    """Export to CSV with readable labels."""
    df_out = X.copy()
    df_out[TARGET_COL] = y.map(label_map_inv)
    df_out[ID_COLS] = ids.values
    # Reorder columns: ids first, then features, then target
    feature_cols = [c for c in df_out.columns if c not in ID_COLS + [TARGET_COL]]
    df_out = df_out[ID_COLS + feature_cols + [TARGET_COL]]
    df_out.to_csv(filepath, index=False)
    print(f"Saved: {filepath} ({len(df_out)} rows)")


def main():
    # 1. Load
    df = load_data()

    # 2. Prepare
    X, y, ids = prepare_features(df)

    # 3. Split
    X_train, X_test, y_train, y_test, ids_train, ids_test = split_data(X, y, ids)

    # 4. Balance training set only
    X_bal, y_bal = balance_train(X_train, y_train)

    # 5. Export
    print("=== Exporting CSVs ===")
    export_csv(X_bal, y_bal, ids_train.iloc[:len(X_bal)],
               "data/mastisense_balanced_train.csv", INV_LABEL_MAP)
    export_csv(X_test, y_test, ids_test,
               "data/mastisense_test.csv", INV_LABEL_MAP)

    # 6. Summary
    print("\n=== Summary ===")
    print(f"Train (balanced): {len(X_bal)} rows")
    print(f"  Healthy:      {int((y_bal == 0).sum())} ({(y_bal == 0).mean()*100:.1f}%)")
    print(f"  Subclinical:  {int((y_bal == 1).sum())} ({(y_bal == 1).mean()*100:.1f}%)")
    print(f"  Clinical:     {int((y_bal == 2).sum())} ({(y_bal == 2).mean()*100:.1f}%)")
    print(f"\nTest (untouched): {len(X_test)} rows")
    print(f"  Healthy:      {int((y_test == 0).sum())} ({(y_test == 0).mean()*100:.1f}%)")
    print(f"  Subclinical:  {int((y_test == 1).sum())} ({(y_test == 1).mean()*100:.1f}%)")
    print(f"  Clinical:     {int((y_test == 2).sum())} ({(y_test == 2).mean()*100:.1f}%)")


if __name__ == "__main__":
    main()
