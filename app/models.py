from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class Job(Base):
    """
    Job application model representing a single application sent by a user.
    """
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    # The ForeignKey explicitly links this job to a user.
    # ondelete="CASCADE" is crucial: if a user deletes their account, the database 
    # will automatically wipe all their jobs so we don't have orphaned data floating around.
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    company = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    status = Column(String(50), default="Applied")
    location = Column(String(100))
    salary = Column(String(50))
    source = Column(String(50))
    job_url = Column(String(300))
    notes = Column(String(500))
    interview_date = Column(Date, nullable=True)
    date_applied = Column(Date)
    created_at = Column(DateTime, server_default=func.now())


class StatusHistory(Base):
    """
    Tracks changes to a job's status over time for analytics purposes.
    """
    __tablename__ = "status_history"

    id = Column(Integer, primary_key=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"))
    old_status = Column(String(50))
    new_status = Column(String(50))
    changed_at = Column(DateTime, server_default=func.now())


class Referral(Base):
    """
    Represents a referral or networking contact.
    """
    __tablename__ = "referrals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)
    company = Column(String(100))
    linkedin = Column(String(200))
    email = Column(String(100))
    status = Column(String(50), default="Pending")
    notes = Column(String(500))
    created_at = Column(DateTime, server_default=func.now())


class NoteHistory(Base):
    """
    Stores individual textual notes added to a job application.
    """
    __tablename__ = "note_history"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"))
    note = Column(String(1000), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class User(Base):
    """
    User model to store registered account information.
    """
    # We define __tablename__ explicitly. If we don't, SQLAlchemy might guess 
    # plural forms incorrectly or use weird casing.
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    # email must be unique and indexed because it's our primary lookup key during login.
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(200), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())