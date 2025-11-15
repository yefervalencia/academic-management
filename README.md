# 🎓 Academic Management API  
Sistema académico modular construido con **FastAPI**, **SQLAlchemy**, **Pydantic v2** y arquitectura limpia aplicando **principios SOLID**.

Este proyecto gestiona:
- Profesores  
- Estudiantes  
- Cursos  
- Inscripciones (Enrollments)

Incluye separación por capas (routes, controllers, models, schemas) para mantener escalabilidad, mantenibilidad y facilidad de pruebas.

---

## 🚀 Características principales

- Arquitectura modular basada en buenas prácticas.
- Principios **SOLID** aplicados en toda la estructura.
- CRUD completo para Profesores, Estudiantes y Cursos.
- Sistema de inscripciones con validaciones:
  - Capacidad máxima
  - Evitar inscripciones duplicadas
  - Validación de relaciones
- Documentación automática con Swagger (`/docs`).
- Configuración mediante variables de entorno con `pydantic-settings`.

---

## 📁 Estructura del Proyecto

app/
│── main.py
│── routes/
│ ├── professor_routes.py
│ ├── student_routes.py
│ ├── course_routes.py
│ └── enrollment_routes.py
│
│── controllers/
│ ├── professor_controller.py
│ ├── student_controller.py
│ ├── course_controller.py
│ └── enrollment_controller.py
│
│── models/
│ ├── professor_model.py
│ ├── student_model.py
│ ├── course_model.py
│ └── enrollment_model.py
│
│── schemas/
│ ├── professor_schema.py
│ ├── student_schema.py
│ ├── course_schema.py
│ └── enrollment_schema.py
│
│── database/
│ ├── connection.py
│ └── config.py


---

## 🧱 Principios SOLID aplicados

### **S — Single Responsibility**
Cada módulo cumple **una única responsabilidad**:
- Controllers → lógica de negocio  
- Routes → entrada HTTP  
- Schemas → validación  
- Models → persistencia  

### **O — Open/Closed**
Los controladores permiten agregar nuevas operaciones sin modificar las existentes.

### **L — Liskov Substitution**
Los modelos y schemas siguen estándares homogéneos, permitiendo intercambiarlos sin romper la arquitectura.

### **I — Interface Segregation**
Las rutas NO dependen directamente de SQLAlchemy, sino de controladores.

### **D — Dependency Inversion**
Las rutas dependen de **abstracciones**, no de implementaciones concretas.

---

## 🛠 Dependencias usadas

fastapi==0.116.1
uvicorn==0.35.0
sqlalchemy==2.0.43
python-dotenv==1.1.1
alembic==1.16.4
passlib==1.7.4
pydantic==2.11.7
pydantic-settings==2.10.1
asyncpg==0.30.0
greenlet==3.2.4
bcrypt==4.3.0
python-jose==3.5.0
python-multipart==0.0.20


---

## ⚙️ Configuración del entorno

Crear archivo `.env`:

DATABASE_URL=sqlite:///./academic.db


---

## ▶️ Ejecutar el proyecto

1. Instalar dependencias:

pip install -r requirements.txt


2. Correr el servidor:

uvicorn app.main:app --reload


3. Abrir documentación:

http://127.0.0.1:8000/docs


---

## 🔗 Endpoints principales (resumen)

### **Profesores**
| Método | Endpoint | Descripción |
|-------|----------|-------------|
| GET | /professors | Listar |
| GET | /professors/{id} | Obtener por ID |
| POST | /professors | Crear |
| PUT | /professors/{id} | Actualizar |
| DELETE | /professors/{id} | Eliminar |

### **Estudiantes**
(similar a teachers)

### **Cursos**
(similar a teachers)

### **Inscripciones**
| Método | Endpoint | Descripción |
|-------|----------|-------------|
| POST | /courses/{id}/enroll | Inscribir |
| DELETE | /courses/{id}/unenroll/{student_id} | Desinscribir |
| GET | /courses/{id}/students | Estudiantes en curso |
| GET | /students/{id}/courses | Cursos del estudiante |

---

## 🧪 Pruebas

En desarrollo...

---

## 📌 Autor

**Yeferson Valencia Aristizábal**  
Proyecto Académico — Ingeniería de Software II  
Universidad Autónoma de Manizales
