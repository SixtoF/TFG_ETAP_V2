"""
API ROUTER PRINCIPAL (Version 1).
Centraliza todos los routers especificos de cada modulo.
Organiza la API mediante prefijos (URL) y etiquetas (Tags para Swagger).
Permite que el sistema sea modular y facil de mantener.
"""
from fastapi import APIRouter
from app.api.v1.approvals import router as approvals_router
from app.api.v1.commands import router as commands_router
from app.api.v1.jobs import router as jobs_router
from app.api.v1.scheduled_tasks import router as scheduled_tasks_router

# Instancia del router principal de la V1
api_router = APIRouter()

# Registro del modulo de comandos (interprete de texto)
api_router.include_router(commands_router, prefix="/commands", tags=["commands"])

# Registro del modulo de jobs (gestion de tareas de fondo)
api_router.include_router(jobs_router, prefix="/jobs", tags=["jobs"])

# Registro del modulo de aprobaciones (seguridad humana)
api_router.include_router(approvals_router, prefix="/approvals", tags=["approvals"])

# Registro del modulo de tareas programadas (automatizaciones cron)
api_router.include_router(scheduled_tasks_router, prefix="/scheduled-tasks", tags=["scheduled-tasks"])