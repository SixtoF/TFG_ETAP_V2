"""
TAREAS DE CELERY (Workers).
Define las unidades de trabajo asincronas que se ejecutan en segundo plano.
Incluye la ejecucion de jobs individuales y el despachador de tareas programadas.
Se utiliza importacion diferida dentro de las funciones para evitar dependencias
circulares con los servicios de negocio.
"""
from app.core.celery_app import celery_app
from app.db.session import SessionLocal

# IMPORTANTE: Forzar el registro de modelos en el mapeador de SQLAlchemy
from app.models.command import Command
from app.models.intent_prediction import IntentPrediction
from app.models.job import Job
from app.models.job_step import JobStep
from app.models.execution_log import ExecutionLog
from app.models.job_result import JobResult
from app.models.approval import Approval
from app.models.scheduled_task import ScheduledTask


@celery_app.task(name="app.workers.job_tasks.execute_job_task")
def execute_job_task(job_id: str):
    # Task que ejecuta un job en segundo plano
    # Import local para evitar conflicto de inicializacion modular
    from app.services.execution_service import ExecutionService
    
    db = SessionLocal()
    try:
        execution_service = ExecutionService()
        # Inicia el proceso de ejecucion real del job solicitado
        execution_service.execute_job(db, job_id)
        return {"status": "completed", "job_id": job_id}
    except Exception as exc:
        # En caso de error se revierte cualquier cambio pendiente en la sesion
        db.rollback()
        raise exc
    finally:
        # Cierre obligatorio de la conexion para liberar recursos en Postgres
        db.close()


@celery_app.task(name="app.workers.job_tasks.dispatch_due_scheduled_tasks")
def dispatch_due_scheduled_tasks():
    # Task periodica que revisa tareas programadas vencidas
    # Import local para evitar dependencia circular con el scheduler
    from app.services.scheduler_service import SchedulerService
    
    db = SessionLocal()
    try:
        scheduler_service = SchedulerService()
        # Busca y lanza todas las tareas cuya fecha de ejecucion ya ha llegado
        result = scheduler_service.dispatch_due_tasks(db)
        return result
    except Exception as exc:
        db.rollback()
        raise exc
    finally:
        db.close()