"""
Configuracion del entorno de migraciones de Alembic.
Este script orquestra la conexion entre SQLAlchemy y Alembic, permitiendo la 
deteccion automatica de cambios en los modelos y su aplicacion en la base de datos.
"""
from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool
from alembic import context

from app.core.config import settings
from app.db.base import Base

# --- REGISTRO DE MODELOS ---
# Importa todos los modelos para registrar metadata en la clase Base.
# El comentario # noqa: F401 evita avisos de importaciones no utilizadas.
from app.models.command import Command  # noqa: F401
from app.models.intent_prediction import IntentPrediction  # noqa: F401
from app.models.job import Job  # noqa: F401
from app.models.job_step import JobStep  # noqa: F401
from app.models.execution_log import ExecutionLog  # noqa: F401
from app.models.job_result import JobResult  # noqa: F401
from app.models.approval import Approval  # noqa: F401
from app.models.scheduled_task import ScheduledTask  # noqa: F401
from app.models.role import Role  # noqa: F401
from app.models.user import User  # noqa: F401

# Objeto de configuracion de Alembic que accede a los valores del archivo .ini
config = context.config

# Sobrescribe la URL con la configuracion real del proyecto desde las variables de entorno
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Configura el sistema de registro de eventos (logging)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata objetivo que contiene la definicion de todas las tablas
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Ejecuta migraciones en modo 'offline'.
    Configura el contexto mediante una URL en lugar de una conexion activa.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True, # Permite detectar cambios en tipos de datos de columnas
        compare_server_default=True, # Permite detectar cambios en valores por defecto
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Ejecuta migraciones en modo 'online'.
    Crea un motor de conexion (Engine) y aplica los cambios directamente.
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True, # Sincroniza tipos de datos entre Python y SQL
            compare_server_default=True, # Sincroniza valores por defecto del servidor
        )

        # Inicia una transaccion de base de datos para asegurar la consistencia
        with context.begin_transaction():
            context.run_migrations()


# Punto de entrada para decidir el modo de ejecucion segun los argumentos del comando
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()