"""
CONECTOR DE EMAIL (EmailConnector).
Implementa la logica de envio de correos electronicos.
En esta fase funciona en modo 'mock' (simulado) para facilitar las pruebas
de integracion sin depender de servicios externos de correo.
"""
from app.connectors.base import BaseConnector


class EmailConnector(BaseConnector):
    # Punto de entrada principal que redirige la ejecucion segun el tipo de paso
    def execute(self, step_type: str, input_json: dict) -> dict:
        # Caso 1: Envio de un correo estandar de texto
        if step_type == "send_email":
            return self.send_email(
                to=input_json.get("to", ["direccion@empresa.local"]),
                subject=input_json.get("subject", "Resumen diario"),
                body=input_json.get("body", "Resumen generado por ETAP")
            )

        # Caso 2: Envio de un correo que incluye archivos adjuntos (como el PDF del budget)
        if step_type == "send_email_with_attachment":
            return self.send_email(
                to=input_json.get("to", ["contactos@empresa.local"]),
                subject=input_json.get("subject", "Budget actualizado"),
                body=input_json.get("body", "Adjunto budget actualizado"),
                attachments=input_json.get("attachments", ["budget.pdf"])
            )

        # Si el motor de ejecucion pide algo que este conector no sabe hacer
        raise NotImplementedError(f"Step type no soportado por EmailConnector: {step_type}")

    # Metodo interno que simula la operacion final de envio
    # Devuelve un diccionario con el resultado para que el motor de logs lo registre
    def send_email(self, to, subject: str, body: str, attachments: list[str] | None = None) -> dict:
        return {
            "success": True,
            "message": "Email processed in mock mode",
            "sent_to": to if isinstance(to, list) else [to],
            "subject": subject,
            "attachments": attachments or []
        }