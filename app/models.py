from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Job(Base):
    __tablename__ = "jobs"

    id             = Column(Integer, primary_key=True, index=True)
    user_id        = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    company        = Column(String(100), nullable=False)
    role           = Column(String(100), nullable=False)
    status         = Column(String(50), default="Applied")
    location       = Column(String(100))
    salary         = Column(String(50))
    source         = Column(String(50))
    job_url        = Column(String(300))
    notes          = Column(String(500))
    interview_date = Column(Date, nullable=True)
    date_applied   = Column(Date)
    created_at     = Column(DateTime, server_default=func.now())

class StatusHistory(Base):
    __tablename__ = "status_history"

    id         = Column(Integer, primary_key=True)
    job_id     = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"))
    old_status = Column(String(50))
    new_status = Column(String(50))
    changed_at = Column(DateTime, server_default=func.now())

class Referral(Base):
    __tablename__ = "referrals"

    id         = Column(Integer, primary_key=True, index=True)
    user_id    = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name       = Column(String(100), nullable=False)
    company    = Column(String(100))
    linkedin   = Column(String(200))
    email      = Column(String(100))
    status     = Column(String(50), default="Pending")
    notes      = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())

class NoteHistory(Base):
    __tablename__ = "note_history"

    id         = Column(Integer, primary_key=True, index=True)
    job_id     = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"))
    note       = Column(String(1000), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

class User(Base):
    __tablename__ = "users"

    id         = Column(Integer, primary_key=True, index=True)
    name       = Column(String(100), nullable=False)
    email      = Column(String(100), unique=True, nullable=False)
    password   = Column(String(200), nullable=False)
    created_at = Column(DateTime, server_default=func.now())