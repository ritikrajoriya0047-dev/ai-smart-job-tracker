from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from collections import Counter

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

    # DSA & Core CS
"dsa": ["Software Engineer", "Backend Developer", "SDE"],
"data structures": ["Software Engineer", "Backend Developer"],
"algorithms": ["Software Engineer", "SDE"],
"oops": ["Software Engineer", "Backend Developer"],
"operating systems": ["System Engineer", "Software Engineer"],
"computer networks": ["Network Engineer", "Software Engineer"],
"dbms": ["Database Developer", "Backend Developer"],

# Salesforce
"salesforce": ["Salesforce Developer", "CRM Developer"],
"apex": ["Salesforce Developer"],
"lightning": ["Salesforce Developer", "CRM Developer"],
"salesforce admin": ["Salesforce Administrator"],
"sales cloud": ["Salesforce Consultant"],
"service cloud": ["Salesforce Consultant"],

# Cloud Computing
"cloud computing": ["Cloud Engineer", "Cloud Architect"],
"aws ec2": ["Cloud Engineer"],
"aws lambda": ["Cloud Engineer", "Serverless Developer"],
"aws s3": ["Cloud Engineer"],
"azure devops": ["DevOps Engineer"],
"azure functions": ["Cloud Engineer"],
"google cloud": ["Cloud Engineer"],
"cloud security": ["Cloud Security Engineer"],

# Data Engineering
"apache spark": ["Data Engineer", "Big Data Engineer"],
"hadoop": ["Big Data Engineer", "Data Engineer"],
"hive": ["Data Engineer"],
"kafka": ["Data Engineer", "Backend Developer"],
"airflow": ["Data Engineer"],
"etl": ["Data Engineer"],
"data warehousing": ["Data Engineer"],
"snowflake": ["Data Engineer", "Data Architect"],

# AI / LLM
"chatgpt": ["AI Engineer", "LLM Developer"],
"prompt engineering": ["AI Engineer", "Generative AI Engineer"],
"rag": ["LLM Engineer", "AI Engineer"],
"vector database": ["LLM Engineer"],
"pinecone": ["LLM Engineer"],
"weaviate": ["LLM Engineer"],
"hugging face": ["AI Engineer", "ML Engineer"],

# Blockchain
"blockchain": ["Blockchain Developer"],
"ethereum": ["Blockchain Developer"],
"solidity": ["Blockchain Developer"],
"web3": ["Blockchain Developer"],

# SAP / ERP
"sap": ["SAP Consultant"],
"sap abap": ["SAP ABAP Developer"],
"sap fico": ["SAP FICO Consultant"],
"sap hana": ["SAP Consultant"],
"erp": ["ERP Consultant"],

# CRM
"crm": ["CRM Developer", "Business Analyst"],
"zoho": ["CRM Developer"],
"hubspot": ["CRM Specialist"],
"sales": ["Sales Executive", "Business Development Executive"],
"business development": ["Business Development Executive"],

# UI/UX Advanced
"photoshop": ["Graphic Designer", "UI Designer"],
"illustrator": ["Graphic Designer"],
"canva": ["Graphic Designer", "Content Designer"],

# Automation
"robot framework": ["Automation Engineer"],
"cypress": ["QA Automation Engineer"],
"playwright": ["QA Automation Engineer"],
"postman": ["API Tester", "Backend Developer"],

# Containers & DevOps Advanced
"helm": ["DevOps Engineer"],
"grafana": ["DevOps Engineer", "Site Reliability Engineer"],
"prometheus": ["DevOps Engineer"],
"nginx": ["DevOps Engineer", "Backend Developer"],
"apache": ["System Administrator"],
"ci/cd": ["DevOps Engineer"],

# SRE
"site reliability engineering": ["Site Reliability Engineer"],
"sre": ["Site Reliability Engineer"],

# Embedded Systems
"embedded c": ["Embedded Engineer"],
"arduino": ["Embedded Engineer", "IoT Engineer"],
"raspberry pi": ["IoT Engineer"],
"iot": ["IoT Engineer"],

# Game Development
"unity": ["Game Developer"],
"unreal engine": ["Game Developer"],
"opengl": ["Graphics Engineer", "Game Developer"],

# Analytics
"business intelligence": ["BI Developer", "Business Analyst"],
"qlik sense": ["BI Developer"],
"qlikview": ["BI Developer"],

