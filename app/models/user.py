# MODELO DE BASE DE DATOS PARA GESTION DE USUARIOS AUTENTICADOS
# Este modelo almacena la identidad de los operadores y administradores de la ETAP.

import uuid
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    # Nombre de la tabla fisica en PostgreSQL
    __tablename__ = "users"

    # ID unico del usuario: Se genera automaticamente como UUID v4.
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Email unico para login: 'index=True' agiliza la busqueda durante el inicio de sesion.
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)

    # Password hasheada: Se implementa para no guardar la clave real; se guarda el hash generado por passlib.
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    # Nombre visible del usuario: Almacena el nombre completo (ej. 'Juan Perez') para logs y auditorias.
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Usuario activo o no: Permite banear o suspender cuentas sin borrar sus registros historicos.
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # FK al rol: Clave foranea que conecta con la tabla 'roles'. 
    # 'ondelete="RESTRICT"' impide borrar un rol si todavia tiene usuarios asignados.
    role_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="RESTRICT"),
        nullable=False
    )

    # Fechas de control: 'created_at' para registro inicial y 'updated_at' se actualiza solo en cada cambio.
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacion con rol: Permite acceder al objeto Role completo desde el usuario (ej. user.role.name).
    role = relationship("Role", back_populates="users")