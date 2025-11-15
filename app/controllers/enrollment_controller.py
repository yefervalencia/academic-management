from sqlalchemy.orm import Session
from app.models.course_model import CourseModel
from app.models.student_model import StudentModel
from app.models.enrollment_model import EnrollmentModel
from app.schemas.enrollment_schema import EnrollmentCreate

# -------------------------------------------------------------
# APLICACIÓN PRINCIPIOS SOLID EN ESTE CONTROLADOR
# -------------------------------------------------------------
#
# S — SINGLE RESPONSIBILITY PRINCIPLE
# -------------------------------------------------------------
# Esta clase se encarga ÚNICAMENTE de la lógica de negocio
# relacionada con inscripciones (Enrollment).
#
# No maneja rutas, ni Pydantic, ni detalles HTTP.
#
# -------------------------------------------------------------
# O — OPEN/CLOSED PRINCIPLE
# -------------------------------------------------------------
# Si mañana quiero implementar "reenroll", "pausar inscripción",
# o "historial", lo agrego aquí sin modificar los métodos actuales.
#
# -------------------------------------------------------------
# L — LISKOV SUBSTITUTION PRINCIPLE
# -------------------------------------------------------------
# El controlador funciona igual usando SQLite, PostgreSQL
# o incluso una sesión mock para pruebas.
#
# -------------------------------------------------------------
# I — INTERFACE SEGREGATION PRINCIPLE
# -------------------------------------------------------------
# Las rutas sólo llaman los métodos que necesitan.
#
# -------------------------------------------------------------
# D — DEPENDENCY INVERSION PRINCIPLE
# -------------------------------------------------------------
# Las rutas dependen de esta abstracción (el controlador),
# no directamente de SQLAlchemy.
# -------------------------------------------------------------


class EnrollmentController:

    @staticmethod
    def enroll_student(db: Session, course_id: int, payload: EnrollmentCreate):

        # Validar curso
        course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not course:
            return "course_not_found"

        # Validar estudiante
        student = db.query(StudentModel).filter(StudentModel.id == payload.student_id).first()
        if not student:
            return "student_not_found"

        # Validar inscripción duplicada
        existing = (
            db.query(EnrollmentModel)
            .filter(
                EnrollmentModel.course_id == course_id,
                EnrollmentModel.student_id == payload.student_id,
                EnrollmentModel.status == "active"
            )
            .first()
        )
        if existing:
            return "already_enrolled"

        # Validar cupos
        if course.maximum_capacity is not None:
            active_count = (
                db.query(EnrollmentModel)
                .filter(
                    EnrollmentModel.course_id == course_id,
                    EnrollmentModel.status == "active"
                )
                .count()
            )
            if active_count >= course.maximum_capacity:
                return "capacity_full"

        enrollment = EnrollmentModel(
            course_id=course_id,
            student_id=payload.student_id
        )

        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
        return enrollment

    @staticmethod
    def unenroll_student(db: Session, course_id: int, student_id: int):

        enrollment = (
            db.query(EnrollmentModel)
            .filter(
                EnrollmentModel.course_id == course_id,
                EnrollmentModel.student_id == student_id
            )
            .first()
        )

        if not enrollment:
            return None

        db.delete(enrollment)
        db.commit()
        return True

    @staticmethod
    def list_students_in_course(db: Session, course_id: int):

        course = db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not course:
            return "course_not_found"

        return [e.student for e in course.enrollments]

    @staticmethod
    def list_courses_of_student(db: Session, student_id: int):

        student = db.query(StudentModel).filter(StudentModel.id == student_id).first()
        if not student:
            return "student_not_found"

        return [e.course for e in student.enrollments]
