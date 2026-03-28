"""
CONFIGURACION DE CELERY Y BEAT (Planificador).
Establece la conexion con Redis como broker y backend de resultados.
Define el calendario (Beat Schedule) para tareas que deben ejecutarse
automaticamente de forma recurrente cada minuto.
Configura la importacion explicita de modulos de tareas para asegurar 
su registro en el worker de Docker.
"""
from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

# Instancia principal de Celery utilizada por la API y los Workers
celery_app = Celery(
    "etap_worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

# Configuracion basica de Celery y definicion de tareas periodicas
celery_app.conf.update(
    # Formato de serializacion para el intercambio de mensajes
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    
    # Configuracion de zona horaria para coincidir con el entorno local
    timezone="Europe/Madrid",
    enable_utc=False,
    
    # Seguimiento del estado de las tareas al iniciar su ejecucion
    task_track_started=True,
    
    # Importacion explicita de tareas para evitar problemas de registro en el worker
    imports=("app.workers.job_tasks",),
    
    # Planificador de tareas automaticas (Celery Beat)
    beat_schedule={
        "dispatch-due-scheduled-tasks-every-minute": {
            # Tarea que revisa y lanza las ejecuciones programadas segun cron
            "task": "app.workers.job_tasks.dispatch_due_scheduled_tasks",
            "schedule": crontab(minute="*"),
        }
    }
)