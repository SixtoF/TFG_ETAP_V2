"""
SERVICIO DE GESTION DE APROBACIONES (ApprovalService).
Controla el ciclo de vida de las solicitudes de autorizacion.
Permite transicionar trabajos de riesgo alto desde un estado de pausa 
hacia la ejecucion final o el rechazo definitivo tras supervision humana.
"""
from datetime import datetime

from sqlalchemy.orm import Session

from app.repositories.approval_repository import ApprovalRepository
from app.repositories.command_repository import CommandRepository
from app.repositories.execution_log_repository import ExecutionLogRepository
from app.repositories.job_repository import JobRepository
from app.repositories.job_result_repository import JobResultRepository


class ApprovalService:
    # Inicializa todos los componentes necesarios para la auditoria y control
    def __init__(self):
        self.approval_repository = ApprovalRepository()
        self.job_repository = JobRepository()
        self.command_repository = CommandRepository()
        self.log_repository = ExecutionLogRepository()
        self.job_result_repository = JobResultRepository()

    # Evalua si un Job debe ser pausado para revision humana
    def create_approval_if_needed(self, db: Session, job):
        if job.risk_level != "high":
            return None

        # Crea el registro de aprobacion en estado pendiente
        approval = self.approval_repository.create(
            db=db,
            job_id=job.id,
            reason="High risk job requires approval",
            status="pending"
        )

        # Actualiza el estado del Job y del Comando para reflejar la espera
        job.status = "approval_pending"
        db.add(job)

        command = job.command
        command.status = "approval_pending"
        db.add(command)

        # Registra el evento en la bitacora de ejecucion
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

        db.flush() # Persiste los cambios en la transaccion actual
        return approval

    # Metodos de consulta delegados al repositorio
    def list_approvals(self, db: Session, limit: int = 50, offset: int = 0, status: str | None = None):
        return self.approval_repository.list(db, limit=limit, offset=offset, status=status)

    def get_approval_by_id(self, db: Session, approval_id):
        return self.approval_repository.get_by_id(db, approval_id)

    # Autoriza la ejecucion de un trabajo bloqueado
    def approve(self, db: Session, approval_id, resolved_by: str, resolved_by_name: str, resolution_comment: str | None):
        approval = self.approval_repository.get_by_id(db, approval_id)
        if not approval:
            raise ValueError("Approval no encontrada")

        if approval.status != "pending":
            raise ValueError("La aprobacion ya fue resuelta")

        # Registra la decision del supervisor
        approval.status = "approved"
        approval.resolved_at = datetime.utcnow()
        approval.resolved_by = resolved_by
        approval.resolved_by_name = resolved_by_name
        approval.resolution_comment = resolution_comment
        self.approval_repository.save(db, approval)

        # Prepara el Job para que el ExecutionService pueda procesarlo
        job = approval.job
        job.status = "ready_to_execute"
        db.add(job)

        command = job.command
        command.status = "ready_to_execute"
        db.add(command)

        # Logs dobles: uno para la aprobacion y otro para el cambio de estado del Job
        self.log_repository.create(
            db=db,
            job_id=job.id,
            level="INFO",
            message="Approval approved",
            details_json={
                "approval_id": str(approval.id),
                "resolved_by": resolved_by,
                "resolved_by_name": resolved_by_name,
                "resolution_comment": resolution_comment
            }
        )

        self.log_repository.create(
            db=db,
            job_id=job.id,
            level="INFO",
            message="Job approved and ready to execute",
            details_json={"job_status": job.status}
        )

        db.commit() # Cierre definitivo de la autorizacion
        db.refresh(approval)
        return approval

    # Cancela definitivamente la ejecucion de un trabajo bloqueado
    def reject(self, db: Session, approval_id, resolved_by: str, resolved_by_name: str, resolution_comment: str | None):
        approval = self.approval_repository.get_by_id(db, approval_id)
        if not approval:
            raise ValueError("Approval no encontrada")

        if approval.status != "pending":
            raise ValueError("La aprobacion ya fue resuelta")

        # Registra el rechazo
        approval.status = "rejected"
        approval.resolved_at = datetime.utcnow()
        approval.resolved_by = resolved_by
        approval.resolved_by_name = resolved_by_name
        approval.resolution_comment = resolution_comment
        self.approval_repository.save(db, approval)

        # Marca Job y Comando como rechazados (finalizados con error)
        job = approval.job
        job.status = "rejected"
        job.finished_at = datetime.utcnow()
        db.add(job)

        command = job.command
        command.status = "rejected"
        db.add(command)

        self.log_repository.create(
            db=db,
            job_id=job.id,
            level="WARNING",
            message="Approval rejected",
            details_json={
                "approval_id": str(approval.id),
                "resolved_by": resolved_by,
                "resolved_by_name": resolved_by_name,
                "resolution_comment": resolution_comment
            }
        )

        # Genera un resultado final negativo para cerrar el ciclo de vida
        self.job_result_repository.upsert(
            db=db,
            job_id=job.id,
            success=False,
            summary="Job rechazado en el flujo de aprobacion",
            result_json={
                "status": "rejected",
                "reason": "Aprobacion rechazada",
                "resolved_by": resolved_by,
                "resolved_by_name": resolved_by_name,
                "resolution_comment": resolution_comment
            }
        )

        db.commit()
        db.refresh(approval)
        return approval