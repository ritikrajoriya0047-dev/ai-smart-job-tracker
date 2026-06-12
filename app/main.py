from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.database import engine
from app.models import Base
from app.routers.jobs import router as jobs_router
from app.routers.analytics import router as analytics_router
from app.routers.search import router as search_router
from app.routers.resume import router as resume_router
from app.routers.referral import router as referral_router
from app.routers.recommend import router as recommend_router
from app.routers.predictor import router as predictor_router
from app.routers.notes import router as notes_router
from app.routers.auth import router as auth_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Smart Job Tracker",
    description="Track and manage your job applications",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router)
app.include_router(jobs_router)
app.include_router(analytics_router)
app.include_router(search_router)
app.include_router(resume_router)
app.include_router(referral_router)
app.include_router(recommend_router)
app.include_router(predictor_router)
app.include_router(notes_router)

@app.get("/")
def root():
    return {"message": "AI Smart Job Tracker API is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/login-page", response_class=HTMLResponse)
def login_page():
    with open("static/login.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return f.read()