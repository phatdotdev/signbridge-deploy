from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from pydantic import BaseModel

from ..db import get_db, User
from app.core.oauth2 import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    verify_access_token,
)

class LoginRequest(BaseModel):
    username: str
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class IntrospectRequest(BaseModel):
    access_token: str

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        (User.username == request.username) | (User.email == request.username)
    ).first()  # type: ignore
    if not user or not bcrypt.verify(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})

    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
    }

@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}

@router.post("/introspect")
def introspect(request: IntrospectRequest):
    username = verify_access_token(request.access_token)
    return {"message": "Access token is valid", "username": username}

@router.post("/refresh")
def refresh(request: RefreshRequest):
    username = verify_refresh_token(request.refresh_token)
    new_access_token = create_access_token({"sub": username})
    return {
        "message": "Access token refreshed",
        "access_token": new_access_token
    }
