"""
CONECTOR DE RESUMENES (SummaryConnector).
Simula la capacidad de lectura, filtrado y sintesis de informacion de correos.
Este conector demuestra como el sistema puede procesar datos complejos antes de 
generar una respuesta o una accion final.
"""

class SummaryConnector:
    # Simula la conexion a un servidor de correo para obtener una lista de mensajes
    def fetch_emails(self) -> dict:
        # Lista estatica de prueba que emula mensajes reales en una bandeja de entrada
        emails = [
            {"subject": "Urgente: presupuesto", "important": True},
            {"subject": "Recordatorio de reunion", "important": True},
            {"subject": "Newsletter", "important": False}
        ]
        return {"success": True, "emails": emails}

    # Recibe una lista de correos y devuelve solo aquellos marcados como relevantes
    def filter_important_emails(self, emails: list[dict]) -> dict:
        # Logica de filtrado basada en el campo booleano 'important'
        important = [email for email in emails if email.get("important") is True]
        return {"success": True, "important_emails": important}

    # Toma los asuntos de los correos y los concatena para crear un resumen legible
    def generate_summary(self, emails: list[dict]) -> dict:
        # Extrae solo el titulo de cada mensaje para la sintesis
        subjects = [email.get("subject", "Sin asunto") for email in emails]
        # Crea la cadena de texto final del resumen
        summary = "Resumen de correos importantes: " + "; ".join(subjects) if subjects else "No hay correos importantes"
        return {"success": True, "summary": summary}