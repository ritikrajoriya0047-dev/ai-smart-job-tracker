from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class JobCreate(BaseModel):
    company:      str
    role:         str
    status:       Optional[str] = "Applied"
    location:     Optional[str] = None
    salary:       Optional[str] = None
    source:       Optional[str] = None
    job_url:      Optional[str] = None
    notes:        Optional[str] = None
    date_applied: Optional[date] = None

class JobResponse(JobCreate):
    id:         int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ReferralCreate(BaseModel):
    name:    str
    company: Optional[str] = None
    linkedin:Optional[str] = None
    email:   Optional[str] = None
    status:  Optional[str] = "Pending"
    notes:   Optional[str] = None

class ReferralResponse(ReferralCreate):
    id:         int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True