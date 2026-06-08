from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Smart Job Tracker",
    description="Track and manage your job applications",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "Smart Job Tracker API is running!"}

@app.get("/health")
def health():
    return {"status": "ok"}