from sqlalchemy import Column,UniqueConstraint, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.connection import Base

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

