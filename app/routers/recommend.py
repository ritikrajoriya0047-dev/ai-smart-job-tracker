from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Job

router = APIRouter(prefix="/recommend", tags=["AI Recommendations"])

SKILL_JOB_MAP = {
    # Programming Languages
    "python": ["Python Developer", "Backend Developer", "Data Engineer", "ML Engineer"],
    "java": ["Java Developer", "Backend Developer", "Software Engineer"],
    "c": ["Software Developer", "Embedded Engineer", "Systems Engineer"],
    "c++": ["C++ Developer", "Game Developer", "Systems Engineer"],
    "c#": [".NET Developer", "Software Engineer", "Backend Developer"],
    "javascript": ["Frontend Developer", "Full Stack Developer", "Web Developer"],
    "typescript": ["Frontend Developer", "Full Stack Developer", "Web Developer"],
    "php": ["PHP Developer", "Backend Developer", "Web Developer"],
    "ruby": ["Ruby Developer", "Backend Developer"],
    "go": ["Go Developer", "Backend Developer", "Cloud Engineer"],
    "rust": ["Rust Developer", "Systems Engineer"],
    "kotlin": ["Android Developer", "Mobile Developer"],
    "swift": ["iOS Developer", "Mobile Developer"],
    "r": ["Data Analyst", "Data Scientist"],
    "scala": ["Data Engineer", "Backend Developer"],

    # Frontend
    "html": ["Frontend Developer", "Web Developer"],
    "css": ["Frontend Developer", "UI Developer"],
    "bootstrap": ["Frontend Developer", "Web Developer"],
    "tailwind": ["Frontend Developer", "UI Developer"],
    "react": ["Frontend Developer", "Full Stack Developer"],
    "next.js": ["Frontend Developer", "Full Stack Developer"],
    "angular": ["Frontend Developer", "Web Developer"],
    "vue.js": ["Frontend Developer", "Web Developer"],
    "jquery": ["Frontend Developer", "Web Developer"],

    # Backend
    "django": ["Python Developer", "Backend Developer"],
    "flask": ["Python Developer", "Backend Developer"],
    "fastapi": ["Python Developer", "API Developer"],
    "spring boot": ["Java Developer", "Backend Developer"],
    "node.js": ["Backend Developer", "Full Stack Developer"],
    "express.js": ["Backend Developer", "Full Stack Developer"],
    ".net": [".NET Developer", "Backend Developer"],

    # Databases
    "sql": ["Database Developer", "Data Analyst"],
    "mysql": ["Database Developer", "Backend Developer"],
    "postgresql": ["Database Developer", "Backend Developer"],
    "mongodb": ["Backend Developer", "Full Stack Developer"],
    "sqlite": ["Backend Developer", "Database Developer"],
    "oracle": ["Database Administrator", "Database Developer"],
    "redis": ["Backend Developer", "Cloud Engineer"],
    "firebase": ["Mobile Developer", "Backend Developer"],

    # Data Science
    "pandas": ["Data Analyst", "Data Scientist"],
    "numpy": ["Data Scientist", "ML Engineer"],
    "matplotlib": ["Data Analyst", "Data Scientist"],
    "seaborn": ["Data Analyst", "Data Scientist"],
    "power bi": ["Data Analyst", "Business Analyst"],
    "tableau": ["Data Analyst", "Business Analyst"],
    "excel": ["Data Analyst", "Business Analyst"],
    "statistics": ["Data Scientist", "Data Analyst"],
    "data analysis": ["Data Analyst", "Business Analyst"],
    "data visualization": ["Data Analyst", "BI Developer"],

    # Machine Learning & AI
    "machine learning": ["ML Engineer", "Data Scientist"],
    "deep learning": ["AI Engineer", "ML Engineer"],
    "tensorflow": ["ML Engineer", "AI Engineer"],
    "pytorch": ["ML Engineer", "AI Engineer"],
    "nlp": ["NLP Engineer", "AI Engineer"],
    "computer vision": ["Computer Vision Engineer", "AI Engineer"],
    "artificial intelligence": ["AI Engineer", "ML Engineer"],
    "llm": ["AI Engineer", "Generative AI Engineer"],
    "generative ai": ["Generative AI Engineer", "AI Developer"],
    "openai": ["AI Engineer", "LLM Developer"],
    "langchain": ["LLM Developer", "AI Engineer"],

    # Cloud & DevOps
    "docker": ["DevOps Engineer", "Cloud Engineer"],
    "kubernetes": ["DevOps Engineer", "Cloud Engineer"],
    "aws": ["Cloud Engineer", "DevOps Engineer"],
    "azure": ["Cloud Engineer", "DevOps Engineer"],
    "gcp": ["Cloud Engineer", "DevOps Engineer"],
    "jenkins": ["DevOps Engineer", "Automation Engineer"],
    "terraform": ["DevOps Engineer", "Cloud Engineer"],
    "ansible": ["DevOps Engineer", "Automation Engineer"],
    "linux": ["System Administrator", "DevOps Engineer"],
    "shell scripting": ["DevOps Engineer", "System Administrator"],

    # Version Control
    "git": ["Software Developer", "Backend Developer"],
    "github": ["Software Developer", "Full Stack Developer"],
    "gitlab": ["DevOps Engineer", "Software Developer"],

    # Mobile Development
    "android": ["Android Developer", "Mobile Developer"],
    "ios": ["iOS Developer", "Mobile Developer"],
    "flutter": ["Flutter Developer", "Mobile Developer"],
    "react native": ["Mobile Developer", "Frontend Developer"],

    # Cyber Security
    "cyber security": ["Security Analyst", "Cyber Security Engineer"],
    "ethical hacking": ["Ethical Hacker", "Security Analyst"],
    "penetration testing": ["Penetration Tester", "Security Engineer"],
    "network security": ["Security Engineer", "Network Engineer"],

    # Networking
    "networking": ["Network Engineer", "System Administrator"],
    "ccna": ["Network Engineer", "Network Administrator"],
    "tcp/ip": ["Network Engineer", "System Administrator"],

    # Testing
    "manual testing": ["QA Engineer", "Software Tester"],
    "automation testing": ["QA Automation Engineer", "Software Tester"],
    "selenium": ["QA Automation Engineer", "Test Engineer"],
    "pytest": ["QA Engineer", "Python Developer"],

    # Business & Management
    "project management": ["Project Manager", "Program Manager"],
    "agile": ["Scrum Master", "Project Manager"],
    "scrum": ["Scrum Master", "Project Manager"],
    "jira": ["Project Manager", "Business Analyst"],

    # UI/UX
    "figma": ["UI/UX Designer", "Product Designer"],
    "adobe xd": ["UI/UX Designer"],
    "ui design": ["UI Designer", "Product Designer"],
    "ux design": ["UX Designer", "Product Designer"]
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