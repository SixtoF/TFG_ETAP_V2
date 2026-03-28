"""
Modelo de Comando (Command).
Es el registro principal que guarda el texto original del usuario,
su origen y coordina las predicciones de IA y los trabajos de ejecucion.
"""
import uuid
from datetime import datetime

from sqlalchemy import String, Text, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Command(Base):
    # Nombre de la tabla en PostgreSQL
    __tablename__ = "commands"

    # ID unico para identificar cada peticion (formato UUID)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # El texto tal cual lo escribio el usuario (ej: "Enviame el reporte por mail")
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)

    # De donde viene la peticion (ej: 'web', 'api', 'mobile', 'telegram')
    source: Mapped[str] = mapped_column(String(50), nullable=False, default="web")

    # Estado del ciclo de vida (ej: 'received', 'processed', 'failed')
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="received")

    # Momento exacto en que se recibio la peticion
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    # --- RELACIONES ---

    # Enlace con la interpretacion de la IA (Uno a Uno)
    # uselist=False asegura que un comando solo tenga una prediccion
    intent_prediction = relationship(
        "IntentPrediction",
        back_populates="command",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # Enlace con los trabajos de ejecucion (Uno a Muchos)
    # Un comando puede generar varios intentos de trabajo si falla el primero
    jobs = relationship(
        "Job",
        back_populates="command",
        cascade="all, delete-orphan"
    )