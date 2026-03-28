"""
ROUTER DEFINITIVO DE TAREAS PROGRAMADAS.
Define los puntos de entrada (endpoints) para la gestion de automatizaciones.
Utiliza el SchedulerService para realizar operaciones de negocio y calculos cron.
Incluye endpoints para crear, listar, obtener, activar y desactivar tareas.
"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.scheduled_task import ScheduledTaskCreate, ScheduledTaskResponse
from app.services.scheduler_service import SchedulerService

# Instancia del router y del servicio coordinador
router = APIRouter()
scheduler_service = SchedulerService()


@router.post("", response_model=ScheduledTaskResponse, status_code=201)
def create_scheduled_task(payload: ScheduledTaskCreate, db: Session = Depends(get_db)):
    """
    Crea una nueva tarea automatizada.
    Valida la expresion cron y calcula el primer disparo antes de guardar.
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
        # Si croniter detecta un error en el formato cron, devuelve un 400
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("", response_model=list[ScheduledTaskResponse])
def list_scheduled_tasks(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Lista las tareas programadas existentes con soporte para paginacion.
    """
    return scheduler_service.list_scheduled_tasks(db, limit=limit, offset=offset)


@router.get("/{scheduled_task_id}", response_model=ScheduledTaskResponse)
def get_scheduled_task(scheduled_task_id: UUID, db: Session = Depends(get_db)):
    """
    Obtiene la informacion detallada de una tarea especifica por su UUID.
    """
    scheduled_task = scheduler_service.get_scheduled_task_by_id(db, scheduled_task_id)
    if not scheduled_task:
        raise HTTPException(status_code=404, detail="Scheduled task no encontrada")
    return scheduled_task


@router.patch("/{scheduled_task_id}/activate", response_model=ScheduledTaskResponse)
def activate_scheduled_task(scheduled_task_id: UUID, db: Session = Depends(get_db)):
    """
    Pone una tarea en estado activo para que vuelva a generar ejecuciones.
    """
    try:
        return scheduler_service.activate(db, scheduled_task_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.patch("/{scheduled_task_id}/deactivate", response_model=ScheduledTaskResponse)
def deactivate_scheduled_task(scheduled_task_id: UUID, db: Session = Depends(get_db)):
    """
    Pausa una tarea para evitar que se ejecute sin borrar su configuracion.
    """
    try:
        return scheduler_service.deactivate(db, scheduled_task_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))