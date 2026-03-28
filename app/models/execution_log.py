"""
MODELO DE LOGS DE EJECUCION (ExecutionLog).
Registra el historial detallado de eventos ocurridos durante la ejecucion de un Job.
Permite rastrear errores o mensajes informativos vinculados a un Job o un Step especifico.
"""
from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey, BigInteger
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    # Identificador unico incremental para cada entrada del log
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    # Relacion con el Job principal (obligatoria para saber a que tarea pertenece)
    job_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False
    )

    # Relacion con un paso especifico (opcional, para logs detallados de un step)
    job_step_id: Mapped[str | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("job_steps.id", ondelete="CASCADE"),
        nullable=True
    )

    # Nivel de importancia del mensaje (ej: INFO, WARNING, ERROR, DEBUG)
    level: Mapped[str] = mapped_column(String(20), nullable=False)

    # Descripcion textual de lo que ocurrio
    message: Mapped[str] = mapped_column(Text, nullable=False)

    # Datos tecnicos adicionales en formato JSON (ej: traza del error o respuesta de una API)
    details_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Fecha y hora exacta en la que se genero el evento
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    # Definicion de relaciones para navegacion entre objetos en SQLAlchemy
    job = relationship("Job", back_populates="execution_logs")
    job_step = relationship("JobStep", back_populates="execution_logs")