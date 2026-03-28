"""
MODELO DE RESULTADO DE TRABAJO (JobResult).
Almacena el desenlace final de la ejecucion de un Job.
Contiene el estado de exito, un resumen legible y los datos finales generados.
"""
import uuid
from datetime import datetime

from sqlalchemy import Boolean, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class JobResult(Base):
    __tablename__ = "job_results"

    # Identificador unico universal para este registro de resultado
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Relacion uno a uno con el Job (unique=True garantiza que un Job solo tenga un resultado final)
    job_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    # Indicador booleano: True si el trabajo cumplio su objetivo, False si fallo
    success: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # Descripcion textual del resultado (ej: 'El email fue enviado correctamente a 5 destinatarios')
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Datos finales estructurados (ej: IDs de los mensajes enviados o datos extraidos de una web)
    result_json: Mapped[dict | None] = mapped_column(JSONB, nullable=True)

    # Marca temporal de cuando se cerro el trabajo y se registro el resultado
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    # Relacion inversa para acceder al objeto Job desde el resultado
    job = relationship("Job", back_populates="job_result")