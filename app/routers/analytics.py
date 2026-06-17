from typing import Optional
from fastapi import APIRouter, Depends, Query
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from datetime import date, timedelta
from app.database import get_db
from app.models import Job
import pandas as pd
import io

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/")
@router.get("/")
def get_stats(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    from typing import Optional as Opt
    q = db.query(Job)
    if user_id:
        q = q.filter(Job.user_id == user_id)

    total     = q.count()
    applied   = q.filter(Job.status=="Applied").count()
    screening = q.filter(Job.status=="Screening").count()
    interview = q.filter(Job.status=="Interview").count()
    offer     = q.filter(Job.status=="Offer").count()
    rejected  = q.filter(Job.status=="Rejected").count()

    cutoff   = date.today() - timedelta(days=7)
    followup = db.query(Job).filter(
        Job.user_id == user_id,
        Job.status=="Applied",
        Job.date_applied <= cutoff
    ).count() if user_id else 0

    return {
        "total": total,
        "by_status": {
            "Applied":   applied,
            "Screening": screening,
            "Interview": interview,
            "Offer":     offer,
            "Rejected":  rejected
        },
        "interview_rate_pct": round(interview/total*100, 1) if total else 0,
        "offer_rate_pct":     round(offer/total*100, 1)     if total else 0,
        "rejection_rate_pct": round(rejected/total*100, 1)  if total else 0,
        "followup_needed":    followup
    }
@router.get("/export/csv")
def export_csv(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    data = [{
        "id":           j.id,
        "company":      j.company,
        "role":         j.role,
        "status":       j.status,
        "location":     j.location,
        "salary":       j.salary,
        "source":       j.source,
        "date_applied": j.date_applied,
        "notes":        j.notes
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
    from datetime import date, timedelta
    cutoff = date.today() - timedelta(days=7)
    q = db.query(Job).filter(
        Job.status == "Applied",
        Job.date_applied <= cutoff
    )
    if user_id:
        q = q.filter(Job.user_id == user_id)
    jobs = q.order_by(Job.date_applied.asc()).all()

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
    from datetime import date
    today = date.today()
    q = db.query(Job).filter(
        Job.interview_date.isnot(None),
        Job.interview_date >= today,
        Job.status == "Interview"
    )
    if user_id:
        q = q.filter(Job.user_id == user_id)
    jobs = q.order_by(Job.interview_date.asc()).all()

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
 