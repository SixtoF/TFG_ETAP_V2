# SERVICIO DE AUTENTICACION Y CONTROL DE ACCESO
# Gestiona el proceso de login y la generacion de credenciales temporales (JWT).

from sqlalchemy.orm import Session

from app.core.jwt import create_access_token
from app.core.security import verify_password
from app.repositories.user_repository import UserRepository


class AuthService:
    # Inicializa el servicio conectandolo con el repositorio de usuarios.
    def __init__(self):
        self.user_repository = UserRepository()

    # Hace login y devuelve token: Verifica identidad y estado del usuario.
    def login(self, db: Session, email: str, password: str) -> str:
        # 1. Busqueda: Intenta localizar al usuario por su correo electronico.
        user = self.user_repository.get_by_email(db, email)
        
        # 2. Validacion de existencia: Si no existe, lanza error de credenciales.
        # Nota: Se usa el mismo mensaje que en password para no dar pistas a atacantes.
        if not user:
            raise ValueError("Credenciales invalidas")

        # 3. Validacion de estado: Comprueba si la cuenta ha sido desactivada.
        if not user.is_active:
            raise ValueError("Usuario inactivo")

        # 4. Verificacion de Password: Compara la clave recibida con el hash de la base de datos.
        if not verify_password(password, user.password_hash):
            raise ValueError("Credenciales invalidas")

        # 5. Generacion de Token: Si todo es correcto, crea un JWT con la informacion esencial.
        # Se incluye el ID (sub), el email y el rol para que la API sepa que permisos tiene el portador.
        token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email,
                "role": user.role.name
            }
        )
        return token