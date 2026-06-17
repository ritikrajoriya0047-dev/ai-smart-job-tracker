from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import Job

router = APIRouter(prefix="/predict", tags=["Success Predictor"])

@router.get("/")
def predict_success(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    q = db.query(Job)
    if user_id:
        q = q.filter(Job.user_id == user_id)
    jobs = q.all()

    total = len(jobs)
    if total == 0:
        return {
            "total_applications": 0,
            "message": "No applications found. Add some jobs first!"
        }

    interview  = sum(1 for j in jobs if j.status == "Interview")
    offer      = sum(1 for j in jobs if j.status == "Offer")
    rejected   = sum(1 for j in jobs if j.status == "Rejected")
    screening  = sum(1 for j in jobs if j.status == "Screening")
    applied    = sum(1 for j in jobs if j.status == "Applied")

    # Rates based on total
    offer_rate      = round(offer    / total * 100, 1)
    interview_rate  = round(interview / total * 100, 1)
    rejection_rate  = round(rejected / total * 100, 1)

    # Score out of 100
    # Formula: based on positive outcomes vs total

    # Positive outcomes = interviews + offers
    positive = interview + offer

    # Positive rate out of total
    positive_rate = positive / total

    # Offer bonus — offers are better than interviews
    offer_bonus = (offer / total) * 30

    # Base score from positive rate (max 70)
    base_score = positive_rate * 70

    # Offer bonus (max 30)
    # Total max = 100

    # Rejection penalty — only penalize if rejection rate > 50%
    rejection_rate_val = rejected / total
    if rejection_rate_val > 0.5:
        penalty = (rejection_rate_val - 0.5) * 20
    else:
        penalty = 0

    score = round(base_score + offer_bonus - penalty)
    score = max(0, min(score, 100))

    # Grade
    if score >= 75:
        grade   = "Excellent"
        message = "Outstanding! You are getting great results."
        tip     = "Focus on companies where you got offers before."
    elif score >= 50:
        grade   = "Good"
        message = "Good progress! Keep applying consistently."
        tip     = "Follow up with companies after 7 days of applying."
    elif score >= 25:
        grade   = "Average"
        message = "You are getting some results. Keep improving."
        tip     = "Customize your resume for each job description."
    elif score >= 10:
        grade   = "Needs Improvement"
        message = "High rejection rate. Focus on quality over quantity."
        tip     = "Use the resume parser to match your skills with job requirements."
    else:
        grade   = "Just Starting"
        message = "Keep going! Apply to more relevant jobs."
        tip     = "Apply to jobs that match your skill set for better results."

    # Best source
    source_stats = {}
    for j in jobs:
        src = j.source or "Unknown"
        if src not in source_stats:
            source_stats[src] = {"total": 0, "interviews": 0, "offers": 0}
        source_stats[src]["total"] += 1
        if j.status == "Interview":
            source_stats[src]["interviews"] += 1
        if j.status == "Offer":
            source_stats[src]["offers"] += 1

    best_source = max(
        source_stats.items(),
        key=lambda x: (x[1]["offers"] * 3 + x[1]["interviews"]) / x[1]["total"]
        if x[1]["total"] > 0 else 0
    )

    return {
        "total_applications":  total,
        "by_status": {
            "Applied":   applied,
            "Screening": screening,
            "Interview": interview,
            "Offer":     offer,
            "Rejected":  rejected
        },
        "interview_rate_pct":  interview_rate,
        "offer_rate_pct":      offer_rate,
        "rejection_rate_pct":  rejection_rate,
        "success_score":       f"{score}/100",
        "grade":               grade,
        "message":             message,
        "tip":                 tip,
        "best_source":         best_source[0],
        "source_breakdown":    source_stats
    }