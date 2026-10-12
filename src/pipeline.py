
import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)


def process_file(input_file, output_file, config):
    input_path = Path(input_file)
    output_path = Path(output_file)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}"
        )

    logger.info("Reading file: %s", input_path)

    # Read CSV or JSON
    suffix = input_path.suffix.lower()

    if suffix == ".csv":
        df = pd.read_csv(input_path)
    elif suffix == ".json":
        df = pd.read_json(input_path)
    else:
        raise ValueError(
            "Unsupported input format. Use CSV or JSON."
        )

    if df.empty:
        raise ValueError("Input file contains no data.")

    # Standardize column names
    df.columns = df.columns.str.strip().str.lower()

    # Remove duplicates only when enabled in config
    if config.get("remove_duplicates", True):
        before = len(df)
        df = df.drop_duplicates()
        logger.info("Removed %s duplicate rows", before - len(df))

    # Convert numeric columns safely
    for column in ["age", "salary"]:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column], errors="coerce"
            )

            strategy = config.get(
                "missing_value_strategy", "median"
            )

            if strategy == "median":
                if df[column].notna().any():
                    df[column] = df[column].fillna(
                        df[column].median()
                    )
            elif strategy == "zero":
                df[column] = df[column].fillna(0)
            elif strategy == "drop":
                df = df.dropna(subset=[column])
            else:
                raise ValueError(
                    f"Unknown missing value strategy: {strategy}"
                )

    # Convert age to integer if all values are present
    if "age" in df.columns and df["age"].notna().all():
        df["age"] = df["age"].round().astype(int)

    # Add annual salary if salary is available
    if "salary" in df.columns:
        df["annual_salary"] = df["salary"] * 12

    # Save output as CSV
    output_path.parent.mkdir(
        parents=True, exist_ok=True
    )
    df.to_csv(output_path, index=False)

    logger.info("Output saved to %s", output_path)
    return df
