"""
SERVICIO DE MANEJO DE PASOS (StepHandlerService).
Es el ejecutor inteligente que procesa cada JobStep individualmente.
Gestiona el contexto compartido entre pasos, permitiendo que la salida de una tarea 
sirva como entrada para la siguiente, y coordina las llamadas a los conectores.
"""
from app.connectors.registry import ConnectorRegistry


class StepHandlerService:
    # Inicializa el registro para localizar los conectores necesarios
    def __init__(self):
        self.registry = ConnectorRegistry()

    # Metodo principal que ejecuta la logica de un paso basandose en su tipo y contexto
    def execute_step(self, step, context: dict) -> dict:
        step_type = step.step_type
        connector_type = step.connector_type
        input_json = step.input_json or {}

        # --- SECCION DE HANDLERS INTERNOS (Logica de transformacion rapida) ---
        
        # Genera el contenido textual del resumen diario
        if step_type == "build_summary_content":
            return {
                "success": True,
                "summary_content": "Resumen diario generado por ETAP"
            }

        # Define los correos electronicos por defecto
        if step_type == "resolve_default_recipients":
            return {
                "success": True,
                "recipients": ["direccion@empresa.local"]
            }

        # Procesa las referencias temporales del input
        if step_type == "parse_event_datetime":
            return {
                "success": True,
                "date_ref": input_json.get("date_ref"),
                "time_ref": input_json.get("time_ref")
            }

        # Prepara los datos finales para la creacion de un evento
        if step_type == "build_calendar_payload":
            return {
                "success": True,
                "title": "Reunion creada por ETAP",
                "date_ref": input_json.get("date_ref"),
                "time_ref": input_json.get("time_ref")
            }

        # Simula la obtencion de una lista de contactos completa
        if step_type == "resolve_all_contacts":
            return {
                "success": True,
                "recipients": [
                    "contacto1@empresa.local",
                    "contacto2@empresa.local",
                    "contacto3@empresa.local"
                ]
            }

        # Define la lista de carpetas para un nuevo proyecto
        if step_type == "build_project_structure_definition":
            return {
                "success": True,
                "structure": ["app", "tests", "docs", "scripts"]
            }

        # Define el nombre de una nueva automatizacion
        if step_type == "build_automation_definition":
            return {
                "success": True,
                "automation_name": "Nightly automation"
            }

        # Prepara la configuracion del programador de tareas
        if step_type == "prepare_schedule_payload":
            return {
                "success": True,
                "schedule_type": input_json.get("schedule_type", "nightly")
            }

        # Simula el registro en un cron o scheduler externo
        if step_type == "register_scheduled_task":
            return {
                "success": True,
                "message": "Scheduled task prepared but scheduler not enabled yet"
            }

        # --- SECCION DE RESOLUCION POR CONECTOR (Logica compleja o externa) ---

        # Busca el conector adecuado en el registro
        handler = self.registry.resolve(step_type=step_type, connector_type=connector_type)
        if handler is None:
            raise NotImplementedError(
                f"No existe handler para step_type={step_type} connector_type={connector_type}"
            )

        # Flujo de resumen de correos: Encadena la salida del contexto
        if step_type == "fetch_emails":
            return handler.fetch_emails()

        if step_type == "filter_important_emails":
            emails = context.get("fetch_emails", {}).get("emails", [])
            return handler.filter_important_emails(emails)

        if step_type == "generate_summary":
            emails = context.get("filter_important_emails", {}).get("important_emails", [])
            return handler.generate_summary(emails)

        # Caso especial para peticiones no entendidas por la IA
        if step_type == "mark_for_manual_review":
            return handler.handle()

        # Flujo de Email: Usa destinatarios y cuerpos resueltos en pasos anteriores
        if step_type == "send_email":
            recipients = context.get("resolve_default_recipients", {}).get("recipients", ["direccion@empresa.local"])
            body = context.get("build_summary_content", {}).get("summary_content", "Resumen por defecto")
            return handler.send_email(
                to=recipients,
                subject="Resumen diario",
                body=body
            )

        # Flujo de Email con adjuntos: Recupera la ruta del archivo del contexto de Filesystem
        if step_type == "send_email_with_attachment":
            recipients = context.get("resolve_all_contacts", {}).get("recipients", [])
            budget_data = context.get("find_budget_pdf", {})
            attachments = [budget_data.get("file_path")] if budget_data.get("file_path") else []
            return handler.send_email(
                to=recipients,
                subject="Budget actualizado",
                body="Adjunto budget actualizado",
                attachments=attachments
            )

        # Ejecucion directa para operaciones de sistema de archivos
        if connector_type == "filesystem":
            return handler.execute(step_type=step_type, input_json=input_json)

        # Ejecucion de calendario usando el payload construido previamente
        if step_type == "create_calendar_event":
            payload = context.get("build_calendar_payload", {})
            return handler.create_event(
                title=payload.get("title", "Reunion creada por ETAP"),
                date_ref=payload.get("date_ref"),
                time_ref=payload.get("time_ref")
            )

        # Error de seguridad si el flujo llega aqui sin resolucion
        raise NotImplementedError(
            f"No existe implementacion final para step_type={step_type} connector_type={connector_type}"
        )