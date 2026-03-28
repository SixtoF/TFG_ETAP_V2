#el motor que transforma el plan de la IA en tareas reales. 
#Su trabajo es crear el "contenedor" principal (el Job) y luego generar uno por uno todos los pasos (steps) que el sistema debe ejecutar

from sqlalchemy.orm import Session

from app.repositories.job_repository import JobRepository
from app.repositories.job_step_repository import JobStepRepository


class JobService:
    def __init__(self):
        # Inicializa los repositorios para manejar trabajos y sus pasos
        self.job_repository = JobRepository()
        self.job_step_repository = JobStepRepository()

    # Crea la estructura completa de ejecucion basada en la prediccion de la IA
    def create_job_from_prediction(self, db: Session, command_id, prediction):
        # 1. Creamos el registro del Job principal vinculado al comando
        job = self.job_repository.create(
            db=db,
            command_id=command_id,
            intent_name=prediction.intent_name,
            risk_level=prediction.risk_level,
            status="created"
        )

        # 2. Extraemos la lista de pasos del plan generado por el Planner
        steps = prediction.plan_json.get("steps", [])
        
        # 3. Recorremos cada paso y lo guardamos en la base de datos
        for step in steps:
            self.job_step_repository.create(
                db=db,
                job_id=job.id, # Vinculamos el paso al Job que acabamos de crear
                step_order=step["step_order"],
                name=step["name"],
                step_type=step["step_type"],
                connector_type=step.get("connector_type"),
                input_json=step.get("input_json", {}),
                status="pending" # Todos los pasos nacen en estado pendiente
            )

        # 4. Actualizamos el objeto Job para que reconozca sus nuevos pasos (steps)
        db.refresh(job)
        
        # Devolvemos el Job completo usando el repositorio para asegurar que incluya los pasos
        return self.job_repository.get_by_id(db, job.id)