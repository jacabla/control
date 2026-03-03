from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, get_db
from models import User, Workout
from routers import workouts

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://fitness-tracker-loye.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workouts.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Fitness Tracker API funcionando 🚀"}

@app.get("/admin/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": u.id, "name": u.name, "email": u.email} for u in users]

@app.get("/admin/workouts")
def get_all_workouts(db: Session = Depends(get_db)):
    workouts = db.query(Workout).all()
    return [{"id": w.id, "user_id": w.user_id, "type": w.type, "duration": w.duration, "date": str(w.date)} for w in workouts]