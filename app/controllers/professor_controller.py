from sqlalchemy.orm import Session
from app.models.professor_model import ProfessorModel
from app.schemas.professor_schema import ProfessorCreate


# -------------------------------------------------------------
# APLICACIÓN DE PRINCIPIOS S.O.L.I.D EN ESTE CONTROLADOR
# -------------------------------------------------------------
#
# S — SINGLE RESPONSIBILITY PRINCIPLE (SRP)
# -------------------------------------------------------------
# Este controlador tiene una única responsabilidad: manejar la
# lógica de negocio de los profesores.
#
# No maneja rutas, no maneja serialización Pydantic, no maneja
# conexiones a la base de datos. Solo contiene reglas, validaciones
# y operaciones relacionadas al dominio "Profesor".
#
# Esto garantiza alta cohesión y facilita mantenimiento.
#
# -------------------------------------------------------------
# O — OPEN / CLOSED PRINCIPLE (OCP)
# -------------------------------------------------------------
# El controlador está abierto a extensión, pero cerrado a
# modificación. Si mañana quiero agregar búsquedas avanzadas,
# paginación, filtros o estadísticas, puedo añadir nuevos métodos
# sin tener que modificar los existentes ni tocar las rutas.
#
# Esto reduce riesgos y evita efectos secundarios.
#
# -------------------------------------------------------------
# L — LISKOV SUBSTITUTION PRINCIPLE (LSP)
# -------------------------------------------------------------
# Cualquier método aquí usa tipos genéricos como Session.
# Si en un test quiero reemplazar Session por una sesión simulada
# o una FakeDB, todo sigue funcionando.
#
# Lo mismo ocurre si reemplazo ProfessorModel por un modelo mock.
#
# -------------------------------------------------------------
# I — INTERFACE SEGREGATION PRINCIPLE (ISP)
# -------------------------------------------------------------
# Las rutas no necesitan conocer detalles internos del ORM.
# Les entrego solo métodos específicos:
#   - create()
#   - list_all()
#   - get_by_id()
#   - update()
#   - delete()
#
# Rutas más limpias, código más pequeño y desacoplado.
#
# -------------------------------------------------------------
# D — DEPENDENCY INVERSION PRINCIPLE (DIP)
# -------------------------------------------------------------
# Las rutas dependen de este controlador (una abstracción), no del
# ORM ni del modelo directamente. Si cambiara de SQLAlchemy a otro
# motor ORM, solo tendría que cambiar esta capa.
#
# El controlador actúa como una capa intermedia que desacopla
# infraestructura (BD) de la capa superior (API).
# -------------------------------------------------------------


class ProfessorController:

    @staticmethod
    def create(db: Session, payload: ProfessorCreate):
        """
        Creates a new professor record.

        Aplicación SOLID:
        - SRP: este método solo hace creación, nada más.
        - OCP: si mañana agrego validaciones extras, no rompo dependencias.
        """

        # Validar correo único
        existing = db.query(ProfessorModel).filter(ProfessorModel.email == payload.email).first()
        if existing:
            return "email_exists"

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

    @staticmethod
    def list_all(db: Session):
        """
        Returns all professors.
        """
        return db.query(ProfessorModel).all()

    @staticmethod
    def get_by_id(db: Session, professor_id: int):
        """
        Gets a professor by ID.
        """
        return db.query(ProfessorModel).filter(ProfessorModel.id == professor_id).first()

    @staticmethod
    def update(db: Session, professor_id: int, payload: ProfessorCreate):
        """
        Updates an existing professor.

        SOLID aplicado:
        - LSP: este método funciona igual con cualquier objeto DB Session.
        """

        prof = db.query(ProfessorModel).filter(ProfessorModel.id == professor_id).first()
        if not prof:
            return None

        # Validar correo único si cambia
        if payload.email != prof.email:
            existing = db.query(ProfessorModel).filter(ProfessorModel.email == payload.email).first()
            if existing:
                return "email_in_use"

        prof.name = payload.name
        prof.email = payload.email
        prof.tittle = payload.tittle
        prof.contratation_date = payload.contratation_date

        db.commit()
        db.refresh(prof)
        return prof

    @staticmethod
    def delete(db: Session, professor_id: int):
        """
        Deletes a professor.

        SOLID aplicado:
        - DIP: dependencia contraída hacia este método, no hacia SQLAlchemy.
        """

        prof = db.query(ProfessorModel).filter(ProfessorModel.id == professor_id).first()
        if not prof:
            return None

        db.delete(prof)
        db.commit()
        return True
