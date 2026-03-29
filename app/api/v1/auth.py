# ==============================================================================
# ENDPOINTS DE AUTENTICACION Y PERFIL DE USUARIO
# Gestiona el inicio de sesion y la consulta de identidad para el cliente.
# ==============================================================================

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.schemas.auth import MeResponse, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter()
auth_service = AuthService()


@router.post("/login", response_model=TokenResponse)
def login(
    db: Session = Depends(get_db),
    # Cambiamos LoginRequest por OAuth2PasswordRequestForm para compatibilidad con Swagger
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Endpoint para iniciar sesion: Recibe las credenciales desde el formulario de Swagger
    o una peticion POST estandar y devuelve un JWT.
    """
    try:
        # form_data.username contiene el email y form_data.password la contrasena
        token = auth_service.login(db, form_data.username, form_data.password)
        return TokenResponse(access_token=token, token_type="bearer")
    except ValueError as exc:
        # Error 401 si el usuario no existe o la clave es incorrecta
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Credenciales invalidas"
        )


@router.get("/me", response_model=MeResponse)
def me(current_user=Depends(get_current_user)):
    """
    Endpoint para obtener el perfil del usuario logueado.
    La identidad se extrae automaticamente del token JWT.
    """
    return MeResponse(
        id=str(current_user.id),
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role.name
    )