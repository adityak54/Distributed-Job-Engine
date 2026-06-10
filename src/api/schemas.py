from pydantic import BaseModel, Field
from typing import Dict, Any
from datetime import datetime
from src.models import JobStatus

# What the client sends us
class JobCreate(BaseModel):
    handler_name: str = Field(..., example="generate_report")
    payload: Dict[str, Any] = Field(default_factory=dict, example={"user_id": 123})

# What we send back to the client
class JobResponse(BaseModel):
    id: str
    handler_name: str
    status: JobStatus
    created_at: datetime

    class Config:
        from_attributes = True  # Allows Pydantic to read SQLAlchemy models