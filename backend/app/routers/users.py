from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.hash import bcrypt
from typing import List
from datetime import date, datetime

from ..db import get_db, User
from ..core.oauth2 import get_current_user, get_current_admin

router = APIRouter(prefix="/users", tags=["users"])

router.post("/users")

# ---- Models ----
class UserCreate(BaseModel):
    username: str
    password: str
    email: EmailStr
    gender: str = "unknown"
    birthdate: date | None = None
    role: str = "user"

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    gender: str
    birthdate: date | None
    role: str
    created_at: datetime
    
    class Config:
        orm_mode = True
        

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db = Depends(get_db)):
    existing = db.query(User) \
        .filter((User.username == user.username) | (User.email == user.email)) \
        .first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")
    hashed_password = bcrypt.hash(user.password)
    
    user_data = user.dict()
    user_data["password"] = hashed_password
    new_user = User(**user_data)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get("/", response_model=List[UserOut])
def get_all_users(admin_user = Depends(get_current_admin), db = Depends(get_db)):
    return db.query(User).all()

@router.get("/me", response_model=UserOut)
def get_user_info(current_user = Depends(get_current_user)):
    user_dict = current_user.__dict__.copy()
    return user_dict

