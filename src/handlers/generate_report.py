import time
import logging
from src.handlers.base import JobHandler

logger = logging.getLogger(__name__)


class GenerateReportHandler(JobHandler):
    name = "generate_report"

    def validate(self, payload: dict) -> bool:
        return "report_type" in payload

    def execute(self, payload: dict) -> dict:
        report_type = payload["report_type"]
        filters = payload.get("filters", {})
        logger.info(f"Generating '{report_type}' report with filters: {filters}")

        # Simulate report generation work
        time.sleep(2)

        row_count = 150
        return {
            "report_type": report_type,
            "rows_processed": row_count,
            "output_file": f"/reports/{report_type}_{int(time.time())}.csv",
        }
