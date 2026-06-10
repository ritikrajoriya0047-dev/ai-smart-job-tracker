from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Job

router = APIRouter(prefix="/predict", tags=["Success Predictor"])

@router.get("/")
def predict_success(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    total    = len(jobs)

    if total == 0:
        return {"message": "No applications found. Add some jobs first!"}

    interview = sum(1 for j in jobs if j.status in ["Interview", "Offer"])
    offer     = sum(1 for j in jobs if j.status == "Offer")
    rejected  = sum(1 for j in jobs if j.status == "Rejected")
    pending   = sum(1 for j in jobs if j.status == "Applied")

    interview_rate = round(interview / total * 100, 1)
    offer_rate     = round(offer     / total * 100, 1)
    rejection_rate = round(rejected  / total * 100, 1)

    # Score out of 100
    score = 0
    score += min(interview_rate * 2, 40)
    score += min(offer_rate * 4, 40)
    score += max(0, 20 - rejection_rate)
    score = round(score)

    # Grade
    if score >= 80:
        grade   = "Excellent"
        message = "You are performing very well! Keep applying to similar companies."
        tip     = "Focus on companies where you got interviews before."
    elif score >= 60:
        grade   = "Good"
        message = "Good progress! A few improvements can increase your success rate."
        tip     = "Try to improve your resume keywords and apply to more companies."
    elif score >= 40:
        grade   = "Average"
        message = "You are getting some responses but there is room to improve."
        tip     = "Customize your resume for each job and follow up after 7 days."
    else:
        grade   = "Needs Improvement"
        message = "Do not give up! Focus on quality applications over quantity."
        tip     = "Use the resume parser to match your skills with job requirements."

    # Best performing source
    source_stats = {}
    for j in jobs:
        src = j.source or "Unknown"
        if src not in source_stats:
            source_stats[src] = {"total": 0, "interviews": 0}
        source_stats[src]["total"] += 1
        if j.status in ["Interview", "Offer"]:
            source_stats[src]["interviews"] += 1

    best_source = max(
        source_stats.items(),
        key=lambda x: x[1]["interviews"] / x[1]["total"] if x[1]["total"] > 0 else 0
    )

    return {
        "total_applications":  total,
        "interview_rate_pct":  interview_rate,
        "offer_rate_pct":      offer_rate,
        "rejection_rate_pct":  rejection_rate,
        "pending_responses":   pending,
        "success_score":       f"{score}/100",
        "grade":               grade,
        "message":             message,
        "tip":                 tip,
        "best_source":         best_source[0],
        "source_breakdown":    source_stats
    }