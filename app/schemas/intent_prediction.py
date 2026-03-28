"""
Esquema de Respuesta para Prediccion de Intenciones (Response Schema).
Define el formato JSON que el usuario recibira al consultar una prediccion.
Transforma los objetos de la base de datos en datos listos para la web.
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class IntentPredictionResponse(BaseModel):
    # Campos que se incluiran en la respuesta JSON
    id: UUID
    command_id: UUID
    intent_name: str
    confidence: float
    normalized_text: str
    entities_json: dict
    risk_level: str
    plan_json: dict
    created_at: datetime

    # Configuracion del modelo Pydantic
    model_config = ConfigDict(
        # Permite que Pydantic lea datos directamente desde objetos de SQLAlchemy
        # (Convierte automaticamente el modelo de base de datos a este formato JSON)
        from_attributes=True 
    )