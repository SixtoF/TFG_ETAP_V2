# SERVICIO DE LOGICA DE NEGOCIO PARA LA GESTION DE USUARIOS
# Coordina la validacion, creacion y consulta de usuarios aplicando reglas de seguridad.

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.models.user import User
from app.repositories.role_repository import RoleRepository
from app.repositories.user_repository import UserRepository


class UserService:
    # Inicializa el servicio conectandolo con los repositorios necesarios.
    def __init__(self):
        self.user_repository = UserRepository()
        self.role_repository = RoleRepository()

    # Crea usuario nuevo: Valida duplicados, busca el rol y aplica seguridad a la clave.
    def create_user(self, db: Session, email: str, password: str, full_name: str, role_name: str):
        # 1. Validacion: Comprueba si el email ya esta registrado para evitar duplicados.
        existing_user = self.user_repository.get_by_email(db, email)
        if existing_user:
            raise ValueError("Ya existe un usuario con ese email")

        # 2. Validacion: Verifica que el rol solicitado (ej. 'admin') exista en el sistema.
        role = self.role_repository.get_by_name(db, role_name)
        if not role:
            raise ValueError("El rol indicado no existe")

        # 3. Construccion del objeto: Se implementa 'hash_password' para proteger la clave real.
        user = User(
            email=email,
            password_hash=hash_password(password), # La clave se guarda encriptada
            full_name=full_name,
            is_active=True,
            role_id=role.id
        )

        # 4. Persistencia: Guarda el usuario y confirma la transaccion en la base de datos.
        self.user_repository.create(db, user)
        db.commit()
        
        # 5. Respuesta: Devuelve el usuario recien creado con su ID y Rol cargados.
        return self.user_repository.get_by_id(db, user.id)

    # Lista usuarios: Accede al repositorio para devolver todos los usuarios registrados.
    def list_users(self, db: Session):
        return self.user_repository.list(db)

    # Busca usuario por id: Util para consultas de perfiles especificos.
    def get_user_by_id(self, db: Session, user_id):
        return self.user_repository.get_by_id(db, user_id)