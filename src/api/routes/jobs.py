from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.models import Job, JobStatus
from src.api.schemas import JobCreate, JobResponse
from src.queue.redis_queue import enqueue_job

router = APIRouter()

# Dependency to get a database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=JobResponse, status_code=202)
def submit_job(job_in: JobCreate, db: Session = Depends(get_db)):
    # 1. Write to Database (PENDING)
    new_job = Job(
        handler_name=job_in.handler_name,
        payload=job_in.payload,
        status=JobStatus.PENDING
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    # 2. Push to Redis & Update State (QUEUED)
    try:
        enqueue_job(new_job.id)
        new_job.status = JobStatus.QUEUED
        db.commit()
        db.refresh(new_job)
    except Exception as e:
        # If Redis is down, it stays PENDING. 
        # A separate cleanup script could re-enqueue PENDING jobs later.
        print(f"Failed to enqueue to Redis: {e}")

    return new_job

@router.get("/{job_id}", response_model=JobResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job