# REPOSITORIO PARA LA GESTION DE CONSULTAS SQL DE ROLES
# Centraliza todas las operaciones de lectura y escritura para los niveles de acceso.

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role


class RoleRepository:
    # Crea un nuevo rol en la base de datos: Recibe el nombre (ej. 'admin') y una descripcion.
    def create(self, db: Session, name: str, description: str | None = None) -> Role:
        role = Role(name=name, description=description)
        db.add(role)
        # 'flush' envia el cambio a la base de datos para generar el ID, pero sin finalizar la transaccion.
        db.flush()
        # 'refresh' actualiza el objeto con los datos generados por la BD (como el ID y la fecha).
        db.refresh(role)
        return role

    # Devuelve rol por nombre: Se implementa para verificar si un rol existe antes de asignar un usuario.
    def get_by_name(self, db: Session, name: str) -> Role | None:
        # Crea la sentencia SELECT filtrando por la columna 'name'.
        stmt = select(Role).where(Role.name == name)
        result = db.execute(stmt)
        # 'scalar_one_or_none' devuelve el objeto si existe, o None si no se encuentra nada.
        return result.scalar_one_or_none()

    # Lista roles: Devuelve todos los roles registrados ordenados alfabeticamente de la A a la Z.
    def list(self, db: Session) -> list[Role]:
        stmt = select(Role).order_by(Role.name.asc())
        result = db.execute(stmt)
        # Convierte el resultado en una lista de objetos Python manejables.
        return list(result.scalars().all())