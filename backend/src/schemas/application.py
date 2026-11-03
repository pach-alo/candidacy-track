from datetime import date
from pydantic import BaseModel, ValidationError, HttpUrl
from enum import Enum

class ApplicationStatus(str, Enum):
    SAVED = "saved"
    APPLIED = "applied"
    ASSESSMENT = "assessment"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"

class ApplicationCreate(BaseModel):
    company_id: int
    job_title: str
    job_url: HttpUrl | None = None
    date_applied: date | None = None
    status: ApplicationStatus = ApplicationStatus.SAVED.value
    notes: str | None = None