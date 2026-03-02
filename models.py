from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)  # uid de Firebase
    email = Column(String, unique=True, index=True)
    name = Column(String)
    photo_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    workouts = relationship("Workout", back_populates="user")


class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"))
    type = Column(String)
    duration = Column(Integer)
    notes = Column(Text, nullable=True)
    date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="workouts")
    exercises = relationship("Exercise", back_populates="workout")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, autoincrement=True)
    workout_id = Column(Integer, ForeignKey("workouts.id"))
    name = Column(String)
    sets = Column(Integer, nullable=True)
    reps = Column(Integer, nullable=True)
    weight = Column(Float, nullable=True)

    workout = relationship("Workout", back_populates="exercises")