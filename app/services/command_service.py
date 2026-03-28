"""
SERVICIO DE COMANDOS (CommandService).
Orquesta el flujo inicial del sistema: recibe el texto del usuario, 
invoca al Planner para predecir la intencion, genera el Job con sus pasos
y evalua si requiere aprobacion humana antes de permitir la ejecucion.
"""
from sqlalchemy.orm import Session

from app.repositories.command_repository import CommandRepository
from app.schemas.command import CommandCreate
from app.services.approval_service import ApprovalService
from app.services.intent_service import IntentService
from app.services.job_service import JobService
from app.services.planner_service import PlannerService


class CommandService:
    # Inicializa todos los servicios satelite necesarios para procesar una orden
    def __init__(self):
        self.command_repository = CommandRepository()
        self.planner_service = PlannerService()
        self.intent_service = IntentService()
        self.job_service = JobService()
        self.approval_service = ApprovalService()

    # Transforma un texto bruto en un plan de ejecucion persistido
    def create_command_with_job(self, db: Session, command_in: CommandCreate) -> dict:
        cleaned_text = command_in.raw_text.strip()

        if not cleaned_text:
            raise ValueError("raw_text no puede estar vacio")

        # Normalizacion basica de la entrada
        normalized_command = CommandCreate(
            raw_text=cleaned_text,
            source=command_in.source.strip() if command_in.source else "web"
        )

        try:
            # 1. Persiste el comando original recibido
            command = self.command_repository.create(db, normalized_command)

            # 2. IA: El Planner analiza el texto y extrae intencion y entidades
            planner_result = self.planner_service.plan(command.raw_text)

            # 3. Crea el registro tecnico de la prediccion de la IA
            prediction = self.intent_service.create_prediction(
                db=db,
                command_id=command.id,
                planner_result=planner_result
            )

            # 4. Genera el Job y desglosa los Steps necesarios segun el Intent
            job = self.job_service.create_job_from_prediction(
                db=db,
                command_id=command.id,
                prediction=prediction
            )

            # 5. Seguridad: Verifica si el Job es sensible y requiere aprobacion
            approval = self.approval_service.create_approval_if_needed(db, job)

            # 6. Si NO requiere aprobacion, marcamos todo como listo para disparar
            if approval is None:
                self.command_repository.update_status(db, command, "ready_to_execute")
                job.status = "ready_to_execute"
                db.add(job)

            # Commit atomico: o se crea todo el flujo (Command->Job->Steps) o nada
            db.commit()
            db.refresh(command)

            return {
                "command": command,
                "intent_prediction": prediction,
                "job": job
            }

        except Exception:
            # Si cualquier paso falla (ej: fallo la IA), se deshacen los cambios en la DB
            db.rollback()
            raise

    # Consultas de historial de comandos
    def list_commands(self, db: Session, limit: int = 50, offset: int = 0):
        return self.command_repository.list(db, limit=limit, offset=offset)

    def get_command_by_id(self, db: Session, command_id):
        return self.command_repository.get_by_id(db, command_id)