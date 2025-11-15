"""
Archivo centralizado para gestionar todos los routers del proyecto.

Aquí se incluyen y se registran todos los módulos de rutas:
professors, students, courses, enrollments, etc.

Este patrón permite mantener el main.py limpio y organizado.
"""

from fastapi import FastAPI

# Importación de cada router individual
from app.routes.professor_routes import router as professor_router
from app.routes.student_routes import router as student_router
from app.routes.course_routes import router as course_router
from app.routes.enrollment_routes import router as enrollment_router


def init_routes(app: FastAPI):
    """
    Registra todos los routers del proyecto en la instancia
    principal de FastAPI.

    SRP: Este archivo tiene una única responsabilidad:
         gestionar el enrutamiento global del proyecto.

    OCP: Si mañana creas más routers (auth, admin, reports),
         solo necesitas añadirlos aquí sin modificar main.py.

    DIP: El main.py depende de esta abstracción de rutas,
         no de cada router individual.
    """

    app.include_router(professor_router)
    app.include_router(student_router)
    app.include_router(course_router)
    app.include_router(enrollment_router)

