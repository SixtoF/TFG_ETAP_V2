"""
CONECTOR DE SISTEMA DE ARCHIVOS (FilesystemConnector).
Gestiona todas las operaciones locales de lectura y escritura en disco.
Permite la creacion de estructuras de proyectos, busqueda de documentos 
y persistencia temporal de archivos generados por el sistema.
"""
from pathlib import Path

from app.connectors.base import BaseConnector


class FilesystemConnector(BaseConnector):
    # Directorio base donde se realizaran todas las operaciones para evitar dispersión
    BASE_PATH = Path("runtime_data")

    def __init__(self):
        # Asegura que la carpeta base existe al inicializar el conector
        self.BASE_PATH.mkdir(exist_ok=True)

    # Punto de entrada que canaliza la ejecucion segun la accion requerida
    def execute(self, step_type: str, input_json: dict) -> dict:
        # Busca un archivo especifico (util para el flujo de envio de budget)
        if step_type == "find_budget_pdf":
            return self.find_budget_pdf()

        # Genera la estructura de carpetas de un nuevo proyecto
        if step_type == "create_directories":
            return self.create_directories(input_json)

        # Crea los archivos iniciales con contenido predefinido
        if step_type == "create_base_files":
            return self.create_base_files(input_json)

        # Lanza error si el motor de ejecucion solicita una accion no programada
        raise NotImplementedError(f"Step type no soportado por FilesystemConnector: {step_type}")

    # Simula la localizacion de un documento; si no existe, lo genera como mock
    def find_budget_pdf(self) -> dict:
        budget_path = self.BASE_PATH / "budget.pdf"

        if not budget_path.exists():
            budget_path.write_text("Mock budget PDF content", encoding="utf-8")

        return {
            "success": True,
            "file_path": str(budget_path),
            "filename": budget_path.name
        }

    # Crea el andamiaje de directorios para un proyecto estandar
    def create_directories(self, input_json: dict) -> dict:
        project_root = self.BASE_PATH / "generated_project"
        dirs = ["app", "tests", "docs", "scripts"]

        created_paths = []
        for directory in dirs:
            path = project_root / directory
            # parents=True crea carpetas intermedias si es necesario
            path.mkdir(parents=True, exist_ok=True)
            created_paths.append(str(path))

        return {
            "success": True,
            "created_paths": created_paths
        }

    # Genera archivos fisicos con contenido base (README, gitignore, main)
    def create_base_files(self, input_json: dict) -> dict:
        project_root = self.BASE_PATH / "generated_project"
        files = {
            "README.md": "# Proyecto generado por ETAP\n",
            ".gitignore": "__pycache__/\n.venv/\n",
            "app/main.py": 'print("Hola ETAP")\n'
        }

        created_files = []
        for relative_path, content in files.items():
            full_path = project_root / relative_path
            # Asegura que la carpeta contenedora existe antes de escribir el archivo
            full_path.parent.mkdir(parents=True, exist_ok=True)
            full_path.write_text(content, encoding="utf-8")
            created_files.append(str(full_path))

        return {
            "success": True,
            "created_files": created_files
        }