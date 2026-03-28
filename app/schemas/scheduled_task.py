"""
ESQUEMAS DE VALIDACION PARA TAREAS PROGRAMADAS (Pydantic).
Define la estructura de los datos que entran y salen de la API.
ScheduledTaskCreate: Valida los datos que envia el usuario al crear una tarea.
ScheduledTaskResponse: Define como se envian los datos al cliente (Swagger/Frontend).
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ScheduledTaskCreate(BaseModel):
    # Datos obligatorios para identificar la tarea
    name: str = Field(..., min_length=1, max_length=255, example="Resumen diario")
    
    # Explicacion opcional sobre que hace esta programacion
    description: str | None = Field(default=None, example="Envia el resumen diario a direccion")
    
    # El comando exacto que el bot debe ejecutar automaticamente
    command_text: str = Field(..., min_length=1, example="Envia el email diario de resumen")
    
    # Formato cron para la periodicidad (ej: cada dia a las 18:00 de lunes a viernes)
    cron_expression: str = Field(..., min_length=1, max_length=100, example="0 18 * * 1-5")
    
    # Zona horaria para evitar desfases horarios en la ejecucion
    timezone: str = Field(default="Europe/Madrid", max_length=100, example="Europe/Madrid")
    
    # Determina si el sistema debe ejecutar el comando sin pedir confirmacion
    auto_enqueue: bool = Field(default=True)


class ScheduledTaskResponse(BaseModel):
    # ID unico generado por la base de datos
    id: UUID
    name: str
    description: str | None
    command_text: str
    cron_expression: str
    timezone: str
    is_active: bool
    auto_enqueue: bool
    
    # Tiempos de ejecucion calculados por el sistema
    last_run_at: datetime | None
    next_run_at: datetime
    
    # Marcas de tiempo de auditoria
    created_at: datetime
    updated_at: datetime

    # Permite que Pydantic lea los datos directamente desde el modelo de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)