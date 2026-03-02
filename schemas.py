from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ExerciseCreate(BaseModel):
    name: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None

class ExerciseOut(ExerciseCreate):
    id: int
    class Config:
        from_attributes = True

class WorkoutCreate(BaseModel):
    type: str
    duration: int
    notes: Optional[str] = None
    exercises: List[ExerciseCreate] = []

class WorkoutOut(BaseModel):
    id: int
    type: str
    duration: int
    notes: Optional[str] = None
    date: datetime
    exercises: List[ExerciseOut] = []
    class Config:
        from_attributes = True