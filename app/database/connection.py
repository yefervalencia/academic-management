from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.database.config import settings


# -------------------------------------------------------------------
# DATABASE ENGINE
# -------------------------------------------------------------------
# Aquí aplico el principio de SINGLE RESPONSIBILITY (SRP):
# ----------------------------------------------------------
# Esta sección del archivo se encarga únicamente de crear el engine
# de SQLAlchemy según la URL de la base de datos definida. Nada más.
#
# No mezclo lógica de rutas, validaciones ni modelos. Solo la creación
# del motor de conexión.
#
# Además, si en un futuro decido cambiar SQLite por PostgreSQL,
# este bloque se adapta sin afectar el resto del proyecto,
# aplicando OPEN/CLOSED (OCP): el código está abierto a extensión,
# pero cerrado a modificación en otras capas.
# -------------------------------------------------------------------

# Ajuste necesario cuando uso SQLite para permitir múltiples hilos
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(settings.DATABASE_URL)


# -------------------------------------------------------------------
# Declarative Base
# -------------------------------------------------------------------
# Nuevamente aplico SRP:
# Este archivo solo crea la base declarativa para los modelos ORM.
# No define modelos en sí. Cada cosa en su lugar.
# -------------------------------------------------------------------
Base = declarative_base()


# -------------------------------------------------------------------
# DATABASE SESSION FACTORY
# -------------------------------------------------------------------
# Este bloque crea la fábrica de sesiones (SessionLocal).
#
# Aquí aplico el principio de INVERSION OF DEPENDENCY (DIP):
# ----------------------------------------------------------
# En vez de que los controladores o rutas creen conexiones directas,
# dependen de esta abstracción (SessionLocal), lo que desacopla
# completamente la lógica de datos del resto del sistema.
#
# Esto también reduce el impacto si cambio el motor SQL.
# -------------------------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# -------------------------------------------------------------------
# DEPENDENCY: get_db()
# -------------------------------------------------------------------
# Esta función proporciona una sesión por request.
#
# PRINCIPIOS SOLID APLICADOS:
# ---------------------------
# ✔ SRP:
#   - get_db() solo administra el ciclo de vida de la sesión.
#
# ✔ LISKOV SUBSTITUTION (LSP):
#   - Cualquier componente que dependa de "db: Session" puede
#     reemplazarla por una mock session en pruebas sin romper nada.
#
# ✔ DEPENDENCY INVERSION (DIP):
#   - Las rutas y controladores dependen de esta función en lugar
#     de depender directamente de SQLAlchemy.
#
# ✔ OPEN/CLOSED:
#   - Si en el futuro uso un ORM diferente, solo modifico este archivo.
#
# Este patrón coincide con las mejores prácticas oficiales de FastAPI.
# -------------------------------------------------------------------
def get_db():
    """
    Provides a database session per request.
    Ensures proper opening and closing.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
