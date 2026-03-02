from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Workout, Exercise, User
from schemas import WorkoutCreate, WorkoutOut
from typing import List

router = APIRouter()

def get_or_create_user(db: Session, uid: str, email: str, name: str, photo_url: str):
    user = db.query(User).filter(User.id == uid).first()
    if not user:
        user = User(id=uid, email=email, name=name, photo_url=photo_url)
        db.add(user)
        db.commit()
        db.refresh(user)
    return user

@router.post("/workouts", response_model=WorkoutOut)
def create_workout(
    workout_data: WorkoutCreate,
    uid: str,
    email: str,
    name: str,
    photo_url: str = "",
    db: Session = Depends(get_db)
):
    get_or_create_user(db, uid, email, name, photo_url)

    workout = Workout(
        user_id=uid,
        type=workout_data.type,
        duration=workout_data.duration,
        notes=workout_data.notes
    )
    db.add(workout)
    db.commit()
    db.refresh(workout)

    for ex in workout_data.exercises:
        exercise = Exercise(
            workout_id=workout.id,
            name=ex.name,
            sets=ex.sets,
            reps=ex.reps,
            weight=ex.weight
        )
        db.add(exercise)

    db.commit()
    db.refresh(workout)
    return workout

@router.get("/workouts", response_model=List[WorkoutOut])
def get_workouts(uid: str, db: Session = Depends(get_db)):
    workouts = db.query(Workout).filter(Workout.user_id == uid).order_by(Workout.date.desc()).all()
    return workouts

@router.delete("/workouts/{workout_id}")
def delete_workout(workout_id: int, uid: str, db: Session = Depends(get_db)):
    workout = db.query(Workout).filter(Workout.id == workout_id, Workout.user_id == uid).first()
    if not workout:
        raise HTTPException(status_code=404, detail="Entrenamiento no encontrado")
    db.delete(workout)
    db.commit()
    return {"message": "Eliminado"}