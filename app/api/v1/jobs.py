"""
ROUTER DE TRABAJOS ASINCRONOS (Job Router - Async Mode).
Gestiona la visualizacion de Jobs y el disparo de ejecuciones en segundo plano.
Utiliza Celery para liberar el hilo principal de la API, devolviendo un ID de tarea
para que el cliente pueda monitorear el progreso de forma no bloqueante.
"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.execution_log import ExecutionLogResponse
from app.schemas.job import JobResponse
from app.services.execution_service import ExecutionService
from app.services.job_query_service import JobQueryService
from app.workers.job_tasks import execute_job_task

router = APIRouter()
job_query_service = JobQueryService()
execution_service = ExecutionService()


@router.get("", response_model=list[JobResponse])
def list_jobs(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Lista el historial de trabajos registrados en el sistema.
    """
    return job_query_service.list_jobs(db, limit=limit, offset=offset)


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: UUID, db: Session = Depends(get_db)):
    """
    Recupera los detalles de un trabajo especifico.
    """
    job = job_query_service.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job no encontrado")
    return job


@router.post("/{job_id}/execute")
def execute_job(job_id: UUID, db: Session = Depends(get_db)):
    """
    Dispara la ejecucion asincrona de un Job.
    1. El servicio valida riesgos y prepara el estado inicial en la DB.
    2. Se envia la tarea al Broker de Celery usando .delay().
    3. La API responde inmediatamente con el ID de la tarea de Celery.
    """
    try:
        # Prepara el Job (valida riesgos, cambia estado a 'running' o 'queued')
        job = execution_service.enqueue_job_for_execution(db, job_id)
        
        # Envia la tarea al worker pasando el ID como string para evitar problemas de serializacion
        async_result = execute_job_task.delay(str(job.id))

        return {
            "job_id": str(job.id),
            "status": job.status,
            "message": "Job encolado correctamente",
            "celery_task_id": async_result.id  # Permite rastrear la tarea en Celery
        }
    except ValueError as exc:
        # Captura errores de validacion (riesgo alto, job ya finalizado, etc.)
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/{job_id}/logs", response_model=list[ExecutionLogResponse])
def get_job_logs(job_id: UUID, db: Session = Depends(get_db)):
    """
    Consulta los logs generados por el Worker durante la ejecucion del Job.
    """
    job = job_query_service.get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job no encontrado")
    return execution_service.list_job_logs(db, job_id)