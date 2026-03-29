"""
ROUTER DE TRABAJOS ASINCRONOS (Job Router - Async Mode).
Gestiona la visualizacion de Jobs y el disparo de ejecuciones en segundo plano.
Utiliza Celery para liberar el hilo principal de la API, devolviendo un ID de tarea
para que el cliente pueda monitorear el progreso de forma no bloqueante.
"""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.deps import require_roles
from app.db.session import get_db
from app.schemas.execution_log import ExecutionLogResponse
from app.schemas.job import JobResponse
from app.services.execution_service import ExecutionService
from app.services.job_query_service import JobQueryService
from app.workers.job_tasks import execute_job_task

# Instancia del router para el modulo de jobs
router = APIRouter()

# Inicializacion de servicios para logica de consultas y ejecuciones
job_query_service = JobQueryService()
execution_service = ExecutionService()


@router.get(
    "",
    response_model=list[JobResponse],
    # Todos los roles autenticados pueden listar jobs
    dependencies=[Depends(require_roles("admin", "operator", "viewer"))]
)
def list_jobs(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Obtiene una lista paginada de todos los jobs registrados en el sistema.
    """
    return job_query_service.list_jobs(db, limit=limit, offset=offset)


@router.get(
    "/{job_id}",
    response_model=JobResponse,
    # El detalle de un job es visible para cualquier usuario con acceso
    dependencies=[Depends(require_roles("admin", "operator", "viewer"))]
)
def get_job(job_id: UUID, db: Session = Depends(get_db)):
    """
    Busca y retorna la informacion detallada de un job especifico por su UUID.
    """
    job = job_query_service.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job no encontrado")
    return job


@router.post(
    "/{job_id}/execute",
    # SEGURIDAD CRITICA: Solo admin y operator pueden disparar ejecuciones
    dependencies=[Depends(require_roles("admin", "operator"))]
)
def execute_job(job_id: UUID, db: Session = Depends(get_db)):
    """
    Solicita la ejecucion inmediata de un job. 
    Cambia el estado en BD e inicia la tarea asincrona en Celery.
    """
    try:
        # Preparamos el job para ejecucion (validaciones de estado)
        job = execution_service.enqueue_job_for_execution(db, job_id)
        
        # Enviamos la tarea al worker de Celery (proceso en segundo plano)
        async_result = execute_job_task.delay(str(job.id))

        return {
            "job_id": str(job.id),
            "status": job.status,
            "message": "Job encolado correctamente",
            "celery_task_id": async_result.id
        }
    except ValueError as exc:
        # Captura errores de logica (ej: job ya en ejecucion o pendiente de aprobacion)
        raise HTTPException(status_code=400, detail=str(exc))


@router.get(
    "/{job_id}/logs",
    response_model=list[ExecutionLogResponse],
    # Permite auditar la ejecucion consultando los registros de salida
    dependencies=[Depends(require_roles("admin", "operator", "viewer"))]
)
def get_job_logs(job_id: UUID, db: Session = Depends(get_db)):
    """
    Retorna el historial de logs de ejecucion asociados a un job concreto.
    """
    job = job_query_service.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job no encontrado")
    return execution_service.list_job_logs(db, job_id)