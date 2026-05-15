import argparse

import pandas as pd

try:
    from src.config import DATA_PATH, USE_COLUMNS
except ModuleNotFoundError:
    from config import DATA_PATH, USE_COLUMNS


def explore(data_path, rows):
    df = pd.read_csv(data_path, usecols=USE_COLUMNS, nrows=rows, low_memory=False)

    print("Shape:", df.shape)
    print("\nColumns:")
    print(df.columns.tolist())

    print("\nMissing values:")
    print(df.isna().sum().sort_values(ascending=False))

    print("\nTop complaint types:")
    print(df["Complaint Type"].value_counts().head(15))

    print("\nTop boroughs:")
    print(df["Borough"].value_counts(dropna=False))

    created = pd.to_datetime(df["Created Date"], errors="coerce")
    closed = pd.to_datetime(df["Closed Date"], errors="coerce")
    resolution_hours = (closed - created).dt.total_seconds() / 3600

    print("\nResolution hours summary:")
    print(resolution_hours.describe())


def main():
    parser = argparse.ArgumentParser(description="Explore the DSML 311 dataset.")
    parser.add_argument("--data", default=str(DATA_PATH), help="Path to the 311 CSV file.")
    parser.add_argument("--rows", type=int, default=100_000, help="Number of rows to inspect.")
    args = parser.parse_args()

    explore(args.data, args.rows)


if __name__ == "__main__":
    main()
