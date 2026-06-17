from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class JobCreate(BaseModel):
    company:        str
    role:           str
    status:         Optional[str] = "Applied"
    location:       Optional[str] = None
    salary:         Optional[str] = None
    source:         Optional[str] = None
    job_url:        Optional[str] = None
    notes:          Optional[str] = None
    date_applied:   Optional[date] = None
    interview_date: Optional[date] = None
    user_id:        Optional[int] = None

class JobResponse(JobCreate):
    id:         int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class ReferralCreate(BaseModel):
    name:     str
    company:  Optional[str] = None
    linkedin: Optional[str] = None
    email:    Optional[str] = None
    status:   Optional[str] = "Pending"
    notes:    Optional[str] = None
    user_id:  Optional[int] = None

class ReferralResponse(ReferralCreate):
    id:         int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class NoteCreate(BaseModel):
    note: str

class NoteResponse(NoteCreate):
    id:         int
    job_id:     int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
    
class UserRegister(BaseModel):
    name:     str
    email:    str
    password: str

class UserLogin(BaseModel):
    email:    str
    password: str

class UserResponse(BaseModel):
    id:    int
    name:  str
    email: str

    class Config:
        from_attributes = True