"""
SERVICIO DE EJECUCION DE TRABAJOS (ExecutionService).
Gestiona el ciclo de vida de los Jobs en entornos asincronos.
Incluye logica de validacion para encolado (Broker) y la logica 
de ejecucion secuencial de pasos (Worker) con gestion de contexto.
"""
from datetime import datetime

from sqlalchemy.orm import Session

from app.repositories.command_repository import CommandRepository
from app.repositories.execution_log_repository import ExecutionLogRepository
from app.repositories.job_repository import JobRepository
from app.repositories.job_result_repository import JobResultRepository
from app.services.step_handler_service import StepHandlerService


class ExecutionService:
    # Inicializa los repositorios necesarios para el seguimiento de la ejecucion
    def __init__(self):
        self.job_repository = JobRepository()
        self.command_repository = CommandRepository()
        self.log_repository = ExecutionLogRepository()
        self.job_result_repository = JobResultRepository()
        self.step_handler_service = StepHandlerService()

    # FASE 1: Validacion y preparacion para la cola de Celery
    def enqueue_job_for_execution(self, db: Session, job_id):
        job = self.job_repository.get_by_id(db, job_id)
        if not job:
            raise ValueError("Job no encontrado")

        # --- VALIDACIONES DE MAQUINA DE ESTADOS ---
        if job.status == "approval_pending":
            raise ValueError("El job requiere aprobacion antes de ejecutarse")

        if job.status == "rejected":
            raise ValueError("El job fue rechazado y no puede ejecutarse")

        if job.status == "queued":
            raise ValueError("El job ya esta encolado")

        if job.status == "running":
            raise ValueError("El job ya se esta ejecutando")

        if job.status == "completed":
            raise ValueError("El job ya fue completado")

        # Solo permitimos encolar si el Job esta listo para ser disparado
        if job.status not in {"ready_to_execute"}:
            raise ValueError(f"No se puede encolar un job en estado {job.status}")

        # Cambiamos el estado a 'queued' para que nadie mas intente dispararlo
        job.status = "queued"
        db.add(job)

        # Registramos el evento de encolado para trazabilidad
        self.log_repository.create(
            db=db,
            job_id=job.id,
            level="INFO",
            message="Job queued for async execution",
            details_json={"job_status": job.status}
        )

        db.commit()
        db.refresh(job)
        return job

    # FASE 2: Ejecucion real (Ejecutada por el Worker de Celery)
    def execute_job(self, db: Session, job_id):
        job = self.job_repository.get_by_id(db, job_id)
        if not job:
            raise ValueError("Job no encontrado")

        # Doble validacion de seguridad en el Worker
        if job.status in {"approval_pending", "rejected", "completed", "failed"}:
            raise ValueError(f"Estado invalido para ejecucion en worker: {job.status}")

        # --- INICIO DE EJECUCION ---
        job.status = "running"
        job.started_at = datetime.utcnow()
        db.add(job)

        self.log_repository.create(
            db=db,
            job_id=job.id,
            level="INFO",
            message="Job execution started",
            details_json={"intent_name": job.intent_name}
        )

        db.flush()

        context = {}

        try:
            # Recuperamos los pasos ordenados por su secuencia definida
            steps = sorted(job.steps, key=lambda step: step.step_order)

            for step in steps:
                # Marcamos el inicio de cada sub-tarea
                step.status = "running"
                step.started_at = datetime.utcnow()
                db.add(step)

                self.log_repository.create(
                    db=db,
                    job_id=job.id,
                    job_step_id=step.id,
                    level="INFO",
                    message="Step execution started",
                    details_json={
                        "step_type": step.step_type,
                        "connector_type": step.connector_type
                    }
                )

                db.flush()

                # Ejecutamos el conector correspondiente a traves del StepHandler
                result = self.step_handler_service.execute_step(step=step, context=context)

                # Almacenamos el resultado en el contexto compartido
                context[step.step_type] = result

                # Finalizamos el paso actual
                step.status = "completed"
                step.finished_at = datetime.utcnow()
                db.add(step)

                self.log_repository.create(
                    db=db,
                    job_id=job.id,
                    job_step_id=step.id,
                    level="INFO",
                    message="Step execution completed",
                    details_json={
                        "step_type": step.step_type,
                        "output_summary": result
                    }
                )

                db.flush()

            # --- CIERRE DE TRABAJO EXITOSO ---
            job.status = "completed"
            job.finished_at = datetime.utcnow()
            db.add(job)

            # Sincronizamos el comando original a completado
            command = job.command
            command.status = "completed"
            db.add(command)

            self.log_repository.create(
                db=db,
                job_id=job.id,
                level="INFO",
                message="Job execution completed",
                details_json={"steps_executed": len(steps)}
            )

            # Persistimos el resultado final con todos los datos recolectados
            self.job_result_repository.upsert(
                db=db,
                job_id=job.id,
                success=True,
                summary="Job ejecutado correctamente",
                result_json={"step_results": context}
            )

            db.commit()
            db.refresh(job)
            return self.job_repository.get_by_id(db, job.id)

        except Exception as exc:
            # --- MANEJO DE ERRORES EN EL TRABAJO ---
            for step in job.steps:
                if step.status == "running":
                    step.status = "failed"
                    step.finished_at = datetime.utcnow()
                    db.add(step)
                    
                    self.log_repository.create(
                        db=db,
                        job_id=job.id,
                        job_step_id=step.id,
                        level="ERROR",
                        message="Step execution failed",
                        details_json={"error": str(exc)}
                    )
                    break

            job.status = "failed"
            job.finished_at = datetime.utcnow()
            db.add(job)

            command = job.command
            command.status = "failed"
            db.add(command)

            # Guardamos el error final para visibilidad del usuario
            self.job_result_repository.upsert(
                db=db,
                job_id=job.id,
                success=False,
                summary="Job fallo durante la ejecucion",
                result_json={"error": str(exc), "partial_context": context}
            )

            db.commit()
            db.refresh(job)
            return self.job_repository.get_by_id(db, job.id)

    # Recupera los logs de auditoria
    def list_job_logs(self, db: Session, job_id):
        return self.log_repository.list_by_job_id(db, job_id)