"""
REPOSITORIO DE PASOS DE TRABAJO (JobStepRepository).
Maneja la persistencia detallada de cada tarea individual (step) dentro de un Job.
Permite registrar el orden, el tipo de conector y los datos de entrada para la ejecucion.
"""

from sqlalchemy.orm import Session

from app.models.job_step import JobStep


class JobStepRepository:
    # Crea un registro individual para un paso (step) del trabajo en la base de datos
    def create(
        self,
        db: Session,
        job_id,
        step_order: int,
        name: str,
        step_type: str,
        connector_type: str | None,
        input_json: dict,
        status: str = "pending"
    ) -> JobStep:
        # Instancia el modelo JobStep con los datos de ejecucion y configuracion
        step = JobStep(
            job_id=job_id,
            step_order=step_order,
            name=name,
            step_type=step_type,
            connector_type=connector_type,
            input_json=input_json,
            status=status
        )
        # Registra el objeto en la sesion actual
        db.add(step)
        # Sincroniza con la base de datos para obtener IDs pero sin cerrar la transaccion
        db.flush()
        # Refresca el objeto para asegurar que tiene todos los datos generados por la DB
        db.refresh(step)
        return step