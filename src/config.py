from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = Path(
    r"C:\Users\Sadiqul Islam\Downloads\NY 311 Service Requests\311-service-requests-from-2010-to-present.csv"
)

MODEL_PATH = PROJECT_ROOT / "models" / "dsml_311_fast_close_model.joblib"
REPORT_PATH = PROJECT_ROOT / "reports" / "classification_report.txt"
CONFUSION_MATRIX_PATH = PROJECT_ROOT / "reports" / "confusion_matrix.png"

USE_COLUMNS = [
    "Created Date",
    "Closed Date",
    "Agency",
    "Complaint Type",
    "Descriptor",
    "Location Type",
    "Incident Zip",
    "Borough",
    "Open Data Channel Type",
    "Latitude",
    "Longitude",
]

CATEGORICAL_FEATURES = [
    "Agency",
    "Complaint Type",
    "Descriptor",
    "Location Type",
    "Incident Zip",
    "Borough",
    "Open Data Channel Type",
]

NUMERIC_FEATURES = [
    "Latitude",
    "Longitude",
    "created_hour",
    "created_dayofweek",
    "created_month",
]
