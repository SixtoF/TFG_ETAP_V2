"""
REPOSITORIO DE APROBACIONES (ApprovalRepository).
Gestiona la persistencia y recuperacion de solicitudes de autorizacion.
Permite una navegacion eficiente entre aprobaciones y sus trabajos asociados 
mediante carga anticipada (eager loading).
"""
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.approval import Approval
from app.models.job import Job


class ApprovalRepository:
    # Registra una nueva solicitud de bloqueo por seguridad en la base de datos
    def create(self, db: Session, job_id, reason: str, status: str = "pending") -> Approval:
        approval = Approval(
            job_id=job_id,
            reason=reason,
            status=status
        )
        db.add(approval)
        db.flush() # Sincroniza para obtener el ID generado
        db.refresh(approval)
        return approval

    # Recupera una lista de solicitudes con filtros opcionales
    def list(self, db: Session, limit: int = 50, offset: int = 0, status: str | None = None) -> list[Approval]:
        # Prepara la consulta cargando el objeto Job relacionado de forma eficiente
        stmt = (
            select(Approval)
            .options(selectinload(Approval.job)) 
            .order_by(Approval.requested_at.desc()) # Mostrar las mas recientes primero
            .offset(offset)
            .limit(limit)
        )

        # Filtro opcional por estado (ej: solo ver las 'pending')
        if status:
            stmt = stmt.where(Approval.status == status)

        result = db.execute(stmt)
        return list(result.scalars().all())

    # Obtiene una aprobacion detallada incluyendo Job y sus pasos (Steps)
    def get_by_id(self, db: Session, approval_id):
        stmt = (
            select(Approval)
            # Carga anidada: Approval -> Job -> Steps
            .options(selectinload(Approval.job).selectinload(Job.steps))
            .where(Approval.id == approval_id)
        )
        result = db.execute(stmt)
        return result.scalar_one_or_none()

    # Busca si un trabajo especifico tiene ya una solicitud vinculada
    def get_by_job_id(self, db: Session, job_id):
        stmt = select(Approval).where(Approval.job_id == job_id)
        result = db.execute(stmt)
        return result.scalar_one_or_none()

    # Metodo generico para guardar cambios tras una aprobacion o rechazo
    def save(self, db: Session, approval: Approval) -> Approval:
        db.add(approval)
        db.flush()
        db.refresh(approval)
        return approval