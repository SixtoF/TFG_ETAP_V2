# SCHEMAS DE ENTRADA Y SALIDA PARA LA ENTIDAD DE USUARIOS (DTO)
# Gestiona la validacion de datos al crear usuarios y la proteccion de informacion al responder.

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.role import RoleResponse


class UserCreateRequest(BaseModel):
    # Datos de entrada para crear usuario: Validacion estricta antes de llegar a la BD.
    
    # EmailStr: Valida automaticamente que el formato sea un correo real (ej. usuario@etap.com).
    email: EmailStr
    
    # password: Obliga a que la clave tenga entre 8 y 128 caracteres para cumplir con politicas de seguridad.
    password: str = Field(..., min_length=8, max_length=128)
    
    # full_name: Asegura que el nombre no este vacio y tenga un tamaño razonable.
    full_name: str = Field(..., min_length=1, max_length=255)
    
    # role_name: Recibe el nombre del rol (ej. 'admin') en lugar del ID, para que sea mas facil de usar.
    role_name: str = Field(..., min_length=1, max_length=50)


class UserResponse(BaseModel):
    # Respuesta serializada de usuario: Lo que el cliente ve tras la creacion o consulta.
    
    # id: Identificador unico en formato UUID.
    id: UUID
    
    # email y full_name: Datos publicos del perfil del usuario.
    email: str
    full_name: str
    
    # is_active: Informa si la cuenta esta operativa o suspendida.
    is_active: bool
    
    # role: Se implementa la inclusion del RoleResponse completo (ID, nombre y descripcion).
    # Esto permite que el Frontend sepa los permisos del usuario de un solo vistazo.
    role: RoleResponse
    
    # created_at: Fecha de alta del usuario.
    created_at: datetime

    # Configuracion de Pydantic: 'from_attributes=True' permite mapear objetos de SQLAlchemy.
    # Es vital para que la relacion 'role' funcione correctamente en la respuesta.
    model_config = ConfigDict(from_attributes=True)