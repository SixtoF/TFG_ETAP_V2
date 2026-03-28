"""
REPOSITORIO DE TAREAS PROGRAMADAS (Acceso a Datos).
Encapsula todas las consultas a la base de datos relacionadas con ScheduledTask.
Centraliza el uso de SQLAlchemy para mantener limpio el resto del codigo.
Este componente es esencial para que los servicios consulten tareas vencidas
o registren nuevas automatizaciones en PostgreSQL.
"""
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.scheduled_task import ScheduledTask


class ScheduledTaskRepository:
    # Crea una tarea programada
    def create(
        self,
        db: Session,
        name: str,
        description: str | None,
        command_text: str,
        cron_expression: str,
        timezone: str,
        auto_enqueue: bool,
        next_run_at: datetime
    ) -> ScheduledTask:
        # Instancia el modelo con los parametros recibidos para guardarlos en la base de datos
        scheduled_task = ScheduledTask(
            name=name,
            description=description,
            command_text=command_text,
            cron_expression=cron_expression,
            timezone=timezone,
            auto_enqueue=auto_enqueue,
            is_active=True,
            next_run_at=next_run_at
        )
        db.add(scheduled_task)
        # flush envia los cambios a la base de datos sin finalizar la transaccion
        db.flush()
        # Actualiza el objeto con los datos generados por el motor de base de datos
        db.refresh(scheduled_task)
        return scheduled_task

    # Lista tareas programadas
    def list_scheduled_tasks(self, db: Session, limit: int = 50, offset: int = 0) -> list[ScheduledTask]:
        # Ejecuta la consulta para obtener un listado paginado ordenado por creacion
        stmt = (
            select(ScheduledTask)
            .order_by(ScheduledTask.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        result = db.execute(stmt)
        # Retorna los resultados escalares como una lista de Python
        return list(result.scalars().all())

    # Devuelve tarea por id
    def get_by_id(self, db: Session, scheduled_task_id) -> ScheduledTask | None:
        # Busca un registro unico por su identificador UUID
        stmt = select(ScheduledTask).where(ScheduledTask.id == scheduled_task_id)
        result = db.execute(stmt)
        # Devuelve el objeto encontrado o None si no existe en Postgres
        return result.scalar_one_or_none()

    # Devuelve tareas activas vencidas
    def get_due_tasks(self, db: Session, now_dt: datetime) -> list[ScheduledTask]:
        # Selecciona tareas que deben ejecutarse basandose en la marca de tiempo actual
        stmt = (
            select(ScheduledTask)
            .where(ScheduledTask.is_active.is_(True))
            .where(ScheduledTask.next_run_at <= now_dt)
            .order_by(ScheduledTask.next_run_at.asc())
        )
        result = db.execute(stmt)
        # Retorna las tareas que el planificador debe despachar de inmediato
        return list(result.scalars().all())

    # Persiste cambios
    def save(self, db: Session, scheduled_task: ScheduledTask) -> ScheduledTask:
        # Metodo para actualizar registros existentes en la base de datos
        db.add(scheduled_task)
        db.flush()
        db.refresh(scheduled_task)
        return scheduled_task