# Soft Skills
"communication": ["Business Analyst", "Project Manager"],
"leadership": ["Project Manager", "Team Lead"],
"problem solving": ["Software Engineer", "SDE"],
"team management": ["Project Manager"],

# Finance
"financial analysis": ["Financial Analyst"],
"accounting": ["Accountant"],
"taxation": ["Tax Consultant"],

# HR
"recruitment": ["HR Executive", "Talent Acquisition Specialist"],
"talent acquisition": ["Talent Acquisition Specialist"],
"hr management": ["HR Manager"],

# Digital Marketing
"seo": ["SEO Specialist", "Digital Marketing Executive"],
"sem": ["Digital Marketing Executive"],
"google ads": ["Digital Marketing Specialist"],
"social media marketing": ["Digital Marketing Executive"],
"content marketing": ["Content Strategist"],

    # UI/UX
    "figma": ["UI/UX Designer", "Product Designer"],
    "adobe xd": ["UI/UX Designer"],
    "ui design": ["UI Designer", "Product Designer"],
    "ux design": ["UX Designer", "Product Designer"],

        # Aliases

    "js": ["Frontend Developer", "Full Stack Developer", "Web Developer"],

    "reactjs": ["Frontend Developer", "Full Stack Developer"],
    "react.js": ["Frontend Developer", "Full Stack Developer"],

    "node": ["Backend Developer", "Full Stack Developer"],
    "nodejs": ["Backend Developer", "Full Stack Developer"],

    "postgres": ["Database Developer", "Backend Developer"],
    "postgres database": ["Database Developer", "Backend Developer"],

    "ml": ["ML Engineer", "Data Scientist"],

    "ai": ["AI Engineer", "ML Engineer"],

    "oop": ["Software Engineer", "Backend Developer"],
    "object oriented programming": ["Software Engineer", "Backend Developer"],

    "powerbi": ["Data Analyst", "Business Analyst"],

    "tf": ["ML Engineer", "AI Engineer"],

    "git hub": ["Software Developer", "Full Stack Developer"],

    "aws cloud": ["Cloud Engineer", "DevOps Engineer"],

    "google cloud platform": ["Cloud Engineer", "DevOps Engineer"],

    "data structures and algorithms": ["Software Engineer", "SDE"],

    "chat gpt": ["AI Engineer", "LLM Developer"],

    "gen ai": ["Generative AI Engineer", "AI Developer"],

    "k8s": ["DevOps Engineer", "Cloud Engineer"],

    "containerization": ["DevOps Engineer", "Cloud Engineer"],

    "ci cd": ["DevOps Engineer"],

    "rest api": ["Backend Developer", "API Developer"],

    "api development": ["Backend Developer", "API Developer"],

    "microservices": ["Backend Developer", "Software Engineer"],

    "web development": ["Frontend Developer", "Full Stack Developer"],

    "backend development": ["Backend Developer", "Software Engineer"],

    "frontend development": ["Frontend Developer", "UI Developer"],

    "full stack": ["Full Stack Developer"],

    "full stack development": ["Full Stack Developer"]
}

@router.post("/")
def get_recommendations(skills: list[str], db: Session = Depends(get_db)):
    """
    Recommend job roles based on a user's skillset.
    Uses a predefined skill-to-role map and filters out roles the user has already applied for.
    """
    skills_lower = [s.lower().strip() for s in skills]

    # Find matching job roles from skill map
    matched_skills = [skill for skill in skills_lower if skill in SKILL_JOB_MAP]
    
    # Flatten the list of roles for matched skills
    matched_roles = [role for skill in matched_skills for role in SKILL_JOB_MAP[skill]]

    # Count frequency of each role to determine the best match
    role_scores = Counter(matched_roles)

    # Extract the top 5 matching roles
    top_roles = [{"role": role, "match_score": score} for role, score in role_scores.most_common(5)]

    # Fetch ONLY the role column from the database to save memory and bandwidth
    # Using a set for O(1) lookups
    applied_roles = {role[0].lower() for role in db.query(Job.role).all()}

    # Check which top roles have NOT been applied to yet
    not_applied = [
        role_data for role_data in top_roles
        if role_data["role"].lower() not in applied_roles
    ]

    return {
        "your_skills": skills_lower,
        "matched_skills": matched_skills,
        "top_recommended_roles": top_roles,
        "not_applied_yet": not_applied,
        "tip": "Focus on roles in not_applied_yet — these match your skills but you haven't applied yet!"
    }