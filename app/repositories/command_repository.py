"""
Repositorio de Comandos (CommandRepository).
Centraliza todas las operaciones de base de datos para los comandos.
Permite crear, listar, actualizar estados y obtener detalles completos.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.command import Command
from app.models.job import Job
from app.schemas.command import CommandCreate

class CommandRepository:
    # Crea un nuevo registro de comando en la base de datos
    def create(self, db: Session, command_in: CommandCreate) -> Command:
        # Crea el objeto Command usando los datos validados del esquema
        command = Command(
            raw_text=command_in.raw_text,
            source=command_in.source
        )
        # Lo agrega a la sesion de base de datos
        db.add(command)
        # flush() sincroniza con la DB para generar el ID sin cerrar la transaccion
        db.flush()
        # refresh() actualiza el objeto con los datos generados por la DB
        db.refresh(command)
        return command

    # Lista comandos ordenados por fecha, los mas recientes primero
    def list(self, db: Session, limit: int = 50, offset: int = 0) -> list[Command]:
        # Prepara la consulta de seleccion con paginacion
        stmt = (
            select(Command)
            .order_by(Command.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        # Ejecuta la consulta
        result = db.execute(stmt)
        # Devuelve la lista de resultados
        return list(result.scalars().all())

    # Busca un comando por ID incluyendo TODA su informacion relacionada
    def get_by_id(self, db: Session, command_id):
        # Esta consulta es muy eficiente: carga la IA, los Jobs y los Steps de esos Jobs
        stmt = (
            select(Command)
            .options(
                # selectinload evita hacer multiples consultas a la base de datos
                selectinload(Command.intent_prediction),
                selectinload(Command.jobs).selectinload(Job.steps),
                selectinload(Command.jobs).selectinload(Job.job_result)
            )
            .where(Command.id == command_id)
        )
        result = db.execute(stmt)
        # Devuelve el objeto completo o None si no existe
        return result.scalar_one_or_none()

    # Cambia el estado del comando (ej: de 'received' a 'processed')
    def update_status(self, db: Session, command: Command, status: str) -> Command:
        # Modifica el campo status del objeto existente
        command.status = status
        # Indica a SQLAlchemy que el objeto ha cambiado
        db.add(command)
        # Sincroniza el cambio con la base de datos
        db.flush()
        db.refresh(command)
        return command