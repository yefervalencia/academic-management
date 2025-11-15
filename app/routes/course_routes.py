from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.course_schema import CourseCreate, CourseRead
from app.controllers.course_controller import CourseController


# -------------------------------------------------------------
# DEFINICIÓN DEL ROUTER
# -------------------------------------------------------------
router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


# -------------------------------------------------------------
# APLICACIÓN DE PRINCIPIOS S.O.L.I.D EN ESTA CAPA
# -------------------------------------------------------------
#
# D — DEPENDENCY INVERSION (DIP)
# -------------------------------------------------------------
# Las rutas no manipulan SQLAlchemy ni modelos directamente.
# Dependen del controlador como una abstracción de la lógica.
#
# -------------------------------------------------------------
# I — INTERFACE SEGREGATION (ISP)
# -------------------------------------------------------------
# Cada ruta usa solo el método que necesita del controlador.
#
# -------------------------------------------------------------
# S — SINGLE RESPONSIBILITY (SRP)
# -------------------------------------------------------------
# Cada función maneja una solicitud HTTP específica y delega toda
# la lógica al controlador.
# -------------------------------------------------------------


# -------------------------------------------------------------
# CREATE
# -------------------------------------------------------------
@router.post("/", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
def create_course(payload: CourseCreate, db: Session = Depends(get_db)):
    result = CourseController.create(db, payload)

    if result == "code_exists":
        raise HTTPException(400, "Course code already exists.")

    if result == "professor_not_found":
        raise HTTPException(400, "Professor not found.")

    return result


# -------------------------------------------------------------
# READ - List all
# -------------------------------------------------------------
@router.get("/", response_model=List[CourseRead])
def list_courses(db: Session = Depends(get_db)):
    return CourseController.list_all(db)


# -------------------------------------------------------------
# READ - Get by ID
# -------------------------------------------------------------
@router.get("/{course_id}", response_model=CourseRead)
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = CourseController.get_by_id(db, course_id)

    if not course:
        raise HTTPException(404, "Course not found.")

    return course


# -------------------------------------------------------------
# UPDATE
# -------------------------------------------------------------
@router.put("/{course_id}", response_model=CourseRead)
def update_course(course_id: int, payload: CourseCreate, db: Session = Depends(get_db)):
    result = CourseController.update(db, course_id, payload)

    if result is None:
        raise HTTPException(404, "Course not found.")

    if result == "code_in_use":
        raise HTTPException(400, "Course code already in use.")

    if result == "professor_not_found":
        raise HTTPException(400, "Professor not found.")

    return result


# -------------------------------------------------------------
# DELETE
# -------------------------------------------------------------
@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    deleted = CourseController.delete(db, course_id)

    if not deleted:
        raise HTTPException(404, "Course not found.")

    return None
