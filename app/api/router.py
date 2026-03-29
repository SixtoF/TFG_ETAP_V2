# ==============================================================================
# ENRUTADOR CENTRAL DE LA API (API_ROUTER)
# Este modulo unifica todos los sub-routers de la aplicacion en un unico punto.
# Permite organizar el codigo por dominios (auth, users, jobs, etc.) y aplicar
# prefijos y etiquetas (tags) para la documentacion automatica de Swagger.
# ==============================================================================

from fastapi import APIRouter

# Importacion de los enrutadores especificos de cada modulo de la version 1 (v1)
from app.api.v1.approvals import router as approvals_router
from app.api.v1.auth import router as auth_router
from app.api.v1.commands import router as commands_router
from app.api.v1.jobs import router as jobs_router
from app.api.v1.scheduled_tasks import router as scheduled_tasks_router
from app.api.v1.users import router as users_router

# Instancia principal del enrutador
api_router = APIRouter()

# --- REGISTRO DE RUTAS ---

# Modulo de Autenticacion: Gestiona el login y la obtencion de tokens JWT
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])

# Modulo de Usuarios: Administracion de cuentas y perfiles
api_router.include_router(users_router, prefix="/users", tags=["users"])

# Modulo de Comandos: Definicion de las acciones tecnicas que el sistema puede realizar
api_router.include_router(commands_router, prefix="/commands", tags=["commands"])

# Modulo de Jobs: Ejecucion y seguimiento de tareas en tiempo real
api_router.include_router(jobs_router, prefix="/jobs", tags=["jobs"])

# Modulo de Approvals: Sistema de seguridad para validar acciones criticas por un admin
api_router.include_router(approvals_router, prefix="/approvals", tags=["approvals"])

# Modulo de Scheduled Tasks: Automatizacion y programacion de tareas recurrentes
api_router.include_router(scheduled_tasks_router, prefix="/scheduled-tasks", tags=["scheduled-tasks"])