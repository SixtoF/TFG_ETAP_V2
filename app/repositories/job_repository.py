"""
Repositorio de Trabajos (JobRepository).
Gestiona la creacion y consulta de trabajos en la base de datos.
Incluye la carga eficiente de los pasos asociados (steps) para cada trabajo.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.job import Job
from app.models.job_step import JobStep

class JobRepository:
    # Crea un nuevo trabajo asociado a un comando
    def create(self, db: Session, command_id, intent_name: str, risk_level: str, status: str = "created") -> Job:
        # Crea el objeto Job con los datos iniciales
        job = Job(
            command_id=command_id,
            intent_name=intent_name,
            risk_level=risk_level,
            status=status
        )
        # Lo añade a la sesion
        db.add(job)
        # flush() sincroniza con la DB para obtener el ID generado sin cerrar la transaccion
        db.flush()
        # Actualiza el objeto con los datos de la DB
        db.refresh(job)
        return job

    # Obtiene una lista de trabajos con sus pasos incluidos
    def list(self, db: Session, limit: int = 50, offset: int = 0) -> list[Job]:
        # Prepara la consulta
        stmt = (
            select(Job)
            # selectinload carga los pasos (steps) de forma eficiente en una sola consulta extra
            .options(selectinload(Job.steps))
            # Ordena por fecha de creacion, los mas nuevos primero
            .order_by(Job.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        # Ejecuta la consulta
        result = db.execute(stmt)
        # Devuelve todos los resultados como una lista de objetos Job
        return list(result.scalars().all())

    # Busca un trabajo especifico por su ID incluyendo sus pasos
    def get_by_id(self, db: Session, job_id):
        stmt = (
            select(Job)
            # Tambien cargamos los pasos aqui para tener la informacion completa
            .options(selectinload(Job.steps))
            .where(Job.id == job_id)
        )
        result = db.execute(stmt)
        # Devuelve el Job encontrado o None si el ID no existe
        return result.scalar_one_or_none()