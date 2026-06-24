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
    """
    Parse an uploaded PDF resume and extract text and matching skills.
    """
    # We restrict to PDFs early to fail fast. Parsing Word docs or images 
    # requires entirely different libraries (like python-docx or OCR).
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files accepted")

    content = await file.read()
    extracted_text = ""

    try:
        # We load the PDF directly from the byte stream in memory (io.BytesIO).
        # This completely avoids writing temporary files to disk, saving I/O overhead 
        # and preventing disk clutter/cleanup issues.
        with pdfplumber.open(io.BytesIO(content)) as pdf:
            total_pages = len(pdf.pages)
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    extracted_text += page_text + " "
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not parse PDF: {str(e)}")

    # We convert all text to lowercase. This normalizes the data so we don't 
    # have to do complex regex matching for "Python", "PYTHON", and "python".
    text_lower = extracted_text.lower()
    found_skills = [skill for skill in SKILLS if skill in text_lower]

    return {
        "filename": file.filename,
        "pages": total_pages,
        "word_count": len(extracted_text.split()),
        "skills_found": found_skills,
        "skill_count": len(found_skills),
        # We only return the first 400 chars for the preview. Returning the entire 
        # resume text would blow up the JSON payload size unnecessarily.
        "preview": extracted_text[:400].strip()
    }
