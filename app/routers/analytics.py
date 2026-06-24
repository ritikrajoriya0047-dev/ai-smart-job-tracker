from typing import Optional
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date, timedelta
import pandas as pd
import io

from app.database import get_db
from app.models import Job

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# --- Helper Functions ---

def _get_status_counts(db: Session, user_id: Optional[int]) -> dict:
    """Fetch and aggregate job counts grouped by status."""
    query = db.query(Job.status, func.count(Job.id))
    if user_id:
        query = query.filter(Job.user_id == user_id)
    return dict(query.group_by(Job.status).all())


def _get_followups_needed(db: Session, user_id: Optional[int]) -> int:
    """Calculate how many applications are stuck in 'Applied' for over 7 days."""
    cutoff = date.today() - timedelta(days=7)
    query = db.query(Job).filter(Job.status == "Applied", Job.date_applied <= cutoff)
    if user_id:
        query = query.filter(Job.user_id == user_id)
    return query.count()


@router.get("/")
def get_stats(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """
    Retrieve application statistics aggregated by status.
    Uses database-level grouping to minimize memory usage and optimize performance.
    """
    # 1. Fetch data via helper functions
    status_counts = _get_status_counts(db, user_id)
    followups = _get_followups_needed(db, user_id)
    
    total = sum(status_counts.values())
    
    # We use `.get()` with a default of 0 because certain statuses might not 
    # exist in the DB yet, and we want a stable JSON schema for the frontend.
    applied = status_counts.get("Applied", 0)
    screening = status_counts.get("Screening", 0)
    interview = status_counts.get("Interview", 0)
    offer = status_counts.get("Offer", 0)
    rejected = status_counts.get("Rejected", 0)

    return {
        "total": total,
        "by_status": {
            "Applied": applied,
            "Screening": screening,
            "Interview": interview,
            "Offer": offer,
            "Rejected": rejected
        },
        # We calculate rates purely for the dashboard visualization.
        # The `if total else 0` avoids a nasty ZeroDivisionError on new accounts.
        "interview_rate_pct": round(interview / total * 100, 1) if total else 0,
        "offer_rate_pct": round(offer / total * 100, 1) if total else 0,
        "rejection_rate_pct": round(rejected / total * 100, 1) if total else 0,
        "followup_needed": followups
    }
@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    """
    Export all job applications to a CSV file.
    """
    # We specify exact columns to avoid loading heavy, unnecessary fields 
    # (like full HTML notes) just to build a simple CSV export.
    jobs = db.query(
        Job.id, Job.company, Job.role, Job.status, 
        Job.location, Job.salary, Job.source, 
        Job.date_applied, Job.notes
    ).all()
    
    data = [{
        "id": j.id,
        "company": j.company,
        "role": j.role,
        "status": j.status,
        "location": j.location,
        "salary": j.salary,
        "source": j.source,
        "date_applied": j.date_applied,
        "notes": j.notes
    } for j in jobs]
    
    # We use pandas for CSV generation because it handles edge cases 
    # (like commas inside string fields) automatically without manual escaping.
    df = pd.DataFrame(data)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    
    # Reset stream cursor to the beginning before yielding so the response isn't empty.
    stream.seek(0)
    
    # Streaming the response directly prevents us from having to write a temporary file to disk.
    return StreamingResponse(
        iter([stream.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=job_applications.csv"}
    )

@router.get("/followups")
def get_followup_jobs(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """
    Get a list of jobs that were applied to more than 7 days ago and are still in the 'Applied' state.
    """
    cutoff = date.today() - timedelta(days=7)
    
    query = db.query(Job).filter(
        Job.status == "Applied",
        Job.date_applied <= cutoff
    )
    if user_id:
        query = query.filter(Job.user_id == user_id)
        
    jobs = query.order_by(Job.date_applied.asc()).all()

    result = []
    for j in jobs:
        days_waiting = (date.today() - j.date_applied).days if j.date_applied else 0
        result.append({
            "id":           j.id,
            "company":      j.company,
            "role":         j.role,
            "date_applied": str(j.date_applied),
            "days_waiting": days_waiting,
            "source":       j.source
        })

    return {
        "total_followups": len(result),
        "jobs":            result
    }
@router.get("/upcoming-interviews")
def get_upcoming_interviews(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """
    Retrieve a list of upcoming interviews.
    """
    today = date.today()
    
    # We filter out past interviews because the user usually only cares about 
    # what they need to prepare for *next*, not what already happened.
    query = db.query(Job).filter(
        Job.interview_date.isnot(None),
        Job.interview_date >= today,
        Job.status == "Interview"
    )
    if user_id:
        query = query.filter(Job.user_id == user_id)
        
    # Order by ascending date so the most immediate interviews show up first.
    jobs = query.order_by(Job.interview_date.asc()).all()

    result = []
    for j in jobs:
        # Pre-calculating "days_until" on the backend saves the frontend from doing date math.
        days_until = (j.interview_date - today).days
        result.append({
            "id":             j.id,
            "company":        j.company,
            "role":           j.role,
            "interview_date": str(j.interview_date),
            "days_until":     days_until,
            "location":       j.location,
            "source":         j.source
        })

    return {
        "total_upcoming": len(result),
        "interviews":     result
    }
 