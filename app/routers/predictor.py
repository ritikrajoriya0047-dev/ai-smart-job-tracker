from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from collections import Counter
from app.database import get_db
from app.models import Job

router = APIRouter(prefix="/predict", tags=["Success Predictor"])

# --- Helper Functions ---

def _calculate_score(total: int, interview: int, offer: int, rejected: int) -> int:
    """Calculate a success score from 0 to 100 based on conversion metrics."""
    if total == 0:
        return 0

    positive = interview + offer
    positive_rate = positive / total
    
    offer_bonus = (offer / total) * 30
    base_score = positive_rate * 70
    
    rejection_rate_val = rejected / total
    penalty = (rejection_rate_val - 0.5) * 20 if rejection_rate_val > 0.5 else 0

    score = round(base_score + offer_bonus - penalty)
    return max(0, min(score, 100))


def _determine_grade(score: int) -> tuple[str, str, str]:
    """Return grade, message, and tip based on the success score."""
    if score >= 75:
        return ("Excellent", "Outstanding! You are getting great results.", "Focus on companies where you got offers before.")
    if score >= 50:
        return ("Good", "Good progress! Keep applying consistently.", "Follow up with companies after 7 days of applying.")
    if score >= 25:
        return ("Average", "You are getting some results. Keep improving.", "Customize your resume for each job description.")
    if score >= 10:
        return ("Needs Improvement", "High rejection rate. Focus on quality over quantity.", "Use the resume parser to match your skills with job requirements.")
    
    return ("Just Starting", "Keep going! Apply to more relevant jobs.", "Apply to jobs that match your skill set for better results.")


def _calculate_best_source(jobs: list[tuple]) -> tuple[str, dict]:
    """Calculate the highest converting job source based on weighted outcomes."""
    source_stats = {}
    
    for source, status in jobs:
        src = source or "Unknown"
        if src not in source_stats:
            source_stats[src] = {"total": 0, "interviews": 0, "offers": 0}
            
        source_stats[src]["total"] += 1
        if status == "Interview":
            source_stats[src]["interviews"] += 1
        if status == "Offer":
            source_stats[src]["offers"] += 1

    best_source = "Unknown"
    if source_stats:
        best_source = max(
            source_stats.items(),
            key=lambda x: (x[1]["offers"] * 3 + x[1]["interviews"]) / x[1]["total"] if x[1]["total"] > 0 else 0
        )[0]
        
    return best_source, source_stats


@router.get("/")
def predict_success(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """
    Predict the success of a user's job search based on historical application data.
    """
    # 1. Fetch Aggregated Status Data
    status_query = db.query(Job.status, func.count(Job.id))
    if user_id:
        status_query = status_query.filter(Job.user_id == user_id)
        
    status_counts = dict(status_query.group_by(Job.status).all())
    total = sum(status_counts.values())
    
    if total == 0:
        return {"total_applications": 0, "message": "No applications found. Add some jobs first!"}

    # 2. Extract Key Metrics
    interview = status_counts.get("Interview", 0)
    offer = status_counts.get("Offer", 0)
    rejected = status_counts.get("Rejected", 0)
    screening = status_counts.get("Screening", 0)
    applied = status_counts.get("Applied", 0)

    offer_rate = round(offer / total * 100, 1)
    interview_rate = round(interview / total * 100, 1)
    rejection_rate = round(rejected / total * 100, 1)

    # 3. Calculate Score & Grade
    score = _calculate_score(total, interview, offer, rejected)
    grade, message, tip = _determine_grade(score)

    # 4. Determine Best Job Source
    source_query = db.query(Job.source, Job.status)
    if user_id:
        source_query = source_query.filter(Job.user_id == user_id)
        
    best_source, source_stats = _calculate_best_source(source_query.all())

    return {
        "total_applications": total,
        "by_status": {
            "Applied": applied,
            "Screening": screening,
            "Interview": interview,
            "Offer": offer,
            "Rejected": rejected
        },
        "interview_rate_pct": interview_rate,
        "offer_rate_pct": offer_rate,
        "rejection_rate_pct": rejection_rate,
        "success_score": f"{score}/100",
        "grade": grade,
        "message": message,
        "tip": tip,
        "best_source": best_source,
        "source_breakdown": source_stats
    }