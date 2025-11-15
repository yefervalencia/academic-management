from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

DATABASE_URL = "sqlite:///./academic.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

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
    curso_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    estudiante_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    fecha_inscripcion = Column(DateTime, default=datetime.utcnow)
    estado = Column(String, default="inscrito")

    course = relationship("CourseModel", back_populates="enrollments")
    student = relationship("StudentModel", back_populates="enrollments")

    __table_args__ = (
        UniqueConstraint("curso_id", "estudiante_id", name="uq_course_student"),
    )

Base.metadata.create_all(bind=engine)