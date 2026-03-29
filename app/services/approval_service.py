# ==============================================================================
# SERVICIO DE GESTION DE APROBACIONES (APPROVAL SERVICE)
# Este servicio implementa la logica para el manejo de tareas de alto riesgo,
# gestionando el ciclo de vida de una aprobacion desde su creacion hasta
# su resolucion (aprobado/rechazado) por un usuario administrador.
# ==============================================================================

from datetime import datetime
from sqlalchemy.orm import Session

from app.repositories.approval_repository import ApprovalRepository
from app.repositories.execution_log_repository import ExecutionLogRepository
from app.repositories.job_result_repository import JobResultRepository


class ApprovalService:
    def __init__(self):
        # Inicializacion de los repositorios necesarios para la persistencia
        self.approval_repository = ApprovalRepository()
        self.log_repository = ExecutionLogRepository()
        self.job_result_repository = JobResultRepository()

    def create_approval_if_needed(self, db: Session, job):
        """
        Determina si un job requiere aprobacion humana basandose en el riesgo.
        Si el riesgo es 'high', bloquea la ejecucion y crea una solicitud.
        """
        if job.risk_level != "high":
            return None

        # Creacion de la solicitud de aprobacion en estado pendiente
        approval = self.approval_repository.create(
            db=db,
            job_id=job.id,
            reason="High risk job requires approval",
            status="pending"
        )

        # Actualizacion de estados del job y comando para reflejar el bloqueo
        job.status = "approval_pending"
        db.add(job)

        command = job.command
        command.status = "approval_pending"
        db.add(command)

        # Registro en el historial de logs del sistema
        self.log_repository.create(
            db=db,
            job_id=job.id,
            level="INFO",
            message="Approval request created",
            details_json={
                "approval_id": str(approval.id),
                "reason": approval.reason,
                "risk_level": job.risk_level
            }
        )

        db.flush()  # Sincroniza con la BD sin cerrar la transaccion
        return approval

    def list_approvals(self, db: Session, limit: int = 50, offset: int = 0, status: str | None = None):
        """Lista las aprobaciones con soporte para paginacion y filtrado."""
        return self.approval_repository.list(db, limit=limit, offset=offset, status=status)

    def get_approval_by_id(self, db: Session, approval_id):
        """Recupera una aprobacion especifica por su identificador unico."""
        return self.approval_repository.get_by_id(db, approval_id)

    def approve(self, db: Session, approval_id, current_user, resolution_comment: str | None):
        """
        Procesa la aprobacion de una solicitud. 
        Vincula al usuario administrador real que toma la decision.
        """
        approval = self.approval_repository.get_by_id(db, approval_id)
        if not approval:
            raise ValueError("Approval no encontrada")

        if approval.status != "pending":
            raise ValueError("La aprobacion ya fue resuelta")

        # Registro de la decision del administrador
        approval.status = "approved"
        approval.resolved_at = datetime.utcnow()
        approval.resolved_by_user_id = current_user.id
        approval.resolved_by_name = current_user.full_name
        approval.resolution_comment = resolution_comment
        self.approval_repository.save(db, approval)

        # Desbloqueo del job y el comando para que puedan ser ejecutados
        job = approval.job
        job.status = "ready_to_execute"
        db.add(job)

        command = job.command
        command.status = "ready_to_execute"
        db.add(command)

        # Logs de auditoria detallando quien autorizo la accion
        self.log_repository.create(
            db=db,
            job_id=job.id,
            level="INFO",
            message="Approval approved",
            details_json={
                "approval_id": str(approval.id),
                "resolved_by_user_id": str(current_user.id),
                "resolved_by_name": current_user.full_name,
                "resolution_comment": resolution_comment
            }
        )

        db.commit()
        db.refresh(approval)
        return approval

    def reject(self, db: Session, approval_id, current_user, resolution_comment: str | None):
        """
        Procesa el rechazo de una solicitud.
        Cancela la ejecucion del job definitivamente.
        """
        approval = self.approval_repository.get_by_id(db, approval_id)
        if not approval:
            raise ValueError("Approval no encontrada")

        if approval.status != "pending":
            raise ValueError("La aprobacion ya fue resuelta")

        # Registro del rechazo
        approval.status = "rejected"
        approval.resolved_at = datetime.utcnow()
        approval.resolved_by_user_id = current_user.id
        approval.resolved_by_name = current_user.full_name
        approval.resolution_comment = resolution_comment
        self.approval_repository.save(db, approval)

        # Finalizacion del job con estado rechazado
        job = approval.job
        job.status = "rejected"
        job.finished_at = datetime.utcnow()
        db.add(job)

        command = job.command
        command.status = "rejected"
        db.add(command)

        # Registro del resultado negativo en el repositorio de resultados
        self.job_result_repository.upsert(
            db=db,
            job_id=job.id,
            success=False,
            summary="Job rechazado en el flujo de aprobacion",
            result_json={
                "status": "rejected",
                "reason": "Aprobacion rechazada",
                "resolved_by_user_id": str(current_user.id),
                "resolved_by_name": current_user.full_name,
                "resolution_comment": resolution_comment
            }
        )

        db.commit()
        db.refresh(approval)
        return approval