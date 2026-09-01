import os
import joblib
import pandas as pd


# -------------------------------------------------
# Paths
# -------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "gaucare_model.pkl")
LABEL_ENCODER_PATH = os.path.join(BASE_DIR, "gaucare_label_encoder.pkl")
FEATURE_SPEC_PATH = os.path.join(BASE_DIR, "gaucare_feature_spec.pkl")


# -------------------------------------------------
# Load ML files
# -------------------------------------------------

model = joblib.load(MODEL_PATH)
label_encoder = joblib.load(LABEL_ENCODER_PATH)
feature_spec = joblib.load(FEATURE_SPEC_PATH)


# -------------------------------------------------
# Features expected by the model
# -------------------------------------------------

FEATURES = [
    "conductivity_raw_mScm",
    "temperature_C",
    "conductivity_temp_adjusted_mScm",

    "as7343_F1",
    "as7343_F2",
    "as7343_FZ",
    "as7343_F3",
    "as7343_F4",
    "as7343_F5",
    "as7343_FY",
    "as7343_FXL",
    "as7343_F6",
    "as7343_F7",
    "as7343_F8",
    "as7343_NIR",
    "as7343_VIS",
    "as7343_FD",

    "conductivity_deviation",
]


# -------------------------------------------------
# Prediction function
# -------------------------------------------------

def predict_risk(data):

    # Check for missing features
    missing_features = [
        feature for feature in FEATURES
        if feature not in data
    ]

    if missing_features:
        raise ValueError(
            f"Missing features: {missing_features}"
        )

    # Keep exact training feature order
    input_data = pd.DataFrame(
    [[float(data[feature]) for feature in FEATURES]],
    columns=FEATURES
)
    # Get encoded prediction
    prediction_encoded = model.predict(input_data)[0]

    # Convert encoded value to class name
    risk_label = label_encoder.inverse_transform(
        [prediction_encoded]
    )[0]

    # Get class probabilities
    probabilities = model.predict_proba(input_data)[0]

    probability_dict = {
        label_encoder.inverse_transform([i])[0]: float(probability)
        for i, probability in enumerate(probabilities)
    }

    return {
        "risk_label": risk_label,
        "probabilities": probability_dict,
    }