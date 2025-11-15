from sqlalchemy.orm import Session
from app.models.student_model import StudentModel
from app.schemas.student_schema import StudentCreate


# -------------------------------------------------------------
# APLICACIÓN DE PRINCIPIOS S.O.L.I.D EN ESTE CONTROLADOR
# -------------------------------------------------------------
#
# S — SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# -------------------------------------------------------------
# Este controlador tiene una única responsabilidad:
# manejar TODA la lógica de negocio relacionada con "Student".
# No maneja rutas ni serialización; eso está en otras capas.
#
# -------------------------------------------------------------
# O — OPEN / CLOSED PRINCIPLE (OCP)
# -------------------------------------------------------------
# El controlador está diseñado para extenderse con nuevos métodos 
# (como filtros o paginación) sin modificar los existentes ni romper lógica.
#
# -------------------------------------------------------------
# L — LISKOV SUBSTITUTION PRINCIPLE (LSP)
# -------------------------------------------------------------
# Los métodos usan tipos genéricos (Session).  
# Si uso una sesión mock para pruebas, todo sigue funcionando.
#
# -------------------------------------------------------------
# I — INTERFACE SEGREGATION PRINCIPLE (ISP)
# -------------------------------------------------------------
# Las rutas consumen solo los métodos que necesitan 
# (create, list_all, get_by_id, update, delete).
#
# -------------------------------------------------------------
# D — DEPENDENCY INVERSION PRINCIPLE (DIP)
# -------------------------------------------------------------
# Las rutas dependen de este controlador (una abstracción),
# no del modelo StudentModel ni del ORM directamente.
# -------------------------------------------------------------


class StudentController:

    @staticmethod
    def create(db: Session, payload: StudentCreate):
        """
        Creates a new student.
        Aplicación SRP: este método solo hace creación.
        """

        # Validar correo único
        existing = db.query(StudentModel).filter(StudentModel.email == payload.email).first()
        if existing:
            return "email_exists"

        student = StudentModel(
            name=payload.name,
            email=payload.email,
            birthdate=payload.birthdate,
            degree=payload.degree,
        )

        db.add(student)
        db.commit()
        db.refresh(student)
        return student

    @staticmethod
    def list_all(db: Session):
        """Returns all students."""

        return db.query(StudentModel).all()

    @staticmethod
    def get_by_id(db: Session, student_id: int):
        """Gets a student by ID."""

        return db.query(StudentModel).filter(StudentModel.id == student_id).first()

    @staticmethod
    def update(db: Session, student_id: int, payload: StudentCreate):
        """Updates a student."""

        student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
        if not student:
            return None

        # Validar correo único si cambia
        if payload.email != student.email:
            existing = db.query(StudentModel).filter(StudentModel.email == payload.email).first()
            if existing:
                return "email_in_use"

        student.name = payload.name
        student.email = payload.email
        student.birthdate = payload.birthdate
        student.degree = payload.degree

        db.commit()
        db.refresh(student)
        return student

    @staticmethod
    def delete(db: Session, student_id: int):
        """Deletes a student."""

        student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
        if not student:
            return None

        db.delete(student)
        db.commit()
        return True
