"""
Esquemas de Respuesta para Jobs y sus Pasos (Job & JobStep Response).
Permiten devolver informacion detallada del estado de ejecucion.
Organizan los datos de forma anidada (Un Job contiene una lista de Steps).
"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.schemas.job_result import JobResultResponse

class JobStepResponse(BaseModel):
    # Datos detallados de cada paso individual del trabajo
    id: UUID
    job_id: UUID
    step_order: int      # Posicion en la secuencia de ejecucion
    name: str            # Nombre del paso
    step_type: str       # Tipo tecnico del paso
    connector_type: str | None # Conector usado (opcional)
    input_json: dict     # Parametros de entrada en formato JSON
    status: str          # Estado (pending, success, failed, etc.)
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None

    model_config = ConfigDict(from_attributes=True)

class JobResponse(BaseModel):
    # Datos principales del trabajo (Job)
    id: UUID
    command_id: UUID
    status: str
    intent_name: str
    risk_level: str
    created_at: datetime
    started_at: datetime | None
    finished_at: datetime | None
    
    # Lista anidada: Aqui se incluyen todos los JobStepResponse asociados
    # Si el Job no tiene pasos, devuelve una lista vacia por defecto []
    steps: list[JobStepResponse] = []

    model_config = ConfigDict(
        # Permite convertir objetos de SQLAlchemy (modelos) a estos esquemas JSON
        from_attributes=True
    )