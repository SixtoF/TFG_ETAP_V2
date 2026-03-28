"""
ESQUEMA DE RESPUESTA DE RESULTADOS (JobResultResponse).
Define la estructura de datos final que se envia al cliente al terminar un Job.
Contiene el veredicto de exito o fallo y los datos finales generados.
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class JobResultResponse(BaseModel):
    # Identificador unico universal del registro de resultado
    id: UUID
    
    # Referencia al trabajo original que genero este resultado
    job_id: UUID
    
    # Indicador de exito (True si todo salio bien, False si hubo errores criticos)
    success: bool
    
    # Resumen legible para el usuario final (ej: 'Proceso completado con exito')
    summary: str | None
    
    # Datos tecnicos finales en formato JSON resultantes de la operacion
    result_json: dict | None
    
    # Fecha y hora exacta en la que se registro el fin del trabajo
    created_at: datetime

    # Configuracion para mapear directamente desde objetos de base de datos (SQLAlchemy)
    model_config = ConfigDict(from_attributes=True)