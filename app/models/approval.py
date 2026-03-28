"""
MODELO DE APROBACIONES (Approval).
Gestiona el flujo de autorizacion humana para tareas de riesgo elevado.
Permite auditar quien, cuando y por que se permitio o denego una ejecucion sensible.
"""
import uuid
from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Approval(Base):
    __tablename__ = "approvals"

    # Identificador unico de la solicitud de aprobacion
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Relacion Uno a Uno con el Job (unique=True garantiza una sola peticion por trabajo)
    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    # Estado actual de la solicitud (ej: 'pending', 'approved', 'rejected')
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")

    # Explicacion de por que el sistema requiere intervencion humana (ej: 'Riesgo Alto detectado')
    reason: Mapped[str] = mapped_column(Text, nullable=False)

    # Fecha automatica de cuando el motor de ejecucion detuvo el proceso
    requested_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    # Marca temporal de cuando el supervisor tomo la decision
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # ID tecnico o correo del usuario que autorizo o rechazo
    resolved_by: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Nombre legible del supervisor para mostrar en el historial
    resolved_by_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Justificacion escrita por el humano al aprobar o rechazar
    resolution_comment: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Navegacion hacia el objeto Job relacionado
    job = relationship("Job", back_populates="approval")