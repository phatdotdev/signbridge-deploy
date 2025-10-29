from fastapi import APIRouter, Response, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from pydantic import BaseModel

from ..db import get_db, User
from app.core.oauth2 import create_access_token, create_refresh_token, verify_refresh_token, get_access_token, verify_access_token

class LoginRequest(BaseModel):
    username: str
    password: str

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/login")
def login(request: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = db.query(User).filter((User.username == request.username) | (User.email == request.username)).first() # type: ignore
    if not user or not bcrypt.verify(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})

    response.set_cookie("access_token", access_token, httponly=True, samesite="lax")
    response.set_cookie("refresh_token", refresh_token, httponly=True, samesite="lax")
    return {"message": "Login successful"}

@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}

@router.post("/introspect")
def introspect(response: Response, request: Request):
    username = verify_access_token(request.cookies.get("access_token")) # type: ignore
    return {"message": "Access token is valid"}

@router.post("/refresh")
def refresh(response: Response, request: Request):
    username = verify_refresh_token(request.cookies.get("refresh_token")) # type: ignore
    access_token = create_access_token({"sub": username})
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False 
    )
    return {"message": "Access token refreshed"}