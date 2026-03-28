"""
ESQUEMAS DE APROBACION (Approval Schemas).
Define la estructura para la visualizacion de estados de seguridad y los 
datos requeridos para la toma de decisiones manuales sobre Jobs bloqueados.
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ApprovalResponse(BaseModel):
    # Identificador unico de la solicitud de aprobacion
    id: UUID
    
    # Referencia al trabajo que requiere supervision
    job_id: UUID
    
    # Estado actual (pending, approved, rejected)
    status: str
    
    # Motivo tecnico o de negocio por el cual se detuvo la ejecucion
    reason: str
    
    # Fecha de creacion de la solicitud
    requested_at: datetime
    
    # Datos de resolucion (pueden ser None si aun no se ha decidido)
    resolved_at: datetime | None
    resolved_by: str | None
    resolved_by_name: str | None
    resolution_comment: str | None

    # Habilita la lectura directa desde el modelo de SQLAlchemy
    model_config = ConfigDict(from_attributes=True)


class ApprovalDecisionRequest(BaseModel):
    """
    Estructura requerida para resolver una aprobacion pendiente.
    Utiliza Field para garantizar que los datos del supervisor sean validos.
    """
    # ID tecnico del supervisor (obligatorio)
    resolved_by: str = Field(..., min_length=1, max_length=100, example="manager_001")
    
    # Nombre visible del responsable (obligatorio)
    resolved_by_name: str = Field(..., min_length=1, max_length=255, example="Juan Perez")
    
    # Comentario opcional para justificar la decision
    resolution_comment: str | None = Field(default=None, example="Aprobado para continuar")