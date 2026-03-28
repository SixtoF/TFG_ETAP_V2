"""
Modelo de Trabajo (Job).
Rastrea la ejecucion de un comando, su estado actual (creado, iniciado, finalizado)
y mantiene la relacion con los pasos específicos (steps) que lo componen.
"""
import uuid
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Job(Base):
    # Nombre de la tabla en la base de datos
    __tablename__ = "jobs"

    # Identificador unico del trabajo (formato UUID)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Relacion con el comando que lo creo. Si el comando se borra, el job tambien desaparece.
    command_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("commands.id", ondelete="CASCADE"),
        nullable=False
    )

    # Estado actual del trabajo (ej: 'created', 'running', 'completed', 'failed')
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="created")

    # Copia el nombre de la intención detectada para tenerlo a mano en la ejecución
    intent_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Nivel de riesgo para saber si requiere supervisión durante la ejecución
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False)

    # --- FECHAS DE CONTROL ---
    # Cuando se creo el registro
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    # Cuándo empezo a ejecutarse realmente el trabajador (worker)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    # Cuando termino el proceso con exito o error
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # --- RELACIONES ---
    # Enlace hacia el objeto Command original
    command = relationship("Command", back_populates="jobs")
    
    # Enlace hacia la lista de pasos detallados (JobStep). 
    # 'delete-orphan' significa que si borras un Job, se borran todos sus pasos automaticamente.
    steps = relationship("JobStep", back_populates="job", cascade="all, delete-orphan")

    # Relacion con los registros de eventos (Logs)
    # Un Job puede tener muchisimos logs (relacion Uno a Muchos)
    execution_logs = relationship("ExecutionLog", back_populates="job", cascade="all, delete-orphan")

    # Relacion con el resultado definitivo (Result)
    # uselist=False transforma esto en una relacion Uno a Uno (un Job = un Resultado)
    job_result = relationship("JobResult", back_populates="job", uselist=False, cascade="all, delete-orphan")

    # Relacion Uno a Uno con el modelo Approval
    # uselist=False asegura que un Job no pueda tener multiples solicitudes de aprobacion activas
    approval = relationship("Approval", back_populates="job", uselist=False, cascade="all, delete-orphan")