"""
CONFIGURACION GLOBAL DEL SISTEMA (Settings).
Gestiona las variables de entorno y las conexiones a servicios externos.
Utiliza Pydantic para validar que las URLs de base de datos, Redis y Celery
sean correctas al iniciar la aplicacion.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # URL de conexion a PostgreSQL (ej: postgresql://user:pass@localhost:5432/db)
    DATABASE_URL: str

    # URL de acceso a Redis para cache o estados rapidos
    REDIS_URL: str

    # URL del Broker de Celery: Donde se envian las tareas (usualmente Redis)
    CELERY_BROKER_URL: str

    # Backend de resultados de Celery: Donde se guarda si la tarea tuvo exito
    CELERY_RESULT_BACKEND: str

    # Configuracion para leer automaticamente desde un archivo .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


# Instancia unica de configuracion para ser importada en toda la app
settings = Settings()