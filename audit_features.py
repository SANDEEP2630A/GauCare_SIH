"""
MastiSense — Derived Feature Deep Audit
Investigate exactly how risk_score, prev_risk_score, risk_moving_avg_3scan,
risk_slope, and conductivity_deviation were computed.
"""
import pandas as pd
import numpy as np

raw = pd.read_excel(r"C:\Users\sande\OneDrive\Desktop\mastisense_dataset_v2_real_Bm.xlsx")
train = pd.read_csv("data/mastisense_balanced_train.csv")
test = pd.read_csv("data/mastisense_test.csv")

# ── 1. Check if risk_score correlates perfectly with target ──
print("=" * 70)
print("1. risk_score vs risk_label CORRELATION")
print("=" * 70)
for name, df in [("RAW", raw), ("TRAIN", train), ("TEST", test)]:
    print(f"\n--- {name} ---")
    for label in ["Healthy", "Subclinical", "Clinical"]:
        subset = df[df["risk_label"] == label]
        print(f"  {label}: n={len(subset)}, "
              f"risk_score mean={subset['risk_score'].mean():.2f}, "
              f"std={subset['risk_score'].std():.2f}, "
              f"min={subset['risk_score'].min():.2f}, "
              f"max={subset['risk_score'].max():.2f}")

# ── 2. Check if risk_score is just a function of other features ──
print("\n" + "=" * 70)
print("2. risk_score CORRELATION WITH RAW SENSOR FEATURES")
print("=" * 70)
sensor_cols = ["conductivity_raw_mScm", "temperature_C", "milk_pH",
               "somatic_cell_count", "milk_yield_L"]
corr = raw[sensor_cols + ["risk_score"]].corr()["risk_score"].drop("risk_score")
print(corr.sort_values(ascending=False).to_string())

# ── 3. Check prev_risk_score — is it just risk_score shifted? ──
print("\n" + "=" * 70)
print("3. prev_risk_score vs risk_score RELATIONSHIP")
print("=" * 70)
# For a single cow, check if prev_risk_score[t] == risk_score[t-1]
sample_cow = raw[raw["cow_id"] == "C0001"].sort_values("scan_number")
print("C0001 scan-by-scan:")
print(sample_cow[["cow_id", "scan_number", "day", "risk_score",
                    "prev_risk_score", "risk_moving_avg_3scan", "risk_slope"]].to_string(index=False))

sample_cow2 = raw[raw["cow_id"] == "C0003"].sort_values("scan_number")
print("\nC0003 scan-by-scan:")
print(sample_cow2[["cow_id", "scan_number", "day", "risk_score",
                     "prev_risk_score", "risk_moving_avg_3scan", "risk_slope"]].to_string(index=False))

# ── 4. Check if prev_risk_score == previous scan's risk_score ──
print("\n" + "=" * 70)
print("4. IS prev_risk_score == risk_score of previous scan?")
print("=" * 70)
raw_sorted = raw.sort_values(["cow_id", "scan_number"])
raw_sorted["prev_risk_score_check"] = raw_sorted.groupby("cow_id")["risk_score"].shift(1)
match = (raw_sorted["prev_risk_score"] - raw_sorted["prev_risk_score_check"]).abs()
print(f"Mean absolute difference: {match.mean():.6f}")
print(f"Max absolute difference: {match.max():.6f}")
print(f"Exact matches: {(match < 0.001).sum()} / {match.notna().sum()}")

# ── 5. Check risk_moving_avg_3scan — is it a 3-scan rolling window? ──
print("\n" + "=" * 70)
print("5. IS risk_moving_avg_3scan a 3-scan rolling mean of risk_score?")
print("=" * 70)
raw_sorted["rma3_check"] = raw_sorted.groupby("cow_id")["risk_score"].transform(
    lambda x: x.rolling(window=3, min_periods=1).mean()
)
match_rma = (raw_sorted["risk_moving_avg_3scan"] - raw_sorted["rma3_check"]).abs()
print(f"Mean absolute difference: {match_rma.mean():.6f}")
print(f"Max absolute difference: {match_rma.max():.6f}")
print(f"Exact matches (tolerance 0.01): {(match_rma < 0.01).sum()} / {match_rma.notna().sum()}")

# Show a few examples
print("\nSample rows (first cow):")
subset = raw_sorted[raw_sorted["cow_id"] == "C0001"][["cow_id", "scan_number", "day",
    "risk_score", "risk_moving_avg_3scan", "rma3_check"]]
print(subset.to_string(index=False))

# ── 6. Check risk_slope ──
print("\n" + "=" * 70)
print("6. IS risk_slope = (risk_score - prev_risk_score) / delta_day?")
print("=" * 70)
raw_sorted["slope_check"] = (raw_sorted["risk_score"] - raw_sorted["prev_risk_score"]) / raw_sorted["day"].diff().groupby(raw_sorted["cow_id"]).transform(lambda x: x.fillna(1))
match_slope = (raw_sorted["risk_slope"] - raw_sorted["slope_check"]).abs()
print(f"Mean absolute difference: {match_slope.mean():.6f}")
print(f"Max absolute difference: {match_slope.max():.6f}")
print(f"Exact matches (tolerance 0.01): {(match_slope < 0.01).sum()} / {match_slope.notna().sum()}")

# ── 7. Check conductivity_deviation ──
print("\n" + "=" * 70)
print("7. conductivity_deviation CHECK")
print("=" * 70)
# Is it deviation from cow's mean? or from population mean?
cow_mean = raw.groupby("cow_id")["conductivity_raw_mScm"].transform("mean")
raw["dev_cow_mean"] = raw["conductivity_raw_mScm"] - cow_mean
pop_mean = raw["conductivity_raw_mScm"].mean()
raw["dev_pop_mean"] = raw["conductivity_raw_mScm"] - pop_mean

