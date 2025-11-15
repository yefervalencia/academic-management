from sqlalchemy import Column, Integer,Text, ForeignKey, String, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base


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