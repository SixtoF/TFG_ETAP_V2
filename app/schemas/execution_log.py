"""
ESQUEMA DE RESPUESTA DE LOGS (ExecutionLogResponse).
Define la estructura de datos para la serializacion de los registros de eventos.
Permite exponer de forma segura los detalles de la ejecucion a traves de la API.
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ExecutionLogResponse(BaseModel):
    # Identificador unico incremental del registro de log
    id: int
    
    # Referencia al trabajo principal al que pertenece el log
    job_id: UUID
    
    # Referencia opcional al paso especifico (puede ser None si es un log general del Job)
    job_step_id: UUID | None
    
    # Nivel de severidad del mensaje (ej: INFO, ERROR, WARNING)
    level: str
    
    # Contenido textual del evento registrado
    message: str
    
    # Informacion tecnica adicional en formato diccionario
    details_json: dict | None
    
    # Marca temporal de cuando se genero el registro
    created_at: datetime

    # Configuracion para permitir la conversion automatica desde modelos de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)