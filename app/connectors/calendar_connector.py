"""
CONECTOR DE CALENDARIO (CalendarConnector).
Gestiona la programacion de eventos y reuniones.
En esta fase funciona en modo 'mock' (simulado), permitiendo validar
que las entidades de tiempo extraidas por la IA se procesan correctamente.
"""
from app.connectors.base import BaseConnector


class CalendarConnector(BaseConnector):
    # Punto de entrada que canaliza la ejecucion hacia acciones de calendario
    def execute(self, step_type: str, input_json: dict) -> dict:
        # Caso unico: Creacion de un nuevo evento en la agenda
        if step_type == "create_calendar_event":
            return self.create_event(
                title=input_json.get("title", "Reunion creada por ETAP"),
                date_ref=input_json.get("date_ref"),
                time_ref=input_json.get("time_ref")
            )

        # Lanza error si el motor de ejecucion solicita una accion no implementada
        raise NotImplementedError(f"Step type no soportado por CalendarConnector: {step_type}")

    # Simula la interaccion con una API de calendario (como Google Calendar o Outlook)
    # Devuelve los datos que confirman que la reunion se habria agendado con exito
    def create_event(self, title: str, date_ref: str | None, time_ref: str | None) -> dict:
        return {
            "success": True,
            "event_id": "mock-event-001",
            "title": title,
            "date_ref": date_ref,
            "time_ref": time_ref
        }