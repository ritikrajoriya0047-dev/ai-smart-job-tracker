from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app import schemas
import bcrypt

router = APIRouter(prefix="/auth", tags=["Authentication"])

def hash_password(password: str) -> str:
    """
    Generate a bcrypt hash for the provided password.
    We truncate to 72 characters because bcrypt natively truncates inputs longer than 72 bytes.
    Enforcing this limit upfront prevents silent data loss and potential security footguns.
    """
    return bcrypt.hashpw(password[:72].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    """
    Safely compare a plaintext password against a stored bcrypt hash.
    Again, we truncate to 72 characters to match the hashing logic.
    """
    return bcrypt.checkpw(plain[:72].encode('utf-8'), hashed.encode('utf-8'))

@router.post("/register", response_model=schemas.UserResponse, status_code=201)
def register(data: schemas.UserRegister, db: Session = Depends(get_db)):
    """
    Register a new user in the system.
    We hash the password on the fly to ensure we never accidentally log or store plaintext credentials.
    """
    # Bcrypt throws a fit if the payload exceeds 72 bytes. We reject it here
    # rather than failing mysteriously during the hashing process.
    if len(data.password) > 72:
        raise HTTPException(status_code=400, detail="Password must be 72 characters or less")
        
    # We must enforce unique emails to prevent account hijacking and ensure 
    # users can reliably log in and recover their accounts later.
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)  # Refresh so we return the newly generated DB constraints (like the ID)
    return user

@router.post("/login")
def login(data: schemas.UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user and return their session details.
    """
    # We fetch the user first. If they exist, we do a secure timing-safe 
    # password comparison via bcrypt. If either fails, we drop a generic 401.
    user = db.query(User).filter(User.email == data.email).first()
    
    # We return a generic "Invalid email or password" to prevent user enumeration attacks.
    # An attacker shouldn't be able to guess which emails are valid based on error messages.
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
        
    return {
        "message": "Login successful",
        "user_id": user.id,
        "name": user.name,
        "email": user.email
    }