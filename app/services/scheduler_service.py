"""
SERVICIO DE PLANIFICACION (SchedulerService).
Contiene la logica de negocio para gestionar tareas programadas.
Coordina la validacion de expresiones Cron, el calculo de tiempos de ejecucion
y el despacho de tareas hacia el sistema de comandos y workers.
Este servicio actua como puente entre el repositorio de datos y la ejecucion asincrona.
"""
from datetime import datetime

from croniter import croniter
from sqlalchemy.orm import Session

from app.repositories.scheduled_task_repository import ScheduledTaskRepository
from app.schemas.command import CommandCreate
from app.services.command_service import CommandService
from app.services.execution_service import ExecutionService


class SchedulerService:
    # Servicio principal del scheduler
    def __init__(self):
        self.repository = ScheduledTaskRepository()
        self.command_service = CommandService()
        self.execution_service = ExecutionService()

    # Calcula la siguiente fecha de ejecucion a partir del cron
    def calculate_next_run_at(self, cron_expression: str, base_dt: datetime) -> datetime:
        # Usa la libreria croniter para proyectar la fecha futura segun la expresion
        return croniter(cron_expression, base_dt).get_next(datetime)

    # Valida cron de forma simple
    def validate_cron_expression(self, cron_expression: str) -> None:
        try:
            # Intenta parsear la expresion para asegurar que es valida
            croniter(cron_expression, datetime.utcnow())
        except Exception as exc:
            raise ValueError(f"Cron expression invalida: {exc}")

    # Crea tarea programada
    def create_scheduled_task(
        self,
        db: Session,
        name: str,
        description: str | None,
        command_text: str,
        cron_expression: str,
        timezone: str,
        auto_enqueue: bool
    ):
        self.validate_cron_expression(cron_expression)

        # Determina el primer disparo antes de persistir la tarea
        next_run_at = self.calculate_next_run_at(cron_expression, datetime.utcnow())

        scheduled_task = self.repository.create(
            db=db,
            name=name,
            description=description,
            command_text=command_text,
            cron_expression=cron_expression,
            timezone=timezone,
            auto_enqueue=auto_enqueue,
            next_run_at=next_run_at
        )

        db.commit()
        db.refresh(scheduled_task)
        return scheduled_task

    # Lista tareas programadas
    def list_scheduled_tasks(self, db: Session, limit: int = 50, offset: int = 0):
        # Llama al metodo actualizado del repositorio para evitar conflictos de nombres
        return self.repository.list_scheduled_tasks(db, limit=limit, offset=offset)

    # Devuelve tarea por id
    def get_scheduled_task_by_id(self, db: Session, scheduled_task_id):
        return self.repository.get_by_id(db, scheduled_task_id)

    # Activa tarea
    def activate(self, db: Session, scheduled_task_id):
        scheduled_task = self.repository.get_by_id(db, scheduled_task_id)
        if not scheduled_task:
            raise ValueError("Scheduled task no encontrada")

        if scheduled_task.is_active:
            return scheduled_task

        scheduled_task.is_active = True
        # Recalcula la proxima ejecucion si estaba en blanco
        if scheduled_task.next_run_at is None:
            scheduled_task.next_run_at = self.calculate_next_run_at(
                scheduled_task.cron_expression,
                datetime.utcnow()
            )

        self.repository.save(db, scheduled_task)
        db.commit()
        db.refresh(scheduled_task)
        return scheduled_task

    # Desactiva tarea
    def deactivate(self, db: Session, scheduled_task_id):
        scheduled_task = self.repository.get_by_id(db, scheduled_task_id)
        if not scheduled_task:
            raise ValueError("Scheduled task no encontrada")

        scheduled_task.is_active = False
        self.repository.save(db, scheduled_task)
        db.commit()
        db.refresh(scheduled_task)
        return scheduled_task

    # Revisa tareas vencidas y dispara jobs
    def dispatch_due_tasks(self, db: Session) -> dict:
        now_dt = datetime.utcnow()
        # Obtiene las tareas que ya han cumplido su tiempo de espera
        due_tasks = self.repository.get_due_tasks(db, now_dt)

        dispatched_count = 0
        blocked_count = 0
        failed_count = 0

        for scheduled_task in due_tasks:
            try:
                command_payload = CommandCreate(
                    raw_text=scheduled_task.command_text,
                    source="scheduler"
                )

                # Transforma la tarea en un comando ejecutable
                result = self.command_service.create_command_with_job(db, command_payload)
                job = result["job"]

                # Actualiza marcas de tiempo y calcula el siguiente ciclo
                scheduled_task.last_run_at = now_dt
                scheduled_task.next_run_at = self.calculate_next_run_at(
                    scheduled_task.cron_expression,
                    now_dt
                )
                self.repository.save(db, scheduled_task)
                db.commit()

                # Si el job requiere aprobacion, no se encola automaticamente
                if job.status == "approval_pending":
                    blocked_count += 1
                    continue

                # Si es ejecutable y tiene auto enqueue, se envia a la cola de Celery
                if job.status == "ready_to_execute" and scheduled_task.auto_enqueue:
                    # Import perezoso para evitar dependencia circular con el modulo de tareas
                    from app.workers.job_tasks import execute_job_task

                    queued_job = self.execution_service.enqueue_job_for_execution(db, job.id)
                    execute_job_task.delay(str(queued_job.id))
                    dispatched_count += 1

            except Exception:
                db.rollback()
                failed_count += 1
                continue

        return {
            "due_tasks_found": len(due_tasks),
            "dispatched_count": dispatched_count,
            "blocked_count": blocked_count,
            "failed_count": failed_count
        }