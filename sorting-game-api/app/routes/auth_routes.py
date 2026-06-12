from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..auth import create_token, get_current_user, hash_password, verify_password
from ..database import get_db
from ..models import User
from ..schemas import AuthResponse, LoginRequest, RegisterRequest

router = APIRouter(prefix="/auth", tags=["auth"])

ALLOWED_CLASSES = {"12SV", "12SD", "13AG", "13TA"}

def user_payload(user: User) -> dict:
    return {"id": user.id, "username": user.username, "email": user.email, "class_name": user.class_name}

@router.post("/register", response_model=AuthResponse)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    if payload.class_name.upper() not in ALLOWED_CLASSES:
        raise HTTPException(status_code=400, detail="Class must be one of 12SV, 12SD, 13AG, 13TA")
    existing = db.scalar(select(User).where((User.username == payload.username) | (User.email == payload.email)))
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    user = User(
        username=payload.username.strip(),
        email=str(payload.email).lower(),
        class_name=payload.class_name.upper(),
        password_hash=hash_password(payload.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"token": create_token(user.id), "user": user_payload(user)}

@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == payload.username.strip()))
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    return {"token": create_token(user.id), "user": user_payload(user)}

@router.get("/me")
def me(user: User = Depends(get_current_user)):
    return user_payload(user)
