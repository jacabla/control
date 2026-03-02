from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import workouts

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fitness Tracker API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(workouts.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "Fitness Tracker API funcionando 🚀"}