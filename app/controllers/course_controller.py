from sqlalchemy.orm import Session
from app.models.course_model import CourseModel
from app.models.professor_model import ProfessorModel
from app.schemas.course_schema import CourseCreate


# -------------------------------------------------------------
# APLICACIÓN DE PRINCIPIOS S.O.L.I.D EN ESTE CONTROLADOR
# -------------------------------------------------------------
#
# S — SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# -------------------------------------------------------------
# Esta clase tiene una única responsabilidad: manejar TODA la lógica
# relacionada con la entidad Course. No maneja rutas, ni reglas de
# serialización, ni responde peticiones HTTP. Solo lógica de negocio.
#
# -------------------------------------------------------------
# O — OPEN / CLOSED PRINCIPLE (OCP)
# -------------------------------------------------------------
# Si quiero añadir filtros, paginación o reglas adicionales,
# simplemente agrego nuevos métodos sin modificar los existentes.
#
# -------------------------------------------------------------
# L — LISKOV SUBSTITUTION PRINCIPLE (LSP)
# -------------------------------------------------------------
# Todos los métodos funcionan igual si uso Session o una sesión
# simulada. Esto permite pruebas unitarias sin romper el código.
#
# -------------------------------------------------------------
# I — INTERFACE SEGREGATION PRINCIPLE (ISP)
# -------------------------------------------------------------
# Las rutas consumen solo los métodos que necesitan:
#   create, list_all, get_by_id, update, delete
#
# -------------------------------------------------------------
# D — DEPENDENCY INVERSION PRINCIPLE (DIP)
# -------------------------------------------------------------
# Las rutas no dependen de SQLAlchemy directamente. Dependen de
# este controlador, que es una abstracción de la lógica del dominio.
# -------------------------------------------------------------


class CourseController:

    @staticmethod
    def create(db: Session, payload: CourseCreate):
        """Creates a new course."""

        # Validar código único
        existing = db.query(CourseModel).filter(CourseModel.code == payload.code).first()
        if existing:
            return "code_exists"

        # Validar profesor si se envía profesor_id
        if payload.professor_id is not None:
            prof = db.query(ProfessorModel).filter(ProfessorModel.id == payload.professor_id).first()
            if not prof:
                return "professor_not_found"

        course = CourseModel(
            code=payload.code,
            name=payload.name,
            description=payload.description,
            professor_id=payload.professor_id,
            maximum_capacity=payload.maximum_capacity,
        )

        db.add(course)
        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def list_all(db: Session):
        """Returns all courses."""
        return db.query(CourseModel).all()

    @staticmethod
    def get_by_id(db: Session, course_id: int):
        """Returns a course by ID."""
        return db.query(CourseModel).filter(CourseModel.id == course_id).first()

    @staticmethod
    def update(db: Session, course_id: int, payload: CourseCreate):
        """Updates a course."""

        course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not course:
            return None

        # Validar código único si cambia
        if payload.code != course.code:
            existing = db.query(CourseModel).filter(CourseModel.code == payload.code).first()
            if existing:
                return "code_in_use"

        # Validar profesor si se envía
        if payload.professor_id is not None:
            prof = db.query(ProfessorModel).filter(ProfessorModel.id == payload.professor_id).first()
            if not prof:
                return "professor_not_found"

        course.code = payload.code
        course.name = payload.name
        course.description = payload.description
        course.professor_id = payload.professor_id
        course.maximum_capacity = payload.maximum_capacity

        db.commit()
        db.refresh(course)
        return course

    @staticmethod
    def delete(db: Session, course_id: int):
        """Deletes a course."""
        course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not course:
            return None

        db.delete(course)
        db.commit()
        return True
