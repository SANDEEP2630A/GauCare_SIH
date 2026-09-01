import pandas as pd
import numpy as np
from sklearn.model_selection import GroupShuffleSplit

RAW = r"C:\Users\sande\OneDrive\Desktop\mastisense_dataset_v2_real_Bm.xlsx"
TRAIN_OUT = "data/mastisense_balanced_train.csv"
TEST_OUT = "data/mastisense_test.csv"
SEED = 42

DROP_COLS = ["risk_score", "prev_risk_score", "risk_moving_avg_3scan", "risk_slope", "source_class1_final"]

df = pd.read_excel(RAW)

# GroupShuffleSplit by cow_id, 80/20
gss = GroupShuffleSplit(n_splits=1, test_size=0.2, random_state=SEED)
train_idx, test_idx = next(gss.split(df, df["risk_label"], groups=df["cow_id"]))

train = df.iloc[train_idx].copy()
test = df.iloc[test_idx].copy()

# Drop leaked features
train.drop(columns=DROP_COLS, inplace=True)
test.drop(columns=DROP_COLS, inplace=True)

# Verify
train_cows = set(train["cow_id"].unique())
test_cows = set(test["cow_id"].unique())
overlap = train_cows & test_cows

print(f"Train cows: {len(train_cows)}, Test cows: {len(test_cows)}, Overlap: {len(overlap)}")
print(f"Train rows: {len(train)}, Test rows: {len(test)}")
print("Train classes:", train["risk_label"].value_counts().to_dict())
print("Test classes:", test["risk_label"].value_counts().to_dict())
print("Train cols:", list(train.columns))

# Overwrite existing files
train.to_csv(TRAIN_OUT, index=False)
test.to_csv(TEST_OUT, index=False)
print("Files overwritten.")
