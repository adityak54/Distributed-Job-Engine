import time
import logging
from src.handlers.base import JobHandler

logger = logging.getLogger(__name__)


class ProcessCsvHandler(JobHandler):
    name = "process_csv"

    def validate(self, payload: dict) -> bool:
        return "file_path" in payload

    def execute(self, payload: dict) -> dict:
        file_path = payload["file_path"]
        logger.info(f"Processing CSV file: {file_path}")

        # Simulate CSV parsing work
        time.sleep(3)

        return {
            "file_path": file_path,
            "rows_parsed": 1024,
            "errors": 0,
        }
