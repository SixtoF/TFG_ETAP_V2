"""
MODELO DE TAREAS PROGRAMADAS (ScheduledTask).
Representa tareas que se deben ejecutar de forma periodica segun una expresion Cron.
Este modelo permite que el sistema lance comandos automaticamente (ej: cada lunes a las 08:00)
sin intervencion manual del usuario.
"""
import uuid
from datetime import datetime

from sqlalchemy import String, Text, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ScheduledTask(Base):
    __tablename__ = "scheduled_tasks"

    # ID unico de la tarea programada
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Nombre descriptivo para identificar la tarea en el panel
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Notas sobre el proposito de esta programacion
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Texto que el bot interpretara como comando al llegar el momento
    command_text: Mapped[str] = mapped_column(Text, nullable=False)

    # Formato cron (ej: '0 8 * * 1' para cada lunes a las 8 AM)
    cron_expression: Mapped[str] = mapped_column(String(100), nullable=False)

    # Region horaria para asegurar la precision del disparo
    timezone: Mapped[str] = mapped_column(String(100), nullable=False, default="Europe/Madrid")

    # Permite pausar o reactivar la tarea sin borrarla
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Si es True, el job se mandara directamente al worker de Celery
    auto_enqueue: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Marca de tiempo de la ejecucion mas reciente
    last_run_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Fecha calculada para el siguiente disparo segun el cron
    next_run_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # Registro de cuando se creo la entrada en la base de datos
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    
    # Registro de la ultima modificacion de la configuracion
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)