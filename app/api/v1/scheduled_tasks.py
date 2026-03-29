"""
ROUTER DEFINITIVO DE TAREAS PROGRAMADAS.
Define los puntos de entrada (endpoints) para la gestion de automatizaciones.
Utiliza el SchedulerService para realizar operaciones de negocio y calculos cron.
Incluye endpoints para crear, listar, obtener, activar y desactivar tareas
y gestionar su estado (activacion/desactivacion) segun el rol del usuario.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.session import get_db
from app.schemas.scheduled_task import ScheduledTaskCreate, ScheduledTaskResponse
from app.services.scheduler_service import SchedulerService

# Instancia del router para el modulo de tareas programadas
router = APIRouter()

# Inicializacion del servicio encargado de la logica del planificador
scheduler_service = SchedulerService()


@router.post(
    "",
    response_model=ScheduledTaskResponse,
    status_code=201,
    # SEGURIDAD CRITICA: Solo el administrador puede crear nuevas programaciones
    dependencies=[Depends(require_roles("admin"))]
)
def create_scheduled_task(payload: ScheduledTaskCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva tarea programada definiendo su nombre, comando y expresion cron.
    """
    try:
        return scheduler_service.create_scheduled_task(
            db=db,
            name=payload.name,
            description=payload.description,
            command_text=payload.command_text,
            cron_expression=payload.cron_expression,
            timezone=payload.timezone,
            auto_enqueue=payload.auto_enqueue
        )
    except ValueError as exc:
        # Captura errores de formato en la expresion cron o nombres duplicados
        raise HTTPException(status_code=400, detail=str(exc))


@router.get(
    "",
    response_model=list[ScheduledTaskResponse],
    # Todos los usuarios autenticados pueden consultar el calendario de tareas
    dependencies=[Depends(require_roles("admin", "operator", "viewer"))]
)
def list_scheduled_tasks(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Lista todas las automatizaciones configuradas en el sistema.
    """
    return scheduler_service.list_scheduled_tasks(db, limit=limit, offset=offset)


@router.get(
    "/{scheduled_task_id}",
    response_model=ScheduledTaskResponse,
    dependencies=[Depends(require_roles("admin", "operator", "viewer"))]
)
def get_scheduled_task(scheduled_task_id: UUID, db: Session = Depends(get_db)):
    """
    Obtiene los detalles de una tarea programada especifica por su ID.
    """
    scheduled_task = scheduler_service.get_scheduled_task_by_id(db, scheduled_task_id)
    if not scheduled_task:
        raise HTTPException(status_code=404, detail="Scheduled task no encontrada")
    return scheduled_task


@router.patch(
    "/{scheduled_task_id}/activate",
    response_model=ScheduledTaskResponse,
    # Solo el admin puede activar procesos automaticos
    dependencies=[Depends(require_roles("admin"))]
)
def activate_scheduled_task(scheduled_task_id: UUID, db: Session = Depends(get_db)):
    """
    Activa una tarea programada para que empiece a ejecutarse segun su horario.
    """
    try:
        return scheduler_service.activate(db, scheduled_task_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.patch(
    "/{scheduled_task_id}/deactivate",
    response_model=ScheduledTaskResponse,
    # Solo el admin puede detener procesos automaticos por seguridad
    dependencies=[Depends(require_roles("admin"))]
)
def deactivate_scheduled_task(scheduled_task_id: UUID, db: Session = Depends(get_db)):
    """
    Desactiva una tarea programada de forma inmediata.
    """
    try:
        return scheduler_service.deactivate(db, scheduled_task_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))