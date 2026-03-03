from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import BodyMetric, User
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter()

class MetricCreate(BaseModel):
    weight: Optional[float] = None
    height: Optional[float] = None
    age: Optional[int] = None
    body_fat: Optional[float] = None
    muscle_mass: Optional[float] = None
    chest: Optional[float] = None
    waist: Optional[float] = None
    hips: Optional[float] = None
    arms: Optional[float] = None
    legs: Optional[float] = None
    neck: Optional[float] = None
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None

class MetricOut(MetricCreate):
    id: int
    date: datetime
    imc: Optional[float] = None
    class Config:
        from_attributes = True

@router.post("/metrics", response_model=MetricOut)
def create_metric(
    data: MetricCreate,
    uid: str,
    db: Session = Depends(get_db)
):
    metric = BodyMetric(user_id=uid, **data.dict())
    db.add(metric)
    db.commit()
    db.refresh(metric)

    result = MetricOut(**{c.name: getattr(metric, c.name) for c in metric.__table__.columns})
    if metric.weight and metric.height:
        result.imc = round(metric.weight / ((metric.height / 100) ** 2), 1)
    return result

@router.get("/metrics", response_model=List[MetricOut])
def get_metrics(uid: str, db: Session = Depends(get_db)):
    metrics = db.query(BodyMetric).filter(
        BodyMetric.user_id == uid
    ).order_by(BodyMetric.date.desc()).all()

    result = []
    for m in metrics:
        item = MetricOut(**{c.name: getattr(m, c.name) for c in m.__table__.columns})
        if m.weight and m.height:
            item.imc = round(m.weight / ((m.height / 100) ** 2), 1)
        result.append(item)
    return result