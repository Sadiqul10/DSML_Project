import argparse

import joblib
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import ConfusionMatrixDisplay, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

try:
    from src.config import (
        CATEGORICAL_FEATURES,
        CONFUSION_MATRIX_PATH,
        DATA_PATH,
        MODEL_PATH,
        NUMERIC_FEATURES,
        REPORT_PATH,
        USE_COLUMNS,
    )
except ModuleNotFoundError:
    from config import (
        CATEGORICAL_FEATURES,
        CONFUSION_MATRIX_PATH,
        DATA_PATH,
        MODEL_PATH,
        NUMERIC_FEATURES,
        REPORT_PATH,
        USE_COLUMNS,
    )


def load_rows(data_path, rows):
    return pd.read_csv(data_path, usecols=USE_COLUMNS, nrows=rows, low_memory=False)


def build_training_frame(df, fast_close_hours):
    df = df.copy()

    df["Created Date"] = pd.to_datetime(df["Created Date"], errors="coerce")
    df["Closed Date"] = pd.to_datetime(df["Closed Date"], errors="coerce")
    df["resolution_hours"] = (
        df["Closed Date"] - df["Created Date"]
    ).dt.total_seconds() / 3600

    df = df[df["Created Date"].notna()]
    df = df[df["resolution_hours"].notna()]
    df = df[df["resolution_hours"] >= 0]
    df = df[df["resolution_hours"] <= 24 * 365]

    df["fast_close"] = (df["resolution_hours"] <= fast_close_hours).astype(int)
    df["created_hour"] = df["Created Date"].dt.hour
    df["created_dayofweek"] = df["Created Date"].dt.dayofweek
    df["created_month"] = df["Created Date"].dt.month

    for column in CATEGORICAL_FEATURES:
        df[column] = df[column].fillna("Unknown").astype(str)

    return df


def make_pipeline():
    categorical_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="Unknown")),
            (
                "onehot",
                OneHotEncoder(handle_unknown="ignore", min_frequency=20),
            ),
        ]
    )

    numeric_pipeline = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
            ("numeric", numeric_pipeline, NUMERIC_FEATURES),
        ]
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            (
                "model",
                LogisticRegression(
                    max_iter=1000,
                    class_weight="balanced",
                ),
            ),
        ]
    )


def train(data_path, rows, fast_close_hours):
    raw_df = load_rows(data_path, rows)
    df = build_training_frame(raw_df, fast_close_hours)

    features = CATEGORICAL_FEATURES + NUMERIC_FEATURES
    X = df[features]
    y = df["fast_close"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y,
    )

    pipeline = make_pipeline()
    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    report = classification_report(
        y_test,
        y_pred,
        target_names=["slow_close", "fast_close"],
    )

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(
        {
            "pipeline": pipeline,
            "features": features,
            "fast_close_hours": fast_close_hours,
        },
        MODEL_PATH,
    )

    REPORT_PATH.write_text(report, encoding="utf-8")

    ConfusionMatrixDisplay.from_predictions(
        y_test,
        y_pred,
        display_labels=["slow_close", "fast_close"],
        cmap="Blues",
    )
    plt.title("DSML 311 Fast Close Prediction")
    plt.tight_layout()
    plt.savefig(CONFUSION_MATRIX_PATH, dpi=150)
    plt.close()

    print(report)
    print(f"Saved model to: {MODEL_PATH}")
    print(f"Saved report to: {REPORT_PATH}")
    print(f"Saved confusion matrix to: {CONFUSION_MATRIX_PATH}")


def main():
    parser = argparse.ArgumentParser(
        description="Train a DSML model to predict whether 311 requests close quickly."
    )
    parser.add_argument("--data", default=str(DATA_PATH), help="Path to the 311 CSV file.")
    parser.add_argument("--rows", type=int, default=100_000, help="Rows to train on.")
    parser.add_argument(
        "--fast-close-hours",
        type=float,
        default=48,
        help="Requests closed within this many hours are labeled fast_close.",
    )
    args = parser.parse_args()

    train(args.data, args.rows, args.fast_close_hours)


if __name__ == "__main__":
    main()
