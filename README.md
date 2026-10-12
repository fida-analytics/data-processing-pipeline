
# Python Data Processing Pipeline

## Project Overview

This project reads raw data from CSV or JSON files,
cleans and transforms the data, and saves structured
output as a CSV file.

## Features

- Reads CSV and JSON input files
- Handles missing numeric values
- Converts invalid numeric values
- Removes duplicate rows
- Standardizes column names
- Calculates annual salary
- Supports configurable cleaning strategies
- Logs processing status and errors
- Includes automated unit tests

## Project Structure

```text
data-processing-pipeline/
├── data/
│   ├── raw_data.csv
│   └── cleaned_data.csv
├── logs/
│   └── pipeline.log
├── src/
│   ├── main.py
│   └── pipeline.py
├── tests/
│   └── test_pipeline.py
├── config.json
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.10 or newer
- pandas

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Update `config.json`:

```json
{
  "input_file": "data/raw_data.csv",
  "output_file": "data/cleaned_data.csv",
  "missing_value_strategy": "median",
  "remove_duplicates": true
}
```

Supported missing value strategies are `median`,
`zero`, and `drop` for numeric columns.

## Run the Pipeline

From the project root directory, run:

```bash
python src/main.py
```

The cleaned CSV file will be saved at the path
specified in `config.json`.

## Run Tests

```bash
python -m unittest discover -s tests -v
```

## Logging

Pipeline activity and errors are recorded in:

`logs/pipeline.log`

## Future Improvements

- Add API data ingestion
- Support more file formats
- Add data validation rules
- Improve error handling and reporting
