import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

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

# Initialize database schema automatically. 
# In a massive production app, we'd use Alembic for migrations instead, 
# but for a tracker this size, create_all is completely fine and reduces setup friction.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Smart Job Tracker",
    description="Track and manage your job applications efficiently.",
    version="1.0.0"
)

# Configure CORS for frontend access.
# If we don't do this, modern browsers will block our frontend from talking to our backend API
# due to Same-Origin Policy restrictions, especially since we might host the frontend elsewhere (like GitHub Pages).
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ritikrajoriya0047-dev.github.io",
        "http://localhost:3000",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (HTML, CSS, JS). 
# This lets FastAPI serve our frontend assets directly without needing a separate web server like Nginx.
app.mount("/static", StaticFiles(directory="static"), name="static")

# We split the API into discrete routers instead of dumping 50 endpoints in main.py.
# This keeps the codebase highly modular, testable, and prevents merge conflict nightmares on big teams.
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
    """Health check endpoint to verify API is running."""
    return {"message": "AI Smart Job Tracker API is running!"}


@app.get("/health")
def health():
    """Standard health check endpoint."""
    return {"status": "ok"}


@app.get("/login-page", response_class=HTMLResponse)
def login_page():
    """Serve the static login HTML page."""
    with open("static/login.html", "r", encoding="utf-8") as file:
        return file.read()


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    """Serve the static dashboard HTML page."""
    with open("static/index.html", "r", encoding="utf-8") as file:
        return file.read()
