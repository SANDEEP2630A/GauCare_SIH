import pandas as pd

# =========================
# 1. LOAD DATASET
# =========================
FILE_PATH = "C:/Users/ADYASHA/OneDrive/Documents/Mastisense_SIH/backend/audit/mastisense_dataset_v2_real_ec_with_as7343.xlsx"
df = pd.read_excel(FILE_PATH)

print("\n========== DATASET OVERVIEW ==========")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nColumns:")
for i, col in enumerate(df.columns, start=1):
    print(f"{i}. {col}")


# =========================
# 2. BASIC INFORMATION
# =========================

print("\n========== DATA TYPES ==========")
print(df.dtypes)

print("\n========== MISSING VALUES ==========")
missing = df.isnull().sum()
print(missing[missing > 0])

print("\n========== DUPLICATES ==========")
print("Duplicate rows:", df.duplicated().sum())


# =========================
# 3. COW DISTRIBUTION
# =========================

print("\n========== COW DISTRIBUTION ==========")

cow_counts = df.groupby("cow_id").size()

print("Number of cows:", df["cow_id"].nunique())

print("\nScans per cow:")
print(cow_counts.value_counts().sort_index())

print("\nCows NOT having exactly 6 scans:")

incorrect_cows = cow_counts[cow_counts != 6]

if len(incorrect_cows) == 0:
    print("✓ Every cow has exactly 6 scans")
else:
    print(incorrect_cows)


# =========================
# 4. CHECK SCAN/DAY PATTERN
# =========================

print("\n========== SCAN/DAY PATTERN ==========")

expected_days = [3, 6, 9, 12, 15, 18]
expected_scans = [1, 2, 3, 4, 5, 6]

problems = []

for cow, group in df.groupby("cow_id"):

    group = group.sort_values("scan_number")

    scans = group["scan_number"].tolist()
    days = group["day"].tolist()

    if scans != expected_scans or days != expected_days:
        problems.append(
            (cow, scans, days)
        )

if len(problems) == 0:
    print("✓ All cows follow 1,2,3,4,5,6 scans")
    print("✓ All cows follow days 3,6,9,12,15,18")
else:
    print("Problems found:")

    for problem in problems[:20]:
        print(problem)


# =========================
# 5. DISEASE LABEL DISTRIBUTION
# =========================

print("\n========== DISEASE LABEL DISTRIBUTION ==========")

print(df["risk_label"].value_counts())

print("\nPercentage:")
print(
    df["risk_label"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)


# =========================
# 6. LABEL DISTRIBUTION PER COW
# =========================

print("\n========== LABELS PER COW ==========")

for cow, group in df.groupby("cow_id"):

    labels = group.sort_values("day")["risk_label"].tolist()

    print(cow, "→", " → ".join(labels))


# =========================
# 7. AS7343 SENSOR CHECK
# =========================

print("\n========== AS7343 SENSOR CHECK ==========")

as7343_columns = [
    col for col in df.columns
    if col.startswith("as7343_")
]

print("AS7343 columns:")
print(as7343_columns)

print("\nNumber of AS7343 channels/features:",
      len(as7343_columns))

print("\nAS7343 statistics:")

print(
    df[as7343_columns]
    .describe()
    .T[["min", "max", "mean", "std"]]
)


# =========================
# 8. OTHER SENSOR FEATURES
# =========================

sensor_columns = [
    "conductivity_raw_mScm",
    "temperature_C",
    "conductivity_temp_adjusted_mScm",
    "milk_pH",
    "somatic_cell_count",
    "milk_yield_L",
    "clotting"
]

print("\n========== SENSOR / MILK FEATURES ==========")

print(
    df[sensor_columns]
    .describe()
    .T[["min", "max", "mean", "std"]]
)


# =========================
# 9. RISK FEATURES
# =========================

risk_columns = [
    "conductivity_deviation",
    "prev_risk_score",
    "risk_moving_avg_3scan",
    "risk_slope",
    "risk_score"
]

print("\n========== RISK FEATURES ==========")

print(
    df[risk_columns]
    .describe()
    .T[["min", "max", "mean", "std"]]
)


# =========================
# 10. SOURCE CLASS
# =========================

print("\n========== SOURCE CLASS ==========")

print(df["source_class1_final"].value_counts())

print(
    "\nCross-tabulation:"
)

print(
    pd.crosstab(
        df["source_class1_final"],
        df["risk_label"]
    )
)

# =========================
# 12. EXACT COW-LEVEL CLASS DISTRIBUTION
# =========================

print("\n========== COW-LEVEL DISEASE DISTRIBUTION ==========")

cow_summary = (
    df.groupby("cow_id")["risk_label"]
    .apply(lambda x: list(x))
)

healthy_only = 0
subclinical_progression = 0
clinical_progression = 0

for cow, labels in cow_summary.items():

    if all(label == "Healthy" for label in labels):
        healthy_only += 1

    if "Subclinical" in labels:
        subclinical_progression += 1

    if "Clinical" in labels:
        clinical_progression += 1


print("Healthy-only cows:", healthy_only)
print("Cows reaching Subclinical:", subclinical_progression)
print("Cows reaching Clinical:", clinical_progression)

print("\nTotal cows:", len(cow_summary))


# =========================
# 13. EXACT TARGET DISTRIBUTION
# =========================

print("\n========== EXACT TARGET DISTRIBUTION ==========")

target_counts = df["risk_label"].value_counts()

for label, count in target_counts.items():

    percentage = (count / len(df)) * 100

    print(
        f"{label}: {count} records "
        f"({percentage:.2f}%)"
    )


# =========================
# 14. SOURCE CLASS BY COW
# =========================

print("\n========== SOURCE CLASS BY COW ==========")

cow_source = (
    df.groupby("cow_id")["source_class1_final"]
    .first()
)

print(
    cow_source.value_counts()
)

print("\nCross-tab at COW level:")

cow_label = (
    df.groupby("cow_id")["risk_label"]
    .last()
)

print(
    pd.crosstab(
        cow_source,
        cow_label
    )
)
# =========================
# 11. FINAL
# =========================

print("\n========================================")
print("AUDIT COMPLETE")
print("========================================")