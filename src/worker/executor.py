import logging
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from src.models import Job, JobStatus
from src.handlers.registry import registry

logger = logging.getLogger(__name__)


def execute_job(db: Session, job: Job) -> None:
    """Transition job through states: RUNNING → COMPLETED or FAILED/RETRYING/DEAD."""
    handler = registry.get(job.handler_name)

    # Validate payload before running
    if not handler.validate(job.payload):
        job.status = JobStatus.FAILED
        job.error_message = f"Payload validation failed for handler '{job.handler_name}'"
        job.finished_at = datetime.now(timezone.utc)
        db.commit()
        logger.error(f"Job {job.id}: validation failed")
        return

    # Mark as RUNNING
    job.status = JobStatus.RUNNING
    job.started_at = datetime.now(timezone.utc)
    db.commit()
    logger.info(f"Job {job.id}: RUNNING ({job.handler_name})")

    try:
        result = handler.execute(job.payload)
        job.status = JobStatus.COMPLETED
        job.finished_at = datetime.now(timezone.utc)
        db.commit()
        logger.info(f"Job {job.id}: COMPLETED — {result}")

    except Exception as e:
        job.retries += 1
        job.error_message = str(e)

        if job.retries >= job.max_retries:
            job.status = JobStatus.DEAD
            job.finished_at = datetime.now(timezone.utc)
            db.commit()
            logger.error(f"Job {job.id}: DEAD after {job.retries} retries — {e}")
        else:
            job.status = JobStatus.RETRYING
            db.commit()
            logger.warning(f"Job {job.id}: RETRYING ({job.retries}/{job.max_retries}) — {e}")
