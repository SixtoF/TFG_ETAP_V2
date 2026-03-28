"""
Servicio de Consultas de Trabajos (JobQueryService).
Se encarga exclusivamente de las operaciones de lectura.
Separa las consultas (Queries) de las acciones de escritura (Commands).
"""
from sqlalchemy.orm import Session

from app.repositories.job_repository import JobRepository


class JobQueryService:
    def __init__(self):
        # Inicializa el repositorio de trabajos para acceder a la base de datos
        self.repository = JobRepository()

    # Recupera una lista de trabajos con soporte para paginacion
    def list_jobs(self, db: Session, limit: int = 50, offset: int = 0):
        # Llama al repositorio para obtener los registros segun el limite y el desplazamiento
        return self.repository.list(db, limit=limit, offset=offset)

    # Busca un trabajo por su identificador unico
    def get_job_by_id(self, db: Session, job_id):
        # Solicita al repositorio el objeto Job con todos sus detalles y pasos
        return self.repository.get_by_id(db, job_id)