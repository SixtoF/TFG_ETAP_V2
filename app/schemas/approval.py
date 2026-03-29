"""
ESQUEMAS DE APROBACION (Approval Schemas).
Define la estructura para la visualizacion de estados de seguridad y los 
datos requeridos para la toma de decisiones manuales sobre Jobs bloqueados.
"""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ApprovalResponse(BaseModel):
    # Respuesta serializada de aprobacion: Lo que el sistema muestra al consultar un bloqueo.
    
    # id y job_id: Identificadores unicos de la aprobacion y del trabajo vinculado.
    id: UUID
    job_id: UUID
    
    # status: Estado actual (ej. 'pending', 'approved', 'rejected').
    status: str
    
    # reason: Texto que explica por que este trabajo requiere supervision humana.
    reason: str
    
    # Tiempos de control: Fecha de peticion y fecha en la que se tomo la decision.
    requested_at: datetime
    resolved_at: datetime | None
    
    # Auditoria real: Se añade el ID del usuario de la BD que firmo la resolucion.
    resolved_by_user_id: UUID | None
    
    # Auditoria visible: Nombre del usuario en el momento de la firma (ej. 'Admin Carlos').
    resolved_by_name: str | None
    
    # Comentario final: Explicacion opcional de por que se aprobo o rechazo el trabajo.
    resolution_comment: str | None

    # Configuracion para mapear desde los modelos de SQLAlchemy.
    model_config = ConfigDict(from_attributes=True)


class ApprovalDecisionRequest(BaseModel):
    # Payload para aprobar o rechazar: Lo que el administrador envia al pulsar el boton.
    
    # resolution_comment: El unico dato que el usuario escribe; el resto lo saca la API del Token JWT.
    # El valor por defecto es None por si el administrador no quiere dejar ningun comentario.
    resolution_comment: str | None = Field(default=None, example="Aprobado para continuar")