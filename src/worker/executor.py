from datetime import datetime
from src.database import SessionLocal
from src.models import Job, JobStatus
from src.handlers.registry import HANDLER_REGISTRY

def process_job(job_id: str):
    db = SessionLocal()
    try:
        # 1. Fetch the job from Postgres
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            print(f"Job {job_id} not found in DB.")
            return

        # 2. Mark as RUNNING
        job.status = JobStatus.RUNNING
        job.started_at = datetime.utcnow()
        db.commit()

        # 3. Find the correct handler
        handler = HANDLER_REGISTRY.get(job.handler_name)
        if not handler:
            raise ValueError(f"No handler registered for '{job.handler_name}'")

        # 4. Execute the work
        handler.execute(job.payload)

        # 5. Mark as COMPLETED
        job.status = JobStatus.COMPLETED
        job.finished_at = datetime.utcnow()
        db.commit()
        print(f"Job {job_id} COMPLETED.")

    except Exception as e:
        # Catch errors and mark as FAILED
        job.status = JobStatus.FAILED
        job.finished_at = datetime.utcnow()
        job.error_message = str(e)
        db.commit()
        print(f"Job {job_id} FAILED: {str(e)}")
    finally:
        db.close()