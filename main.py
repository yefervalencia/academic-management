from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime, date
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List

# -------------------------------------------------------------
# FASTAPI APP
# -------------------------------------------------------------
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# -------------------------------------------------------------
# DATABASE SETUP
# -------------------------------------------------------------
DATABASE_URL = "sqlite:///./academic.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

# -------------------------------------------------------------
# MODELS
# -------------------------------------------------------------
class ProfessorModel(Base):
    __tablename__ = "professors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    tittle = Column(String, nullable=True)
    contratation_date = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    courses = relationship("CourseModel", back_populates="professor", cascade="all, delete-orphan")

class StudentModel(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    birthdate = Column(Date, nullable=True)
    degree = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    enrollments = relationship("EnrollmentModel", back_populates="student", cascade="all, delete-orphan")

class CourseModel(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    professor_id = Column(Integer, ForeignKey("professors.id"), nullable=True)
    maximum_capacity = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    professor = relationship("ProfessorModel", back_populates="courses")
    enrollments = relationship("EnrollmentModel", back_populates="course", cascade="all, delete-orphan")
  
class EnrollmentModel(Base):
    __tablename__ = "enrollments"
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    inscription_date = Column(DateTime, default=datetime.utcnow)
    state = Column(String, default="inscrito")

    course = relationship("CourseModel", back_populates="enrollments")
    student = relationship("StudentModel", back_populates="enrollments")

    __table_args__ = (
        UniqueConstraint("course_id", "student_id", name="uq_course_student"),
    )

# -------------------------------------------------------------
# SCHEMAS (Pydantic v2)
# -------------------------------------------------------------

# ---------- Professors ----------
class ProfessorBase(BaseModel):
    name: str
    email: EmailStr
    tittle: Optional[str] = None
    contratation_date: Optional[date] = None

class ProfessorCreate(ProfessorBase):
    pass

class ProfessorRead(ProfessorBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ---------- Students ----------
class StudentBase(BaseModel):
    name: str
    email: EmailStr
    birthdate: Optional[date] = None
    degree: Optional[str] = None

class StudentCreate(StudentBase):
    pass

class StudentRead(StudentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ---------- Courses ----------
class CourseBase(BaseModel):
    code: str
    name: str
    description: Optional[str] = None
    professor_id: Optional[int] = None
    maximum_capacity: Optional[int] = None

class CourseCreate(CourseBase):
    pass

class CourseRead(CourseBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# ---------- Enrollments ----------
class EnrollmentCreate(BaseModel):
    course_id: int
    student_id: int

class EnrollmentRead(BaseModel):
    id: int
    course_id: int
    student_id: int
    inscription_date: datetime
    state: str

    model_config = ConfigDict(from_attributes=True)

# Crear tablas
Base.metadata.create_all(bind=engine)