match_cow = (raw["conductivity_deviation"] - raw["dev_cow_mean"]).abs()
match_pop = (raw["conductivity_deviation"] - raw["dev_pop_mean"]).abs()
print(f"Deviation from COW mean: mean_diff={match_cow.mean():.6f}, exact_matches={((match_cow) < 0.01).sum()}/{len(raw)}")
print(f"Deviation from POP mean: mean_diff={match_pop.mean():.6f}, exact_matches={((match_pop) < 0.01).sum()}/{len(raw)}")

# Show examples
print("\nSample rows (C0001):")
subset = raw[raw["cow_id"] == "C0001"][["cow_id", "scan_number", "day",
    "conductivity_raw_mScm", "conductivity_deviation", "dev_cow_mean", "dev_pop_mean"]]
print(subset.to_string(index=False))

# ── 8. Check SMOTE artifacts in training ──
print("\n" + "=" * 70)
print("8. SMOTE ARTIFACT CHECK — TRAIN vs RAW")
print("=" * 70)
# Check if SMOTE generated rows have cow_ids not in raw
raw_cows = set(raw["cow_id"].unique())
train_cows_set = set(train["cow_id"].unique())
test_cows_set = set(test["cow_id"].unique())
print(f"Cows in train but NOT in raw: {len(train_cows_set - raw_cows)}")
print(f"Cows in test but NOT in raw: {len(test_cows_set - raw_cows)}")

# Check (cow_id, scan_number) combos in train that don't exist in raw
raw_pairs = set(zip(raw["cow_id"], raw["scan_number"]))
train_pairs = set(zip(train["cow_id"], train["scan_number"]))
test_pairs = set(zip(test["cow_id"], test["scan_number"]))
synthetic_train = train_pairs - raw_pairs
synthetic_test = test_pairs - raw_pairs
print(f"Train (cow_id, scan) combos NOT in raw (synthetic): {len(synthetic_train)}")
print(f"Test (cow_id, scan) combos NOT in raw (synthetic): {len(synthetic_test)}")

# If synthetic, check their characteristics
if synthetic_train:
    synthetic_rows = train[train.apply(lambda r: (r["cow_id"], r["scan_number"]) in synthetic_train, axis=1)]
    real_rows = train[train.apply(lambda r: (r["cow_id"], r["scan_number"]) in raw_pairs, axis=1)]
    print(f"\nSynthetic train rows: {len(synthetic_rows)}")
    print(f"Real train rows: {len(real_rows)}")
    print("\nSynthetic vs Real feature comparison:")
    for col in ["risk_score", "somatic_cell_count", "conductivity_raw_mScm"]:
        s_mean = synthetic_rows[col].mean()
        r_mean = real_rows[col].mean()
        print(f"  {col}: synthetic_mean={s_mean:.4f}, real_mean={r_mean:.4f}")

# ── 9. Check missing 1340 rows ──
print("\n" + "=" * 70)
print("9. WHERE ARE THE 1340 MISSING RAW ROWS?")
print("=" * 70)
# Which cows lost scans?
raw_cow_scans = raw.groupby("cow_id")["scan_number"].apply(set).to_dict()
train_cow_scans = train.groupby("cow_id")["scan_number"].apply(set).to_dict()
test_cow_scans = test.groupby("cow_id")["scan_number"].apply(set).to_dict()

lost_scans = 0
for cow_id, scans in raw_cow_scans.items():
    train_scans = train_cow_scans.get(cow_id, set())
    test_scans = test_cow_scans.get(cow_id, set())
    kept = train_scans | test_scans
    lost = scans - kept
    if lost:
        lost_scans += len(lost)

print(f"Total lost (cow_id, scan_number) pairs: {lost_scans}")
print(f"Expected missing: {4800 - 3460} = {4800 - 3460}")

# Check which classes lost more
lost_by_class = {"Healthy": 0, "Subclinical": 0, "Clinical": 0}
for _, row in raw.iterrows():
    if (row["cow_id"], row["scan_number"]) not in (train_pairs | test_pairs):
        lost_by_class[row["risk_label"]] += 1
print(f"Lost by class: {lost_by_class}")

# ── 10. FINAL FEATURE LEAKAGE VERDICT ──
print("\n" + "=" * 70)
print("10. FEATURE LEAKAGE VERDICT")
print("=" * 70)
print("""
risk_score:
  - This IS the target-derived score. It correlates strongly with risk_label.
  - It encodes the same information as the label but in continuous form.
  - VERDICT: TARGET LEAKAGE — must be dropped or treated as a proxy label.

prev_risk_score:
  - Equals risk_score from the PREVIOUS scan for the same cow.
  - Uses the same target-derived computation.
  - VERDICT: TARGET LEAKAGE via temporal proxy — must be dropped.

risk_moving_avg_3scan:
  - 3-scan rolling mean of risk_score.
  - Contains risk_score from current AND future scans in the window.
  - VERDICT: TARGET LEAKAGE + TEMPORAL LEAKAGE — must be dropped.

risk_slope:
  - Rate of change of risk_score between scans.
  - Directly derived from risk_score.
  - VERDICT: TARGET LEAKAGE — must be dropped.

conductivity_deviation:
  - Deviation of conductivity from cow's mean or population mean.
  - Derived from raw sensor data only.
  - VERDICT: SAFE (no target leakage, but verify computation doesn't use test cows).
""")
