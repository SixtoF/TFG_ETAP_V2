# SCHEMAS PARA PROCESO DE AUTENTICACION Y TOKENS (JWT)
# Define la estructura de datos para el inicio de sesion y la entrega de credenciales digitales.

from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    # Credenciales de login: Lo que el usuario envia en el formulario de acceso.
    
    # email: Se valida como correo real antes de intentar buscarlo en la base de datos.
    email: EmailStr
    
    # password: Clave en texto plano que sera verificada contra el hash de la BD.
    password: str


class TokenResponse(BaseModel):
    # Respuesta del login: El "paquete" que recibe el Frontend tras un acceso correcto.
    
    # access_token: Es el string largo (JWT) que el cliente debe guardar para futuras peticiones.
    access_token: str
    
    # token_type: Por defecto 'bearer', indicando el estandar de autenticacion OAuth2.
    token_type: str = "bearer"


class MeResponse(BaseModel):
    # Usuario autenticado actual: Lo que devuelve el endpoint de "Quien soy yo".
    
    # id, email y full_name: Datos basicos para mostrar en la interfaz (ej. el nombre en el menu).
    id: str
    email: str
    full_name: str
    
    # role: Devuelve solo el nombre del rol (ej. 'admin') para facilitar la logica de permisos en el Frontend.
    role: str