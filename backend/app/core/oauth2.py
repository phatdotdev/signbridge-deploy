# app/core/oauth2.py
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.security import ACCESS_TOKEN_SECRET, REFRESH_TOKEN_SECRET, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from ..db import get_db, User

credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token not found in cookies",
            headers={"WWW-Authenticate": "Bearer"},
        )

def get_access_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception
    return token

def get_refresh_token(request: Request) -> str:
    token = request.cookies.get("refresh_token")
    if not token:
        raise credentials_exception
    return token

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, ACCESS_TOKEN_SECRET, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    data.update({"exp": expire})
    return jwt.encode(data, REFRESH_TOKEN_SECRET, algorithm=ALGORITHM)

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

def verify_refresh_token(token: str):
    if not token:
        raise credentials_exception
    try:
        payload = jwt.decode(token, REFRESH_TOKEN_SECRET, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception

def get_current_user(token: str = Depends(get_access_token), db: Session = Depends(get_db)):
    username = verify_access_token(token)
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user

def get_current_admin(token: str = Depends(get_access_token), db: Session = Depends(get_db)):
    user = get_current_user(token, db)
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user
