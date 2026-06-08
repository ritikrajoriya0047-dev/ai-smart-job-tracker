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
def get_stats(db: Session = Depends(get_db)):
    total     = db.query(Job).count()
    applied   = db.query(Job).filter(Job.status=="Applied").count()
    screening = db.query(Job).filter(Job.status=="Screening").count()
    interview = db.query(Job).filter(Job.status=="Interview").count()
    offer     = db.query(Job).filter(Job.status=="Offer").count()
    rejected  = db.query(Job).filter(Job.status=="Rejected").count()

    cutoff   = date.today() - timedelta(days=7)
    followup = db.query(Job).filter(
        Job.status=="Applied",
        Job.date_applied <= cutoff
    ).count()

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