from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.models import Job, StatusHistory
from app.database import get_db
from app import schemas

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.post("/", response_model=schemas.JobResponse, status_code=201)
def create_job(job: schemas.JobCreate, db: Session = Depends(get_db)):
    try:
        new_job = Job(**job.dict())
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        return new_job
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_jobs(
    user_id: Optional[int] = Query(None),
    status:  Optional[str] = Query(None),
    company: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    q = db.query(Job)
    if user_id: q = q.filter(Job.user_id == user_id)
    if status:  q = q.filter(Job.status == status)
    if company: q = q.filter(Job.company.ilike(f"%{company}%"))
    return q.order_by(Job.created_at.desc()).all()

@router.get("/{job_id}", response_model=schemas.JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.put("/{job_id}", response_model=schemas.JobResponse)
def update_job(job_id: int, data: schemas.JobCreate, db: Session = Depends(get_db)):
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        old_status = job.status
        for key, val in data.dict(exclude_unset=True).items():
            setattr(job, key, val)
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
    try:
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        db.delete(job)
        db.commit()
        return {"message": f"Job {job_id} deleted successfully"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

