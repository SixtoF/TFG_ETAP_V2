"""
MODELO DE APROBACIONES (Approval).
Gestiona el flujo de autorizacion humana para tareas de riesgo elevado.
Permite auditar quien, cuando y por que se permitio o denego una ejecucion sensible.
"""
# Se actualiza para vincular las decisiones de seguridad con usuarios reales del sistema.

import uuid
from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Approval(Base):
    # Nombre de la tabla fisica en PostgreSQL
    __tablename__ = "approvals"

    # ID unico de la aprobacion: Generado automaticamente como UUID.
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # FK unica al job sensible: Conecta con la tabla 'jobs'. 'unique=True' asegura 1 aprobacion por job.
    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    # Estado de la aprobacion: Puede ser 'pending', 'approved' o 'rejected'.
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")

    # Motivo por el cual se requiere aprobacion: Texto que explica el riesgo detectado (ej. 'Riesgo alto').
    reason: Mapped[str] = mapped_column(Text, nullable=False)

    # Fecha de solicitud: Momento exacto en que se bloqueo el job esperando firma.
    requested_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    # Fecha de resolucion: Momento en que el administrador tomo la decision.
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Usuario real que resolvio: FK que conecta con la nueva tabla 'users'.
    # 'ondelete="SET NULL"' mantiene el registro aunque el usuario sea borrado algun dia.
    resolved_by_user_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    # Nombre visible congelado para auditoria: Guarda el nombre del usuario en ese momento (ej. 'Admin Juan').
    # Sirve como backup historico si el usuario cambia su perfil mas adelante.
    resolved_by_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Comentario de resolucion: Espacio para que el responsable explique por que aprueba o rechaza.
    resolution_comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relaciones:
    # 'job' conecta con el trabajo asociado.
    # 'resolved_by_user' permite acceder al perfil del administrador que firmo la aprobacion.
    job = relationship("Job", back_populates="approval")
    resolved_by_user = relationship("User")