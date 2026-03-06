from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    photo_url = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Datos del perfil
    birth_date = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    goal = Column(String, nullable=True)
    activity_level = Column(String, nullable=True)
    profile_complete = Column(Integer, default=0)  # 0 = incompleto, 1 = completo

    workouts = relationship("Workout", back_populates="user")
    metrics = relationship("BodyMetric", back_populates="user")
    cooper_tests = relationship("CooperTest", back_populates="user")
    strength_tests = relationship("StrengthTest", back_populates="user")


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

class BodyMetric(Base):
    __tablename__ = "body_metrics"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.utcnow)

    # Datos físicos
    weight = Column(Float, nullable=True)       # kg
    height = Column(Float, nullable=True)       # cm
    age = Column(Integer, nullable=True)
    body_fat = Column(Float, nullable=True)     # %
    muscle_mass = Column(Float, nullable=True)  # kg

    # Medidas corporales (cm)
    chest = Column(Float, nullable=True)
    waist = Column(Float, nullable=True)
    hips = Column(Float, nullable=True)
    arms = Column(Float, nullable=True)
    legs = Column(Float, nullable=True)
    neck = Column(Float, nullable=True)

    # Salud
    systolic_bp = Column(Integer, nullable=True)   # presión sistólica
    diastolic_bp = Column(Integer, nullable=True)  # presión diastólica

    user = relationship("User", back_populates="metrics")

class CooperTest(Base):
    __tablename__ = "cooper_tests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.utcnow)

    # Datos del test
    distance = Column(Float, nullable=True)        # metros recorridos en 12 min
    vo2_max = Column(Float, nullable=True)         # calculado automáticamente
    classification = Column(String, nullable=True) # Muy malo, Malo, Regular, Bueno, Excelente, Superior
    age = Column(Integer, nullable=True)
    gender = Column(String, nullable=True)         # M / F

    # Frecuencia cardíaca
    hr_before = Column(Integer, nullable=True)     # antes del test
    hr_after = Column(Integer, nullable=True)      # después del test

    # Condiciones
    conditions = Column(String, nullable=True)     # pista, calle, clima
    notes = Column(Text, nullable=True)

    user = relationship("User", back_populates="cooper_tests")

class StrengthTest(Base):
    __tablename__ = "strength_tests"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"))
    date = Column(DateTime, default=datetime.utcnow)

    # Fuerza y resistencia
    sit_ups = Column(Integer, nullable=True)        # abdominales en 1 min
    push_ups = Column(Integer, nullable=True)       # flexiones en 1 min
    squats = Column(Integer, nullable=True)         # sentadillas en 1 min
    sit_and_reach = Column(Float, nullable=True)    # flexibilidad en cm

    user = relationship("User", back_populates="strength_tests")

class TrainingPlan(Base):
    __tablename__ = "training_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)          # ej: "Karla - Marzo 2026"
    month = Column(Integer, nullable=False)        # 3
    year = Column(Integer, nullable=False)         # 2026
    competition = Column(String, nullable=True)    # "5 km"
    objective = Column(String, nullable=True)
    observations = Column(String, nullable=True)
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    sessions = relationship("PlannedSession", back_populates="plan", cascade="all, delete-orphan")


class PlannedSession(Base):
    __tablename__ = "planned_sessions"

    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("training_plans.id"), nullable=False)
    week = Column(Integer, nullable=True)
    date = Column(String, nullable=True)           # "02/03/2026"
    day = Column(String, nullable=True)            # "Lunes"
    exercise_type = Column(String, nullable=True)  # "Carrera Continua"
    description = Column(String, nullable=True)
    duration_min = Column(Float, nullable=True)
    distance_km = Column(Float, nullable=True)
    pulse_min = Column(Integer, nullable=True)
    pulse_max = Column(Integer, nullable=True)
    notes = Column(String, nullable=True)
    is_rest = Column(Boolean, default=False)       # True si es LIBRE

    plan = relationship("TrainingPlan", back_populates="sessions")
    result = relationship("SessionResult", back_populates="session", uselist=False, cascade="all, delete-orphan")


class SessionResult(Base):
    __tablename__ = "session_results"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("planned_sessions.id"), nullable=False)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    status = Column(String, nullable=True)         # "completed", "partial", "skipped"
    duration_real = Column(Float, nullable=True)
    distance_real = Column(Float, nullable=True)
    avg_pulse = Column(Integer, nullable=True)
    feeling = Column(String, nullable=True)        # "excellent", "good", "regular", "hard"
    notes = Column(String, nullable=True)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("PlannedSession", back_populates="result")