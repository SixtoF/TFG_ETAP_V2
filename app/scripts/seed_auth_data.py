# ==============================================================================
# SCRIPT DE INICIALIZACION DE DATOS DE AUTENTICACION Y ROLES (SEEDING)
# Este script puebla la base de datos con los roles basicos y el administrador
# inicial necesario para el primer acceso al sistema ETAP.
# = ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: : =
# Instrucciones de ejecucion:
#en local: python -m app.scripts.seed_auth_data
# Docker: docker compose exec api python -m app.scripts.seed_auth_data
# ==============================================================================

from app.db.session import SessionLocal
from app.core.security import hash_password
from app.models.role import Role
from app.models.user import User


def seed_roles_and_admin():
    # Se abre una sesion local con la base de datos de PostgreSQL
    db = SessionLocal()

    try:
        # Definicion de los roles base del sistema segun la logica de negocio
        roles_to_create = [
            {"name": "admin", "description": "Acceso total al sistema"},
            {"name": "operator", "description": "Puede operar jobs pero no administrar seguridad"},
            {"name": "viewer", "description": "Solo lectura"},
        ]

        # Obtenemos los roles que ya existen para evitar duplicados (idempotencia)
        existing_roles = {role.name: role for role in db.query(Role).all()}

        for role_data in roles_to_create:
            # Si el rol no esta en la base de datos, lo creamos
            if role_data["name"] not in existing_roles:
                role = Role(
                    name=role_data["name"],
                    description=role_data["description"]
                )
                db.add(role)

        # Confirmamos la creacion de roles para que esten disponibles para el usuario
        db.commit()

        # Recuperamos el objeto del rol 'admin' para obtener su ID unico (UUID)
        admin_role = db.query(Role).filter(Role.name == "admin").one()

        # Definimos las credenciales del administrador inicial
        # NOTA: Se recomienda cambiar el .local por .com en produccion/pruebas reales
        admin_email = "admin@etap.com"
        
        # Verificamos si el usuario ya existe para no intentar recrearlo
        existing_admin = db.query(User).filter(User.email == admin_email).one_or_none()

        if not existing_admin:
            # Creamos la instancia del usuario vinculandola al ID del rol administrador
            admin_user = User(
                email=admin_email,
                # La contraseña se guarda HASHEADA, nunca en texto plano
                password_hash=hash_password("Admin1234"),
                full_name="Administrador ETAP",
                is_active=True,
                role_id=admin_role.id
            )
            db.add(admin_user)
            db.commit()
            print(f"Admin inicial creado: {admin_email} / Admin1234")
        else:
            print("El admin inicial ya existe en la base de datos")

        print("Seed de roles y admin completado correctamente")

    except Exception as exc:
        # En caso de error, se deshacen los cambios para mantener la integridad
        db.rollback()
        print(f"Error durante el seeding: {exc}")
        raise exc
    finally:
        # Es vital cerrar la conexion para no saturar el pool de PostgreSQL
        db.close()


if __name__ == "__main__":
    seed_roles_and_admin()