# ==============================================================================
# GESTION DE SEGURIDAD Y CRIPTOGRAFIA (PASSWORDS)
# Este modulo se encarga del hashing y verificacion de contrasenas utilizando
# el algoritmo BCrypt, garantizando que las credenciales no sean legibles en BD.
# ==============================================================================

from passlib.context import CryptContext

# Configuracion del contexto de hashing
# 'bcrypt' es el algoritmo estandar de oro por su resistencia a ataques de fuerza bruta.
# 'deprecated="auto"' permite que el sistema ignore esquemas antiguos si se actualiza la libreria.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Transforma una contrasena de texto plano en un hash irreversible.
    Se utiliza durante el registro de usuarios o en el script de 'Seeding'.
    """
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Compara una contrasena enviada por el usuario (login) con el hash guardado en BD.
    Retorna True si coinciden, False en caso contrario.
    """
    return pwd_context.verify(password, hashed_password)