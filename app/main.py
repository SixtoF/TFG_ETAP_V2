"""
Punto de entrada principal de la aplicacion FastAPI.
Este archivo inicializa la API, configura el enrutamiento modular
y define los endpoints de control de estado (health checks).
"""
from fastapi import FastAPI

# Importacion del enrutador central que agrupa todos los modulos (jobs, tasks, etc.)
from app.api.router import api_router

# Inicializacion de la aplicacion con metadatos para la documentacion automatica (Swagger)
app = FastAPI(title="ETAP API", version="0.7.0")

# Esto permite que todos los endpoints comiencen por /api/v1/...
app.include_router(api_router, prefix="/api/v1")

# Sirve para verificar que el servicio esta levantado y operativo
@app.get("/health")
def health():
    """
    Retorna un estado simple para monitoreo del sistema.
    """
    return {"status": "ok"}