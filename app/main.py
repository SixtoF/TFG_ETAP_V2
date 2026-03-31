"""
Punto de entrada principal de la aplicacion FastAPI.
Configura la seguridad CORS para permitir la conexion con el Frontend.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # Importacion necesaria

# Importacion del enrutador central
from app.api.router import api_router

# Inicializacion de la aplicacion
app = FastAPI(title="ETAP API", version="0.7.0")

# --- CONFIGURACION DE CORS (FUNDAMENTAL PARA EL FRONTEND) ---
app.add_middleware(
    CORSMiddleware,
    # Permite que el puerto 3000 del frontend acceda a la API
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    # Permite todos los metodos (GET, POST, PUT, DELETE, etc.)
    allow_methods=["*"],
    # Permite todas las cabeceras (incluyendo Authorization para el JWT)
    allow_headers=["*"],
)

# Inclusio de rutas
app.include_router(api_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}