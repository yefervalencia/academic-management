from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.enrollment_schema import EnrollmentCreate, EnrollmentRead
from app.schemas.student_schema import StudentRead
from app.schemas.course_schema import CourseRead
from app.controllers.enrollment_controller import EnrollmentController


router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"]
)

# -------------------------------------------------------------
# SOLID EN LAS RUTAS
# -------------------------------------------------------------
#
# DIP — Dependency Inversion:
#     Las rutas dependen del controlador, NO de SQLAlchemy.
#
# ISP — Interface Segregation:
#     Cada endpoint usa solo el método que necesita.
#
# SRP — Single Responsibility:
#     Las rutas solo manejan HTTP. Toda la lógica se delega.
# -------------------------------------------------------------


# -------------------------------------------------------------
# ENROLL STUDENT
# -------------------------------------------------------------
@router.post("/course/{course_id}", response_model=EnrollmentRead, status_code=201)
def enroll_student(course_id: int, payload: EnrollmentCreate, db: Session = Depends(get_db)):

    result = EnrollmentController.enroll_student(db, course_id, payload)

    if result == "course_not_found":
        raise HTTPException(404, "Course not found.")

    if result == "student_not_found":
        raise HTTPException(404, "Student not found.")

    if result == "already_enrolled":
        raise HTTPException(400, "Student is already enrolled in this course.")

    if result == "capacity_full":
        raise HTTPException(400, "Course has reached maximum capacity.")

    return result


# -------------------------------------------------------------
# UNENROLL STUDENT
# -------------------------------------------------------------
@router.delete("/course/{course_id}/student/{student_id}", status_code=204)
def unenroll_student(course_id: int, student_id: int, db: Session = Depends(get_db)):

    result = EnrollmentController.unenroll_student(db, course_id, student_id)

    if not result:
        raise HTTPException(404, "Enrollment not found.")

    return None


# -------------------------------------------------------------
# LIST STUDENTS IN A COURSE
# -------------------------------------------------------------
@router.get("/course/{course_id}/students", response_model=List[StudentRead])
def list_students_in_course(course_id: int, db: Session = Depends(get_db)):

    result = EnrollmentController.list_students_in_course(db, course_id)

    if result == "course_not_found":
        raise HTTPException(404, "Course not found.")

    return result


# -------------------------------------------------------------
# LIST COURSES OF A STUDENT
# -------------------------------------------------------------
@router.get("/student/{student_id}/courses", response_model=List[CourseRead])
def list_courses_of_student(student_id: int, db: Session = Depends(get_db)):

    result = EnrollmentController.list_courses_of_student(db, student_id)

    if result == "student_not_found":
        raise HTTPException(404, "Student not found.")

    return result
