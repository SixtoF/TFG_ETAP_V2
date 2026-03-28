"""
Modelo de Paso de Trabajo (JobStep).
Representa una tarea individual dentro de un Job mas grande.
Permite ejecutar acciones en orden y rastrear su progreso por separado.
"""
import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class JobStep(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = "job_steps"

    # ID unico del paso (formato UUID)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Relacion con el Job principal. Si el Job se borra, este paso tambien.
    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False
    )

    # Posicion o numero del paso en la secuencia (1, 2, 3...)
    step_order: Mapped[int] = mapped_column(Integer, nullable=False)

    # Nombre descriptivo de la accion (ej: "Leer archivo", "Enviar correo")
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Categoria tecnica del paso
    step_type: Mapped[str] = mapped_column(String(100), nullable=False)

    # Indica que conector externo se usa (ej: "gmail", "file_system")
    connector_type: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Datos de entrada necesarios para este paso en formato JSON
    input_json: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    # Estado actual del paso (ej: 'pending', 'running', 'success', 'failed')
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="pending")

    # --- FECHAS DE CONTROL ---
    # Fecha de creacion del paso
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    # Fecha de inicio de ejecucion real
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    # Fecha de finalizacion de la tarea
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # --- RELACIONES ---
    # Enlace logico hacia el objeto Job padre
    job = relationship("Job", back_populates="steps")

    # Relacion con los registros de eventos generados durante la ejecucion de este paso
    execution_logs = relationship("ExecutionLog", back_populates="job_step", cascade="all, delete-orphan")