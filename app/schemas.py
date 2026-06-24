from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class JobCreate(BaseModel):
    """Schema for creating a new job application."""
    company: str
    role: str
    status: Optional[str] = "Applied"
    location: Optional[str] = None
    salary: Optional[str] = None
    source: Optional[str] = None
    job_url: Optional[str] = None
    notes: Optional[str] = None
    date_applied: Optional[date] = None
    interview_date: Optional[date] = None
    user_id: Optional[int] = None


class JobResponse(JobCreate):
    """Schema for returning a job application with DB-generated fields."""
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ReferralCreate(BaseModel):
    """Schema for creating a new referral contact."""
    name: str
    company: Optional[str] = None
    linkedin: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = "Pending"
    notes: Optional[str] = None
    user_id: Optional[int] = None


class ReferralResponse(ReferralCreate):
    """Schema for returning a referral contact."""
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NoteCreate(BaseModel):
    """Schema for creating a new note."""
    note: str


class NoteResponse(NoteCreate):
    """Schema for returning a note."""
    id: int
    job_id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserRegister(BaseModel):
    """Schema for user registration."""
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    """Schema for user authentication."""
    email: str
    password: str


class UserResponse(BaseModel):
    """
    Schema for returning user data. Excludes password to ensure it is never exposed in API responses.
    """
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        # orm_mode=True (from_attributes in v2) is absolute magic. It allows Pydantic to 
        # take a raw SQLAlchemy model object and read properties off it using dot notation 
        # (obj.id) instead of requiring us to manually convert the model to a dictionary first.
        orm_mode = True