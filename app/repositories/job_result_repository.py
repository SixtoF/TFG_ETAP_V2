"""
REPOSITORIO DE RESULTADOS DE TRABAJO (JobResultRepository).
Gestiona el desenlace final de los trabajos. Utiliza una logica de 'upsert'
para asegurar que cada Job tenga un unico registro de resultado definitivo.
"""
from sqlalchemy.orm import Session

from app.models.job_result import JobResult


class JobResultRepository:
    # Crea un resultado o lo actualiza si ya existe para ese job_id
    def upsert(
        self,
        db: Session,
        job_id,
        success: bool,
        summary: str | None = None,
        result_json: dict | None = None
    ) -> JobResult:
        # Busca si ya existe un resultado previo para este trabajo
        existing = db.query(JobResult).filter(JobResult.job_id == job_id).one_or_none()

        # Si existe, actualizamos los campos con la nueva informacion
        if existing:
            existing.success = success
            existing.summary = summary
            existing.result_json = result_json
            db.add(existing)
            db.flush() # Sincroniza cambios sin cerrar la transaccion
            db.refresh(existing)
            return existing

        # Si no existe, creamos un registro nuevo desde cero
        job_result = JobResult(
            job_id=job_id,
            success=success,
            summary=summary,
            result_json=result_json
        )
        db.add(job_result)
        db.flush() # Sincroniza para obtener el ID y datos por defecto
        db.refresh(job_result)
        return job_result