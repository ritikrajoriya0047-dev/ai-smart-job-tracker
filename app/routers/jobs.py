from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.models import Job, StatusHistory
from app.database import get_db
from app import schemas

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/", response_model=schemas.JobResponse, status_code=201)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    """
    Create a new job application record.
    If the transaction fails, it rolls back to maintain database integrity.
    """
    try:
        new_job = Job(**job.dict())
        db.add(new_job)
        db.commit()
        # We refresh the object so it pulls the DB-generated primary key (id) back into our local instance.
        db.refresh(new_job)
        return new_job
    except Exception as e:
        # A failed transaction can lock up the session. Always rollback so the connection is clean for the next request.
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_jobs(
    user_id: Optional[int] = Query(None),
    status:  Optional[str] = Query(None),
    company: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """
    Retrieve job applications.
    Supports filtering by user ID, application status, and company name (case-insensitive).
    """
    # We build the query dynamically so we don't have to write 8 different endpoints for every permutation of filters.
    job_query = db.query(Job)
    
    if user_id: 
        job_query = job_query.filter(Job.user_id == user_id)
    if status:  
        job_query = job_query.filter(Job.status == status)
    if company: 
        # Using ilike ensures that searching for 'google' matches 'Google', making the UX much friendlier.
        job_query = job_query.filter(Job.company.ilike(f"%{company}%"))
        
    return job_query.order_by(Job.created_at.desc()).all()

@router.get("/{job_id}", response_model=schemas.JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific job application by ID.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.put("/{job_id}", response_model=schemas.JobResponse)
def update_job(job_id: int, data: schemas.JobCreate, db: Session = Depends(get_db)):
    """
    Update an existing job application.
    If the status changes, a new entry is added to the StatusHistory table to track progression.
    """
    try:
        # We query the DB first so we can return a clear 404. Doing a blind update 
        # would just silently fail or throw a gross internal server error.
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
            
        old_status = job.status
        
        # exclude_unset=True is critical here. It means we only overwrite the fields 
        # the client explicitly passed in the request payload. It prevents us from wiping out data accidentally.
        for key, val in data.dict(exclude_unset=True).items():
            setattr(job, key, val)
            
        # We want to track the lifecycle of the application. If the status changed, log it.
        # This powers our analytics engine later so users can see how long things took.
        if old_status != data.status:
            history = StatusHistory(
                job_id=job_id,
                old_status=old_status,
                new_status=data.status
            )
            db.add(history)
            
        db.commit()
        db.refresh(job)
        return job
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{job_id}")
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific job application.
    Will cascade delete related history automatically based on database schema setup.
    """
    try:
        # Fetching it first to ensure we drop a 404 if it doesn't exist.
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
            
        # The database schema has 'ondelete="CASCADE"' for foreign keys.
        # This means deleting the job here will cleanly wipe out all related notes and status histories automatically!
        db.delete(job)
        db.commit()
        return {"message": f"Job {job_id} deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

