import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, get_db
from models import User, Workout
from routers import workouts

load_dotenv()

Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas correctamente")
print("📊 Tablas disponibles:", Base.metadata.tables.keys())

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

@app.get("/admin/create-tables")
def create_tables():
    Base.metadata.create_all(bind=engine)
    return {"tables": list(Base.metadata.tables.keys())}

@app.get("/admin/db-url")
def check_db():
    url = os.getenv("DATABASE_URL", "no encontrada")
    return {"url": url[:50]}