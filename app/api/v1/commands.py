"""
Rutas de Comandos (Command Router).
Define los puntos de acceso para crear comandos y consultar su estado.
Conecta las peticiones HTTP con la logica de 'CommandService'.
"""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.command import (
    CommandCreate,
    CommandResponse,
    CommandDetailResponse,
    CommandCreateWithJobResponse
)
from app.services.command_service import CommandService

# Definimos el enrutador para agrupar las rutas de comandos
router = APIRouter()
# Instanciamos el servicio que orquestra toda la logica
command_service = CommandService()


@router.post("", response_model=CommandCreateWithJobResponse, status_code=201)
def create_command(command_in: CommandCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo comando y dispara automaticamente el Planner y la creacion de Jobs.
    Devuelve el objeto completo (Command + IA + Job).
    """
    try:
        # Llama al servicio maestro para ejecutar todo el flujo transaccional
        return command_service.create_command_with_job(db, command_in)
    except ValueError as exc:
        # Si el texto esta vacio o hay error de validacion, devuelve error 400
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("", response_model=list[CommandResponse])
def list_commands(
    # Parametros para controlar la cantidad de resultados
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    """
    Retorna una lista simple de comandos para vista general.
    """
    return command_service.list_commands(db, limit=limit, offset=offset)


@router.get("/{command_id}", response_model=CommandDetailResponse)
def get_command(command_id: UUID, db: Session = Depends(get_db)):
    """
    Obtiene el detalle profundo de un comando, incluyendo su prediccion de IA 
    y todos los trabajos (jobs) con sus respectivos pasos (steps).
    """
    command = command_service.get_command_by_id(db, command_id)
    if not command:
        # Si el UUID no existe en la base de datos, devuelve error 404
        raise HTTPException(status_code=404, detail="Command no encontrado")
    return command