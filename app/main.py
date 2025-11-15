from fastapi import FastAPI
from app.routes.api_router import init_routes

app = FastAPI(
    title="Academic Management API",
    version="1.0.0",
    description="Sistema de gestión académica con arquitectura limpia y principios SOLID."
)

# Inicializar todos los routers
init_routes(app)


@app.get("/")
def root():
    return {"message": "API Academic Management Running"}
