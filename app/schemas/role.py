# SCHEMA DE RESPUESTA PARA LA ENTIDAD DE ROLES (DTO)
# Define la estructura de datos que la API devuelve cuando se consulta un rol.

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RoleResponse(BaseModel):
    # ID unico del rol: Se valida automaticamente como un UUID valido.
    id: UUID
    
    # Nombre del rol: Cadena de texto que identifica el permiso (ej. 'admin').
    name: str
    
    # Descripcion opcional: Puede ser nula si el rol no tiene una explicacion detallada.
    description: str | None

    # Configuracion de Pydantic v2:
    # 'from_attributes=True' permite que Pydantic lea los datos directamente desde 
    # los modelos de SQLAlchemy (objetos ORM) y los convierta a JSON automaticamente.
    model_config = ConfigDict(from_attributes=True)