
import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from src.pipeline import process_file


class TestDataPipeline(unittest.TestCase):

    def test_csv_processing(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            folder = Path(temp_dir)
            input_file = folder / "input.csv"
            output_file = folder / "output.csv"

            pd.DataFrame({
                "name": ["Ali", "Ali", "Sara"],
                "age": [25, 25, None],
                "salary": [50000, 50000, 60000]
            }).to_csv(input_file, index=False)

            config = {
                "remove_duplicates": True,
                "missing_value_strategy": "median"
            }

            result = process_file(
                input_file, output_file, config
            )

            self.assertTrue(output_file.exists())
            self.assertEqual(len(result), 2)
            self.assertFalse(result["age"].isna().any())

    def test_missing_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            input_file = Path(temp_dir) / "missing.csv"
            output_file = Path(temp_dir) / "output.csv"

            with self.assertRaises(FileNotFoundError):
                process_file(input_file, output_file, {})


if __name__ == "__main__":
    unittest.main()
