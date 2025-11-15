from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.schemas.professor_schema import ProfessorCreate, ProfessorRead
from app.controllers.professor_controller import ProfessorController


# -------------------------------------------------------------
# DEFINICIÓN DEL ROUTER
# -------------------------------------------------------------
router = APIRouter(
    prefix="/professors",
    tags=["Professors"]
)


# -------------------------------------------------------------
# APLICACIÓN DE PRINCIPIOS S.O.L.I.D EN LA CAPA DE RUTAS
# -------------------------------------------------------------
#
# D — DEPENDENCY INVERSION PRINCIPLE (DIP)
# -------------------------------------------------------------
# En lugar de que las rutas dependan directamente del ORM o de los 
# modelos de la base de datos, dependen del controlador 
# (ProfessorController), que es una abstracción de la lógica 
# de negocio.
#
# Las rutas solo orquestan la petición, delegan la lógica y
# devuelven la respuesta. Nunca manipulan SQLAlchemy directamente.
#
# Esto reduce el acoplamiento y facilita pruebas unitarias.
#
# -------------------------------------------------------------
# I — INTERFACE SEGREGATION PRINCIPLE (ISP)
# -------------------------------------------------------------
# Las rutas consumen únicamente los métodos que ellas mismas
# necesitan (create, list_all, get_by_id, update, delete).
#
# No exponen más operaciones ni dependen de detalles internos 
# del controlador ni del ORM. Cada ruta utiliza la "interfaz" 
# mínima necesaria.
#
# -------------------------------------------------------------
# S — SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# -------------------------------------------------------------
# Cada ruta tiene una única responsabilidad: atender solicitudes 
# HTTP y delegar la lógica al controlador. No realizan operaciones 
# de negocio ni validaciones avanzadas.
#
# Esto hace que la capa de API sea simple, limpia y fácil de mantener.
# -------------------------------------------------------------


# -------------------------------------------------------------
# CREATE
# -------------------------------------------------------------
@router.post("/", response_model=ProfessorRead, status_code=status.HTTP_201_CREATED)
def create_professor(payload: ProfessorCreate, db: Session = Depends(get_db)):
    """
    Ruta responsable de registrar un nuevo profesor.
    Aplicación SOLID:
    - SRP: la ruta solo gestiona la solicitud HTTP y delega la lógica.
    - DIP: delego creación al controlador (no toco SQLAlchemy aquí).
    """

    result = ProfessorController.create(db, payload)

    if result == "email_exists":
        raise HTTPException(400, "Professor email already exists.")

    return result


# -------------------------------------------------------------
# READ - List all
# -------------------------------------------------------------
@router.get("/", response_model=List[ProfessorRead])
def list_professors(db: Session = Depends(get_db)):
    """
    Devuelve todos los profesores registrados.
    SOLID:
    - ISP: esta ruta solo necesita el método list_all().
    """
    return ProfessorController.list_all(db)


# -------------------------------------------------------------
# READ - Get by ID
# -------------------------------------------------------------
@router.get("/{professor_id}", response_model=ProfessorRead)
def get_professor(professor_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un profesor por ID.
    """
    prof = ProfessorController.get_by_id(db, professor_id)

    if not prof:
        raise HTTPException(404, "Professor not found.")

    return prof


# -------------------------------------------------------------
# UPDATE
# -------------------------------------------------------------
@router.put("/{professor_id}", response_model=ProfessorRead)
def update_professor(professor_id: int, payload: ProfessorCreate, db: Session = Depends(get_db)):
    """
    Actualiza los datos de un profesor.
    SOLID:
    - DIP: delego la actualización al controlador.
    """

    result = ProfessorController.update(db, professor_id, payload)

    if result is None:
        raise HTTPException(404, "Professor not found.")

    if result == "email_in_use":
        raise HTTPException(400, "Email already used by another professor.")

    return result


# -------------------------------------------------------------
# DELETE
# -------------------------------------------------------------
@router.delete("/{professor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_professor(professor_id: int, db: Session = Depends(get_db)):
    """
    Elimina un profesor por ID.
    """

    deleted = ProfessorController.delete(db, professor_id)

    if not deleted:
        raise HTTPException(404, "Professor not found.")

    return None
