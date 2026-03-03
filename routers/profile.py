from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()

class ProfileUpdate(BaseModel):
    birth_date: Optional[str] = None
    gender: Optional[str] = None
    goal: Optional[str] = None
    activity_level: Optional[str] = None

class ProfileOut(BaseModel):
    id: str
    name: str
    email: str
    photo_url: Optional[str] = None
    birth_date: Optional[str] = None
    gender: Optional[str] = None
    goal: Optional[str] = None
    activity_level: Optional[str] = None
    profile_complete: int
    age: Optional[int] = None

    class Config:
        from_attributes = True

def calculate_age(birth_date: str) -> int:
    try:
        bd = datetime.strptime(birth_date, "%Y-%m-%d")
        today = datetime.today()
        return today.year - bd.year - ((today.month, today.day) < (bd.month, bd.day))
    except:
        return None

@router.get("/profile", response_model=ProfileOut)
def get_profile(uid: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        return None
    result = ProfileOut(
        id=user.id,
        name=user.name,
        email=user.email,
        photo_url=user.photo_url,
        birth_date=user.birth_date,
        gender=user.gender,
        goal=user.goal,
        activity_level=user.activity_level,
        profile_complete=user.profile_complete or 0,
        age=calculate_age(user.birth_date) if user.birth_date else None
    )
    return result

@router.put("/profile")
def update_profile(
    data: ProfileUpdate,
    uid: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        return {"error": "Usuario no encontrado"}

    if data.birth_date: user.birth_date = data.birth_date
    if data.gender: user.gender = data.gender
    if data.goal: user.goal = data.goal
    if data.activity_level: user.activity_level = data.activity_level

    if all([user.birth_date, user.gender, user.goal, user.activity_level]):
        user.profile_complete = 1

    db.commit()
    db.refresh(user)
    return {"message": "Perfil actualizado", "profile_complete": user.profile_complete}