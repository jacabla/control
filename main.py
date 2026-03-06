import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, get_db
from models import User, Workout
from routers import workouts, metrics, cooper, profile, strength
from routers import training

load_dotenv()

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
app.include_router(metrics.router, prefix="/api")
app.include_router(cooper.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
app.include_router(strength.router, prefix="/api")
app.include_router(training.router)

@app.get("/")
def root():
    return {"message": "Fitness Tracker API funcionando 🚀"}