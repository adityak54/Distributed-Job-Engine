import logging
import signal
import sys

from src.config import settings
from src.database import SessionLocal
from src.models import Job, JobStatus
from src.queue.base import BaseQueue
from src.queue.memory_queue import MemoryQueue
from src.queue.redis_queue import RedisQueue
from src.worker.executor import execute_job
from src.worker.retry import wait_for_retry

# Registering handlers on import
import src.handlers  # noqa: F401

logger = logging.getLogger(__name__)

shutdown_requested = False


def _handle_signal(signum, frame):
    global shutdown_requested
    logger.info(f"Received signal {signum}, shutting down gracefully...")
    shutdown_requested = True


def build_queue() -> BaseQueue:
    if settings.REDIS_URL:
        logger.info(f"Using Redis queue at {settings.REDIS_URL}")
        return RedisQueue(settings.REDIS_URL)
    logger.info("Using in-memory queue (dev mode)")
    return MemoryQueue()


def run_worker():
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    queue = build_queue()
    logger.info(f"Worker '{settings.WORKER_ID}' started. Waiting for jobs...")

    while not shutdown_requested:
        job_id = queue.dequeue(timeout=5)
        if job_id is None:
            continue

        db = SessionLocal()
        try:
            job = db.query(Job).filter(Job.id == job_id).first()
            if job is None:
                logger.warning(f"Job {job_id} not found in database, skipping")
                continue

            if job.status not in (JobStatus.PENDING, JobStatus.QUEUED, JobStatus.RETRYING):
                logger.warning(f"Job {job_id} has status {job.status}, skipping")
                continue

            execute_job(db, job)

            # Re-enqueue if the job needs a retry
            if job.status == JobStatus.RETRYING:
                wait_for_retry(job.retries)
                queue.enqueue(job_id)

        except Exception as e:
            logger.exception(f"Unexpected error processing job {job_id}: {e}")
        finally:
            db.close()

    logger.info("Worker shut down.")


if __name__ == "__main__":
    run_worker()
