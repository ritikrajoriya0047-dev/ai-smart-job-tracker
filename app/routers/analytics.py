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

@router.get("/")
def get_stats(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """
    Retrieve application statistics aggregated by status.
    Uses database-level grouping to minimize memory usage and optimize performance.
    """
    # Base query for status aggregation
    status_query = db.query(Job.status, func.count(Job.id))
    if user_id:
        status_query = status_query.filter(Job.user_id == user_id)
    
    # Execute single query grouped by status
    status_counts = dict(status_query.group_by(Job.status).all())
    
    total = sum(status_counts.values())
    applied = status_counts.get("Applied", 0)
    screening = status_counts.get("Screening", 0)
    interview = status_counts.get("Interview", 0)
    offer = status_counts.get("Offer", 0)
    rejected = status_counts.get("Rejected", 0)

    # Calculate follow-ups needed (applied > 7 days ago and still waiting)
    cutoff = date.today() - timedelta(days=7)
    followup_query = db.query(Job).filter(
        Job.status == "Applied",
        Job.date_applied <= cutoff
    )
    if user_id:
        followup_query = followup_query.filter(Job.user_id == user_id)
        
    followup_needed = followup_query.count()

    return {
        "total": total,
        "by_status": {
            "Applied": applied,
            "Screening": screening,
            "Interview": interview,
            "Offer": offer,
            "Rejected": rejected
        },
        "interview_rate_pct": round(interview / total * 100, 1) if total else 0,
        "offer_rate_pct": round(offer / total * 100, 1) if total else 0,
        "rejection_rate_pct": round(rejected / total * 100, 1) if total else 0,
        "followup_needed": followup_needed
    }
@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    """
    Export all job applications to a CSV file.
    Fetches required fields only for better memory efficiency.
    """
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
    df = pd.DataFrame(data)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    stream.seek(0)
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
    
    query = db.query(Job).filter(
        Job.interview_date.isnot(None),
        Job.interview_date >= today,
        Job.status == "Interview"
    )
    if user_id:
        query = query.filter(Job.user_id == user_id)
        
    jobs = query.order_by(Job.interview_date.asc()).all()

    result = []
    for j in jobs:
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
 