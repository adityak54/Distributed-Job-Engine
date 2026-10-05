import enum
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, DateTime, Enum, JSON, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class JobStatus(str, enum.Enum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"     # Pushed to Redis
    RUNNING = "RUNNING"   # Worker picked it up
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    RETRYING = "RETRYING"
    DEAD = "DEAD"         # Max retries exceeded

class Job(Base):
    __tablename__ = "jobs"

    # Core Identifiers
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    handler_name = Column(String, nullable=False, index=True) # e.g., "generate_report"
    payload = Column(JSON, nullable=False) # The dynamic JSON payload
    
    # State tracking
    status = Column(Enum(JobStatus), default=JobStatus.PENDING, index=True)
    
    # Retry mechanism (from your diagram)
    retries = Column(Integer, default=0)
    max_retries = Column(Integer, default=3)
    error_message = Column(Text, nullable=True)

    # Observability & Metrics (Crucial for Grafana)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)