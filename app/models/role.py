# MODELO DE BASE DE DATOS PARA GESTION DE ROLES DE USUARIO (RBAC)
# Este modelo define los niveles de acceso (admin, operator, viewer) para la seguridad del sistema.

import uuid
from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Role(Base):
    # Nombre de la tabla en PostgreSQL
    __tablename__ = "roles"

    # ID unico del rol: Se implementa como UUID para mayor seguridad y evitar predicciones de IDs.
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Nombre interno del rol: 'unique=True' impide que existan dos roles con el mismo nombre (ej. dos 'admin').
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    # Descripcion opcional: Permite anotar para que sirve cada rol en el panel de administracion.
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Fecha de creacion: Registra automaticamente cuando se dio de alta el rol en el sistema.
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    # Relacion con usuarios: Implementa una relacion 1:N (un rol puede tener muchos usuarios).
    # 'back_populates' conecta este modelo con el atributo 'role' que crearemos en el modelo User.
    users = relationship("User", back_populates="role")