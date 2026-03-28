"""
REPOSITORIO DE LOGS DE EJECUCION (ExecutionLogRepository).
Proporciona los metodos necesarios para registrar eventos en la base de datos
y recuperar el historial de ejecucion de un trabajo especifico.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.execution_log import ExecutionLog


class ExecutionLogRepository:
    # Inserta un nuevo registro de log vinculado a un Job y opcionalmente a un Step
    def create(
        self,
        db: Session,
        job_id,
        level: str,
        message: str,
        details_json: dict | None = None,
        job_step_id=None
    ) -> ExecutionLog:
        # Crea la instancia del modelo con los datos del evento
        log = ExecutionLog(
            job_id=job_id,
            job_step_id=job_step_id,
            level=level,
            message=message,
            details_json=details_json
        )
        # Agrega el log a la sesion y sincroniza con la base de datos
        db.add(log)
        db.flush() # Permite obtener el ID generado sin finalizar la transaccion
        db.refresh(log)
        return log

    # Recupera todos los logs de un Job ordenados por tiempo para ver la secuencia real
    def list_by_job_id(self, db: Session, job_id) -> list[ExecutionLog]:
        # Prepara la consulta filtrando por el ID del trabajo
        stmt = (
            select(ExecutionLog)
            .where(ExecutionLog.job_id == job_id)
            # Ordena primero por fecha y luego por ID para no perder el orden exacto
            .order_by(ExecutionLog.created_at.asc(), ExecutionLog.id.asc())
        )
        # Ejecuta la sentencia y devuelve la lista de resultados
        result = db.execute(stmt)
        return list(result.scalars().all())