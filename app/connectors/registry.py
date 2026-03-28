"""
REGISTRO DE CONECTORES (ConnectorRegistry).
Actua como un catalogo centralizado que mapea los tipos de pasos (step_type)
y los tipos de conectores (connector_type) con sus implementaciones reales.
Es el componente encargado de la resolucion de dependencias durante la ejecucion.
"""
from app.connectors.email_connector import EmailConnector
from app.connectors.filesystem_connector import FilesystemConnector
from app.connectors.calendar_connector import CalendarConnector
from app.connectors.summary_connector import SummaryConnector
from app.connectors.manual_review_handler import ManualReviewHandler


class ConnectorRegistry:
    # Inicializa y mantiene en memoria las instancias de todos los ejecutores
    def __init__(self):
        self.email_connector = EmailConnector()
        self.filesystem_connector = FilesystemConnector()
        self.calendar_connector = CalendarConnector()
        self.summary_connector = SummaryConnector()
        self.manual_review_handler = ManualReviewHandler()

    # Determina que objeto debe ejecutar la logica basandose en la definicion del paso
    def resolve(self, step_type: str, connector_type: str | None):
        # Prioridad 1: Handlers internos de procesamiento de informacion (Summary)
        if step_type in {"fetch_emails", "filter_important_emails", "generate_summary"}:
            return self.summary_connector

        # Prioridad 2: Casos especiales de seguridad o revision manual
        if step_type == "mark_for_manual_review":
            return self.manual_review_handler

        # Prioridad 3: Resolucion por tipo de tecnologia/conector externo
        if connector_type == "email":
            return self.email_connector

        if connector_type == "filesystem":
            return self.filesystem_connector

        if connector_type == "calendar":
            return self.calendar_connector

        # Si el paso no coincide con ninguna logica conocida, devuelve None
        return None