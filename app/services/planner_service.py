"""
Servicio Planificador (PlannerService).
Se encarga de interpretar el lenguaje natural, detectar la intencion del usuario,
extraer datos clave y generar el plan de pasos (steps) a seguir.
"""

import re
import unicodedata


class PlannerService:
    # Limpia y normaliza el texto para que las reglas coincidan mejor
    def normalize_text(self, raw_text: str) -> str:
        # Quita espacios laterales y pasa todo a minusculas
        text = raw_text.strip().lower()
        # Elimina acentos y caracteres especiales mediante normalizacion NFD
        text = unicodedata.normalize("NFD", text)
        text = "".join(char for char in text if unicodedata.category(char) != "Mn")
        # Sustituye multiples espacios o tabulaciones por uno solo
        text = re.sub(r"\s+", " ", text)
        return text

    # Metodo principal que orquestra la interpretacion del comando
    def plan(self, raw_text: str) -> dict:
        normalized_text = self.normalize_text(raw_text)

        # Identifica la intencion, confianza, entidades, riesgo y genera los pasos
        intent_name = self._detect_intent(normalized_text)
        confidence = self._calculate_confidence(intent_name)
        entities = self._extract_entities(intent_name, normalized_text)
        risk_level = self._calculate_risk(intent_name)
        plan_json = self._build_plan(intent_name, entities)

        # Devuelve el diccionario completo para ser guardado en base de datos
        return {
            "intent_name": intent_name,
            "confidence": confidence,
            "normalized_text": normalized_text,
            "entities_json": entities,
            "risk_level": risk_level,
            "plan_json": plan_json
        }

    # Motor de reglas basado en palabras clave para clasificar el texto
    def _detect_intent(self, text: str) -> str:
        # Caso: Enviar email de resumen diario
        if self._contains_all(text, ["envia", "email", "diario", "resumen"]) or \
           self._contains_all(text, ["envia", "correo", "diario", "resumen"]):
            return "send_daily_summary_email"

        # Caso: Resumir correos marcados como importantes
        if self._contains_all(text, ["resume", "correos", "importantes"]) or \
           self._contains_all(text, ["resume", "emails", "importantes"]):
            return "summarize_important_emails"

        # Caso: Crear evento en el calendario
        if self._contains_all(text, ["agrega", "reunion", "calendario"]) or \
           self._contains_all(text, ["anade", "reunion", "calendario"]):
            return "create_calendar_event"

        # Caso critico: Enviar presupuesto PDF a toda la lista de contactos
        if self._contains_all(text, ["manda", "pdf", "budget", "todos los contactos"]) or \
           self._contains_all(text, ["envia", "pdf", "budget", "todos los contactos"]):
            return "send_budget_pdf_to_all_contacts"

        # Caso: Crear carpetas y archivos base de un proyecto
        if self._contains_all(text, ["crea", "estructura", "proyecto"]):
            return "create_project_structure"

        # Caso: Configurar tareas automaticas para la noche
        if self._contains_all(text, ["prepara", "automatizacion", "nocturna"]):
            return "prepare_nightly_automation"

        # Si no coincide con ninguna regla anterior
        return "unknown"

    # Asigna un puntaje de seguridad segun si se reconocio la intencion o no
    def _calculate_confidence(self, intent_name: str) -> float:
        if intent_name == "unknown":
            return 0.20
        return 0.95

    # Clasifica el nivel de riesgo para decidir si requiere aprobacion humana
    def _calculate_risk(self, intent_name: str) -> str:
        # Acciones masivas externas se consideran de alto riesgo
        if intent_name == "send_budget_pdf_to_all_contacts":
            return "high"
        # Acciones de comunicacion o agenda se consideran riesgo medio
        if intent_name in {"send_daily_summary_email", "create_calendar_event", "prepare_nightly_automation"}:
            return "medium"
        # Por defecto o desconocido
        if intent_name == "unknown":
            return "unknown"
        return "low"

    # Extrae parametros especificos del texto segun la intencion detectada
    def _extract_entities(self, intent_name: str, text: str) -> dict:
        entities = {}

        # Busca referencias temporales para el calendario
        if intent_name == "create_calendar_event":
            entities["date_ref"] = "tomorrow" if "manana" in text else None
            entities["time_ref"] = self._extract_time(text)

        # Define detalles para el envio masivo de PDF
        if intent_name == "send_budget_pdf_to_all_contacts":
            entities["target_group"] = "all_contacts"
            entities["attachment_type"] = "pdf"
            entities["document_type"] = "budget"

        # Define el tipo de proyecto para la creacion de archivos
        if intent_name == "create_project_structure":
            entities["project_type"] = "software_project"

        # Define el horario para la automatizacion
        if intent_name == "prepare_nightly_automation":
            entities["schedule_type"] = "nightly"

        return entities

    # Define la secuencia de pasos (steps) que conforman la ejecucion del trabajo
    def _build_plan(self, intent_name: str, entities: dict) -> dict:
        plan_map = {
            "send_daily_summary_email": {
                "job_type": "communication",
                "steps": [
                    {
                        "step_order": 1,
                        "name": "Build summary content",
                        "step_type": "build_summary_content",
                        "connector_type": None,
                        "input_json": {}
                    },
                    {
                        "step_order": 2,
                        "name": "Resolve default recipients",
                        "step_type": "resolve_default_recipients",
                        "connector_type": None,
                        "input_json": {}
                    },
                    {
                        "step_order": 3,
                        "name": "Send email",
                        "step_type": "send_email",
                        "connector_type": "email",
                        "input_json": {}
                    }
                ]
            },
            "summarize_important_emails": {
                "job_type": "analysis",
                "steps": [
                    {
                        "step_order": 1,
                        "name": "Fetch emails",
                        "step_type": "fetch_emails",
                        "connector_type": "email",
                        "input_json": {}
                    },
                    {
                        "step_order": 2,
                        "name": "Filter important emails",
                        "step_type": "filter_important_emails",
                        "connector_type": None,
                        "input_json": {}
                    },
                    {
                        "step_order": 3,
                        "name": "Generate summary",
                        "step_type": "generate_summary",
                        "connector_type": None,
                        "input_json": {}
                    }
                ]
            },
            "create_calendar_event": {
                "job_type": "calendar",
                "steps": [
                    {
                        "step_order": 1,
                        "name": "Parse event datetime",
                        "step_type": "parse_event_datetime",
                        "connector_type": None,
                        "input_json": entities
                    },
                    {
                        "step_order": 2,
                        "name": "Build calendar payload",
                        "step_type": "build_calendar_payload",
                        "connector_type": None,
                        "input_json": entities
                    },
                    {
                        "step_order": 3,
                        "name": "Create calendar event",
                        "step_type": "create_calendar_event",
                        "connector_type": "calendar",
                        "input_json": entities
                    }
                ]
            },
            "send_budget_pdf_to_all_contacts": {
                "job_type": "communication",
                "steps": [
                    {
                        "step_order": 1,
                        "name": "Find budget PDF",
                        "step_type": "find_budget_pdf",
                        "connector_type": "filesystem",
                        "input_json": entities
                    },
                    {
                        "step_order": 2,
                        "name": "Resolve all contacts",
                        "step_type": "resolve_all_contacts",
                        "connector_type": None,
                        "input_json": entities
                    },
                    {
                        "step_order": 3,
                        "name": "Send email with attachment",
                        "step_type": "send_email_with_attachment",
                        "connector_type": "email",
                        "input_json": entities
                    }
                ]
            },
            "create_project_structure": {
                "job_type": "filesystem",
                "steps": [
                    {
                        "step_order": 1,
                        "name": "Build project structure definition",
                        "step_type": "build_project_structure_definition",
                        "connector_type": None,
                        "input_json": entities
                    },
                    {
                        "step_order": 2,
                        "name": "Create directories",
                        "step_type": "create_directories",
                        "connector_type": "filesystem",
                        "input_json": entities
                    },
                    {
                        "step_order": 3,
                        "name": "Create base files",
                        "step_type": "create_base_files",
                        "connector_type": "filesystem",
                        "input_json": entities
                    }
                ]
            },
            "prepare_nightly_automation": {
                "job_type": "scheduler",
                "steps": [
                    {
                        "step_order": 1,
                        "name": "Build automation definition",
                        "step_type": "build_automation_definition",
                        "connector_type": None,
                        "input_json": entities
                    },
                    {
                        "step_order": 2,
                        "name": "Prepare schedule payload",
                        "step_type": "prepare_schedule_payload",
                        "connector_type": None,
                        "input_json": entities
                    },
                    {
                        "step_order": 3,
                        "name": "Register scheduled task",
                        "step_type": "register_scheduled_task",
                        "connector_type": "scheduler",
                        "input_json": entities
                    }
                ]
            },
            "unknown": {
                "job_type": "manual_review",
                "steps": [
                    {
                        "step_order": 1,
                        "name": "Mark for manual review",
                        "step_type": "mark_for_manual_review",
                        "connector_type": None,
                        "input_json": {}
                    }
                ]
            }
        }

        return plan_map[intent_name]

    # Verifica si todas las palabras clave requeridas estan presentes en el texto
    def _contains_all(self, text: str, terms: list[str]) -> bool:
        return all(term in text for term in terms)

    # Busca patrones numericos de hora (como 10 o 14:30) usando expresiones regulares
    def _extract_time(self, text: str) -> str | None:
        match = re.search(r"\b(\d{1,2}(?::\d{2})?)\b", text)
        return match.group(1) if match else None