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

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Smart Job Tracker",
    description="Track and manage your job applications",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(jobs_router)
app.include_router(analytics_router)
app.include_router(search_router)
app.include_router(resume_router)
app.include_router(referral_router)

@app.get("/")
def root():
    return {"message": "AI Smart Job Tracker API is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    with open("static/index.html", "r") as f:
        return f.read()