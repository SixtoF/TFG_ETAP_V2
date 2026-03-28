#el encargado de conectar los resultados logicos que genero Planner con la persistencia en la base de datos.
#Su trabajo es "desempaquetar" el diccionario del planificador y pasárselo al repositorio

from sqlalchemy.orm import Session

from app.repositories.intent_prediction_repository import IntentPredictionRepository


class IntentService:
    def __init__(self):
        # Inicializa el repositorio para interactuar con la tabla de predicciones
        self.repository = IntentPredictionRepository()

    # Recibe el resultado del planner y lo guarda vinculado a un comando
    def create_prediction(self, db: Session, command_id, planner_result: dict):
        # Llama al repositorio pasando cada campo extraido del diccionario 'planner_result'
        return self.repository.create(
            db=db,
            command_id=command_id,
            intent_name=planner_result["intent_name"],
            confidence=planner_result["confidence"],
            normalized_text=planner_result["normalized_text"],
            entities_json=planner_result["entities_json"],
            risk_level=planner_result["risk_level"],
            plan_json=planner_result["plan_json"]
        )