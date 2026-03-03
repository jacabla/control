from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import StrengthTest
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter()

class StrengthCreate(BaseModel):
    sit_ups: Optional[int] = None
    push_ups: Optional[int] = None
    squats: Optional[int] = None
    sit_and_reach: Optional[float] = None

class StrengthOut(StrengthCreate):
    id: int
    date: datetime
    class Config:
        from_attributes = True

@router.post("/strength", response_model=StrengthOut)
def create_strength_test(
    data: StrengthCreate,
    uid: str,
    db: Session = Depends(get_db)
):
    test = StrengthTest(
        user_id=uid,
        sit_ups=data.sit_ups,
        push_ups=data.push_ups,
        squats=data.squats,
        sit_and_reach=data.sit_and_reach
    )
    db.add(test)
    db.commit()
    db.refresh(test)
    return test

@router.get("/strength", response_model=List[StrengthOut])
def get_strength_tests(uid: str, db: Session = Depends(get_db)):
    tests = db.query(StrengthTest).filter(
        StrengthTest.user_id == uid
    ).order_by(StrengthTest.date.desc()).all()
    return tests