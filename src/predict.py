import argparse

import joblib
import pandas as pd

try:
    from src.config import CATEGORICAL_FEATURES, MODEL_PATH, NUMERIC_FEATURES
except ModuleNotFoundError:
    from config import CATEGORICAL_FEATURES, MODEL_PATH, NUMERIC_FEATURES


def prepare_for_prediction(df):
    df = df.copy()
    df["Created Date"] = pd.to_datetime(df["Created Date"], errors="coerce")
    df["created_hour"] = df["Created Date"].dt.hour
    df["created_dayofweek"] = df["Created Date"].dt.dayofweek
    df["created_month"] = df["Created Date"].dt.month

    for column in CATEGORICAL_FEATURES:
        if column not in df.columns:
            df[column] = "Unknown"
        df[column] = df[column].fillna("Unknown").astype(str)

    for column in NUMERIC_FEATURES:
        if column not in df.columns:
            df[column] = pd.NA

    return df


def predict(input_csv, output_csv):
    bundle = joblib.load(MODEL_PATH)
    pipeline = bundle["pipeline"]
    features = bundle["features"]

    df = pd.read_csv(input_csv, low_memory=False)
    prepared = prepare_for_prediction(df)

    probabilities = pipeline.predict_proba(prepared[features])[:, 1]
    predictions = pipeline.predict(prepared[features])

    result = df.copy()
    result["fast_close_prediction"] = predictions
    result["fast_close_probability"] = probabilities
    result.to_csv(output_csv, index=False)

    print(f"Saved predictions to: {output_csv}")


def main():
    parser = argparse.ArgumentParser(description="Predict fast-close probability for 311 rows.")
    parser.add_argument("--input", required=True, help="CSV containing 311 request rows.")
    parser.add_argument("--output", default="reports/predictions.csv", help="Output CSV path.")
    args = parser.parse_args()

    predict(args.input, args.output)


if __name__ == "__main__":
    main()
