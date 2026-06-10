from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import NoteHistory, Job
from app import schemas

router = APIRouter(prefix="/jobs", tags=["Notes History"])

@router.post("/{job_id}/notes", response_model=schemas.NoteResponse, status_code=201)
def add_note(job_id: int, data: schemas.NoteCreate, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    try:
        note = NoteHistory(job_id=job_id, note=data.note)
        db.add(note)
        db.commit()
        db.refresh(note)
        return note
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{job_id}/notes")
def get_notes(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    notes = db.query(NoteHistory).filter(
        NoteHistory.job_id == job_id
    ).order_by(NoteHistory.created_at.desc()).all()
    return {
        "job_id":    job_id,
        "company":   job.company,
        "role":      job.role,
        "total_notes": len(notes),
        "notes":     notes
    }

@router.delete("/{job_id}/notes/{note_id}")
def delete_note(job_id: int, note_id: int, db: Session = Depends(get_db)):
    note = db.query(NoteHistory).filter(
        NoteHistory.id == note_id,
        NoteHistory.job_id == job_id
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"message": f"Note {note_id} deleted"}