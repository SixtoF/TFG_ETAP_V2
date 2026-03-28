"""
Repositorio de Predicciones de Intencion (IntentPredictionRepository).
Se encarga de las operaciones directas de lectura y escritura en la tabla 
de predicciones usando SQLAlchemy.
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.intent_prediction import IntentPrediction

class IntentPredictionRepository:
    # Crea una prediccion asociada a un command en la base de datos
    def create(
        self,
        db: Session,
        command_id,
        intent_name: str,
        confidence: float,
        normalized_text: str,
        entities_json: dict,
        risk_level: str,
        plan_json: dict
    ) -> IntentPrediction:
        # Prepara el objeto con los datos recibidos
        prediction = IntentPrediction(
            command_id=command_id,
            intent_name=intent_name,
            confidence=confidence,
            normalized_text=normalized_text,
            entities_json=entities_json,
            risk_level=risk_level,
            plan_json=plan_json
        )
        # Agrega el objeto a la sesion de la base de datos
        db.add(prediction)
        # flush() envia los datos a la DB pero sin cerrar la transaccion
        db.flush()
        # Actualiza el objeto con datos generados por la DB (como el ID o fechas)
        db.refresh(prediction)
        return prediction

    # Busca y devuelve una prediccion usando el ID del comando original
    def get_by_command_id(self, db: Session, command_id):
        # Prepara la sentencia de seleccion (SELECT * FROM ...)
        stmt = select(IntentPrediction).where(IntentPrediction.command_id == command_id)
        # Ejecuta la consulta
        result = db.execute(stmt)
        # Devuelve el resultado o None si no encuentra nada
        return result.scalar_one_or_none()