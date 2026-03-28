"""
Esquemas de Entrada y Salida para Comandos (Command Schemas).
Define como se reciben los textos del usuario y como se muestran los resultados
completos incluyendo la IA (intent) y los trabajos (jobs).
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict

from app.schemas.intent_prediction import IntentPredictionResponse
from app.schemas.job import JobResponse

class CommandCreate(BaseModel):
    # Datos necesarios para crear un nuevo comando
    # Field(...) indica que el campo es obligatorio
    raw_text: str = Field(..., min_length=1, example="Envia el email diario de resumen")
    source: str = Field(default="web", max_length=50, example="web")

class CommandResponse(BaseModel):
    # Respuesta basica que confirma la recepcion del comando
    id: UUID
    raw_text: str
    source: str
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class CommandDetailResponse(BaseModel):
    # Respuesta completa para ver un comando con todo su historial
    id: UUID
    raw_text: str
    source: str
    status: str
    created_at: datetime
    
    # Incluye la interpretacion de la IA si ya existe
    intent_prediction: IntentPredictionResponse | None = None
    # Incluye la lista de todos los trabajos generados para este comando
    jobs: list[JobResponse] = []

    model_config = ConfigDict(from_attributes=True)

class CommandCreateWithJobResponse(BaseModel):
    # Respuesta especial que devuelve todo el flujo de golpe
    # Se usa cuando el usuario crea un comando y queremos mostrarle 
    # inmediatamente que ya se interpreto y se creo un trabajo.
    command: CommandResponse
    intent_prediction: IntentPredictionResponse
    job: JobResponse