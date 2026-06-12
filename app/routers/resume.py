from fastapi import APIRouter, UploadFile, File, HTTPException
import pdfplumber, io

router = APIRouter(prefix="/resume", tags=["Resume"])

SKILLS = [
    "python", "sql", "postgresql", "mysql", "fastapi", "django", "flask",
    "rest api", "git", "docker", "linux", "pandas", "numpy", "matplotlib",
    "machine learning", "data analysis", "javascript", "html", "css",
    "aws", "azure", "google cloud", "mongodb", "redis", "kafka",
    "java", "c++", "c", "react", "node.js", "typescript", "excel", "power bi",
    "tableau", "scikit-learn", "tensorflow", "keras", "opencv", "nlp",
    "salesforce", "dsa", "data structures", "algorithms", "problem solving",
    "object oriented", "oops", "mysql", "firebase", "postman", "github",
    "computer science", "engineering", "api", "backend", "frontend"
]

@router.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files accepted")

    content = await file.read()
    text = ""

    try:
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            total_pages = len(pdf.pages)
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + " "
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not parse PDF: {str(e)}")

    text_lower = text.lower()
    found = [s for s in SKILLS if s in text_lower]

    return {
        "filename":     file.filename,
        "pages":        total_pages,
        "word_count":   len(text.split()),
        "skills_found": found,
        "skill_count":  len(found),
        "preview":      text[:400].strip()
    }
