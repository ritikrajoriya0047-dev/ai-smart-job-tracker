from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import Referral
from app import schemas

router = APIRouter(prefix="/referrals", tags=["Referral Tracker"])

@router.post("/", response_model=schemas.ReferralResponse, status_code=201)
def create_referral(data: schemas.ReferralCreate, db: Session = Depends(get_db)):
    """
    Create a new referral record.
    """
    try:
        ref = Referral(**data.dict())
        db.add(ref)
        db.commit()
        # We refresh to ensure the returned JSON contains the DB-assigned ID, 
        # which the frontend needs for subsequent edits/deletes.
        db.refresh(ref)
        return ref
    except Exception as e:
        # A failed DB insert leaves the session in an invalid state. 
        # We must rollback before raising the HTTP exception so future requests don't crash.
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_referrals(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    """
    Retrieve referrals, optionally filtered by user ID.
    Results are returned in descending order based on creation time.
    """
    referral_query = db.query(Referral)
    if user_id:
        referral_query = referral_query.filter(Referral.user_id == user_id)
        
    return referral_query.order_by(Referral.created_at.desc()).all()

@router.put("/{ref_id}", response_model=schemas.ReferralResponse)
def update_referral(ref_id: int, data: schemas.ReferralCreate, db: Session = Depends(get_db)):
    """
    Update an existing referral record dynamically.
    """
    ref = db.query(Referral).filter(Referral.id == ref_id).first()
    if not ref:
        raise HTTPException(status_code=404, detail="Referral not found")
        
    # By using `exclude_unset=True`, we only update fields the client explicitly sent. 
    # This enables safe partial updates (PATCH-like behavior) via a PUT endpoint.
    for key, val in data.dict(exclude_unset=True).items():
        setattr(ref, key, val)
        
    db.commit()
    db.refresh(ref)
    return ref

@router.delete("/{ref_id}")
def delete_referral(ref_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific referral record from the database.
    """
    # Fetching the record first allows us to return a semantically correct 404 
    # if it doesn't exist, rather than a generic 500 DB error on delete.
    ref = db.query(Referral).filter(Referral.id == ref_id).first()
    if not ref:
        raise HTTPException(status_code=404, detail="Referral not found")
        
    db.delete(ref)
    db.commit()
    return {"message": f"Referral {ref_id} deleted"}