import time
import logging
from src.handlers.base import JobHandler

logger = logging.getLogger(__name__)


class SendEmailHandler(JobHandler):
    name = "send_email"

    def validate(self, payload: dict) -> bool:
        return all(k in payload for k in ("to", "subject", "body"))

    def execute(self, payload: dict) -> dict:
        to = payload["to"]
        subject = payload["subject"]
        logger.info(f"Sending email to '{to}' with subject '{subject}'")

        # Simulate SMTP send
        time.sleep(1)

        return {"to": to, "subject": subject, "status": "sent"}
