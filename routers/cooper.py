from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import CooperTest
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter()

def calculate_vo2_max(distance: float) -> float:
    return round((distance - 504.9) / 44.73, 1)

def get_classification(vo2_max: float, age: int, gender: str) -> str:
    if gender == 'F':
        if age < 30:
            if vo2_max < 28: return "Deficiente, necasita mejorar"
            elif vo2_max < 34: return "Avanzando, pero necesita mejorar"
            elif vo2_max < 38: return "Regular, sigue avanzando"
            elif vo2_max < 48: return "Bueno, vas mejorando"
            elif vo2_max < 52: return "Excelente"
            else: return "Superior"
        elif age < 40:
            if vo2_max < 27: return "Deficiente, necasita mejorar"
            elif vo2_max < 33: return "Avanzando, pero necesita mejorar"
            elif vo2_max < 37: return "Regular, sigue avanzando"
            elif vo2_max < 45: return "Bueno, vas mejorando"
            elif vo2_max < 49: return "Excelente"
            else: return "Superior"
        else:
            if vo2_max < 25: return "Deficiente, necasita mejorar"
            elif vo2_max < 31: return "Avanzando, pero necesita mejorar"
            elif vo2_max < 35: return "Regular, sigue avanzando"
            elif vo2_max < 42: return "Bueno, vas mejorando"
            elif vo2_max < 46: return "Excelente"
            else: return "Superior"
    else:  # M
        if age < 30:
            if vo2_max < 38: return "Deficiente, necasita mejorar"
            elif vo2_max < 42: return "Avanzando, pero necesita mejorar"
            elif vo2_max < 46: return "Regular, sigue avanzando"
            elif vo2_max < 52: return "Bueno, vas mejorando"
            elif vo2_max < 60: return "Excelente"
            else: return "Superior"
        elif age < 40:
            if vo2_max < 34: return "Deficiente, necasita mejorar"
            elif vo2_max < 38: return "Avanzando, pero necesita mejorar"
            elif vo2_max < 42: return "Regular, sigue avanzando"
            elif vo2_max < 48: return "Bueno, vas mejorando"
            elif vo2_max < 54: return "Excelente"
            else: return "Superior"
        else:
            if vo2_max < 31: return "Deficiente, necasita mejorar"
            elif vo2_max < 35: return "Avanzando, pero necesita mejorar"
            elif vo2_max < 39: return "Regular, sigue avanzando"
            elif vo2_max < 45: return "Bueno, vas mejorando"
            elif vo2_max < 51: return "Excelente"
            else: return "Superior"


class CooperCreate(BaseModel):
    distance: Optional[float] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    hr_before: Optional[int] = None
    hr_after: Optional[int] = None
    conditions: Optional[str] = None
    notes: Optional[str] = None

class CooperOut(BaseModel):
    id: int
    date: datetime
    distance: Optional[float] = None
    vo2_max: Optional[float] = None
    classification: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    hr_before: Optional[int] = None
    hr_after: Optional[int] = None
    conditions: Optional[str] = None
    notes: Optional[str] = None
    class Config:
        from_attributes = True

@router.post("/cooper", response_model=CooperOut)
def create_cooper_test(
    data: CooperCreate,
    uid: str,
    db: Session = Depends(get_db)
):
    vo2_max = None
    classification = None

    if data.distance:
        vo2_max = calculate_vo2_max(data.distance)
        if data.age and data.gender:
            classification = get_classification(vo2_max, data.age, data.gender)

    test = CooperTest(
        user_id=uid,
        distance=data.distance,
        vo2_max=vo2_max,
        classification=classification,
        age=data.age,
        gender=data.gender,
        hr_before=data.hr_before,
        hr_after=data.hr_after,
        conditions=data.conditions,
        notes=data.notes
    )
    db.add(test)
    db.commit()
    db.refresh(test)
    return test

@router.get("/cooper", response_model=List[CooperOut])
def get_cooper_tests(uid: str, db: Session = Depends(get_db)):
    tests = db.query(CooperTest).filter(
        CooperTest.user_id == uid
    ).order_by(CooperTest.date.desc()).all()
    return tests