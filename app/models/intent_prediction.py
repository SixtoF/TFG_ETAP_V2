"""
Modelo de Prediccion de Intenciones (IntentPrediction).
Guarda la interpretación logica de un comando, incluyendo el nivel de riesgo,
la confianza de la IA y el plan de ejecucion generado.
"""
import uuid
from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class IntentPrediction(Base):
    # Nombre de la tabla en PostgreSQL
    __tablename__ = "intent_predictions"

    # ID unico generado automáticamente (formato UUID)
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Relación con la tabla 'commands'. Si el comando se borra, esta predicción también (CASCADE).
    command_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("commands.id", ondelete="CASCADE"),
        nullable=False,
        unique=True # Una predicción por cada comando
    )

    # El nombre de la intencion detectada (ej: "enviar_email", "crear_archivo")
    intent_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Porcentaje de seguridad de la IA (ej: 0.9500 para 95%)
    confidence: Mapped[float] = mapped_column(Numeric(5, 4), nullable=False)

    # El texto limpio y procesado que entendio el sistema
    normalized_text: Mapped[str] = mapped_column(Text, nullable=False)

    # Datos extraidos (nombres, fechas, lugares) guardados en formato JSON de Postgres
    entities_json: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    # Clasificacion de peligro (ej: "bajo", "medio", "alto")
    risk_level: Mapped[str] = mapped_column(String(50), nullable=False)

    # El "paso a paso" generado por la IA guardado como un objeto JSON
    plan_json: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)

    # Fecha y hora exacta de la interpretación
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    # Conexión lógica con el objeto Command en Python
    command = relationship("Command", back_populates="intent_prediction")