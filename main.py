from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import create_engine, Column, Integer, String, Date, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
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

# Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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

# -------------------------------------------------------------
# CRUD - PROFESSORS
# -------------------------------------------------------------

# CREATE
@app.post("/professors/", response_model=ProfessorRead, status_code=status.HTTP_201_CREATED)
def create_professor(payload: ProfessorCreate, db: Session = Depends(get_db)):
    # validar correo único
    existing = db.query(ProfessorModel).filter(ProfessorModel.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Correo de profesor ya registrado.")

    prof = ProfessorModel(
        name=payload.name,
        email=payload.email,
        tittle=payload.tittle,
        contratation_date=payload.contratation_date,
    )
    db.add(prof)
    db.commit()
    db.refresh(prof)
    return prof


# READ - list all
@app.get("/professors/", response_model=List[ProfessorRead])
def list_professors(db: Session = Depends(get_db)):
    return db.query(ProfessorModel).all()


# READ - get by id
@app.get("/professors/{professor_id}", response_model=ProfessorRead)
def get_professor(professor_id: int, db: Session = Depends(get_db)):
    prof = db.query(ProfessorModel).filter(ProfessorModel.id == professor_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Profesor no encontrado.")
    return prof


# UPDATE
@app.put("/professors/{professor_id}", response_model=ProfessorRead)
def update_professor(professor_id: int, payload: ProfessorCreate, db: Session = Depends(get_db)):
    prof = db.query(ProfessorModel).filter(ProfessorModel.id == professor_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Profesor no encontrado.")

    # validar correo único si cambia
    if payload.email != prof.email:
        existing = db.query(ProfessorModel).filter(ProfessorModel.correo == payload.correo).first()
        if existing:
            raise HTTPException(status_code=400, detail="Correo ya está siendo usado por otro profesor.")

    prof.name = payload.name
    prof.email = payload.email
    prof.tittle = payload.tittle
    prof.contratation_date = payload.contratation_date

    db.commit()
    db.refresh(prof)
    return prof


# DELETE
@app.delete("/professors/{professor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_professor(professor_id: int, db: Session = Depends(get_db)):
    prof = db.query(ProfessorModel).filter(ProfessorModel.id == professor_id).first()
    if not prof:
        raise HTTPException(status_code=404, detail="Profesor no encontrado.")

    db.delete(prof)
    db.commit()
    return None

# -------------------------------------------------------------
# CRUD - STUDENTS
# -------------------------------------------------------------

# CREATE
@app.post("/students/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    # validar correo único
    existing = db.query(StudentModel).filter(StudentModel.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Correo de estudiante ya registrado.")

    student = StudentModel(
        name=payload.name,
        emanil=payload.emanil,
        birthdate=payload.birthdate,
        degree=payload.degree,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


# READ - list all
@app.get("/students/", response_model=List[StudentRead])
def list_students(db: Session = Depends(get_db)):
    return db.query(StudentModel).all()


# READ - get by id
@app.get("/students/{student_id}", response_model=StudentRead)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado.")
    return student


# UPDATE
@app.put("/students/{student_id}", response_model=StudentRead)
def update_student(student_id: int, payload: StudentCreate, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado.")

    # validar correo único si cambia
    if payload.email != student.email:
        existing = db.query(StudentModel).filter(StudentModel.email == payload.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Correo ya está siendo usado por otro estudiante.")

    student.name = payload.name
    student.email = payload.email
    student.birthdate = payload.birthdate
    student.degree = payload.degree

    db.commit()
    db.refresh(student)
    return student


# DELETE
@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado.")

    db.delete(student)
    db.commit()
    return None

# -------------------------------------------------------------
# CREATE TABLES
# -------------------------------------------------------------
Base.metadata.create_all(bind=engine)