# REPOSITORIO PARA LA GESTION DE CONSULTAS SQL DE USUARIOS
# Encargado de las operaciones de lectura y escritura de la tabla 'users' y sus relaciones.

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.user import User


class UserRepository:
    # Crea un usuario: Añade el objeto User a la sesion de base de datos.
    def create(self, db: Session, user: User) -> User:
        db.add(user)
        # 'flush' sincroniza con la BD para generar el UUID antes de terminar la transaccion.
        db.flush()
        # 'refresh' recupera los datos actualizados desde PostgreSQL.
        db.refresh(user)
        return user

    # Busca por email: Fundamental para el proceso de Login.
    def get_by_email(self, db: Session, email: str) -> User | None:
        stmt = (
            select(User)
            # 'selectinload' realiza un JOIN inteligente para traer el Rol en la misma consulta.
            .options(selectinload(User.role))
            .where(User.email == email)
        )
        result = db.execute(stmt)
        # Devuelve el usuario si coincide el email, o None si no existe.
        return result.scalar_one_or_none()

    # Busca por id: Utilizado por el sistema de seguridad para validar el Token JWT en cada peticion.
    def get_by_id(self, db: Session, user_id) -> User | None:
        stmt = (
            select(User)
            .options(selectinload(User.role))
            .where(User.id == user_id)
        )
        result = db.execute(stmt)
        return result.scalar_one_or_none()

    # Lista usuarios: Devuelve todos los usuarios registrados ordenados por fecha de creacion.
    def list(self, db: Session) -> list[User]:
        stmt = (
            select(User)
            .options(selectinload(User.role))
            # Orden descendente para ver los ultimos registros primero.
            .order_by(User.created_at.desc())
        )
        result = db.execute(stmt)
        return list(result.scalars().all())