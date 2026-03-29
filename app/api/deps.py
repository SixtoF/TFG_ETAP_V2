# ==============================================================================
# SISTEMA DE DEPENDENCIAS Y CONTROL DE ACCESO (SECURITY DEPS)
# Este modulo gestiona la extraccion de identidad desde los tokens JWT y
# aplica la logica de autorizacion basada en roles (RBAC).
# ==============================================================================

from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.jwt import ALGORITHM, SECRET_KEY
from app.db.session import SessionLocal
from app.repositories.user_repository import UserRepository

# Define la ruta donde Swagger debe buscar el token (el endpoint de login)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Valida el token JWT, extrae el ID del usuario y lo busca en la base de datos.
    Se asegura de que el token sea valido y el usuario este activo.
    """
    # Excepcion estandar para errores de autenticacion (Token invalido o expirado)
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No autenticado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Decodifica el token usando la clave secreta y el algoritmo definido
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")  # 'sub' suele contener el ID del usuario
        if not user_id:
            raise credentials_exception
    except JWTError:
        # Si el token esta corrupto o la firma no coincide, lanzamos error
        raise credentials_exception

    # Abrimos una sesion temporal para validar al usuario contra la BD
    db = SessionLocal()
    try:
        user_repository = UserRepository()
        # Buscamos al usuario por su UUID extraido del token
        user = user_repository.get_by_id(db, UUID(user_id))

        if not user:
            raise credentials_exception

        # Verificamos que la cuenta no haya sido desactivada
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )

        # Si todo es correcto, devolvemos el objeto 'user' completo
        return user
    finally:
        # Cerramos siempre la conexion para evitar fugas de memoria
        db.close()


def require_roles(*allowed_roles: str):
    """
    Fabrica de dependencias para restringir el acceso segun el nombre del Rol.
    Uso: Depends(require_roles("admin", "operator"))
    """
    def dependency(current_user=Depends(get_current_user)):
        # Compara el nombre del rol del usuario con la lista de roles permitidos
        if current_user.role.name not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No autorizado para esta accion"
            )
        # Si tiene el rol necesario, permite continuar la peticion
        return current_user

    return dependency