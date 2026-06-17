from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import Referral
from app import schemas

router = APIRouter(prefix="/referrals", tags=["Referral Tracker"])

@router.post("/", response_model=schemas.ReferralResponse, status_code=201)
def create_referral(data: schemas.ReferralCreate, db: Session = Depends(get_db)):
    try:
        ref = Referral(**data.dict())
        db.add(ref)
        db.commit()
        db.refresh(ref)
        return ref
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
def get_referrals(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    q = db.query(Referral)
    if user_id:
        q = q.filter(Referral.user_id == user_id)
    return q.order_by(Referral.created_at.desc()).all()

@router.put("/{ref_id}", response_model=schemas.ReferralResponse)
def update_referral(ref_id: int, data: schemas.ReferralCreate, db: Session = Depends(get_db)):
    ref = db.query(Referral).filter(Referral.id == ref_id).first()
    if not ref:
        raise HTTPException(status_code=404, detail="Referral not found")
    for key, val in data.dict(exclude_unset=True).items():
        setattr(ref, key, val)
    db.commit()
    db.refresh(ref)
    return ref

@router.delete("/{ref_id}")
def delete_referral(ref_id: int, db: Session = Depends(get_db)):
    ref = db.query(Referral).filter(Referral.id == ref_id).first()
    if not ref:
        raise HTTPException(status_code=404, detail="Referral not found")
    db.delete(ref)
    db.commit()
    return {"message": f"Referral {ref_id} deleted"}