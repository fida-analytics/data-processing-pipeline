
import json
import logging
from pathlib import Path

from pipeline import process_file


# Find the main project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Load configuration from config.json
CONFIG_FILE = BASE_DIR / "config.json"

with open(CONFIG_FILE, "r", encoding="utf-8") as file:
    config = json.load(file)


# Create logs folder
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            LOG_DIR / "pipeline.log",
            encoding="utf-8"
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def main():
    # Read file paths from configuration
    input_file = BASE_DIR / config["input_file"]
    output_file = BASE_DIR / config["output_file"]

    try:
        logger.info("Starting data processing pipeline")

        # Process input data
        result = process_file(
            input_file,
            output_file,
            config
        )

        print("\nCleaned Data:")
        print(result)

        logger.info("Pipeline completed successfully")
        print("\nPipeline completed successfully!")

    except Exception:
        logger.exception("Pipeline failed")
        raise


if __name__ == "__main__":
    main()
