from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.student_schema import StudentCreate, StudentRead
from app.controllers.student_controller import StudentController


# -------------------------------------------------------------
# DEFINICIÓN DEL ROUTER
# -------------------------------------------------------------
router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# -------------------------------------------------------------
# APLICACIÓN DE PRINCIPIOS S.O.L.I.D EN LA CAPA DE RUTAS
# -------------------------------------------------------------
#
# D — DEPENDENCY INVERSION PRINCIPLE (DIP)
# -------------------------------------------------------------
# En lugar de depender directamente del ORM o los modelos,
# las rutas dependen del controlador StudentController, que es 
# una abstracción de la lógica del dominio.
#
# -------------------------------------------------------------
# I — INTERFACE SEGREGATION PRINCIPLE (ISP)
# -------------------------------------------------------------
# Cada ruta utiliza solo los métodos que necesita.
# Las rutas no conocen detalles internos del controlador.
#
# -------------------------------------------------------------
# S — SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# -------------------------------------------------------------
# Las rutas solo gestionan peticiones HTTP, delegando toda 
# la lógica de negocio al controlador.
# -------------------------------------------------------------


# -------------------------------------------------------------
# CREATE
# -------------------------------------------------------------
@router.post("/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
def create_student(payload: StudentCreate, db: Session = Depends(get_db)):
    """
    Route to create a new student.
    """

    result = StudentController.create(db, payload)

    if result == "email_exists":
        raise HTTPException(400, "Student email already registered.")

    return result


# -------------------------------------------------------------
# READ - List all
# -------------------------------------------------------------
@router.get("/", response_model=List[StudentRead])
def list_students(db: Session = Depends(get_db)):
    """Returns all students."""
    return StudentController.list_all(db)


# -------------------------------------------------------------
# READ - Get by ID
# -------------------------------------------------------------
@router.get("/{student_id}", response_model=StudentRead)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """Returns a specific student by ID."""
    student = StudentController.get_by_id(db, student_id)

    if not student:
        raise HTTPException(404, "Student not found.")

    return student


# -------------------------------------------------------------
# UPDATE
# -------------------------------------------------------------
@router.put("/{student_id}", response_model=StudentRead)
def update_student(student_id: int, payload: StudentCreate, db: Session = Depends(get_db)):
    """
    Updates a student's information.
    """

    result = StudentController.update(db, student_id, payload)

    if result is None:
        raise HTTPException(404, "Student not found.")

    if result == "email_in_use":
        raise HTTPException(400, "Email already used by another student.")

    return result


# -------------------------------------------------------------
# DELETE
# -------------------------------------------------------------
@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    """
    Deletes a student by ID.
    """

    deleted = StudentController.delete(db, student_id)

    if not deleted:
        raise HTTPException(404, "Student not found.")

    return None
