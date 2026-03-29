# ENDPOINTS PARA LA GESTION ADMINISTRATIVA DE USUARIOS
# Permite a los administradores crear, listar y consultar usuarios del sistema.

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.schemas.user import UserCreateRequest, UserResponse
from app.services.user_service import UserService

router = APIRouter()
user_service = UserService()


@router.post("", response_model=UserResponse, dependencies=[Depends(require_roles("admin"))])
def create_user(payload: UserCreateRequest, db: Session = Depends(get_db)):
    # Endpoint para registrar un nuevo usuario: Solo accesible para el rol 'admin'.
    try:
        # Se implementa la creacion delegando en el servicio de usuarios.
        return user_service.create_user(
            db=db,
            email=payload.email,
            password=payload.password,
            full_name=payload.full_name,
            role_name=payload.role_name
        )
    except ValueError as exc:
        # Si el email ya existe o el rol es invalido, devuelve un error 400 (Bad Request).
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("", response_model=list[UserResponse], dependencies=[Depends(require_roles("admin"))])
def list_users(db: Session = Depends(get_db)):
    # Endpoint para listar todos los usuarios: Solo para administradores.
    # Se implementa la logica de consulta a traves del servicio.
    return user_service.list_users(db)


@router.get("/{user_id}", response_model=UserResponse, dependencies=[Depends(require_roles("admin"))])
def get_user(user_id: UUID, db: Session = Depends(get_db)):
    # Endpoint para obtener el detalle de un usuario especifico mediante su ID.
    # Tambien protegido para que solo el 'admin' pueda consultar perfiles ajenos.
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user