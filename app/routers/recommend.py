from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Job

router = APIRouter(prefix="/recommend", tags=["AI Recommendations"])

SKILL_JOB_MAP = {
    "python":         ["Python Developer", "Backend Developer", "Data Engineer", "ML Engineer"],
    "sql":            ["Database Developer", "Data Analyst", "Backend Developer"],
    "postgresql":     ["Database Developer", "Backend Developer", "Data Engineer"],
    "machine learning": ["ML Engineer", "Data Scientist", "AI Developer"],
    "data analysis":  ["Data Analyst", "Business Analyst", "Data Scientist"],
    "django":         ["Python Developer", "Full Stack Developer", "Backend Developer"],
    "fastapi":        ["Python Developer", "Backend Developer", "API Developer"],
    "flask":          ["Python Developer", "Backend Developer", "Full Stack Developer"],
    "javascript":     ["Frontend Developer", "Full Stack Developer", "Web Developer"],
    "react":          ["Frontend Developer", "Full Stack Developer", "UI Developer"],
    "html":           ["Frontend Developer", "Web Developer", "Full Stack Developer"],
    "css":            ["Frontend Developer", "Web Developer", "UI Developer"],
    "docker":         ["DevOps Engineer", "Backend Developer", "Cloud Engineer"],
    "aws":            ["Cloud Engineer", "DevOps Engineer", "Backend Developer"],
    "mongodb":        ["Backend Developer", "Full Stack Developer", "Database Developer"],
    "java":           ["Java Developer", "Backend Developer", "Full Stack Developer"],
    "c++":            ["C++ Developer", "Systems Engineer", "Game Developer"],
    "git":            ["Software Developer", "Backend Developer", "Full Stack Developer"],
    "pandas":         ["Data Analyst", "Data Engineer", "Data Scientist"],
    "numpy":          ["Data Scientist", "ML Engineer", "Data Analyst"],
}

@router.post("/")
def get_recommendations(skills: list[str], db: Session = Depends(get_db)):
    skills_lower = [s.lower().strip() for s in skills]

    # Find matching job roles from skill map
    matched_roles = []
    matched_skills = []
    for skill in skills_lower:
        if skill in SKILL_JOB_MAP:
            matched_skills.append(skill)
            matched_roles.extend(SKILL_JOB_MAP[skill])

    # Remove duplicates and count frequency
    role_score = {}
    for role in matched_roles:
        role_score[role] = role_score.get(role, 0) + 1

    # Sort by highest match score
    sorted_roles = sorted(role_score.items(), key=lambda x: x[1], reverse=True)
    top_roles = [{"role": r, "match_score": s} for r, s in sorted_roles[:5]]

    # Check which roles you have NOT applied to yet
    applied_roles = [j.role.lower() for j in db.query(Job).all()]
    not_applied = [
        r for r in top_roles
        if r["role"].lower() not in applied_roles
    ]

    return {
        "your_skills":        skills_lower,
        "matched_skills":     matched_skills,
        "top_recommended_roles": top_roles,
        "not_applied_yet":    not_applied,
        "tip": "Focus on roles in not_applied_yet — these match your skills but you haven't applied yet!"
    }